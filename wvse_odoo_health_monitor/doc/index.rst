Webvirtual Health Monitor
=========================

.. contents:: On this page
   :depth: 3

This technical documentation was generated automatically from the module source code, the manifest definition, and the current filesystem structure. It is intended to help customers, administrators, implementers, and technical reviewers understand how the module is structured, how it should be installed, how it should be updated, and how to request support.

Executive Summary
-----------------

Short business summary of the Webvirtual Health Monitor main features.

Module Snapshot
---------------

- **Display Name:** Webvirtual Health Monitor
- **Technical Name:** ``wvse_odoo_health_monitor``
- **Version:** 15.0.1.1.0
- **Category:** Tools
- **License:** OPL-1
- **Author:** Webvirtual Soluções Empresariais
- **Maintainer:** Webvirtual
- **Website:** https://www.webvirtual.com.br
- **Support:** odoo@webvirtual.com.br
- **Installable:** Yes
- **Application:** Yes
- **Auto Install:** No
- **Price:** 1.49
- **Currency:** USD
- **Live Test URL:** https://15.odoo.webvirtual.com.br

Overview
--------

Daily health checks and safe self-healing for timesheets and attendance
================

Overview
--------
Complete business module for Odoo with backend logic, security rules,
scheduled jobs, reports, portal/website integration, frontend assets,
and automated tests.

Main Features
-------------
- Business model management
- Access rights and record rules
- Menus, actions, views, dashboards
- Wizards and reports
- Scheduled jobs
- Email templates and automated actions
- Website / portal integration
- JavaScript / OWL / SCSS assets
- Demo data and automated tests
- Upgrade scripts support

Technical Notes
---------------
- Compatible with custom deployments on Community and On-Premise
- Published on Odoo Apps
- Use Community or Enterprise depending on declared dependencies

What This Module Includes
-------------------------

- Backend business models and server-side Python logic are present.
- HTTP controller endpoints are present.
- Custom API endpoints are present.
- Webhook endpoints are present.
- Wizard flows are present for guided or transient operations.
- Reporting resources are present.
- Security resources such as access control and record rules are present.
- XML user interface resources such as menus, actions, forms, lists, search views, or dashboards are present.
- Frontend assets such as JavaScript, SCSS, CSS, XML templates, or images are present.
- Frontend test resources are present.
- Python test resources are present.
- Translation resources are present.
- Demo data resources are present.
- Configuration settings are exposed through the Odoo settings interface.
- Portal-facing functionality is present.
- Website-facing functionality is present.
- Versioned upgrade scripts are present under the upgrades directory.
- Manifest dependencies are declared: base, mail, project, hr_attendance, hr_timesheet.

Deployment and Compatibility Guidance
-------------------------------------

- The manifest version indicates that the module targets the Odoo **15.0.1.1.0** series or a variant derived from that series.
- Always validate the target hosting model before deployment.
- Always validate declared dependencies before installation.
- Always validate staging installation before promoting the module to production.
- Always back up the database before installing or updating any custom or third-party module.

Installation Guide
------------------

Installation from a Downloaded Package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Download the module package from the store or receive it from the provider.
2. Extract the package and place the module folder into the custom addons path used by your Odoo server.
3. Restart the Odoo service or Odoo process.
4. Open the Apps menu.
5. Update the apps list.
6. Search for ``wvse_odoo_health_monitor`` or the display name **Webvirtual Health Monitor**.
7. Install the module.
8. Review initial configuration, security groups, menus, and scheduled actions after installation.

Command Line Installation Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    odoo-bin -d <database_name> -i wvse_odoo_health_monitor --stop-after-init

Declared Dependencies
~~~~~~~~~~~~~~~~~~~~~

- ``base``
- ``mail``
- ``project``
- ``hr_attendance``
- ``hr_timesheet``

