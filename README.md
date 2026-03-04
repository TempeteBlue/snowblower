# 🌨️ Concessionnaire Souffleuses - Site Web Statique

Site web professionnel pour concessionnaire de souffleuses à neige et pièces, généré automatiquement avec Hugo et déployé sur GitHub Pages.

## 🚀 Stack Technique

| Technologie | Justification |
|-------------|---------------|
| **Hugo** | Générateur statique ultra-rapide (site généré en ms), excellent support des taxonomies, templating Go puissant |
| **GitHub Actions** | CI/CD natif GitHub, gratuit pour repos publics, déploiement automatique |
| **GitHub Pages** | Hébergement gratuit, HTTPS intégré, CDN global |
| **Python** | Scripts d'automatisation pour générer le contenu depuis CSV/YAML |

## 📁 Structure du Dépôt

```
concessionnaire-souffleuses/
├── .github/workflows/
│   └── deploy.yml              # Pipeline CI/CD GitHub Actions
├── archetypes/
│   └── default.md              # Template pour nouvelles pages
├── assets/
│   ├── css/
│   │   └── style.css           # Styles principaux (design moderne)
│   └── js/
│       └── main.js             # JavaScript (recherche, menu mobile)
├── content/
│   ├── manuels/                # Section manuels de pièces
│   │   ├── _index.md
│   │   ├── souffleuses/
│   │   ├── balais/
│   │   ├── debris/
│   │   ├── lames/
│   │   └── options/
│   ├── produits/               # Pages produits (générées auto)
│   ├── pages/
│   │   └── contact.md
│   └── _index.md               # Page d'accueil
├── data/
│   ├── produits.csv            # Inventaire produits
│   └── specs.yaml              # Spécifications techniques
├── layouts/
│   ├── _default/               # Templates de base
│   ├── partials/               # Composants réutilisables
│   ├── manuels/                # Templates section manuels
│   └── produits/               # Templates section produits
├── scripts/
│   ├── generate-products.py    # Génère pages produits depuis CSV
│   ├── index-manuals.py        # Indexe les PDF de manuels
│   └── generate-search-index.py # Crée index de recherche
├── static/
│   ├── pdf/manuels/            # Manuels PDF (à copier ici)
│   └── images/                 # Images du site
├── hugo.toml                   # Configuration Hugo
└── README.md                   # Ce fichier
```

## 🎯 Fonctionnalités

### ✅ Implémenté

- **Génération automatique** des pages produits depuis CSV
- **Section Manuels** hiérarchique (Catégorie → Modèle → PDF)
- **Design responsive** moderne (mobile-first)
- **SEO optimisé** (meta tags, Open Graph, sitemap)
- **Recherche plein texte** (index JSON)
- **Multilingue** (FR/EN prêt)
- **Déploiement automatique** sur push

### 🎁 Bonus inclus

- Filtres produits par catégorie
- Gallerie photos par produit
- Navigation breadcrumb
- Optimisation images
- Mode sombre prêt (CSS variables)

## 🚀 Installation & Utilisation

### Prérequis

