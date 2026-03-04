#!/usr/bin/env python3
"""
Met à jour les fichiers index.md des produits avec les images et PDFs trouvés.
"""

import os
import yaml
from pathlib import Path


def find_files(folder_path):
    """Trouve tous les PDFs et images dans un dossier"""
    pdfs = []
    images = []

    if not os.path.exists(folder_path):
        return pdfs, images

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            if item.lower().endswith(".pdf"):
                pdfs.append(
                    {
                        "title": item.replace(".pdf", "").replace(".PDF", ""),
                        "file": f"pdf/produits/{os.path.basename(folder_path)}/{item}",
                    }
                )
            elif item.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")):
                images.append(f"images/produits/{os.path.basename(folder_path)}/{item}")

    return pdfs, images


def update_product_index(folder_path):
    """Met à jour le fichier index.md d'un produit"""
    index_path = os.path.join(folder_path, "index.md")

    if not os.path.exists(index_path):
        return False

    # Lire le fichier existant
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Séparer frontmatter et contenu
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1].strip()
            body = parts[2].strip()

            # Parser le frontmatter
            try:
                frontmatter = yaml.safe_load(frontmatter_text) or {}
            except:
                frontmatter = {}
        else:
            frontmatter = {}
            body = content
    else:
        frontmatter = {}
        body = content

    # Trouver les fichiers
    pdfs, img_list = find_files(folder_path)

    # Mettre à jour le frontmatter
    if img_list:
        frontmatter["images"] = img_list

    if pdfs:
        frontmatter["documents"] = pdfs

    # Réécrire le fichier
    new_frontmatter = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
    new_content = f"""---
{new_frontmatter}---

{body}
"""

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Updated: {index_path}")
    return True


def update_all_products():
    """Met à jour tous les produits"""
    base_path = "content/produits"

    if not os.path.exists(base_path):
        print(f"❌ Dossier {base_path} non trouvé")
        return

    count = 0
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            if update_product_index(item_path):
                count += 1

    print(f"\n{count} fichiers index.md mis a jour")


if __name__ == "__main__":
    update_all_products()