Manifest Data Resources Loaded at Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``security/wvse_odoo_health_monitor_groups.xml``
- ``security/ir.model.access.csv``
- ``security/wvse_odoo_health_monitor_security.xml``
- ``security/ir_rule.xml``
- ``data/ir_sequence_data.xml``
- ``data/ir_cron_data.xml``
- ``data/ir_actions_server.xml``
- ``data/ir_config_parameter.xml``
- ``data/mail_template_data.xml``
- ``data/mail_activity_type_data.xml``
- ``data/report_paperformat_data.xml``
- ``data/web_tour_data.xml``
- ``data/decimal_precision_data.xml``
- ``data/wvse_odoo_health_monitor_data.xml``
- ``data/wvse_odoo_health_monitor_demo_bridge.xml``
- ``data/wvse_odoo_health_monitor_onboarding.xml``
- ``views/menus.xml``
- ``views/actions.xml``
- ``views/wvse_model_views.xml``
- ``views/wvse_model_form_views.xml``
- ``views/wvse_model_tree_views.xml``
- ``views/wvse_model_kanban_views.xml``
- ``views/wvse_model_search_views.xml``
- ``views/wvse_model_calendar_views.xml``
- ``views/wvse_model_pivot_views.xml``
- ``views/wvse_model_graph_views.xml``
- ``views/wvse_model_activity_views.xml``
- ``views/wvse_model_cohort_views.xml``
- ``views/wvse_model_dashboard_views.xml``
- ``views/schedule_wizard_views.xml``
- ``views/health_issue_views.xml``
- ``views/health_run_views.xml``
- ``views/res_config_settings_views.xml``
- ``views/portal_templates.xml``
- ``views/website_templates.xml``
- ``views/snippets.xml``
- ``views/assets.xml``
- ``wizard/wvse_wizard_views.xml``
- ``wizard/wvse_batch_wizard_views.xml``
- ``report/wvse_report_templates.xml``
- ``report/wvse_report_actions.xml``
- ``report/wvse_report_paperformat.xml``
- ``report/wvse_label_report.xml``

Demo Resources
~~~~~~~~~~~~~~

- ``demo/demo.xml``
- ``demo/wvse_model_demo.xml``
- ``demo/demo_users.xml``

Initial Configuration Checklist
-------------------------------

- Confirm that the module is visible as installed in Apps.
- Confirm that the menus and actions load successfully.
- Confirm that user groups have the intended access level.
- Confirm that default data such as cron jobs, server actions, sequences, and templates have been loaded correctly.
- Confirm that browser-side assets compile and load without console errors if the module includes frontend resources.
- Review and fill the configuration settings exposed in the settings interface.

How to Use the Module
---------------------

The exact business workflow depends on the real functional scope of the module. Based on the current structure, the following is the recommended operational flow:

1. Download the module from the store or receive the module package from the provider.
2. Place the module into the target custom addons path.
3. Update the apps list and install the module in the desired database.
4. Review access rights and make sure the correct user groups can reach the new features.
5. Configure settings if the module exposes a configuration interface.
6. Validate forms, lists, menus, actions, reports, cron jobs, and static assets after the first installation.
7. Use the available wizard flows for guided operations where applicable.
8. Validate the generated reports, document layouts, and print actions.
9. Test portal-facing behavior with a non-admin external user.
10. Test website-facing behavior with published content and website permissions.
11. Validate custom API routes and authentication behavior if the module exposes integration endpoints.
12. Validate webhook delivery, payload handling, and logging if webhook routes are provided.

Customization and Extension Guide
---------------------------------

The current module structure indicates the following main extension points:

- Backend business rules, fields, computed logic, and ORM behavior can be extended in the `models/` directory.
- Forms, lists, kanban, dashboards, searches, menus, and actions can be adjusted in the `views/` directory.
- Access rights and record rules can be refined in the `security/` directory.
- Transient operational flows can be extended in the `wizard/` directory.
- Report templates, paper formats, and reporting helpers can be customized in the `report/` directory.
- HTTP routes, portal routes, API endpoints, and webhooks can be adjusted in the `controllers/` directory.
- JavaScript, SCSS, CSS, XML templates, and static visual resources can be adjusted in `static/src/`.
- Translations can be extended in the `i18n/` directory.
- Default sequences, cron jobs, server actions, email templates, and parameters can be adjusted in the `data/` directory.
- Versioned upgrade logic can be maintained through the dedicated migration scripts.

Recommended Safe Customization Practice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Avoid editing production code directly without version control.
- Prefer extending behavior through inheritance rather than rewriting stable base logic.
- Retest views, access rules, and reports after every customization.
- Validate customizations in a staging database before production rollout.
- Keep migration or upgrade scripts in sync with source-level changes.

Technical Architecture
----------------------

