# -*- coding: utf-8 -*-
import json
import pytz
from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SdpmHealthRun(models.Model):
    _name = "wvse.health.run"
    _description = "Odoo Health Run"
    _order = "create_date desc, id desc"

    name = fields.Char(default=lambda self: _("Health Run"), required=True)
    started_on = fields.Datetime(string="Started On", readonly=True)
    finished_on = fields.Datetime(string="Finished On", readonly=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("running", "Running"),
        ("done", "Done"),
        ("failed", "Failed"),
    ], default="draft", required=True, index=True, group_expand='_read_group_state')

    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, index=True, required=True)
    triggered_by = fields.Selection([
        ("cron", "Cron"),
        ("manual", "Manual"),
    ], default="manual", required=True, index=True)

    issue_ids = fields.One2many("wvse.health.issue", "run_id", string="Issues", readonly=True)

    issues_total = fields.Integer(compute="_compute_stats")
    fixed_total = fields.Integer(compute="_compute_stats")
    failed_total = fields.Integer(compute="_compute_stats")
    pending_total = fields.Integer(compute="_compute_stats")

    summary_html = fields.Html(string="Summary", sanitize=False, readonly=True)

    health_level = fields.Selection([
        ("ok", "OK"),
        ("warning", "Warning"),
        ("error", "Error"),
    ], compute="_compute_health_level", store=True, index=True)

    color = fields.Integer(string="Color", store=True, compute="_compute_kanban_color")

    @api.depends('health_level')
    def _compute_kanban_color(self):
        for record in self:
            # Mapeamento de Cores Odoo:
            # 1: Vermelho, 3: Amarelo, 10: Verde, 0: Cinza/Branco
            if record.health_level == 'error':
                record.color = 1  # Farol Vermelho
            elif record.health_level == 'warning':
                record.color = 3  # Farol Amarelo
            elif record.health_level == 'ok' or record.health_level == 'success':
                record.color = 10 # Farol Verde
            else:
                record.color = 0  # Sem cor definida

    @api.model
    def _read_group_state(self, stages, domain, order):
        return [key for key, val in self._fields['state'].selection]

    def _compute_stats(self):
        for run in self:
            run.issues_total = len(run.issue_ids)
            run.fixed_total = len(run.issue_ids.filtered(lambda x: x.fix_state == "fixed"))
            run.failed_total = len(run.issue_ids.filtered(lambda x: x.fix_state == "failed"))
            run.pending_total = len(run.issue_ids.filtered(lambda x: x.fix_state in ("pending", "skipped")))

    @api.depends("state", "issue_ids.severity", "issue_ids.issue_type")
    def _compute_health_level(self):
        for run in self:
            if run.state == "failed":
                run.health_level = "error"
                continue
            issues = run.issue_ids.filtered(lambda i: i.issue_type != "unsupported")
            if not issues:
                run.health_level = "ok"
                continue
            if any(i.severity == "critical" for i in issues):
                run.health_level = "error"
            elif any(i.severity == "warning" for i in issues):
                run.health_level = "warning"
            else:
                run.health_level = "ok"

    @api.model
    def _cfg(self, key, default=None):
        icp = self.env["ir.config_parameter"].sudo()
        return icp.get_param(key, default)

    @api.model
    def _get_tz(self):
        return self._cfg("wvse_health.timezone", "America/Sao_Paulo")

    @api.model
    def _get_support_email(self):
        return self._cfg("wvse_health.support_email", "support@webvirtual.com.br")

    @api.model
    def _get_thresholds(self):
        def f(key, dflt):
            try:
                return float(self._cfg(key, dflt))
            except Exception:
                return float(dflt)

        return {
            "min_calc_minutes": f("wvse_health.min_calc_minutes", 1.0),
            "min_abs_diff_minutes": f("wvse_health.min_abs_diff_minutes", 1.0),
            "ratio_low": f("wvse_health.ratio_low", 0.15),
            "ratio_high": f("wvse_health.ratio_high", 2.0),
            "min_abs_diff_hours": f("wvse_health.min_abs_diff_hours", 0.0833333333),
        }

    @api.model
    def _autofix_enabled(self):
        return str(self._cfg("wvse_health.autofix_enabled", "True")).lower() in ("1", "true", "yes", "y", "on")

    def action_run_now(self):
        self.ensure_one()
        if self.state == "running":
            raise UserError(_("This run is already running."))
        new_run = self.create({
            "name": _("Health Run (Manual)"),
            "triggered_by": "manual",
            "company_id": self.env.company.id,
        })
        new_run.execute(apply_fixes=False, send_email=False)
        return {
            "type": "ir.actions.act_window",
            "res_model": "wvse.health.run",
            "res_id": new_run.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_apply_fixes(self):
        self.ensure_one()
        self.execute(apply_fixes=True, send_email=False)
        return True

    def action_send_summary(self):
        self.ensure_one()
        self._send_summary_email()
        return True

    @api.model
    def cron_run_daily(self):
        run = self.create({
            "name": _("Health Run (Cron)"),
            "triggered_by": "cron",
            "company_id": self.env.company.id,
        })
        run.execute(apply_fixes=self._autofix_enabled(), send_email=True)
        return True

    def execute(self, apply_fixes=False, send_email=False):
        self.ensure_one()
        if self.state == "running":
            raise UserError(_("Run is already running."))

        self.write({
            "state": "running",
            "started_on": fields.Datetime.now(),
            "finished_on": False,
            "summary_html": False,
        })

        try:
            self._detect_timesheet_hour_issues()
            self._detect_timesheet_currency_issues()
            self._detect_timesheet_department_issues()
            self._detect_task_department_issues()
            self._detect_attendance_open_issues()

            if apply_fixes:
                self._apply_all_issues()

            self.write({
                "state": "done",
                "finished_on": fields.Datetime.now(),
            })
        except Exception as exc:
            self.write({
                "state": "failed",
                "finished_on": fields.Datetime.now(),
                "summary_html": "<p><b>Failed:</b> %s</p>" % (str(exc),),
            })
            raise

        self._build_summary_html()
        if send_email:
            self._send_summary_email()
        return True

    def _today_local_date(self):
        tz = pytz.timezone(self._get_tz())
        now_local = pytz.utc.localize(fields.Datetime.now()).astimezone(tz)
        return now_local.date()

    def _detect_timesheet_hour_issues(self):
        thresholds = self._get_thresholds()
        tz_name = self._get_tz()
        today = self._today_local_date()

        sql = """
WITH base AS (
    SELECT
        aal.id,
        aal.company_id,
        aal.employee_id,
        aal.project_id,
        aal.task_id,
        aal.name,
        aal.date_start,
        aal.date_end,
        aal.timer_duration,
        aal.unit_amount_dec,
        aal.unit_amount,
        aal.create_date,
        COALESCE(
            aal.date,
            (aal.date_start AT TIME ZONE 'UTC' AT TIME ZONE %(tz)s)::date,
            (aal.create_date AT TIME ZONE 'UTC' AT TIME ZONE %(tz)s)::date
        ) AS work_day,
        EXTRACT(EPOCH FROM (aal.date_end - aal.date_start))::numeric AS calc_seconds
    FROM account_analytic_line aal
    WHERE aal.task_id IS NOT NULL
      AND aal.project_id IS NOT NULL
      AND aal.date_start IS NOT NULL
      AND aal.date_end   IS NOT NULL
      AND aal.date_end >= aal.date_start
),
calc AS (
    SELECT
        b.*,
        (b.calc_seconds / 60.0)   AS calc_minutes,
        (b.calc_seconds / 3600.0) AS calc_hours,
        round((b.calc_seconds / 60.0), 2)   AS timer_duration_recal,
        round((b.calc_seconds / 3600.0), 6) AS unit_amount_dec_recal,
        round((b.calc_seconds / 3600.0), 6) AS unit_amount_recal,
        (b.timer_duration::numeric / NULLIF((b.calc_seconds / 60.0), 0)) AS timer_ratio,
        (b.unit_amount::numeric / NULLIF((b.calc_seconds / 3600.0), 0))  AS unit_amount_ratio,
        (b.unit_amount_dec::numeric / NULLIF((b.calc_seconds / 3600.0), 0)) AS unit_amount_dec_ratio
    FROM base b
)
SELECT c.*
FROM calc c
WHERE
    c.work_day < %(today)s
    AND (
        (
            c.calc_minutes >= %(min_calc_minutes)s
            AND (
                c.timer_duration IS NULL
                OR c.timer_duration <= 0
                OR (
                    ABS(c.calc_minutes - c.timer_duration::numeric) >= %(min_abs_diff_minutes)s
                    AND (c.timer_ratio < %(ratio_low)s OR c.timer_ratio > %(ratio_high)s)
                )
            )
        )
        OR (
            c.calc_hours >= (%(min_calc_minutes)s / 60.0)
            AND c.unit_amount IS NOT NULL
            AND ABS(c.calc_hours - c.unit_amount::numeric) >= %(min_abs_diff_hours)s
            AND (c.unit_amount_ratio < %(ratio_low)s OR c.unit_amount_ratio > %(ratio_high)s)
        )
        OR (
            c.calc_hours >= (%(min_calc_minutes)s / 60.0)
            AND c.unit_amount_dec IS NOT NULL
            AND ABS(c.calc_hours - c.unit_amount_dec::numeric) >= %(min_abs_diff_hours)s
            AND (c.unit_amount_dec_ratio < %(ratio_low)s OR c.unit_amount_dec_ratio > %(ratio_high)s)
        )
    )
ORDER BY c.work_day DESC, c.id DESC
        """

        params = {"tz": tz_name, "today": today, **thresholds}
        self.env.cr.execute(sql, params)
        rows = self.env.cr.dictfetchall()

        Issue = self.env["wvse.health.issue"].sudo()
        for r in rows:
            old_vals = {
                "timer_duration": r.get("timer_duration"),
                "unit_amount_dec": r.get("unit_amount_dec"),
                "unit_amount": r.get("unit_amount"),
            }
            new_vals = {
                "timer_duration": r.get("timer_duration_recal"),
                "unit_amount_dec": r.get("unit_amount_dec_recal"),
                "unit_amount": r.get("unit_amount_recal"),
            }
            Issue.create({
                "run_id": self.id,
                "company_id": r.get("company_id") or self.company_id.id,
                "issue_type": "timesheet_hours",
                "severity": "critical",
                "model_name": "account.analytic.line",
                "res_id": r["id"],
                "description": _("Timesheet duration mismatch (safe scope: excludes today)."),
                "can_fix": True,
                "fix_state": "pending",
                "old_values_json": json.dumps(old_vals, ensure_ascii=False),
                "new_values_json": json.dumps(new_vals, ensure_ascii=False),
                "employee_id": r.get("employee_id"),
                "project_id": r.get("project_id"),
                "task_id": r.get("task_id"),
            })
        return True

    def _detect_timesheet_currency_issues(self):
        tz_name = self._get_tz()
        today = self._today_local_date()

        sql = """
SELECT
    aal.id,
    aal.company_id,
    aal.employee_id,
    aal.project_id,
    aal.task_id
FROM account_analytic_line aal
WHERE aal.currency_id IS NULL
  AND aal.task_id IS NOT NULL
  AND aal.project_id IS NOT NULL
  AND COALESCE(
        aal.date,
        (aal.date_start AT TIME ZONE 'UTC' AT TIME ZONE %(tz)s)::date,
        (aal.create_date AT TIME ZONE 'UTC' AT TIME ZONE %(tz)s)::date
      ) < %(today)s
ORDER BY aal.id DESC
        """
        self.env.cr.execute(sql, {"tz": tz_name, "today": today})
        rows = self.env.cr.dictfetchall()

        Issue = self.env["wvse.health.issue"].sudo()
        for r in rows:
            company = self.env["res.company"].sudo().browse(r["company_id"])
            new_currency = company.currency_id.id if company.currency_id else False
            Issue.create({
                "run_id": self.id,
                "company_id": r["company_id"],
                "issue_type": "timesheet_currency",
                "severity": "warning",
                "model_name": "account.analytic.line",
                "res_id": r["id"],
                "description": _("currency_id is NULL on timesheet line."),
                "can_fix": bool(new_currency),
                "fix_state": "pending" if new_currency else "skipped",
                "old_values_json": json.dumps({"currency_id": False}, ensure_ascii=False),
                "new_values_json": json.dumps({"currency_id": new_currency}, ensure_ascii=False),
                "employee_id": r.get("employee_id"),
                "project_id": r.get("project_id"),
                "task_id": r.get("task_id"),
            })
        return True

    def _detect_timesheet_department_issues(self):
        """Detect timesheet lines missing department_id (safe scope: project+task only, excludes today)."""
        tz_name = self._get_tz()
        today = self._today_local_date()

        sql = """
SELECT
    aal.id,
    aal.company_id,
    aal.employee_id,
    aal.project_id,
    aal.task_id
FROM account_analytic_line aal
WHERE aal.department_id IS NULL
  AND aal.task_id IS NOT NULL
  AND aal.project_id IS NOT NULL
  AND COALESCE(
        aal.date,
        (aal.date_start AT TIME ZONE 'UTC' AT TIME ZONE %(tz)s)::date,
        (aal.create_date AT TIME ZONE 'UTC' AT TIME ZONE %(tz)s)::date
      ) < %(today)s
ORDER BY aal.id DESC
        """
        self.env.cr.execute(sql, {"tz": tz_name, "today": today})
        rows = self.env.cr.dictfetchall()

        Issue = self.env["wvse.health.issue"].sudo()
        AAL = self.env["account.analytic.line"].sudo()
        Task = self.env["project.task"].sudo()
        Project = self.env["project.project"].sudo()

        task_field = "project_department_id" if "project_department_id" in Task._fields else ("department_id" if "department_id" in Task._fields else None)
        project_field = "project_department_id" if "project_department_id" in Project._fields else ("department_id" if "department_id" in Project._fields else None)

        for r in rows:
            line = AAL.browse(r["id"])
            if not line.exists():
                continue

            dept_id = False
            # 1) Task department
            if line.task_id and task_field and getattr(line.task_id, task_field, False):
                dept_id = getattr(line.task_id, task_field).id
            # 2) Project department
            if not dept_id and line.project_id and project_field and getattr(line.project_id, project_field, False):
                dept_id = getattr(line.project_id, project_field).id
            # 3) Employee department
            if not dept_id and line.employee_id and line.employee_id.department_id:
                dept_id = line.employee_id.department_id.id

            can_fix = bool(dept_id)
            Issue.create({
                "run_id": self.id,
                "company_id": r.get("company_id") or self.company_id.id,
                "issue_type": "timesheet_department",
                "severity": "warning",
                "model_name": "account.analytic.line",
                "res_id": r["id"],
                "description": _("Timesheet department_id is NULL (safe scope: project+task only, excludes today)."),
                "can_fix": can_fix,
                "fix_state": "pending" if can_fix else "skipped",
                "old_values_json": json.dumps({"department_id": False}, ensure_ascii=False),
                "new_values_json": json.dumps({"department_id": dept_id}, ensure_ascii=False),
                "employee_id": r.get("employee_id"),
                "project_id": r.get("project_id"),
                "task_id": r.get("task_id"),
            })
        return True

    def _detect_task_department_issues(self):
        Task = self.env["project.task"]
        Project = self.env["project.project"]

        Issue = self.env["wvse.health.issue"].sudo()

        task_field = "project_department_id" if "project_department_id" in Task._fields else ("department_id" if "department_id" in Task._fields else None)
        project_field = "project_department_id" if "project_department_id" in Project._fields else ("department_id" if "department_id" in Project._fields else None)

        # If department fields are not available, do nothing (avoid generating noisy "id=0" issues).
        if not task_field or not project_field:
            return True

        self.env.cr.execute("SELECT DISTINCT task_id FROM account_analytic_line WHERE task_id IS NOT NULL")
        task_ids = [r[0] for r in self.env.cr.fetchall() if r and r[0]]
        tasks = Task.sudo().browse(task_ids)

        def _get(model_rec, field_name):
            return getattr(model_rec, field_name, False) if field_name else False

        for t in tasks:
            if not t or not t.exists():
                continue
            t_dept = _get(t, task_field)
            p_dept = _get(t.project_id, project_field) if t.project_id else False
            if t_dept or not p_dept:
                continue
            Issue.create({
                "run_id": self.id,
                "company_id": (t.company_id.id if "company_id" in t._fields and t.company_id else self.company_id.id),
                "issue_type": "task_department",
                "severity": "warning",
                "model_name": "project.task",
                "res_id": t.id,
                "description": _("Task department is empty; will mirror project department."),
                "can_fix": True,
                "fix_state": "pending",
                "old_values_json": json.dumps({task_field: False}, ensure_ascii=False),
                "new_values_json": json.dumps({task_field: p_dept.id}, ensure_ascii=False),
                "project_id": t.project_id.id,
                "task_id": t.id,
            })
        return True

    def _detect_attendance_open_issues(self):
        tz = pytz.timezone(self._get_tz())
        today = self._today_local_date()
        local_midnight = tz.localize(datetime.combine(today, datetime.min.time()))
        midnight_utc = local_midnight.astimezone(pytz.utc).replace(tzinfo=None)

        Attend = self.env["hr.attendance"].sudo()
        open_att = Attend.search([("check_out", "=", False), ("check_in", "<", midnight_utc)], order="check_in asc")

        Issue = self.env["wvse.health.issue"].sudo()
        for a in open_att:
            Issue.create({
                "run_id": self.id,
                "company_id": a.employee_id.company_id.id if a.employee_id and a.employee_id.company_id else self.company_id.id,
                "issue_type": "attendance_open",
                "severity": "critical",
                "model_name": "hr.attendance",
                "res_id": a.id,
                "description": _("Attendance is open (missing check_out) from a previous day."),
                "can_fix": True,
                "fix_state": "pending",
                "employee_id": a.employee_id.id,
                "old_values_json": json.dumps({"check_in": str(a.check_in), "check_out": False}, ensure_ascii=False),
            })
        return True

    def _apply_all_issues(self):
        for issue in self.issue_ids.filtered(lambda i: i.can_fix and i.fix_state == "pending"):
            self._apply_single_issue(issue)

    def _apply_single_issue(self, issue):
        issue = self.env["wvse.health.issue"].sudo().browse(issue.id)
        if not issue.can_fix or issue.fix_state != "pending":
            return

        try:
            with self.env.cr.savepoint():
                if issue.issue_type == "timesheet_hours":
                    self._fix_timesheet_hours(issue)
                elif issue.issue_type == "timesheet_currency":
                    self._fix_timesheet_currency(issue)
                elif issue.issue_type == "timesheet_department":
                    self._fix_timesheet_department(issue)
                elif issue.issue_type == "task_department":
                    self._fix_task_department(issue)
                elif issue.issue_type == "attendance_open":
                    self._fix_attendance_open(issue)
                else:
                    issue.write({"fix_state": "skipped", "fix_message": _("No fixer for this issue type.")})
                    return

                # A fixer may decide to mark the issue as skipped/failed itself.
                issue.flush()
                issue.invalidate_cache()
                if issue.fix_state == "pending":
                    issue.write({
                        "fix_state": "fixed",
                        "fixed_by": self.env.user.id,
                        "fixed_on": fields.Datetime.now(),
                    })
        except Exception as exc:
            issue.write({
                "fix_state": "failed",
                "fix_message": str(exc),
                "fixed_by": self.env.user.id,
                "fixed_on": fields.Datetime.now(),
            })

    def _fix_timesheet_hours(self, issue):
        line = self.env["account.analytic.line"].sudo().browse(issue.res_id)
        if not line.exists():
            raise UserError(_("Timesheet line not found."))
        new_vals = issue._json_load(issue.new_values_json)
        vals = {k: new_vals[k] for k in ("timer_duration", "unit_amount_dec", "unit_amount") if k in new_vals}
        line.write(vals)

    def _fix_timesheet_currency(self, issue):
        line = self.env["account.analytic.line"].sudo().browse(issue.res_id)
        if not line.exists():
            raise UserError(_("Timesheet line not found."))
        company = line.company_id or self.env.company
        if not company.currency_id:
            raise UserError(_("Company currency is not set."))
        line.write({"currency_id": company.currency_id.id})

    def _fix_task_department(self, issue):
        task = self.env["project.task"].sudo().browse(issue.res_id)
        if not task.exists():
            raise UserError(_("Task not found."))
        new_vals = issue._json_load(issue.new_values_json)
        if not new_vals:
            raise UserError(_("No target values were provided."))
        # Only write fields that exist on project.task.
        vals = {k: v for k, v in new_vals.items() if k in task._fields}
        if not vals:
            raise UserError(_("No supported department field found on project.task."))
        task.write(vals)

    def _fix_timesheet_department(self, issue):
        line = self.env["account.analytic.line"].sudo().browse(issue.res_id)
        if not line.exists():
            raise UserError(_("Timesheet line not found."))
        if line.department_id:
            # Do not override existing department.
            issue.write({"fix_state": "skipped", "fix_message": _("department_id is already set.")})
            return
        new_vals = issue._json_load(issue.new_values_json)
        dept_id = new_vals.get("department_id")
        if not dept_id:
            raise UserError(_("No department_id could be computed."))
        line.write({"department_id": dept_id})

    def _fix_attendance_open(self, issue):
        tz = pytz.timezone(self._get_tz())
        att = self.env["hr.attendance"].sudo().browse(issue.res_id)
        if not att.exists():
            raise UserError(_("Attendance not found."))
        close_dt = self._compute_attendance_close_dt(att, tz)
        if not close_dt:
            raise UserError(_("Could not compute a safe check_out."))
        old = {"check_in": str(att.check_in), "check_out": False}
        att.write({"check_out": close_dt})
        issue.write({
            "old_values_json": json.dumps(old, ensure_ascii=False),
            "new_values_json": json.dumps({"check_out": str(close_dt)}, ensure_ascii=False),
        })

    def _compute_attendance_close_dt(self, att, tz):
        next_att = self.env["hr.attendance"].sudo().search([
            ("employee_id", "=", att.employee_id.id),
            ("check_in", ">", att.check_in),
            ("id", "!=", att.id),
        ], order="check_in asc", limit=1)
        if next_att:
            close_dt = next_att.check_in - timedelta(seconds=1)
            if close_dt > att.check_in:
                return close_dt

        check_in_utc = pytz.utc.localize(att.check_in)
        check_in_local = check_in_utc.astimezone(tz)
        end_local = check_in_local.replace(hour=23, minute=59, second=59, microsecond=0)
        close_dt = end_local.astimezone(pytz.utc).replace(tzinfo=None)
        if close_dt <= att.check_in:
            close_dt = att.check_in + timedelta(seconds=1)
        return close_dt

    def _build_summary_html(self):
        by_type = {}
        for i in self.issue_ids:
            by_type[i.issue_type] = by_type.get(i.issue_type, 0) + 1

        parts = [
            "<h3>Webvirtual Odoo Health Summary</h3>",
            "<ul>",
            "<li><b>Total issues:</b> %s</li>" % self.issues_total,
            "<li><b>Fixed:</b> %s</li>" % self.fixed_total,
            "<li><b>Failed:</b> %s</li>" % self.failed_total,
            "<li><b>Pending/Skipped:</b> %s</li>" % self.pending_total,
            "</ul>",
            "<h4>By Type</h4>",
            "<ul>",
        ]
        for k, v in sorted(by_type.items(), key=lambda x: x[0]):
            parts.append("<li><b>%s</b>: %s</li>" % (k, v))
        parts.append("</ul>")
        self.summary_html = "\n".join(parts)

    def _send_summary_email(self):
        support_email = self._get_support_email()
        if not support_email:
            return

        template = self.env.ref("wvse_odoo_health_monitor.mail_template_wvse_health_summary", raise_if_not_found=False)
        if template:
            template.sudo().send_mail(self.id, force_send=True, email_values={"email_to": support_email})
            return

        Mail = self.env["mail.mail"].sudo()
        Mail.create({
            "subject": "Webvirtual Odoo Health Summary",
            "email_to": support_email,
            "body_html": self.summary_html or "<p>No summary.</p>",
        }).send()
