\
#!/usr/bin/env python3
"""Generate repository README metadata by scanning Odoo module manifests."""

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


def normalize_text(value: Any) -> str:
    if value is None:
        return "-"
    text = str(value).strip()
    return text if text else "-"


def shorten_text(value: Any, max_len: int = 280) -> str:
    text = normalize_text(value)
    if text == "-":
        return text
    normalized = " ".join(text.replace("\r\n", "\n").replace("\r", "\n").split())
    if len(normalized) <= max_len:
        return normalized
    return normalized[: max_len - 1].rstrip() + "…"


def to_bool_text(value: Any) -> str:
    return "Yes" if bool(value) else "No"


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
    return normalize_text(value).replace("|", "\\|").replace("\n", "<br>")


def extract_module_record(root: Path, manifest_path: Path) -> dict[str, Any]:
    module_dir = manifest_path.parent
    manifest = parse_manifest(manifest_path)

    return {
        "technical_name": module_dir.name,
        "relative_dir": module_dir.relative_to(root).as_posix(),
        "manifest_path": manifest_path.relative_to(root).as_posix(),
        "name": normalize_text(manifest.get("name")),
        "summary": shorten_text(manifest.get("summary")),
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
                    "website": "-",
                    "support": "-",
                }
            )
    return sorted(modules, key=lambda item: (item["technical_name"], item["relative_dir"]))


def build_repository_tree(root: Path) -> str:
    lines = [root.name + "/"]

    entries = [
        entry
        for entry in sorted(root.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
        if not entry.name.startswith(".") and entry.name not in IGNORED_DIR_NAMES
    ]

    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "
        lines.append(connector + entry.name + ("/" if entry.is_dir() else ""))
    return "\n".join(lines)


def render_module_inventory(modules: list[dict[str, Any]]) -> str:
    if not modules:
        return "No modules were found in this repository.\n"

    blocks: list[str] = []
    for module in modules:
        summary = (
            f"<code>{markdown_escape(module['technical_name'])}</code> | "
            f"{markdown_escape(module['name'])} | "
            f"{markdown_escape(module['version'])} | "
            f"{markdown_escape(module['category'])} | "
            f"{markdown_escape(module['license'])} | "
            f"{markdown_escape(module['display_price'])}"
        )

        body = f"""<details>
<summary>{summary}</summary>

- **Application:** {to_bool_text(module['application'])}
- **Installable:** {to_bool_text(module['installable'])}
- **Auto Install:** {to_bool_text(module['auto_install'])}
- **Author:** {markdown_escape(module['author'])}
- **Maintainer:** {markdown_escape(module['maintainer'])}
- **Path:** <code>{markdown_escape(module['relative_dir'])}</code>
- **Manifest:** <code>{markdown_escape(module['manifest_path'])}</code>
- **Website:** {markdown_escape(module['website'])}
- **Support:** {markdown_escape(module['support'])}
- **Summary:** {markdown_escape(module['summary'])}

</details>"""
        blocks.append(body)

    legend = (
        "**Columns:** Technical Name | Module Name | Version | Category | License | Price\n\n"
    )
    return legend + "\n\n".join(blocks) + "\n"


def main() -> None:
    modules = scan_modules(ROOT)
    total_modules = len(modules)
    total_applications = sum(1 for module in modules if module["application"])
    total_installable = sum(1 for module in modules if module["installable"])
    total_auto_install = sum(1 for module in modules if module["auto_install"])
    unique_licenses = sorted({module["license"] for module in modules if module["license"] != "-"})

    content = f"""# Odoo Apps Repository

Repository-level inventory, publication support, and legal metadata for Odoo modules maintained by **Webvirtual**.

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
| Modules Found | {total_modules} |
| Applications | {total_applications} |
| Installable Modules | {total_installable} |
| Auto Install Enabled | {total_auto_install} |
| Distinct Licenses | {len(unique_licenses)} |

## Module Inventory

{render_module_inventory(modules)}

## Repository Root Tree

```text
{build_repository_tree(ROOT)}
```

## Publication Notes

- This README is generated automatically from all discovered `__manifest__.py` files below the repository root.
- The technical name is derived from the folder that contains each manifest.
- Each module inventory item is collapsed by default to keep the repository README compact.
- This repository README intentionally excludes per-module structure trees.
- Repository legal files are generated by `_license.py`, `_copyright.py`, and `_notice.py`.

---

Generated automatically in {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.
"""

    output_path = ROOT / "README.md"
    output_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