- **Directory Count:** 37
- **File Count:** 139
- **Detected Extensions:** .css=2, .csv=1, .html=3, .jpg=2, .js=15, .md=2, .png=6, .po=3, .pot=1, .py=39, .rst=1, .scss=5, .svg=2, .txt=1, .xml=53, [no extension]=3

Backend and ORM Layer
~~~~~~~~~~~~~~~~~~~~~

- Business models and ORM logic are located under `models/`.
- Transient wizard logic is located under `wizard/`.
- Reporting helpers and report resources are located under `report/`.
- HTTP integration surfaces are located under `controllers/`.

User Interface Layer
~~~~~~~~~~~~~~~~~~~~

- The XML user interface layer is located under `views/`.
- Static frontend resources are located under `static/src/`.
- Portal templates are present.
- Website templates are present.

Security Layer
~~~~~~~~~~~~~~

- Model access rights are defined through `security/ir.model.access.csv`.
- Security groups or record rules are present under `security/`.

Automation Layer
~~~~~~~~~~~~~~~~

- Scheduled actions are declared.
- Server actions are declared.
- Email templates are declared.

External Dependencies
---------------------

::

    {
        "python": [],
        "bin": []
    }

Frontend Asset Bundles
----------------------

::

    {
        "web.assets_backend": [
            "wvse_odoo_health_monitor/static/src/scss/variables.scss",
            "wvse_odoo_health_monitor/static/src/scss/backend.scss",
            "wvse_odoo_health_monitor/static/src/css/legacy.css",
            "wvse_odoo_health_monitor/static/src/js/backend.js",
            "wvse_odoo_health_monitor/static/src/js/fields/wvse_custom_field.js",
            "wvse_odoo_health_monitor/static/src/js/views/wvse_custom_view.js",
            "wvse_odoo_health_monitor/static/src/js/components/wvse_component.js",
            "wvse_odoo_health_monitor/static/src/js/components/wvse_dialog.js",
            "wvse_odoo_health_monitor/static/src/js/services/wvse_service.js",
            "wvse_odoo_health_monitor/static/src/js/patches/some_patch.js",
            "wvse_odoo_health_monitor/static/src/js/utils/helpers.js"
        ],
        "web.assets_frontend": [
            "wvse_odoo_health_monitor/static/src/scss/frontend.scss",
            "wvse_odoo_health_monitor/static/src/scss/portal.scss",
            "wvse_odoo_health_monitor/static/src/js/frontend.js",
            "wvse_odoo_health_monitor/static/src/js/portal.js"
        ],
        "website.assets_frontend": [
            "wvse_odoo_health_monitor/static/src/scss/website.scss",
            "wvse_odoo_health_monitor/static/src/js/website.js"
        ],
        "web.assets_qweb": [
            "wvse_odoo_health_monitor/static/src/xml/templates.xml",
            "wvse_odoo_health_monitor/static/src/xml/components.xml",
            "wvse_odoo_health_monitor/static/src/xml/dialogs.xml",
            "wvse_odoo_health_monitor/static/src/xml/qweb/common.xml",
            "wvse_odoo_health_monitor/static/src/xml/qweb/backend.xml",
            "wvse_odoo_health_monitor/static/src/xml/qweb/frontend.xml",
            "wvse_odoo_health_monitor/static/src/xml/qweb/portal.xml",
            "wvse_odoo_health_monitor/static/src/xml/qweb/website.xml"
        ],
        "web.qunit_suite_tests": [
            "wvse_odoo_health_monitor/static/tests/**/*.js"
        ]
    }

Update and Upgrade Guide
------------------------

Always update the module in a controlled environment and validate logs immediately after the upgrade.

Recommended Update Steps
~~~~~~~~~~~~~~~~~~~~~~~~

1. Back up the database before any update.
2. Back up the current module source code.
3. Review the target version and change impact.
4. Replace or merge the new source code carefully.
5. Restart the Odoo service.
6. Upgrade the module using ``-u wvse_odoo_health_monitor`` or through the Apps interface.
7. Validate menus, views, reports, scheduled actions, assets, and access rules after the upgrade.

Command Line Update Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    odoo-bin -d <database_name> -u wvse_odoo_health_monitor --stop-after-init

Detected Upgrade Logic
~~~~~~~~~~~~~~~~~~~~~~

