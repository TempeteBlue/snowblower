#!/usr/bin/env python3
"""
Script d'indexation automatique des manuels PDF
Scanne le dossier static/pdf/ et génère les pages de manuels correspondantes
Usage: python scripts/index-manuals.py
"""

import os
import re
from pathlib import Path
import yaml

# Configuration
PDF_BASE_DIR = Path("static/pdf/manuels")
CONTENT_DIR = Path("content/manuels")


def extract_info_from_filename(filename):
    """Extrait les informations du nom de fichier PDF"""
    # Exemple: SA92B-SA98B OM 0440SB92-A 21900001 rev3 01-19.pdf
    info = {"title": "", "lang": "", "doc_number": "", "revision": "", "date": ""}

    # Détecte la langue (-A pour anglais, -F pour français)
    if "-A" in filename or " OM " in filename and "-A " in filename:
        info["lang"] = "Anglais"
    elif "-F" in filename or " OM " in filename and "-F " in filename:
        info["lang"] = "Français"

    # Extrait la date (format MM-YY ou MM-YYYY)
    date_match = re.search(r"(\d{2})[-/](\d{2,4})", filename)
    if date_match:
        month, year = date_match.groups()
        if len(year) == 2:
            year = "20" + year
        info["date"] = f"{month}/{year}"

    # Extraction du numéro de document
    doc_match = re.search(r"OM\s+(\d+\w+)", filename)
    if doc_match:
        info["doc_number"] = doc_match.group(1)

    # Extraction de la révision
    rev_match = re.search(r"rev(\d+)", filename, re.IGNORECASE)
    if rev_match:
        info["revision"] = rev_match.group(1)

    return info


def scan_manuals_directory():
    """Scanne le répertoire des manuels et organise les données"""
    manuals = {}

    if not PDF_BASE_DIR.exists():
        print(f"⚠️ Dossier {PDF_BASE_DIR} non trouvé")
        return manuals

    for category_dir in PDF_BASE_DIR.iterdir():
        if not category_dir.is_dir():
            continue

        category = category_dir.name
        manuals[category] = {}

        for model_dir in category_dir.iterdir():
            if not model_dir.is_dir():
                continue

            model = model_dir.name
            manuals[category][model] = {
                "pdfs": [],
                "path": str(model_dir.relative_to(PDF_BASE_DIR)),
            }

            # Scanne les PDF
            for pdf_file in model_dir.rglob("*.pdf"):
                # Ignore les dossiers archives et désuets
                if (
                    "archives" in str(pdf_file).lower()
                    or "désuet" in str(pdf_file).lower()
                ):
                    continue

                rel_path = pdf_file.relative_to(Path("static"))
                info = extract_info_from_filename(pdf_file.name)

                manuals[category][model]["pdfs"].append(
                    {
                        "file": f"{rel_path}",
                        "title": pdf_file.stem,
                        "lang": info["lang"],
                        "date": info["date"],
                        "version": info["revision"],
                    }
                )

    return manuals


def generate_manual_page(category, model, data):
    """Génère une page de manuel en Markdown"""
    # Détermine les années si présentes dans le nom
    years = ""
    year_match = re.search(r"(\d{4})", model)
    if year_match:
        years = year_match.group(1)

    # Nettoie le titre
    title = model.replace("-", " ").replace("_", " ")

    # Construit le frontmatter
    frontmatter = {
        "title": title,
        "description": f"Manuels de pièces pour {title}",
        "date": "2024-01-01",
        "categories": [category.capitalize()],
        "years": years,
        "draft": False,
        "manuals": [],
    }

    # Ajoute les PDF au frontmatter
    for pdf in data["pdfs"]:
        frontmatter["manuals"].append(
            {
                "title": pdf["title"][:50] + "..."
                if len(pdf["title"]) > 50
                else pdf["title"],
                "file": pdf["file"],
                "lang": pdf["lang"],
                "date": pdf["date"],
                "version": pdf["version"],
                "description": f"Manuel {pdf['lang']}" if pdf["lang"] else "",
            }
        )

    # Génère le contenu
    md_content = f"""---
{yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)}---

# {title}

Cette page contient tous les manuels de pièces disponibles pour le modèle **{title}**.

## Documents disponibles

{{ range .Params.manuals }}
### {{ .title }}

- **Langue**: {{ .lang }}
- **Date**: {{ .date }}
- **Version**: {{ .version }}

[📥 Télécharger le PDF]({{ .file }})

{{ end }}

## Informations complémentaires

Pour toute question concernant ce modèle ou pour commander des pièces, n'hésitez pas à [nous contacter](/contact/).

---

*Dernière mise à jour: {{ now.Format "2 janvier 2006" }}*
"""

    return md_content


def main():
    """Fonction principale"""
    print("📁 Indexation des manuels PDF...")

    # Scanne les répertoires
    manuals = scan_manuals_directory()

    if not manuals:
        print("⚠️ Aucun manuel trouvé")
        return

    generated_count = 0

    # Génère les pages pour chaque catégorie et modèle
    for category, models in manuals.items():
        category_dir = CONTENT_DIR / category.lower()
        category_dir.mkdir(parents=True, exist_ok=True)

        # Crée la page d'index de catégorie
        index_file = category_dir / "_index.md"
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(f"""---
title: "{category.capitalize()}"
description: "Manuels de pièces pour {category.lower()}"
---

# {category.capitalize()}

Retrouvez ci-dessous tous les manuels de pièces pour nos équipements de type **{category.lower()}**.
""")
        print(f"  ✓ {index_file}")

        for model, data in models.items():
            if not data["pdfs"]:
                continue

            # Crée un slug pour le fichier
            model_slug = (
                re.sub(r"[^\w\s-]", "", model).strip().lower().replace(" ", "-")
            )
            output_file = category_dir / f"{model_slug}.md"

            # Skip if file already exists (preserve manual edits)
            if output_file.exists():
                print(f"  ⏭️  {output_file} (existe déjà, préservé)")
                continue

            # Génère le contenu
            content = generate_manual_page(category, model, data)

            # Écrit le fichier
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"  ✓ {output_file} ({len(data['pdfs'])} PDF)")
            generated_count += 1

    print(f"\n✅ {generated_count} pages de manuels générées")
    print(f"📁 Emplacement: {CONTENT_DIR}/")


if __name__ == "__main__":
    main()
