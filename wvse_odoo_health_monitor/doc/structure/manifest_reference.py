
# -*- coding: utf-8 -*-
##############################################################################
# Author      : Webvirtual Soluções Empresariais (<webvirtual.com.br>)
# Copyright(c): 2017-present Webvirtual Soluções Empresariais LTDA
# All Rights Reserved.
#
#   This module and its source code are the exclusive property of
#   Webvirtual Soluções Empresariais LTDA.
#
#   Unauthorized copying, reproduction, modification, distribution,
#   sublicensing, resale, publication, or disclosure of this module,
#   via any medium, is strictly prohibited unless previously authorized
#   in writing by the copyright holder.
#
#   This module is provided under proprietary license terms.
#   See the LICENSE file located in the root of this module for the
#   complete legal terms, conditions, copyright notices, and usage rights.
#
##############################################################################
{
    'name': 'wvse_odoo_health_monitor',
    'summary': 'Short business summary of the [wvse_odoo_health_monitor] main features.',
    'version': '15.0.1.0.0',
    'category': 'Project',
    'description': """
wvse Module Name
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
""",
    'author': 'Webvirtual Soluções Empresariais',
    'maintainer': 'Webvirtual',
    'website': 'https://www.webvirtual.com.br',
    'support': 'odoo@webvirtual.com.br',

    # Licensing
    # Common choices:
    # - LGPL-3 for open source
    # - AGPL-3 for stronger copyleft
    # - OPL-1 for proprietary paid apps
    'license': 'OPL-1',

    # Dependencies
    # Always include every module wvse addon needs.
    # base should normally be declared explicitly.
    'depends': [
        'base',
        'mail',
        'web',
    ],

    # Data files are loaded in order.
    # Keep security first, then business data, then views, wizards, and reports.
    'data': [
        # Security
        'security/wvse_odoo_health_monitor_groups.xml',
        'security/ir.model.access.csv',
        'security/wvse_odoo_health_monitor_security.xml',
        'security/ir_rule.xml',

        # Core data
        'data/ir_sequence_data.xml',
        'data/ir_cron_data.xml',
        'data/ir_actions_server.xml',
        'data/ir_config_parameter.xml',
        'data/mail_template_data.xml',
        'data/mail_activity_type_data.xml',
        'data/report_paperformat_data.xml',
        'data/web_tour_data.xml',
        'data/decimal_precision_data.xml',
        'data/wvse_odoo_health_monitor_data.xml',
        'data/wvse_odoo_health_monitor_demo_bridge.xml',
        'data/wvse_odoo_health_monitor_onboarding.xml',

        # Views and UI
        'views/menus.xml',
        'views/actions.xml',
        'views/wvse_model_views.xml',
        'views/wvse_model_form_views.xml',
        'views/wvse_model_tree_views.xml',
        'views/wvse_model_kanban_views.xml',
        'views/wvse_model_search_views.xml',
        'views/wvse_model_calendar_views.xml',
        'views/wvse_model_pivot_views.xml',
        'views/wvse_model_graph_views.xml',
        'views/wvse_model_activity_views.xml',
        'views/wvse_model_cohort_views.xml',
        'views/wvse_model_dashboard_views.xml',
        'views/res_config_settings_views.xml',
        'views/portal_templates.xml',
        'views/website_templates.xml',
        'views/snippets.xml',
        'views/assets.xml',

        # Wizards
        'wizard/wvse_wizard_views.xml',
        'wizard/wvse_batch_wizard_views.xml',

        # Reports
        'report/wvse_report_templates.xml',
        'report/wvse_report_actions.xml',
        'report/wvse_report_paperformat.xml',
        'report/wvse_label_report.xml',
    ],

    # Demo data only for demo databases or demo mode.
    'demo': [
        'demo/demo.xml',
        'demo/wvse_model_demo.xml',
        'demo/demo_users.xml',
    ],

    # Frontend and backend bundles.
    'assets': {
        'web.assets_backend': [
            'wvse_odoo_health_monitor/static/src/scss/variables.scss',
            'wvse_odoo_health_monitor/static/src/scss/backend.scss',
            'wvse_odoo_health_monitor/static/src/css/legacy.css',
            'wvse_odoo_health_monitor/static/src/js/backend.js',
            'wvse_odoo_health_monitor/static/src/js/fields/wvse_custom_field.js',
            'wvse_odoo_health_monitor/static/src/js/views/wvse_custom_view.js',
            'wvse_odoo_health_monitor/static/src/js/components/wvse_component.js',
            'wvse_odoo_health_monitor/static/src/js/components/wvse_dialog.js',
            'wvse_odoo_health_monitor/static/src/js/services/wvse_service.js',
            'wvse_odoo_health_monitor/static/src/js/patches/some_patch.js',
            'wvse_odoo_health_monitor/static/src/js/utils/helpers.js',
        ],
        'web.assets_frontend': [
            'wvse_odoo_health_monitor/static/src/scss/frontend.scss',
            'wvse_odoo_health_monitor/static/src/scss/portal.scss',
            'wvse_odoo_health_monitor/static/src/js/frontend.js',
            'wvse_odoo_health_monitor/static/src/js/portal.js',
        ],
        'website.assets_frontend': [
            'wvse_odoo_health_monitor/static/src/scss/website.scss',
            'wvse_odoo_health_monitor/static/src/js/website.js',
        ],
        'web.assets_qweb': [
            'wvse_odoo_health_monitor/static/src/xml/templates.xml',
            'wvse_odoo_health_monitor/static/src/xml/components.xml',
            'wvse_odoo_health_monitor/static/src/xml/dialogs.xml',
            'wvse_odoo_health_monitor/static/src/xml/qweb/common.xml',
            'wvse_odoo_health_monitor/static/src/xml/qweb/backend.xml',
            'wvse_odoo_health_monitor/static/src/xml/qweb/frontend.xml',
            'wvse_odoo_health_monitor/static/src/xml/qweb/portal.xml',
            'wvse_odoo_health_monitor/static/src/xml/qweb/website.xml',
        ],
        'web.qunit_suite_tests': [
            'wvse_odoo_health_monitor/static/tests/**/*.js',
        ],
    },

    # External requirements.
    'external_dependencies': {
        'python': [
            # 'requests',
            # 'unidecode',
        ],
        'bin': [
            # 'wkhtmltopdf',
        ],
    },

    # Internals images.
    'images': [
        'static/description/main_screen.gif',
        'static/description/*.png',
        'static/description/*.jpg',
        'static/src/img/*.png',
        'static/src/img/*.jpg',
    ],

    # App behavior.
    'application': True,
    'installable': True,
    'auto_install': False,

    # Hooks.
    # The function names must exist and be imported from __init__.py.
    # 'pre_init_hook': 'pre_init_hook',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',

    # Odoo Apps publication metadata.
    # For free apps, omit price/currency or set price <= 0.
    # Official allowed currencies in Apps guidelines are usually EUR or USD.
    'price': 1.99,
    'currency': 'USD',

    # Public demo URL for Odoo Apps listing.
    'live_test_url': 'https://15.odoo.webvirtual.com.br',

    # Notes.
    # Migration directory selected by version strategy: upgrades/
    # Deprecated in core: do not use 'active'.
}
