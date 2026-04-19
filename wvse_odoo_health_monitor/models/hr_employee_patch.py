# -*- coding: utf-8 -*-

"""Safety patches for integrations with attendance workflows.

This module is installed alongside a custom attendance workflow addon that
pauses task timers (account.analytic.line with task_timer=True) when lunch
starts.

Problem seen in production:
 - Some task timers remain flagged as running for very old/locked periods.
 - When lunch starts, the workflow tries to close ALL running timers and hits
   a timesheet lock ("confirmed timesheet"), blocking lunch registration.

This patch makes the pause operation best-effort and non-blocking:
 - Recent timers are closed normally.
 - Old timers are disabled (task_timer=False) without touching other fields.
 - Any exception is caught per record and logged to wvse.health.issue.
"""

import json
import logging
from datetime import timedelta

from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def end_all_tasks(self):
        """Stop ongoing task timers safely.

        This method is called by the custom attendance workflow when lunch
        starts. It MUST NOT raise, otherwise attendance/lunch UX is blocked.

        Return: int - number of timers successfully closed/disabled.
        """
        self.ensure_one()

        # If the custom field is not installed, do nothing.
        Aal = self.env["account.analytic.line"].sudo()
        if "task_timer" not in Aal._fields:
            return 0

        if not self.user_id:
            return 0

        icp = self.env["ir.config_parameter"].sudo()
        # Close timers normally only if they started recently.
        # Defaults: 3 days is enough to cover weekends/instabilities.
        try:
            close_days = int(icp.get_param("wvse_health.task_timer_close_days", "3"))
        except Exception:
            close_days = 3

        now_dt = fields.Datetime.now()
        close_cutoff = now_dt - timedelta(days=close_days)

        timers = Aal.search([
            ("user_id", "=", self.user_id.id),
            ("task_timer", "=", True),
        ])

        if not timers:
            return 0

        Issue = self.env["wvse.health.issue"].sudo()
        fixed_count = 0
        fixed_task_ids = set()

        for line in timers:
            # Decide the safest operation.
            start_dt = line.date_start
            is_recent = bool(start_dt and start_dt >= close_cutoff)

            with self.env.cr.savepoint():
                try:
                    if is_recent:
                        # Close normally (minimal set of fields).
                        vals = {"task_timer": False}
                        if "date_end" in line._fields:
                            vals["date_end"] = now_dt
                        line.write(vals)

                        # Recompute durations if those fields exist.
                        if line.date_start and line.date_end:
                            diff = (line.date_end - line.date_start).total_seconds()
                            if "timer_duration" in line._fields:
                                line.timer_duration = round(diff / 60.0, 2)
                            if "unit_amount" in line._fields:
                                line.unit_amount = round(diff / 3600.0, 2)
                            if "unit_amount_dec" in line._fields:
                                line.unit_amount_dec = round(diff / 3600.0, 6)
                    else:
                        # For old/locked lines, only try to disable the timer.
                        line.write({"task_timer": False})

                    fixed_count += 1
                    if line.task_id:
                        fixed_task_ids.add(line.task_id.id)

                except Exception as exc:
                    # Never block lunch/attendance actions.
                    _logger.warning("Webvirtual health: could not stop task timer line %s: %s", line.id, exc)
                    Issue.create({
                        "issue_type": "task_timer_pause_failed",
                        "severity": "warning",
                        "model_name": "account.analytic.line",
                        "res_id": line.id,
                        "description": _("Could not pause a running task timer (non-blocking)."),
                        "can_fix": False,
                        "fix_state": "failed",
                        "fix_message": str(exc),
                        "old_values_json": json.dumps({
                            "task_timer": True,
                            "date_start": str(line.date_start) if line.date_start else None,
                            "date_end": str(line.date_end) if getattr(line, "date_end", None) else None,
                        }, ensure_ascii=False),
                        "employee_id": self.id,
                        "project_id": line.project_id.id if line.project_id else False,
                        "task_id": line.task_id.id if line.task_id else False,
                    })

        # Try to mark tasks as not working (best-effort).
        if fixed_task_ids:
            Task = self.env["project.task"].sudo()
            tasks = Task.browse(list(fixed_task_ids)).exists()
            if tasks and "is_user_working" in Task._fields:
                with self.env.cr.savepoint():
                    try:
                        tasks.write({"is_user_working": False})
                    except Exception as exc:
                        _logger.warning("Webvirtual health: could not update is_user_working: %s", exc)

        return fixed_count