- The module includes versioned scripts under `upgrades/`.

Manifest Integrity Review
-------------------------

Missing Required or Recommended Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Manifest key appears to still contain placeholder text: ``summary``
- Manifest key appears to still contain placeholder text: ``description``

Declared Files That Exist
~~~~~~~~~~~~~~~~~~~~~~~~~

- ``data/decimal_precision_data.xml``
- ``data/ir_actions_server.xml``
- ``data/ir_config_parameter.xml``
- ``data/ir_cron_data.xml``
- ``data/ir_sequence_data.xml``
- ``data/mail_activity_type_data.xml``
- ``data/mail_template_data.xml``
- ``data/report_paperformat_data.xml``
- ``data/web_tour_data.xml``
- ``data/wvse_odoo_health_monitor_data.xml``
- ``data/wvse_odoo_health_monitor_demo_bridge.xml``
- ``data/wvse_odoo_health_monitor_onboarding.xml``
- ``demo/demo.xml``
- ``demo/demo_users.xml``
- ``demo/wvse_model_demo.xml``
- ``report/wvse_label_report.xml``
- ``report/wvse_report_actions.xml``
- ``report/wvse_report_paperformat.xml``
- ``report/wvse_report_templates.xml``
- ``security/ir.model.access.csv``
- ``security/ir_rule.xml``
- ``security/wvse_odoo_health_monitor_groups.xml``
- ``security/wvse_odoo_health_monitor_security.xml``
- ``views/actions.xml``
- ``views/assets.xml``
- ``views/health_issue_views.xml``
- ``views/health_run_views.xml``
- ``views/menus.xml``
- ``views/portal_templates.xml``
- ``views/res_config_settings_views.xml``
- ``views/schedule_wizard_views.xml``
- ``views/snippets.xml``
- ``views/website_templates.xml``
- ``views/wvse_model_activity_views.xml``
- ``views/wvse_model_calendar_views.xml``
- ``views/wvse_model_cohort_views.xml``
- ``views/wvse_model_dashboard_views.xml``
- ``views/wvse_model_form_views.xml``
- ``views/wvse_model_graph_views.xml``
- ``views/wvse_model_kanban_views.xml``
- ``views/wvse_model_pivot_views.xml``
- ``views/wvse_model_search_views.xml``
- ``views/wvse_model_tree_views.xml``
- ``views/wvse_model_views.xml``
- ``wizard/wvse_batch_wizard_views.xml``
- ``wizard/wvse_wizard_views.xml``

Declared Files Missing on Disk
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- No missing data or demo files were detected.

Declared Asset Patterns That Exist
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``wvse_odoo_health_monitor/static/src/css/legacy.css``
- ``wvse_odoo_health_monitor/static/src/js/backend.js``
- ``wvse_odoo_health_monitor/static/src/js/components/wvse_component.js``
- ``wvse_odoo_health_monitor/static/src/js/components/wvse_dialog.js``
- ``wvse_odoo_health_monitor/static/src/js/fields/wvse_custom_field.js``
- ``wvse_odoo_health_monitor/static/src/js/frontend.js``
- ``wvse_odoo_health_monitor/static/src/js/patches/some_patch.js``
- ``wvse_odoo_health_monitor/static/src/js/portal.js``
- ``wvse_odoo_health_monitor/static/src/js/services/wvse_service.js``
- ``wvse_odoo_health_monitor/static/src/js/utils/helpers.js``
- ``wvse_odoo_health_monitor/static/src/js/views/wvse_custom_view.js``
- ``wvse_odoo_health_monitor/static/src/js/website.js``
- ``wvse_odoo_health_monitor/static/src/scss/backend.scss``
- ``wvse_odoo_health_monitor/static/src/scss/frontend.scss``
- ``wvse_odoo_health_monitor/static/src/scss/portal.scss``
- ``wvse_odoo_health_monitor/static/src/scss/variables.scss``
- ``wvse_odoo_health_monitor/static/src/scss/website.scss``
- ``wvse_odoo_health_monitor/static/src/xml/components.xml``
- ``wvse_odoo_health_monitor/static/src/xml/dialogs.xml``
- ``wvse_odoo_health_monitor/static/src/xml/qweb/backend.xml``
- ``wvse_odoo_health_monitor/static/src/xml/qweb/common.xml``
- ``wvse_odoo_health_monitor/static/src/xml/qweb/frontend.xml``
- ``wvse_odoo_health_monitor/static/src/xml/qweb/portal.xml``
- ``wvse_odoo_health_monitor/static/src/xml/qweb/website.xml``
- ``wvse_odoo_health_monitor/static/src/xml/templates.xml``
- ``wvse_odoo_health_monitor/static/tests/**/*.js``

