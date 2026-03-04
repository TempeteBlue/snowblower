#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour traiter les dossiers de manuels simples
Structure attendue: content/manuels/<categorie>/<modele>/
  - info.yaml (métadonnées)
  - *.pdf (le manuel)

Le script copie le PDF vers static/pdf/ et génère le fichier .md
"""

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import os
import yaml
from pathlib import Path
import shutil

CONTENT_DIR = Path("content/manuels")
STATIC_PDF_DIR = Path("static/pdf/manuels")
STATIC_IMAGES_DIR = Path("static/images/manuels")


def process_manual_folders():
    """Traite tous les dossiers de manuels"""

    for category_dir in CONTENT_DIR.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith("_"):
            continue

        category = category_dir.name

        for model_dir in category_dir.iterdir():
            if not model_dir.is_dir() or model_dir.name.startswith("_"):
                continue

            yaml_file = model_dir / "info.yaml"
            pdf_files = list(model_dir.glob("*.pdf"))

            if not yaml_file.exists() or not pdf_files:
                continue

            # Lire les métadonnées
            with open(yaml_file, "r", encoding="utf-8") as f:
                metadata = yaml.safe_load(f)

            model_name = model_dir.name
            pdf_target_dir = STATIC_PDF_DIR / category / model_name
            pdf_target_dir.mkdir(parents=True, exist_ok=True)

            # Copier les images (jpg, png, webp)
            images_data = []
            image_target_dir = STATIC_IMAGES_DIR / category / model_name
            image_target_dir.mkdir(parents=True, exist_ok=True)
            image_files = (
                list(model_dir.glob("*.jpg"))
                + list(model_dir.glob("*.jpeg"))
                + list(model_dir.glob("*.png"))
                + list(model_dir.glob("*.webp"))
            )
            image_files = [f for f in image_files if f.name != "desktop.ini"]

            # Also check for PNG files generated from PDFs (same name as PDF)
            pdf_names = [pdf.stem for pdf in pdf_files]
            png_from_pdf = [
                model_dir / f"{pdf_name}.png"
                for pdf_name in pdf_names
                if (model_dir / f"{pdf_name}.png").exists()
            ]
            image_files.extend(png_from_pdf)
            # Remove duplicates
            image_files = list(set(image_files))

            for img_file in image_files:
                target_img = image_target_dir / img_file.name
                shutil.copy2(img_file, target_img)
                images_data.append(
                    f"images/manuels/{category}/{model_name}/{img_file.name}"
                )
                print(f"  🖼️ Copié: {img_file.name}")

            manuals_data = []

            for pdf_file in pdf_files:
                # Copier le PDF
                target_pdf = pdf_target_dir / pdf_file.name
                shutil.copy2(pdf_file, target_pdf)
                print(f"  📄 Copié: {pdf_file.name}")

                # Construire les données du manuel
                lang = metadata.get("lang", "Français")
                if "-A" in pdf_file.name:
                    lang = "Anglais"
                elif "-F" in pdf_file.name:
                    lang = "Français"

                # Utiliser le nom du fichier PDF comme titre (conserver les tirets)
                pdf_title = pdf_file.stem

                manuals_data.append(
                    {
                        "title": pdf_title,
                        "file": f"pdf/manuels/{category}/{model_name}/{pdf_file.name}",
                        "lang": lang,
                        "date": metadata.get("date", ""),
                        "version": metadata.get("version", ""),
                        "description": metadata.get("description", ""),
                    }
                )

            # Générer le fichier _index.md dans le dossier du modèle
            md_content = generate_markdown(
                metadata, model_name, category, manuals_data, images_data
            )
            md_file = model_dir / "_index.md"

            with open(md_file, "w", encoding="utf-8") as f:
                f.write(md_content)

            print(f"  ✓ Généré: {md_file}")


def generate_markdown(metadata, model_name, category, manuals_data, images_data=None):
    """Génère le contenu markdown"""

    if images_data is None:
        images_data = []

    frontmatter = {
        "title": metadata.get("title", model_name),
        "slug": model_name,
        "description": metadata.get("description", f"Manuels pour {model_name}"),
        "years": metadata.get("years", ""),
        "draft": False,
        "manuals": manuals_data,
    }

    if "specs" in metadata:
        frontmatter["specs"] = metadata["specs"]

    if images_data:
        frontmatter["images"] = images_data

    yaml_content = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)

    # Hugo template parts (using regular strings, not f-strings)
    # Note: Les manuels sont déjà affichés par le template layouts/manuels/single.html
    hugo_template = """## Informations complémentaires

Pour toute question concernant ce modèle ou pour commander des pièces, n'hésitez pas à [nous contacter](/contact/).
"""

    return (
        f"""---
{yaml_content}---

# {metadata.get("title", model_name)}

{metadata.get("description", "")}

## Caractéristiques

{generate_specs_table(metadata.get("specs", {}))}

"""
        + hugo_template
    )


def generate_specs_table(specs):
    """Génère un tableau de spécifications"""
    if not specs:
        return ""

    lines = []
    for key, value in specs.items():
        lines.append(f"- **{key}**: {value}")

    return "\n".join(lines)


if __name__ == "__main__":
    print("📁 Traitement des dossiers de manuels...")
    process_manual_folders()
    print("\n✅ Traitement terminé!")
