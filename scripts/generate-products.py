#!/usr/bin/env python3
"""
Script de génération automatique des pages produits à partir de data/produits.csv
Usage: python scripts/generate-products.py
"""

import csv
import os
import yaml
from pathlib import Path

# Configuration
CONTENT_DIR = Path("content/produits")
DATA_DIR = Path("scripts/data")
CSV_FILE = DATA_DIR / "produits.csv"
SPECS_FILE = Path("data/specs.yaml")


def slugify(text):
    """Convertit un texte en slug URL-friendly"""
    return text.lower().replace(" ", "-").replace("/", "-").replace("\\", "-")


def load_specs():
    """Charge les spécifications depuis le fichier YAML"""
    if SPECS_FILE.exists():
        with open(SPECS_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


def generate_product_page(product, specs_data):
    """Génère le contenu Markdown d'un produit"""
    sku = product["sku"].lower()
    name = product["name"]
    category = product["category"]
    description = product["description"]
    image = product.get("image", "")
    manual_ref = product.get("manual_ref", "")
    in_stock = product.get("in_stock", "true").lower() == "true"
    featured = product.get("featured", "false").lower() == "true"

    # Récupère les specs spécifiques au produit
    product_specs = specs_data.get(sku, {})

    # Construit le frontmatter YAML
    frontmatter = {
        "title": name,
        "description": description,
        "date": "2024-01-01",  # Date par défaut
        "categories": [category],
        "tags": [category.lower(), "équipement", "hiver"],
        "image": image if image else "images/produits/placeholder.jpg",
        "manual_ref": f"/{manual_ref}/" if manual_ref else "",
        "in_stock": in_stock,
        "featured": featured,
        "sku": sku.upper(),
        "specs": product_specs,
        "draft": False,
    }

    # Génère le contenu Markdown
    md_content = f"""---
{yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)}---

{name}

## Description

{description}

## Caractéristiques principales

"""

    # Ajoute les specs dans le contenu
    if product_specs:
        for key, value in product_specs.items():
            md_content += f"- **{key.capitalize()}**: {value}\n"

    md_content += f"""

## Informations complémentaires

- **Référence (SKU)**: {sku.upper()}
- **Disponibilité**: {"En stock" if in_stock else "Sur commande"}
- **Garantie**: {product_specs.get("garantie", "Voir détails en magasin")}

Pour plus d'informations ou pour commander ce produit, [contactez-nous](/contact/?produit={slugify(name)}).
"""

    return md_content


def main():
    """Fonction principale"""
    print("🔄 Génération des pages produits...")

    # Crée le dossier de contenu s'il n'existe pas
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    # Charge les spécifications
    specs_data = load_specs()
    print(f"✓ Spécifications chargées: {len(specs_data)} produits")

    # Charge et traite le CSV
    if not CSV_FILE.exists():
        print(f"⚠️ Fichier {CSV_FILE} non trouvé")
        return

    generated_count = 0
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for product in reader:
            sku = product["sku"].lower()
            output_file = CONTENT_DIR / f"{sku}.md"

            # Génère le contenu
            content = generate_product_page(product, specs_data)

            # Écrit le fichier
            with open(output_file, "w", encoding="utf-8") as out:
                out.write(content)

            print(f"  ✓ {output_file}")
            generated_count += 1

    print(f"\n✅ {generated_count} pages produits générées avec succès")
    print(f"📁 Emplacement: {CONTENT_DIR}/")


if __name__ == "__main__":
    main()
