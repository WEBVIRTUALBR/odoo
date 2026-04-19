# Odoo Apps Repository

Repository-level inventory, legal metadata, and publishing support files for Odoo modules maintained by **Webvirtual**.

## Company Information

| Field | Value |
|---|---|
| Company | Webvirtual Soluções Empresariais LTDA |
| Brand | Webvirtual |
| Website | https://www.webvirtual.com.br |
| Support Email | odoo@webvirtual.com.br |
| General Email | contato@webvirtual.com.br |
| Phone 1 | +55 31 97147-4489 |
| Phone 2 | +55 62 99913-2635 |
| Address | Av Alameda dos Ipês, 8625 Sala 12-A - Vale Do Sereno, Belo Horizonte, Minas Gerais, 34012-970, Brasil |

## Maintained By

**Webvirtual**  
https://www.webvirtual.com.br  
odoo@webvirtual.com.br  

## Repository Overview

| Metric | Value |
|---|---:|
| Modules Found | 1 |
| Applications | 1 |
| Installable Modules | 1 |
| Auto Install Enabled | 0 |
| Distinct Licenses | 1 |

## Module Inventory

| Technical Name | Module Name | Version | Category | License | Application | Installable | Auto Install | Price | Author | Maintainer |
|---|---|---:|---|---|---|---|---|---:|---|---|
| wvse_odoo_health_monitor | Webvirtual Health Monitor | 15.0.1.1.0 | Tools | OPL-1 | Yes | Yes | No | USD 1.49 | Webvirtual Soluções Empresariais | Webvirtual |

## Repository Root Tree

```text
odoo_apps/
├── wvse_odoo_health_monitor/
├── _copyright.py
├── _license.py
├── _notice.py
└── _readme.py
```

## Module Structure Trees

## Webvirtual Health Monitor

**Technical Name:** `wvse_odoo_health_monitor`  
**Version:** `15.0.1.1.0`  
**Category:** `Tools`  
**License:** `OPL-1`  
**Application:** `Yes`  
**Installable:** `Yes`  
**Auto Install:** `No`  
**Price:** `USD 1.49`  
**Author:** `Webvirtual Soluções Empresariais`  
**Maintainer:** `Webvirtual`  
**Path:** `wvse_odoo_health_monitor`  
**Dependencies:** `base, mail, project, hr_attendance, hr_timesheet`  

### Description

Daily health checks and safe self-healing for timesheets and attendance ================ Overview -------- Complete business module for Odoo with backend logic, security rules, scheduled jobs, reports, portal/website integration, frontend assets, and automated tests. Main Features ------------- - Business model management - Access rights and record rules - Menus, actions, views, dashboards - Wizards and reports - Scheduled jobs - Email templates and automated actions - Website / portal integration - JavaScript / OWL / SCSS assets - Demo data and automated tests - Upgrade scripts support Technical Notes --------------- - Compatible with custom deployments on Community and On-Premise - Published on Odoo Apps - Use Community or Enterprise depending on declared dependencies

### Structure Tree

