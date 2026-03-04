# 📖 Guide d'Utilisation Rapide

## 🎯 Cas d'usage fréquents

### 1. Modifier le prix d'un produit

```bash
# Éditer le fichier CSV
nano data/produits.csv

# Modifier la colonne 'price' pour le produit concerné

# Commit & push
git add data/produits.csv
git commit -m "Mise à jour prix SA92B"
git push
```

✅ Le site se met à jour automatiquement en ~2 minutes

### 2. Ajouter un nouveau modèle de manuel

```bash
# Créer la structure
mkdir -p static/pdf/manuels/souffleuses/Nouveau-Modele

# Copier les PDF
cp /chemin/vers/manuel.pdf static/pdf/manuels/souffleuses/Nouveau-Modele/

# Commit & push
git add static/pdf/
git commit -m "Ajout manuel Nouveau-Modele"
git push
```

✅ La page du modèle est créée automatiquement

### 3. Modifier les informations de contact

Éditer `hugo.toml`:

```toml
[params]
  phone = "(450) 555-0123"
  email = "nouveau@email.com"
  address = "456 Nouvelle Adresse, Ville, QC"
```

### 4. Ajouter une photo à un produit

```bash
# Copier l'image (dimensions recommandées: 800x600)
cp photo.jpg static/images/produits/mon-produit.jpg

# Mettre à jour le CSV
data/produits.csv:
  image: images/produits/mon-produit.jpg
```

### 5. Créer une page promotionnelle

```bash
# Créer la page
hugo new content pages/promo-hiver.md

# Éditer
nano content/pages/promo-hiver.md
```

Contenu:
```markdown
---
title: "Promotion Hiver 2024"
description: "Offres spéciales sur les souffleuses"
---

# ❄️ Promotion Hiver 2024

## Offres du moment

- **SA92B**: 10% de rabais
- **B84A**: Livraison gratuite
...
```

## 📋 Checklist avant publication

- [ ] Modifier `hugo.toml` avec vos informations
- [ ] Remplacer les images placeholder
- [ ] Copier vos PDF dans `static/pdf/manuels/`
- [ ] Vérifier les liens email/téléphone
- [ ] Tester en local: `hugo server -D`
- [ ] Activer GitHub Pages dans les settings
- [ ] Faire un premier commit & push

## 🔍 Tester en local

```bash
# Installation Hugo
# macOS: brew install hugo
# Windows: choco install hugo-extended
# Linux: sudo apt install hugo

# Lancer le serveur
hugo server -D --bind 0.0.0.0

# Accéder à http://localhost:1313
```

## 📊 Surveiller les déploiements

1. Aller sur l'onglet **Actions** du repo GitHub
2. Voir l'état du workflow "Deploy Hugo Site"
3. Cliquer sur le workflow pour voir les logs

## 🆘 Dépannage rapide

| Problème | Solution |
|----------|----------|
| Page blanche | Vérifier `baseURL` dans hugo.toml |
| CSS non chargé | Vérifier que le site est à la racine ou ajuster baseURL |
| Images cassées | Vérifier les chemins (doivent commencer par /) |
| PDF non trouvé | Vérifier qu'ils sont bien dans static/pdf/ |
| Build échoue | Vérifier la syntaxe YAML des fichiers markdown |

## 💡 Astuces

### Utiliser des versions antérieures des manuels

Créer un sous-dossier `Archives/`:
```
static/pdf/manuels/souffleuses/Modele/Archives/manuel-ancien.pdf
```

### Gérer les produits en rupture

Dans `data/produits.csv`:
```csv
SKU123,Produit,Catégorie,999.99,Sur commande,Description...,image.jpg,,false,false
```

### Personnaliser le style

Modifier `assets/css/style.css`:
```css
/* Changer la couleur principale */
:root {
  --color-primary: #votre-couleur;
}

/* Ajouter un style personnalisé */
.ma-classe {
  ...
}
```

---

**Besoin d'aide ?** Consulter le [README complet](README.md)
