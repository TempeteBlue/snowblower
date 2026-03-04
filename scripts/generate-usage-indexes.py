#!/usr/bin/env python3
"""
Génère automatiquement les fichiers _index.md pour les équipements usagés
à partir des fichiers trouvés dans les dossiers avec structure par catégorie.
Structure: content/usages/<categorie>/<equipement>/
"""

import os
import yaml


def find_files(folder_path):
    """Trouve tous les PDFs, images et fichiers YAML dans un dossier"""
    pdfs = []
    images = []
    info = {}

    if not os.path.exists(folder_path):
        return pdfs, images, info

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            if item.lower().endswith(".pdf"):
                pdfs.append(
                    {
                        "title": item.replace(".pdf", "").replace(".PDF", ""),
                        "file": item,
                    }
                )
            elif item.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                images.append(item)
            elif item.lower() == "info.yaml":
                with open(item_path, "r", encoding="utf-8") as f:
                    info = yaml.safe_load(f) or {}

    return pdfs, images, info


def generate_usage_index(folder_path, category, usage_name):
    """Génère un fichier index.md pour un équipement usagé"""
    pdfs, images, info = find_files(folder_path)

    if not info and not pdfs and not images:
        return False

    frontmatter = {
        "title": info.get("title", usage_name),
        "description": info.get("description", f"Équipement usagé {usage_name}"),
        "draft": False,
    }

    # Ajouter les specs si présentes dans info.yaml
    if "specs" in info:
        frontmatter["specs"] = info["specs"]

    # Ajouter le prix
    if "price" in info:
        frontmatter["price"] = info["price"]

    # Ajouter l'état/condition
    if "condition" in info:
        frontmatter["condition"] = info["condition"]

    # Ajouter l'année
    if "year" in info:
        frontmatter["year"] = info["year"]

    # Ajouter les heures
    if "hours" in info:
        frontmatter["hours"] = info["hours"]

    # Catégorie basée sur le nom du dossier (pas sur le YAML)
    frontmatter["categories"] = [category]

    # Ajouter les images avec le bon chemin
    if images:
        frontmatter["images"] = [
            f"images/usages/{category}/{usage_name}/{img}" for img in images
        ]

    # Ajouter les PDFs avec le bon chemin
    if pdfs:
        frontmatter["documents"] = [
            {
                "title": pdf["title"],
                "file": f"pdf/usages/{category}/{usage_name}/{pdf['file']}",
            }
            for pdf in pdfs
        ]

    index_path = os.path.join(folder_path, "index.md")

    content = f"""---
{yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)}---

# {frontmatter["title"]}

{frontmatter["description"]}

## Détails

Retrouvez toutes les informations techniques et commerciales ci-dessous.

## Contact

Pour toute question ou pour planifier une visite, n'hésitez pas à [nous contacter](/contact/).
"""

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(
        f"✓ Équipement: {category}/{usage_name}/index.md ({len(pdfs)} PDFs, {len(images)} images)"
    )
    return True


def generate_category_index(folder_path, category_name):
    """Génère un fichier _index.md pour une catégorie"""
    frontmatter = {
        "title": category_name,
        "description": f"Équipements usagés {category_name}",
        "draft": False,
    }

    content = f"""---
{yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)}---

# {category_name}

Découvrez nos équipements usagés {category_name}.
"""

    index_path = os.path.join(folder_path, "_index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✓ Catégorie: {category_name}/_index.md")
    return True


def scan_usages_folder():
    """Scanne tous les dossiers dans content/usage avec structure par catégorie"""
    base_path = "content/usage"

    if not os.path.exists(base_path):
        print(f"❌ Dossier {base_path} non trouvé")
        return

    count_categories = 0
    count_usages = 0

    # Parcourir les catégories
    for category in os.listdir(base_path):
        category_path = os.path.join(base_path, category)

        # Ignorer les fichiers et les dossiers spéciaux
        if not os.path.isdir(category_path) or category.startswith("_"):
            continue

        # Générer l'index de la catégorie
        if generate_category_index(category_path, category):
            count_categories += 1

        # Parcourir les équipements dans la catégorie
        for usage in os.listdir(category_path):
            usage_path = os.path.join(category_path, usage)

            if not os.path.isdir(usage_path) or usage.startswith("_"):
                continue

            # Générer l'index de l'équipement
            if generate_usage_index(usage_path, category, usage):
                count_usages += 1

    print(
        f"\n✅ {count_categories} catégories et {count_usages} équipements usagés générés"
    )


if __name__ == "__main__":
    scan_usages_folder()
