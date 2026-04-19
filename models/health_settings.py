# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    wvse_health_timezone = fields.Char(
        string="Health Check Timezone",
        config_parameter="wvse_health.timezone",
        default="America/Sao_Paulo",
        help="Timezone used to compute 'today' boundaries for safe checks (default: America/Sao_Paulo).",
    )

    wvse_min_calc_minutes = fields.Float(
        string="Min Calculated Minutes",
        config_parameter="wvse_health.min_calc_minutes",
        default=1.0,
        help="Minimum calculated duration (in minutes) to consider for timesheet mismatch detection.",
    )
    wvse_min_abs_diff_minutes = fields.Float(
        string="Min Absolute Difference (Minutes)",
        config_parameter="wvse_health.min_abs_diff_minutes",
        default=1.0,
        help="Minimum absolute difference (in minutes) for timer_duration mismatch detection.",
    )
    wvse_ratio_low = fields.Float(
        string="Low Ratio Threshold",
        config_parameter="wvse_health.ratio_low",
        default=0.15,
        help="If stored value / calculated value is below this ratio, it is considered 'too small'.",
    )
    wvse_ratio_high = fields.Float(
        string="High Ratio Threshold",
        config_parameter="wvse_health.ratio_high",
        default=2.0,
        help="If stored value / calculated value is above this ratio, it is considered 'too large'.",
    )
    wvse_min_abs_diff_hours = fields.Float(
        string="Min Absolute Difference (Hours)",
        config_parameter="wvse_health.min_abs_diff_hours",
        default=0.0833333333,
        help="Minimum absolute difference (in hours) for unit_amount / unit_amount_dec mismatch detection.",
    )

    wvse_support_email = fields.Char(
        string="Support Email",
        config_parameter="wvse_health.support_email",
        default="support@webvirtual.com.br",
        help="Email address that receives daily health summary.",
    )

    wvse_autofix_enabled = fields.Boolean(
        string="Enable Automatic Fixes (Cron)",
        config_parameter="wvse_health.autofix_enabled",
        default=True,
        help="If enabled, the daily cron will apply safe fixes automatically.",
    )

    wvse_attendance_autoclose_on_checkin = fields.Boolean(
        string="Auto-close Old Attendance on Check-in",
        config_parameter="wvse_health.attendance_autoclose_on_checkin",
        default=True,
        help="If enabled, when a user checks in and there is an old open attendance, the module auto-closes it.",
    )
