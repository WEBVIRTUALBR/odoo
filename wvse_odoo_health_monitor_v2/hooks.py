"""
Module hooks.

This file defines optional pre-init, post-init, and uninstall hooks.
"""


def pre_init_hook(cr):
    """
    Execute logic before module installation.
    """
    return None


def post_init_hook(cr, registry):
    """
    Execute logic after module installation.
    """
    return None


def uninstall_hook(cr, registry):
    """
    Execute logic before or during module uninstallation.
    """
    return None
