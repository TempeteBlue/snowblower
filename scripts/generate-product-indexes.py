#!/usr/bin/env python3
"""
Génère automatiquement les fichiers _index.md pour les produits
à partir des fichiers trouvés dans les dossiers avec structure par catégorie.
Structure: content/produits/<categorie>/<produit>/
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


def generate_product_index(folder_path, category, product_name):
    """Génère un fichier index.md pour un produit"""
    pdfs, images, info = find_files(folder_path)

    if not info and not pdfs and not images:
        return False

    frontmatter = {
        "title": info.get("title", product_name),
        "description": info.get("description", f"Produit {product_name}"),
        "draft": False,
    }

    # Ajouter les specs si présentes dans info.yaml
    if "specs" in info:
        frontmatter["specs"] = info["specs"]

    # Ajouter le prix
    if "price" in info:
        frontmatter["price"] = info["price"]

    # Catégorie basée sur le nom du dossier (pas sur le YAML)
    frontmatter["categories"] = [category]

    # Ajouter les images avec le bon chemin
    if images:
        frontmatter["images"] = [
            f"images/produits/{category}/{product_name}/{img}" for img in images
        ]

    # Ajouter les PDFs avec le bon chemin
    if pdfs:
        frontmatter["documents"] = [
            {
                "title": pdf["title"],
                "file": f"pdf/produits/{category}/{product_name}/{pdf['file']}",
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

Pour toute question ou commande, n'hésitez pas à [nous contacter](/contact/).
"""

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(
        f"✓ Produit: {category}/{product_name}/index.md ({len(pdfs)} PDFs, {len(images)} images)"
    )
    return True


def generate_category_index(folder_path, category_name):
    """Génère un fichier _index.md pour une catégorie"""
    frontmatter = {
        "title": category_name,
        "description": f"Produits {category_name}",
        "draft": False,
    }

    content = f"""---
{yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)}---

# {category_name}

Découvrez nos produits {category_name}.
"""

    index_path = os.path.join(folder_path, "_index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✓ Catégorie: {category_name}/_index.md")
    return True


def scan_products_folder():
    """Scanne tous les dossiers dans content/produits avec structure par catégorie"""
    base_path = "content/produits"

    if not os.path.exists(base_path):
        print(f"❌ Dossier {base_path} non trouvé")
        return

    count_categories = 0
    count_products = 0

    # Parcourir les catégories
    for category in os.listdir(base_path):
        category_path = os.path.join(base_path, category)

        # Ignorer les fichiers et les dossiers spéciaux
        if not os.path.isdir(category_path) or category.startswith("_"):
            continue

        # Générer l'index de la catégorie
        if generate_category_index(category_path, category):
            count_categories += 1

        # Parcourir les produits dans la catégorie
        for product in os.listdir(category_path):
            product_path = os.path.join(category_path, product)

            if not os.path.isdir(product_path) or product.startswith("_"):
                continue

            # Générer l'index du produit
            if generate_product_index(product_path, category, product):
                count_products += 1

    print(f"\n✅ {count_categories} catégories et {count_products} produits générés")


if __name__ == "__main__":
    scan_products_folder()
