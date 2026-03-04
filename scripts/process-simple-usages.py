#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour traiter les dossiers d'équipements usagés avec structure par catégorie
Structure attendue: content/usages/<categorie>/<equipement>/
  - info.yaml (métadonnées)
  - *.jpg, *.png, *.jpeg (images)
  - *.pdf (documents/fiches techniques)

Le script copie les images vers static/images/usages/<categorie>/ et génère le fichier .md
"""

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import os
import yaml
from pathlib import Path
import shutil

CONTENT_DIR = Path("content/usage")
STATIC_PDF_DIR = Path("static/pdf/usages")
STATIC_IMAGES_DIR = Path("static/images/usages")


def process_usage_folders():
    """Traite tous les dossiers d'équipements usagés (structure: categorie/equipement/)"""

    # Parcourir les catégories (sous-dossiers de content/usages)
    for category_dir in CONTENT_DIR.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith("_"):
            continue

        category = category_dir.name

        # Parcourir les équipements dans chaque catégorie
        for usage_dir in category_dir.iterdir():
            if not usage_dir.is_dir() or usage_dir.name.startswith("_"):
                continue

            yaml_file = usage_dir / "info.yaml"

            if not yaml_file.exists():
                continue

            # Lire les métadonnées
            with open(yaml_file, "r", encoding="utf-8") as f:
                metadata = yaml.safe_load(f)

            usage_name = usage_dir.name

            # Créer les dossiers de destination avec la structure categorie/equipement
            pdf_target_dir = STATIC_PDF_DIR / category / usage_name
            pdf_target_dir.mkdir(parents=True, exist_ok=True)

            image_target_dir = STATIC_IMAGES_DIR / category / usage_name
            image_target_dir.mkdir(parents=True, exist_ok=True)

            # Copier les images
            images_data = []
            image_files = (
                list(usage_dir.glob("*.jpg"))
                + list(usage_dir.glob("*.jpeg"))
                + list(usage_dir.glob("*.png"))
                + list(usage_dir.glob("*.webp"))
            )
            image_files = [f for f in image_files if f.name != "desktop.ini"]

            for img_file in image_files:
                target_img = image_target_dir / img_file.name
                shutil.copy2(img_file, target_img)
                images_data.append(
                    f"images/usages/{category}/{usage_name}/{img_file.name}"
                )
                print(f"  🖼️ Copié: {category}/{usage_name}/{img_file.name}")

            # Copier les PDFs et créer la liste des documents
            documents_data = []
            pdf_files = list(usage_dir.glob("*.pdf"))
            pdf_files = [f for f in pdf_files if f.name != "desktop.ini"]

            for pdf_file in pdf_files:
                target_pdf = pdf_target_dir / pdf_file.name
                shutil.copy2(pdf_file, target_pdf)

                # Utiliser le nom du fichier (sans extension) comme titre
                pdf_title = pdf_file.stem

                documents_data.append(
                    {
                        "title": pdf_title,
                        "file": f"pdf/usages/{category}/{usage_name}/{pdf_file.name}",
                    }
                )
                print(f"  📄 Copié: {category}/{usage_name}/{pdf_file.name}")

            # Générer le fichier markdown
            md_content = generate_markdown(
                metadata, usage_name, category, images_data, documents_data
            )
            md_file = usage_dir / "index.md"

            with open(md_file, "w", encoding="utf-8") as f:
                f.write(md_content)

            print(f"  ✓ Généré: {category}/{usage_name}/index.md")


def generate_markdown(metadata, usage_name, category, images_data, documents_data):
    """Génère le contenu markdown"""

    if images_data is None:
        images_data = []

    frontmatter = {
        "title": metadata.get("title", usage_name),
        "slug": usage_name,
        "description": metadata.get("description", f"Équipement usagé {usage_name}"),
        "date": metadata.get("date", "2024-01-01"),
        "draft": False,
    }

    # Catégorie basée sur le nom du dossier (pas sur le YAML)
    frontmatter["categories"] = [category]

    # Prix
    if "price" in metadata:
        frontmatter["price"] = metadata["price"]
    if "price_note" in metadata:
        frontmatter["price_note"] = metadata["price_note"]

    # État/Condition
    if "condition" in metadata:
        frontmatter["condition"] = metadata["condition"]

    # Année
    if "year" in metadata:
        frontmatter["year"] = metadata["year"]

    # Heures d'utilisation
    if "hours" in metadata:
        frontmatter["hours"] = metadata["hours"]

    # Images
    if images_data:
        frontmatter["images"] = images_data

    # Documents/PDFs
    if documents_data:
        frontmatter["documents"] = documents_data

    # Specs
    if "specs" in metadata:
        frontmatter["specs"] = metadata["specs"]

    # SKU/Référence
    if "sku" in metadata:
        frontmatter["sku"] = metadata["sku"]

    yaml_content = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)

    # Générer le contenu
    content = f"""---
{yaml_content}---

{metadata.get("description", "")}

"""

    # Ajouter les specs dans le contenu
    if "specs" in metadata:
        content += "## Caractéristiques\n\n"
        for key, value in metadata["specs"].items():
            content += f"- **{key}**: {value}\n"
        content += "\n"

    content += """## Informations complémentaires

"""

    if "sku" in metadata:
        content += f"- **Référence (SKU)**: {metadata['sku']}\n"

    if "condition" in metadata:
        content += f"- **État**: {metadata['condition']}\n"

    if "year" in metadata:
        content += f"- **Année**: {metadata['year']}\n"

    if "hours" in metadata:
        content += f"- **Heures d'utilisation**: {metadata['hours']}\n"

    content += f"""

Pour plus d'informations ou pour voir cet équipement, [contactez-nous](/contact/?equipement={usage_name}).
"""

    return content


if __name__ == "__main__":
    print("🔧 Traitement des dossiers d'équipements usagés...")
    process_usage_folders()
    print("\n✅ Traitement terminé!")
