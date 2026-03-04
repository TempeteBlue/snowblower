#!/usr/bin/env python3
"""
Génère automatiquement les fichiers _index.md pour les manuels
à partir des PDFs trouvés dans les dossiers.
"""

import os
import yaml
import re
from pathlib import Path


def find_pdfs_and_images(folder_path):
    """Trouve tous les PDFs et images dans un dossier"""
    pdfs = []
    images = []

    if not os.path.exists(folder_path):
        return pdfs, images

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            if item.lower().endswith(".pdf"):
                title = item.replace(".pdf", "").replace(".PDF", "")
                # Detect language from filename
                lang = ""
                if "-A " in title or "-A" in title:
                    lang = "Anglais"
                elif "-F " in title or "-F" in title:
                    lang = "Français"

                pdfs.append(
                    {
                        "title": title,
                        "file": f"pdf/{folder_path.replace('content/', '').replace(os.sep, '/')}/{item}",
                        "lang": lang,
                    }
                )

    # Look for images in static/images/manuels instead of content/manuels
    static_images_path = folder_path.replace("content/", "static/images/")
    if os.path.exists(static_images_path):
        for item in os.listdir(static_images_path):
            item_path = os.path.join(static_images_path, item)
            if os.path.isfile(item_path) and item.lower().endswith(
                (".jpg", ".jpeg", ".png", ".webp")
            ):
                images.append(
                    f"images/{folder_path.replace('content/', '').replace(os.sep, '/')}/{item}"
                )

    return pdfs, images


def parse_existing_frontmatter(index_path):
    """Parse existing _index.md to extract custom frontmatter like url and aliases"""
    if not os.path.exists(index_path):
        return {}

    try:
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if there's frontmatter
        if content.startswith("---"):
            # Extract frontmatter
            match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            if match:
                frontmatter_text = match.group(1)
                try:
                    existing = yaml.safe_load(frontmatter_text)
                    # Preserve specific fields
                    preserved = {}
                    for key in ["url", "aliases", "slug"]:
                        if key in existing:
                            preserved[key] = existing[key]
                    return preserved
                except:
                    pass
    except:
        pass

    return {}


def generate_index_for_folder(folder_path, relative_path, has_subfolders=False):
    """Génère un fichier _index.md pour un dossier"""
    pdfs, images = find_pdfs_and_images(folder_path)

    # Vérifier si _index.md existe déjà
    index_path = os.path.join(folder_path, "_index.md")

    # Parse existing frontmatter to preserve custom fields
    existing_frontmatter = parse_existing_frontmatter(index_path)

    # Check if this is the root manuals folder
    is_root = relative_path == "" or relative_path == "manuels"

    # Pour un dossier de catégorie (sans PDFs mais avec sous-dossiers)
    if not pdfs and not images and has_subfolders:
        folder_name = os.path.basename(folder_path)

        # Determine title based on folder
        title_map = {
            "Balais": "Brooms",
            "Lames": "Blades",
            "Options": "Options",
            "Débris": "Debris",
            "Souffleuse-Attaches rapides": "Snow Blowers - Quick Attach",
        }

        frontmatter = {
            "title": title_map.get(folder_name, folder_name),
            "description": f"Parts manuals for {folder_name}",
        }

        # Preserve existing custom fields
        frontmatter.update(existing_frontmatter)

        # Add defaults if not already set
        if "draft" not in frontmatter:
            frontmatter["draft"] = False

        content = f"""---
{yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)}---

# {frontmatter["title"]}
"""

        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✓ Section: {relative_path}/_index.md")
        return True

    # Pour un dossier avec PDFs
    if pdfs or images:
        folder_name = os.path.basename(folder_path)

        frontmatter = {
            "title": folder_name,
            "description": f"Parts manual for {folder_name}",
        }

        # Preserve existing custom fields
        frontmatter.update(existing_frontmatter)

        # Add defaults if not already set
        if "draft" not in frontmatter:
            frontmatter["draft"] = False

        if pdfs:
            frontmatter["manuals"] = pdfs

        if images:
            frontmatter["images"] = images

        content = f"""---
{yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)}---

# {folder_name}

## Specifications



## Additional Information

For any questions about this model or to order parts, feel free to [contact us](/contact/).
"""

        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(
            f"✓ Modèle: {relative_path}/_index.md ({len(pdfs)} PDFs, {len(images)} images)"
        )
        return True

    return False


def scan_manuals_folder():
    """Scanne tous les dossiers dans content/manuels et génère les _index.md"""
    base_path = "content/manuels"

    if not os.path.exists(base_path):
        print(f"❌ Dossier {base_path} non trouvé")
        return

    count = 0

    # D'abord, traiter tous les dossiers récursivement (du plus profond au plus superficiel)
    all_dirs = []
    for root, dirs, files in os.walk(base_path):
        all_dirs.append((root, dirs, files))

    # Inverser pour traiter les dossiers enfants d'abord
    all_dirs.reverse()

    for root, dirs, files in all_dirs:
        relative = root.replace(base_path, "").strip(os.sep)

        # Vérifier si ce dossier a des sous-dossiers
        has_subfolders = len(dirs) > 0

        # Vérifier si ce dossier a des PDFs
        has_pdfs = any(f.lower().endswith(".pdf") for f in files)

        # Générer _index.md si nécessaire
        if has_pdfs or has_subfolders:
            if generate_index_for_folder(root, relative, has_subfolders):
                count += 1

    print(f"\n✅ {count} fichiers _index.md générés")


if __name__ == "__main__":
    scan_manuals_folder()
