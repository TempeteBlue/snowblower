# Structure des dossiers pour produits et équipements usagés

## Organisation par catégories

Les produits et équipements usagés sont organisés par catégories :

```
content/produits/
├── Souffleurs/
│   ├── blizzard-b48c/
│   │   ├── info.yaml
│   │   ├── hero.jpg (optionnel)
│   │   └── manuel.pdf (optionnel)
│   └── blizzard-b54c/
│       ├── info.yaml
│       └── ...
├── Balais/
│   └── balais-pro-72/
│       ├── info.yaml
│       └── ...
└── Lame/
    └── lame-pro-96/
        ├── info.yaml
        └── ...

content/usages/
├── Souffleuses/
│   ├── souffleuse-industrielle-2019/
│   │   ├── info.yaml
│   │   └── ...
│   └── blizzard-b54c-2022/
│       ├── info.yaml
│       └── ...
└── Balais/
    ├── balais-municipal-2020/
    │   ├── info.yaml
    │   └── ...
    └── balais-pro-72-2021/
        ├── info.yaml
        └── ...
```

## Comment ajouter un produit

1. **Créer la catégorie** (si elle n'existe pas) : `content/produits/NomCategorie/`
2. **Créer le dossier du produit** : `content/produits/NomCategorie/nom-du-produit/`
3. **Ajouter le fichier info.yaml** avec les métadonnées
4. **Ajouter les images** (.jpg, .png, .webp) - optionnel
5. **Ajouter les PDFs** (.pdf) - optionnel

### Exemple info.yaml pour un produit :

```yaml
title: "Blizzard B72c"
description: "Souffleuse à neige professionnelle 72 pouces"
categories:
  - "Souffleuses"
  - "Professionnel"
price: "18 999 $"
price_note: "Prix avant taxes"
sku: "BLZ-B72C-2026"
in_stock: true
date: "2024-01-15"
specs:
  Largeur de travail: "72 pouces (183 cm)"
  Hauteur d'attaque: "30 pouces (76 cm)"
  Poids: "1 200 lbs (544 kg)"
  Garantie: "3 ans / 2000 heures"
```

## Comment ajouter un équipement usagé

1. **Créer la catégorie** (si elle n'existe pas) : `content/usages/NomCategorie/`
2. **Créer le dossier de l'équipement** : `content/usages/NomCategorie/nom-equipement/`
3. **Ajouter le fichier info.yaml** avec les métadonnées
4. **Ajouter les images** (.jpg, .png, .webp) - optionnel
5. **Ajouter les PDFs** (.pdf) - optionnel

### Exemple info.yaml pour un équipement usagé :

```yaml
title: "Souffleuse Industrielle Pro 2019"
description: "Souffleuse industrielle usagée - Excellente condition"
categories:
  - "Souffleuses"
  - "Usagé"
price: "8 500 $"
price_note: "Prix négociable - Financement disponible"
condition: "Excellent"
year: "2019"
hours: "1 250"
sku: "USED-SOUF-2019-001"
date: "2024-02-10"
specs:
  Largeur de travail: "84 pouces (213 cm)"
  Heures d'utilisation: "1 250 heures"
  État général: "Excellent"
  Garantie: "6 mois pièces et main-d'œuvre"
```

## Ce qui se passe automatiquement

Lors du déploiement (GitHub Actions), les scripts Python :

1. **Copient les images** vers `static/images/produits/categorie/produit/` ou `static/images/usages/categorie/equipement/`
2. **Copient les PDFs** vers `static/pdf/produits/categorie/produit/` ou `static/pdf/usages/categorie/equipement/`
3. **Génèrent le fichier** `index.md` avec tout le frontmatter (images et PDFs détectés automatiquement)
4. **Mettent à jour les index** des catégories

## Champs disponibles

### Champs communs (produits et usagés)

- `title` - Nom du produit/équipement
- `description` - Description courte
- `categories` - Liste des catégories
- `price` - Prix (format texte)
- `price_note` - Note sur le prix
- `sku` - Référence/SKU
- `specs` - Spécifications techniques (dictionnaire)
- `date` - Date de publication

### Champs spécifiques aux produits neufs

- `in_stock` - Boolean (true/false)

### Champs spécifiques aux équipements usagés

- `condition` - État (Excellent, Très bon, Bon, etc.)
- `year` - Année de fabrication
- `hours` - Heures d'utilisation

## Important

- **Ne pas modifier** les fichiers `index.md` générés - ils seront écrasés
- **Modifier uniquement** le fichier `info.yaml` et ajouter les images/PDFs
- Les images et PDFs sont **détectés automatiquement** - pas besoin de les lister dans le YAML
- Le script scanne tous les fichiers `.jpg`, `.png`, `.webp` et `.pdf` dans le dossier