Declared Asset Patterns Missing on Disk
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- No missing asset patterns were detected.

Files That Usually Need to Be Listed in the Manifest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following review is useful for XML and CSV resources in `security/`, `views/`, `data/`, `demo/`, `wizard/`, and `report/`. Not every file must always be loaded, but undeclared files in these folders often indicate incomplete manifest maintenance.

- No obvious undeclared XML or CSV manifest candidates were detected.

Assets That May Need Review
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following review is useful for static resources under `static/src/` and `static/tests/`. Not every file must always be bundled, but unlisted assets may indicate incomplete asset declarations.

- ``wvse_odoo_health_monitor/static/src/lib/third_party_library/lib.css``
- ``wvse_odoo_health_monitor/static/src/lib/third_party_library/lib.js``

Module Structure
----------------

::

    wvse_odoo_health_monitor/
    ├── controllers
    │   ├── __init__.py
    │   ├── api.py
    │   ├── main.py
    │   ├── portal.py
    │   └── webhook.py
    ├── data
    │   ├── decimal_precision_data.xml
    │   ├── ir_actions_server.xml
    │   ├── ir_config_parameter.xml
    │   ├── ir_cron_data.xml
    │   ├── ir_sequence_data.xml
    │   ├── mail_activity_type_data.xml
    │   ├── mail_template_data.xml
    │   ├── report_paperformat_data.xml
    │   ├── web_tour_data.xml
    │   ├── wvse_odoo_health_monitor_data.xml
    │   ├── wvse_odoo_health_monitor_demo_bridge.xml
    │   └── wvse_odoo_health_monitor_onboarding.xml
    ├── demo
    │   ├── demo.xml
    │   ├── demo_users.xml
    │   └── wvse_model_demo.xml
    ├── doc
    │   ├── structure
    │   │   ├── manifest_reference.py
    │   │   └── module_structure.txt
    │   ├── index.rst
    │   ├── README.md
    │   └── viewer.html
    ├── i18n
    │   ├── en_US.po
    │   ├── es.po
    │   ├── pt_BR.po
    │   └── wvse_odoo_health_monitor.pot
    ├── models
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
    ├── report
    │   ├── __init__.py
    │   ├── wvse_label_report.xml
    │   ├── wvse_report.py
    │   ├── wvse_report_actions.xml
    │   ├── wvse_report_paperformat.xml
    │   └── wvse_report_templates.xml
    ├── security
    │   ├── ir.model.access.csv
    │   ├── ir_rule.xml
    │   ├── wvse_odoo_health_monitor_groups.xml
    │   └── wvse_odoo_health_monitor_security.xml
    ├── static
    │   ├── description
    │   │   ├── images
    │   │   │   ├── main-screenshot-1.png
    │   │   │   ├── main-screenshot-2.png
    │   │   │   ├── whatsapp.png
    │   │   │   └── wvse_logo_horizontal_color.png
    │   │   ├── docs.html
    │   │   ├── icon.png
    │   │   ├── index.html
    │   │   ├── wvse_odoo_health_monitor_cover.jpg
    │   │   └── wvse_odoo_health_monitor_screenshot.jpg
    │   ├── src
    │   │   ├── css
    │   │   │   └── legacy.css
    │   │   ├── img
    │   │   │   ├── icons
    │   │   │   ├── icon.svg
    │   │   │   ├── illustration.png
    │   │   │   └── logo.svg
    │   │   ├── js
    │   │   │   ├── components
    │   │   │   │   ├── wvse_component.js
    │   │   │   │   └── wvse_dialog.js
    │   │   │   ├── fields
    │   │   │   │   └── wvse_custom_field.js
    │   │   │   ├── patches
    │   │   │   │   └── some_patch.js
    │   │   │   ├── services
    │   │   │   │   └── wvse_service.js
    │   │   │   ├── utils
    │   │   │   │   └── helpers.js
    │   │   │   ├── views
    │   │   │   │   └── wvse_custom_view.js
    │   │   │   ├── backend.js
    │   │   │   ├── frontend.js
    │   │   │   ├── portal.js
    │   │   │   └── website.js
    │   │   ├── lib
    │   │   │   └── third_party_library
    │   │   │       ├── lib.css
    │   │   │       └── lib.js
    │   │   ├── scss
    │   │   │   ├── backend.scss
    │   │   │   ├── frontend.scss
    │   │   │   ├── portal.scss
    │   │   │   ├── variables.scss
    │   │   │   └── website.scss
    │   │   └── xml
    │   │       ├── qweb
    │   │       │   ├── backend.xml
    │   │       │   ├── common.xml
    │   │       │   ├── frontend.xml
    │   │       │   ├── portal.xml
    │   │       │   └── website.xml
    │   │       ├── components.xml
    │   │       ├── dialogs.xml
    │   │       └── templates.xml
    │   └── tests
    │       ├── helpers
    │       │   └── test_helpers.js
    │       ├── mock_server
    │       │   └── mock_data.js
    │       └── tours
    │           └── wvse_odoo_health_monitor_tour.js
    ├── tests
    │   ├── __init__.py
    │   ├── common.py
    │   ├── test_access_rights.py
    │   ├── test_controllers.py
    │   ├── test_flows.py
    │   ├── test_models.py
    │   ├── test_reports.py
    │   ├── test_security.py
    │   └── test_tours.py
    ├── upgrades
    │   └── 15.0.1.0.0
    │       ├── end-001-cleanup.py
    │       ├── post-001-migrate.py
    │       └── pre-001-prepare.py
    ├── views
    │   ├── actions.xml
    │   ├── assets.xml
    │   ├── health_issue_views.xml
    │   ├── health_run_views.xml
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
    ├── wizard
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