```text
wvse_odoo_health_monitor/
├── controllers/
│   ├── __init__.py
│   ├── api.py
│   ├── main.py
│   ├── portal.py
│   └── webhook.py
├── data/
│   ├── cron.xml
│   ├── decimal_precision_data.xml
│   ├── ir_actions_server.xml
│   ├── ir_config_parameter.xml
│   ├── ir_cron_data.xml
│   ├── ir_sequence_data.xml
│   ├── mail_activity_type_data.xml
│   ├── mail_template.xml
│   ├── mail_template_data.xml
│   ├── report_paperformat_data.xml
│   ├── web_tour_data.xml
│   ├── wvse_odoo_health_monitor_data.xml
│   ├── wvse_odoo_health_monitor_demo_bridge.xml
│   └── wvse_odoo_health_monitor_onboarding.xml
├── demo/
│   ├── demo.xml
│   ├── demo_users.xml
│   └── wvse_model_demo.xml
├── doc/
│   ├── structure/
│   │   ├── manifest_reference.py
│   │   └── module_structure.txt
│   ├── index.rst
│   ├── README.md
│   └── viewer.html
├── i18n/
│   ├── en_US.po
│   ├── es.po
│   ├── pt_BR.mo
│   ├── pt_BR.po
│   └── wvse_odoo_health_monitor.pot
├── models/
│   ├── __init__.py
│   ├── abstract_models.py
│   ├── health_issue.py
│   ├── health_run.py
│   ├── health_settings.py
│   ├── hr_attendance_patch.py
│   ├── hr_employee_patch.py
│   ├── mail_thread_mixin.py
│   ├── res_company.py
│   ├── res_config_settings.py
│   ├── res_partner.py
│   ├── res_users.py
│   └── schedule_wizard.py
├── report/
│   ├── __init__.py
│   ├── wvse_label_report.xml
│   ├── wvse_report.py
│   ├── wvse_report_actions.xml
│   ├── wvse_report_paperformat.xml
│   └── wvse_report_templates.xml
├── security/
│   ├── ir.model.access.csv
│   ├── ir_rule.xml
│   ├── security.xml
│   ├── wvse_odoo_health_monitor_groups.xml
│   └── wvse_odoo_health_monitor_security.xml
├── static/
│   ├── description/
│   │   ├── images/
│   │   │   ├── main-screenshot-1.png
│   │   │   ├── main-screenshot-2.png
│   │   │   ├── whatsapp.png
│   │   │   └── wvse_logo_horizontal_color.png
│   │   ├── docs.html
│   │   ├── icon.png
│   │   ├── index.html
│   │   ├── wvse_odoo_health_monitor_cover.jpg
│   │   └── wvse_odoo_health_monitor_screenshot.jpg
│   ├── src/
│   │   ├── css/
│   │   │   └── legacy.css
│   │   ├── img/
│   │   │   ├── icons/
│   │   │   ├── icon.svg
│   │   │   ├── illustration.png
│   │   │   └── logo.svg
│   │   ├── js/
│   │   │   ├── components/
│   │   │   │   ├── wvse_component.js
│   │   │   │   └── wvse_dialog.js
│   │   │   ├── fields/
│   │   │   │   └── wvse_custom_field.js
│   │   │   ├── patches/
│   │   │   │   └── some_patch.js
│   │   │   ├── services/
│   │   │   │   └── wvse_service.js
│   │   │   ├── utils/
│   │   │   │   └── helpers.js
│   │   │   ├── views/
│   │   │   │   └── wvse_custom_view.js
│   │   │   ├── backend.js
│   │   │   ├── frontend.js
│   │   │   ├── portal.js
│   │   │   └── website.js
│   │   ├── lib/
│   │   │   └── third_party_library/
│   │   │       ├── lib.css
│   │   │       └── lib.js
│   │   ├── scss/
│   │   │   ├── backend.scss
│   │   │   ├── frontend.scss
│   │   │   ├── portal.scss
│   │   │   ├── variables.scss
│   │   │   └── website.scss
│   │   └── xml/
│   │       ├── qweb/
│   │       │   ├── backend.xml
│   │       │   ├── common.xml
│   │       │   ├── frontend.xml
│   │       │   ├── portal.xml
│   │       │   └── website.xml
│   │       ├── components.xml
│   │       ├── dialogs.xml
│   │       └── templates.xml
│   └── tests/
│       ├── helpers/
│       │   └── test_helpers.js
│       ├── mock_server/
│       │   └── mock_data.js
│       └── tours/
│           └── wvse_odoo_health_monitor_tour.js
├── tests/
│   ├── __init__.py
│   ├── common.py
│   ├── test_access_rights.py
│   ├── test_controllers.py
│   ├── test_flows.py
│   ├── test_models.py
│   ├── test_reports.py
│   ├── test_security.py
│   └── test_tours.py
├── upgrades/
│   └── 15.0.1.0.0/
│       ├── end-001-cleanup.py
│       ├── post-001-migrate.py
│       └── pre-001-prepare.py
├── views/
│   ├── actions.xml
│   ├── assets.xml
│   ├── health_issue_views.xml
│   ├── health_run_views.xml
│   ├── menu.xml
│   ├── menus.xml
│   ├── portal_templates.xml
│   ├── res_config_settings_views.xml
│   ├── schedule_wizard_views.xml
│   ├── snippets.xml
│   ├── website_templates.xml
│   ├── wvse_model_activity_views.xml
│   ├── wvse_model_calendar_views.xml
│   ├── wvse_model_cohort_views.xml
│   ├── wvse_model_dashboard_views.xml
│   ├── wvse_model_form_views.xml
│   ├── wvse_model_graph_views.xml
│   ├── wvse_model_kanban_views.xml
│   ├── wvse_model_pivot_views.xml
│   ├── wvse_model_search_views.xml
│   ├── wvse_model_tree_views.xml
│   └── wvse_model_views.xml
├── wizard/
│   ├── __init__.py
│   ├── wvse_batch_wizard.py
│   ├── wvse_batch_wizard_views.xml
│   ├── wvse_wizard.py
│   └── wvse_wizard_views.xml
├── __init__.py
├── __manifest__.py
├── COPYRIGHT
├── hooks.py
├── LICENSE
├── NOTICE
└── README.md
```


## Publication Notes

- This README is generated automatically from all discovered `__manifest__.py` files below the repository root.
- The technical name is derived from the folder that contains each manifest.
- The authoritative module metadata remains the information declared inside each manifest.
- Repository legal files are generated by `_license.py`, `_copyright.py`, and `_notice.py`.

---

Generated automatically in 2026-04-19 15:53:28.
