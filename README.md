# Webvirtual Odoo Health Monitor (Odoo 15.0)

This module provides daily health checks and safe self-healing routines for:

- Timesheet duration inconsistencies in account.analytic.line (timer_duration / unit_amount / unit_amount_dec)
- Null currency_id on account.analytic.line
- Missing department_id on project.task (mirrors project.department_id) when those fields exist
- Open attendances (missing check_out) from previous days (auto-close)

Key properties:

- Safe scope: fixes are applied only to the detected records, and only to the specific fields.
- Audit trail: every run and every issue/fix is recorded.
- Daily cron + manual execution from UI.
- Summary email sent to support@webvirtual.com.br.

Notes:

- Thresholds are configurable in Settings -> Odoo Health.
- Attendance auto-close on check-in is implemented to avoid blocking employees when an old open attendance exists.

