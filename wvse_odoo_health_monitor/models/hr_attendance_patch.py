# -*- coding: utf-8 -*-
import json
import pytz
from datetime import timedelta
from odoo import api, fields, models


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    @api.model_create_multi
    def create(self, vals_list):
        """Auto-close an old open attendance before creating a new check-in.

        This prevents users from being blocked by standard hr.attendance constraints.

        Safety:
        - Only closes when an open attendance exists and its check_in is before the new check_in.
        - Close time is set to 1 second before the new check_in (or end-of-day, whichever is earlier).
        - Records an audit issue (wvse.health.issue) for traceability.
        """
        icp = self.env["ir.config_parameter"].sudo()
        enabled = str(icp.get_param("wvse_health.attendance_autoclose_on_checkin", "True")).lower() in ("1", "true", "yes", "y", "on")
        tz_name = icp.get_param("wvse_health.timezone", "America/Sao_Paulo")
        tz = pytz.timezone(tz_name)

        records = self.browse()

        if enabled:
            for vals in vals_list:
                employee_id = vals.get("employee_id")
                check_in = vals.get("check_in")
                check_out = vals.get("check_out")
                if not employee_id or not check_in or check_out:
                    # Still create the record; just skip autoclose.
                    records |= super(HrAttendance, self).create(vals)
                    continue

                # Ensure comparisons are done with datetime objects.
                check_in_dt = fields.Datetime.to_datetime(check_in)
                if not check_in_dt:
                    records |= super(HrAttendance, self).create(vals)
                    continue

                open_att = self.sudo().search([
                    ("employee_id", "=", employee_id),
                    ("check_out", "=", False),
                ], order="check_in desc", limit=1)

                if not open_att:
                    records |= super(HrAttendance, self).create(vals)
                    continue

                if open_att.check_in and open_att.check_in < check_in_dt:
                    close_dt = check_in_dt - timedelta(seconds=1)

                    check_in_local = pytz.utc.localize(open_att.check_in).astimezone(tz)
                    eod_local = check_in_local.replace(hour=23, minute=59, second=59, microsecond=0)
                    eod_utc_naive = eod_local.astimezone(pytz.utc).replace(tzinfo=None)
                    if close_dt > eod_utc_naive:
                        close_dt = eod_utc_naive
                    if close_dt <= open_att.check_in:
                        close_dt = open_att.check_in + timedelta(seconds=1)

                    old_vals = {"check_in": str(open_att.check_in), "check_out": False}
                    open_att.write({"check_out": close_dt})

                    Issue = self.env["wvse.health.issue"].sudo()
                    Issue.create({
                        "issue_type": "attendance_autoclose",
                        "severity": "warning",
                        "model_name": "hr.attendance",
                        "res_id": open_att.id,
                        "description": "Auto-closed previous open attendance to allow new check-in.",
                        "can_fix": False,
                        "fix_state": "fixed",
                        "fixed_by": self.env.user.id,
                        "fixed_on": fields.Datetime.now(),
                        "old_values_json": json.dumps(old_vals, ensure_ascii=False),
                        "new_values_json": json.dumps({"check_out": str(close_dt)}, ensure_ascii=False),
                        "employee_id": employee_id,
                    })

                # Create the requested attendance (call next create in MRO using a single dict).
                records |= super(HrAttendance, self).create(vals)

        else:
            # Autoclose disabled: create records in a multi-compatible way.
            for vals in vals_list:
                records |= super(HrAttendance, self).create(vals)

        return records