- [Hugo Extended](https://gohugo.io/installation/) (v0.124.1+)
- Python 3.8+ (pour les scripts d'automatisation)

### Installation locale

```bash
# 1. Cloner le repo
git clone https://github.com/votre-username/concessionnaire-souffleuses.git
cd concessionnaire-souffleuses

# 2. Générer le contenu (optionnel - pour tests)
python scripts/generate-products.py
python scripts/generate-search-index.py

# 3. Lancer le serveur de développement
hugo server -D

# 4. Ouvrir http://localhost:1313
```

## 📝 Workflow: Ajouter un Nouveau Produit

### Méthode 1: Via CSV (Recommandé)

1. **Modifier** `data/produits.csv`:

```csv
sku,name,category,price,price_note,description,image,manual_ref,in_stock,featured
NOUVEAU123,Nouveau Produit,Souffleuse,2999.99,Prix suggéré,Description...,images/produits/nouveau.jpg,manuels/souffleuses/nouveau,true,false
```

2. **Ajouter les specs** dans `data/specs.yaml`:

```yaml
nouveau123:
  largeur: "72 pouces"
  poids: "550 kg"
  # ...
```

3. **Copier l'image** dans `static/images/produits/nouveau.jpg`

4. **Commit & Push**:

```bash
git add .
git commit -m "Ajout nouveau produit NOUVEAU123"
git push origin main
```

✅ **GitHub Actions génère automatiquement la page et déploie !**

### Méthode 2: Manuelle (Markdown)

Créer `content/produits/nouveau-produit.md`:

```yaml
---
title: "Nouveau Produit"
description: "Description du produit"
price: 2999.99
categories: ["Souffleuse"]
image: "images/produits/nouveau.jpg"
manual_ref: "/manuels/souffleuses/nouveau/"
---

Contenu du produit...
```

## 📚 Workflow: Ajouter un Manuel PDF (Simple)

### Méthode 1: Dossier Simple (Recommandé)

Crée juste un dossier avec un YAML et un/des PDF - tout est généré automatiquement !

```
content/manuels/souffleuses/nouveau-modele/
├── info.yaml          # Métadonnées
└── manuel.pdf         # Le fichier PDF
```

**Exemple info.yaml:**
```yaml
title: "Nouveau Modèle"
description: "Manuel de pièces pour le nouveau modèle"
years: "2024+"
date: "01/2024"
version: "1"
lang: "Français"
specs:
  Largeur: "80 pouces"
  Poids: "600 kg"
  Capacité: "Jusqu'à 16 pouces de neige"
```

**Commit & Push:**
```bash
git add content/manuels/souffleuses/nouveau-modele/
git commit -m "Ajout manuel nouveau-modele"
git push origin main
```

✅ **GitHub Actions génère automatiquement la page et copie le PDF au bon endroit !**

### Méthode 2: Manuelle (Avancé)

Si tu veux plus de contrôle sur le contenu:

1. **Créer la structure** dans `static/pdf/manuels/{categorie}/{modele}/`
2. **Copier les PDF** dans le dossier
3. **Créer le fichier markdown** dans `content/manuels/{categorie}/{modele}.md`
4. **Commit & Push**

## 🔧 Configuration GitHub

### 1. Activer GitHub Pages

1. Aller sur **Settings → Pages**
2. Source: **GitHub Actions**

### 2. Configurer hugo.toml

```toml
baseURL = 'https://votre-username.github.io/concessionnaire-souffleuses'
```

### 3. Variables d'environnement (optionnel)

Si vous utilisez des secrets:

```bash
# Settings → Secrets and variables → Actions
GOOGLE_MAPS_API_KEY = votre_cle
```

## 📊 Scripts d'Automatisation

### `scripts/generate-products.py`

Génère les pages Markdown des produits depuis `data/produits.csv`.

```bash
python scripts/generate-products.py
```

**Sortie:**
- `content/produits/{sku}.md` pour chaque produit

### `scripts/index-manuals.py`

Scanne `static/pdf/manuels/` et génère les pages de manuels.

```bash
python scripts/index-manuals.py
```

**Sortie:**
- `content/manuels/{categorie}/{modele}.md`

### `scripts/generate-search-index.py`

Crée un index JSON pour la recherche plein texte.

```bash
python scripts/generate-search-index.py
```

**Sortie:**
- `static/search-index.json`

## 🎨 Personnalisation

### Modifier les couleurs

Éditer `assets/css/style.css`:

```css
:root {
  --color-primary: #votre-couleur;
  --color-accent: #votre-accent;
}
```

### Modifier le logo

Éditer `layouts/partials/header.html`:

```html
<span class="logo-icon">🌨️</span>
<span class="logo-text">Votre Nom</span>
```

### Ajouter une page

```bash
hugo new content pages/ma-page.md
```

## 🚀 Déploiement

### Automatique (par défaut)

Chaque `git push` sur `main` déclenche:
1. Génération du contenu
2. Build Hugo
3. Déploiement sur GitHub Pages

### Manuel

```bash
# Build local
hugo --gc --minify

# Les fichiers sont dans public/
# Déployer manuellement si nécessaire
```

## 📈 Performance

- **Build time:** ~100ms pour 100+ pages
- **Lighthouse Score:** 95+ (Performance, SEO, Accessibilité)
- **Taille moyenne:** < 500KB par page

## 🆘 Support

### Problèmes courants

**Le site ne se déploie pas:**
- Vérifier que GitHub Actions est activé
- Vérifier les permissions dans Settings → Actions

**Les images ne s'affichent pas:**
- Vérifier que les images sont dans `static/images/`
- Utiliser des chemins relatifs: `/images/...`

**Les PDF ne sont pas accessibles:**
- Vérifier que les PDF sont dans `static/pdf/`
- Les fichiers > 100MB ne sont pas supportés par GitHub

## 📝 Licence

Ce projet est sous licence MIT. Vous êtes libre de l'utiliser et le modifier.

## 🙏 Crédits

- [Hugo](https://gohugo.io/)
- [GitHub Pages](https://pages.github.com/)
- Icônes: Emoji natifs

---

**Développé avec ❄️ pour les concessionnaires d'équipements d'hiver**
