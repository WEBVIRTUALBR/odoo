# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SdpmHealthScheduleWizard(models.TransientModel):
    _name = "wvse.health.schedule.wizard"
    _description = "Schedule Health Run"

    nextcall = fields.Datetime(string="Next Execution", required=True, default=lambda self: fields.Datetime.now())

    def action_schedule(self):
        self.ensure_one()
        cron = self.env.ref("wvse_odoo_health_monitor.ir_cron_wvse_health_daily", raise_if_not_found=False)
        if not cron:
            raise UserError(_("Health cron was not found."))

        cron.sudo().write({
            "nextcall": self.nextcall,
            "active": True,
        })

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Scheduled"),
                "message": _("Next health execution scheduled for %s") % (self.nextcall,),
                "type": "success",
                "sticky": False,
            },
        }
