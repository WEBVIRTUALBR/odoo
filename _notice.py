#!/usr/bin/env python3
"""Generate repository metadata by scanning Odoo module manifests."""

from __future__ import annotations

import ast
import os
from datetime import datetime
from pathlib import Path
from typing import Any

CURRENT_YEAR = datetime.now().year
ROOT = Path(__file__).resolve().parent
IGNORED_DIR_NAMES = {
    ".git",
    ".github",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
}


def is_ignored(path: Path) -> bool:
    return any(part.startswith(".") or part in IGNORED_DIR_NAMES for part in path.parts)


def parse_manifest(manifest_path: Path) -> dict[str, Any]:
    source = manifest_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(manifest_path))

    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Dict):
            return ast.literal_eval(node.value)
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
            return ast.literal_eval(node.value)

    raise ValueError(f"Could not locate a manifest dictionary in {manifest_path}")


def iter_manifest_paths(root: Path) -> list[Path]:
    manifests: list[Path] = []
    for current_root, dir_names, file_names in os.walk(root):
        current_path = Path(current_root)
        rel_path = current_path.relative_to(root)

        if rel_path != Path(".") and is_ignored(rel_path):
            dir_names[:] = []
            continue

        dir_names[:] = sorted(
            name
            for name in dir_names
            if not name.startswith(".") and name not in IGNORED_DIR_NAMES
        )

        if "__manifest__.py" in file_names:
            manifests.append(current_path / "__manifest__.py")

    return sorted(manifests)


def shorten_text(value: Any, max_len: int = 240) -> str:
    if value is None:
        return "-"
    text = str(value).strip().replace("\r\n", "\n").replace("\r", "\n")
    text = " ".join(part for part in text.split())
    if not text:
        return "-"
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def to_bool_text(value: Any) -> str:
    return "Yes" if bool(value) else "No"


def normalize_text(value: Any) -> str:
    if value is None:
        return "-"
    text = str(value).strip()
    return text if text else "-"


def format_price(price: Any, currency: Any) -> str:
    if price in (None, "", False):
        return "-"
    currency_text = normalize_text(currency)
    try:
        numeric = float(price)
        return f"{currency_text} {numeric:,.2f}"
    except (TypeError, ValueError):
        return f"{currency_text} {price}"


def markdown_escape(value: Any) -> str:
    text = normalize_text(value).replace("|", "\\|").replace("\n", "<br>")
    return text


def extract_module_record(root: Path, manifest_path: Path) -> dict[str, Any]:
    module_dir = manifest_path.parent
    manifest = parse_manifest(manifest_path)
    technical_name = module_dir.name
    relative_dir = module_dir.relative_to(root).as_posix()

    summary = shorten_text(manifest.get("summary"))
    description = shorten_text(manifest.get("description"), max_len=1000)

    return {
        "technical_name": technical_name,
        "relative_dir": relative_dir,
        "manifest_path": manifest_path.relative_to(root).as_posix(),
        "name": normalize_text(manifest.get("name")),
        "summary": summary,
        "description": description,
        "version": normalize_text(manifest.get("version")),
        "category": normalize_text(manifest.get("category")),
        "author": normalize_text(manifest.get("author")),
        "maintainer": normalize_text(manifest.get("maintainer")),
        "license": normalize_text(manifest.get("license")),
        "application": bool(manifest.get("application", False)),
        "installable": bool(manifest.get("installable", False)),
        "auto_install": bool(manifest.get("auto_install", False)),
        "price": manifest.get("price"),
        "currency": normalize_text(manifest.get("currency")),
        "display_price": format_price(manifest.get("price"), manifest.get("currency")),
        "depends": manifest.get("depends", []) if isinstance(manifest.get("depends", []), list) else [],
        "website": normalize_text(manifest.get("website")),
        "support": normalize_text(manifest.get("support")),
    }


def scan_modules(root: Path) -> list[dict[str, Any]]:
    modules: list[dict[str, Any]] = []
    for manifest_path in iter_manifest_paths(root):
        try:
            modules.append(extract_module_record(root, manifest_path))
        except Exception as exc:
            modules.append(
                {
                    "technical_name": manifest_path.parent.name,
                    "relative_dir": manifest_path.parent.relative_to(root).as_posix(),
                    "manifest_path": manifest_path.relative_to(root).as_posix(),
                    "name": "Manifest parsing error",
                    "summary": shorten_text(exc),
                    "description": shorten_text(exc),
                    "version": "-",
                    "category": "-",
                    "author": "-",
                    "maintainer": "-",
                    "license": "-",
                    "application": False,
                    "installable": False,
                    "auto_install": False,
                    "price": None,
                    "currency": "-",
                    "display_price": "-",
                    "depends": [],
                    "website": "-",
                    "support": "-",
                }
            )
    return sorted(modules, key=lambda item: (item["technical_name"], item["relative_dir"]))


