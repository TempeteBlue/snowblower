#!/usr/bin/env python3
"""
Ensure root section _index.md files have proper English URLs
This script runs before other index generation scripts
"""

import os
import yaml


def ensure_root_index(section_folder, title, description, url, aliases=None):
    """Ensure a root section _index.md has proper URL configuration"""
    index_path = os.path.join(section_folder, "_index.md")

    # Default frontmatter
    frontmatter = {
        "title": title,
        "description": description,
        "url": url,
    }

    if aliases:
        frontmatter["aliases"] = aliases

    # Check if file exists and preserve certain fields if present
    if os.path.exists(index_path):
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                content = f.read()

            # If file exists with frontmatter, we might want to preserve some fields
            # But for root sections, we enforce the URL
            pass
        except:
            pass

    # Write the _index.md
    content = f"""---
{yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)}---

# {title}

{description}
"""

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✓ Root index: {section_folder}/_index.md -> {url}")
    return True


def main():
    """Ensure all root section indexes have proper URLs"""

    # Ensure manuals root
    ensure_root_index(
        "content/manuels",
        "Manuals",
        "Technical documentation and parts manuals",
        "/manuals/",
        ["/manuels/"],
    )

    # Ensure products root
    ensure_root_index(
        "content/produits",
        "Products",
        "Discover all our products and equipment",
        "/products/",
        ["/produits/"],
    )

    # Ensure usage root
    ensure_root_index(
        "content/usage",
        "Used Equipment",
        "Verified and guaranteed pre-owned equipment",
        "/used/",
        ["/usage/"],
    )

    # Ensure contact root
    ensure_root_index(
        "content/contact",
        "Contact",
        "Contact us for any questions or orders",
        "/contact/",
    )

    print("\n✅ Root section indexes configured with English URLs")


if __name__ == "__main__":
    main()