Support
-------

- **Company:** Webvirtual Soluções Empresariais
- **Maintainer:** Webvirtual
- **Website:** https://www.webvirtual.com.br
- **Support Email:** odoo@webvirtual.com.br
- **General Contact Email:** contato@webvirtual.com.br
- **Phone 1:** +55 31 97147-4489
- **Phone 2:** +55 62 99913-2635

Recommended Support Request Contents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Module technical name: `wvse_odoo_health_monitor`
- Module version: `15.0.1.1.0`
- Odoo version
- Edition or environment type
- Clear reproduction steps
- Expected behavior
- Actual behavior
- Server traceback or log excerpt
- Screenshots or short screen recording if applicable
- Browser console errors for frontend issues

Suggested Support Message Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    Hello Webvirtual team,

    I need support for the module 'wvse_odoo_health_monitor'.
    Module display name: Webvirtual Health Monitor
    Module version: 15.0.1.1.0
    Odoo version: <fill here>
    Environment: <development / staging / production>
    Issue summary: <fill here>
    Steps to reproduce: <fill here>
    Expected result: <fill here>
    Actual result: <fill here>
    Logs attached: <yes / no>
    Screenshots attached: <yes / no>

Troubleshooting
---------------

- If the module does not appear in Apps, verify the addons path, restart the Odoo service, and update the apps list.
- If installation fails, inspect the server logs for Python, XML, dependency, or access errors.
- If menus or views fail to open, validate XML files, inherited views, field names, and security configuration.
- If a feature is visible to the wrong users, review `ir.model.access.csv`, security groups, and record rules.
- If UI changes do not appear after an update, upgrade the module and refresh browser assets or clear browser cache.
- If reports fail to render, validate report actions, paper formats, template names, and report models.
- If frontend behavior fails, inspect browser console logs and verify that declared assets exist and load correctly.
- If routes fail, validate controller decorators, authentication mode, URLs, and endpoint availability.
- If background automation does not run, verify scheduled actions, server time, execution user, and log output.
- If portal pages fail, validate portal access rights, controller logic, and related QWeb templates.
- If website pages fail, validate website view inheritance and publishing conditions.

Final Technical Notes
---------------------

- This document is generated automatically and should be reviewed before commercial publication.
- Business-specific workflows may still require manual enrichment if they cannot be inferred from the module structure alone.
- The manifest, source tree, and declared assets should be kept synchronized to maintain a reliable customer-facing documentation experience.