def build_tree(root_path: Path, max_depth: int = 5, max_entries_per_dir: int = 50) -> str:
    lines: list[str] = [root_path.name + "/"]

    def visit(path: Path, prefix: str, depth: int) -> None:
        if depth >= max_depth:
            lines.append(prefix + "└── ...")
            return

        entries = [
            entry
            for entry in sorted(path.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
            if not entry.name.startswith(".") and entry.name not in IGNORED_DIR_NAMES
        ]

        if len(entries) > max_entries_per_dir:
            displayed_entries = entries[:max_entries_per_dir]
            truncated = len(entries) - max_entries_per_dir
        else:
            displayed_entries = entries
            truncated = 0

        for index, entry in enumerate(displayed_entries):
            connector = "└── " if index == len(displayed_entries) - 1 and truncated == 0 else "├── "
            lines.append(prefix + connector + entry.name + ("/" if entry.is_dir() else ""))
            if entry.is_dir():
                child_prefix = prefix + ("    " if connector == "└── " else "│   ")
                visit(entry, child_prefix, depth + 1)

        if truncated:
            lines.append(prefix + f"└── ... ({truncated} more entries)")

    visit(root_path, "", 0)
    return "\n".join(lines)


def render_module_inventory_markdown(modules: list[dict[str, Any]]) -> str:
    header = (
        "| Technical Name | Module Name | Version | Category | License | Application | "
        "Installable | Auto Install | Price | Author | Maintainer |\n"
        "|---|---|---:|---|---|---|---|---|---:|---|---|\n"
    )
    rows = []
    for module in modules:
        rows.append(
            "| "
            + " | ".join(
                [
                    markdown_escape(module["technical_name"]),
                    markdown_escape(module["name"]),
                    markdown_escape(module["version"]),
                    markdown_escape(module["category"]),
                    markdown_escape(module["license"]),
                    to_bool_text(module["application"]),
                    to_bool_text(module["installable"]),
                    to_bool_text(module["auto_install"]),
                    markdown_escape(module["display_price"]),
                    markdown_escape(module["author"]),
                    markdown_escape(module["maintainer"]),
                ]
            )
            + " |"
        )
    return header + ("\n".join(rows) if rows else "| - | No modules found | - | - | - | - | - | - | - | - | - |")


def render_module_inventory_plain(modules: list[dict[str, Any]]) -> str:
    if not modules:
        return "- No modules found."

    lines = []
    for module in modules:
        lines.append(
            f"- {module['technical_name']}: {module['name']} | "
            f"Version={module['version']} | Category={module['category']} | "
            f"License={module['license']} | Application={to_bool_text(module['application'])} | "
            f"Installable={to_bool_text(module['installable'])} | Auto Install={to_bool_text(module['auto_install'])} | "
            f"Price={module['display_price']}"
        )
    return "\n".join(lines)


def main() -> None:
    modules = scan_modules(ROOT)

    content = f"""================================================================
NOTICE
================================================================

This module repository includes legal and ownership metadata for distribution,
commercial delivery, maintenance, and technical support.

Publisher
---------
Webvirtual Soluções Empresariais LTDA
Tax ID : 27.460.661/0001-56
Address : Av Alameda dos Ipês, 8625 Sala 12-A - Vale Do Sereno, Belo Horizonte, Minas Gerais, 34012-970, Brasil
Website : https://www.webvirtual.com.br

Support and Contact
-------------------
Support Email : odoo@webvirtual.com.br
General Email : contato@webvirtual.com.br
Phone 1 : +55 31 97147-4489
Phone 2 : +55 62 99913-2635

Distribution Notice
-------------------
This module may be distributed, installed, maintained, updated, modified, or
used only under the conditions defined by the applicable license in the root
LICENSE file.

For proprietary distributions under OPL-1, redistribution and reuse rights are
limited by the Odoo Proprietary License terms.

For open source distributions under LGPL-3, distribution and modification rights
are governed by the GNU Lesser General Public License version 3 and related terms.

Commercial and Technical Notice
-------------------------------
This NOTICE file is intended to provide repository-level identity, publisher
contact channels, and high-level legal orientation for customers, implementers,
partners, and auditors.

For contract, warranty, implementation, support scope, service-level, or custom
development matters, contact Webvirtual Soluções Empresariais LTDA through the official channels
listed above.

Module Inventory
----------------
{render_module_inventory_plain(modules)}

Generated automatically in {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.
"""

    output_path = ROOT / "NOTICE"
    output_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
