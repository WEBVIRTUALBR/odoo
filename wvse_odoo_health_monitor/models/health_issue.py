# -*- coding: utf-8 -*-
import json
from odoo import fields, models, _
from odoo.exceptions import UserError


class SdpmHealthIssue(models.Model):
    _name = "wvse.health.issue"
    _description = "Odoo Health Issue"
    _order = "create_date desc, id desc"

    run_id = fields.Many2one("wvse.health.run", string="Run", ondelete="set null", index=True)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company, index=True)

    issue_type = fields.Selection([
        ("timesheet_hours", "Timesheet Hours Mismatch"),
        ("timesheet_currency", "Timesheet Currency Missing"),
        ("timesheet_department", "Timesheet Department Missing"),
        ("task_department", "Task Department Missing"),
        ("attendance_open", "Attendance Missing Check-out"),
        ("attendance_autoclose", "Attendance Auto-closed on Check-in"),
        ("task_timer_pause_failed", "Task Timer Pause Failed"),
        ("unsupported", "Unsupported / Skipped"),
    ], required=True, index=True)

    severity = fields.Selection([
        ("info", "Info"),
        ("warning", "Warning"),
        ("critical", "Critical"),
    ], default="warning", required=True, index=True)

    model_name = fields.Char(string="Model")
    res_id = fields.Integer(string="Record ID")
    description = fields.Text(string="Description")

    can_fix = fields.Boolean(string="Can Fix", default=False)
    fix_state = fields.Selection([
        ("pending", "Pending"),
        ("fixed", "Fixed"),
        ("skipped", "Skipped"),
        ("failed", "Failed"),
    ], default="pending", required=True, index=True)

    fixed_by = fields.Many2one("res.users", string="Fixed By")
    fixed_on = fields.Datetime(string="Fixed On")
    fix_message = fields.Text(string="Fix Message")

    old_values_json = fields.Text(string="Old Values (JSON)")
    new_values_json = fields.Text(string="New Values (JSON)")

    employee_id = fields.Many2one("hr.employee", string="Employee", index=True)
    project_id = fields.Many2one("project.project", string="Project", index=True)
    task_id = fields.Many2one("project.task", string="Task", index=True)

    def _json_load(self, txt):
        if not txt:
            return {}
        try:
            return json.loads(txt)
        except Exception:
            return {}

    def action_apply_fix(self):
        for issue in self:
            if not issue.can_fix:
                raise UserError(_("This issue cannot be fixed automatically."))
            if issue.fix_state == "fixed":
                continue
            if not issue.run_id:
                raise UserError(_("This issue is not linked to a run."))
            issue.run_id._apply_single_issue(issue)

    def action_open_record(self):
        self.ensure_one()
        if not self.model_name or not self.res_id:
            raise UserError(_("No linked record."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Linked Record"),
            "res_model": self.model_name,
            "res_id": self.res_id,
            "view_mode": "form",
            "target": "current",
        }
