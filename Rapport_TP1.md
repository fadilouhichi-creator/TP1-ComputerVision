# Rapport de TP 1 : Introduction aux images numériques (Computer Vision)

**Date limite :** 27/02/2026
**Matière :** Computer Vision 1
**Étudiant :** [Votre Nom et Prénom]
**Section :** [S3 ou S4]

---

## 1. Introduction & Objectif du TP
L'objectif principal de ce TP était de concevoir et de développer une interface graphique (GUI) interactive en utilisant **Python, OpenCV et PyQt5**. Cette application permet d'effectuer des opérations fondamentales de traitement d'images telles que l'extraction des canaux colorimétriques, le calcul et l'affichage d'histogrammes et l'ajustement de la dynamique de l'image (contraste et brillance).

Afin d'aller plus loin, nous avons opté pour une interface moderne (Thème Sombre) robuste contre les redimensionnements intempestifs et nous avons ajouté un **Labo Créatif** contenant des filtres supplémentaires (Détection de contours, Flou, Négatif et Sépia).

---

## 2. Architecture et Outils Utilisés
* **PyQt5** : Utilisé pour la création de l'interface graphique. Le design a été modélisé dans un fichier `design.ui` (converti dynamiquement avec `uic.loadUiType`) structuré via des onglets (`QTabWidget`) et des regroupements (`QGroupBox`).
* **OpenCV (`cv2`)** : La bibliothèque cœur pour le traitement d'images (lecture matricielle, conversion d'espaces colorimétriques, seuillage, filtres).
* **NumPy** : Utilisé pour extraire les canaux de couleurs rapidement par *slicing* des tableaux multidimensionnels et pour lire les fichiers images de manière robuste (gestion des caractères spéciaux avec `np.fromfile`).
* **Matplotlib** : Utilisé pour la génération et la sauvegarde des courbes d’histogrammes (couleurs et niveaux de gris).

---

## 3. Description des Fonctionnalités Réalisées

### A. Chargement et Affichage (Format BGR vers RGB)
Lorsqu'une image est chargée, OpenCV lit les pixels au format BGR. Pour que l'image soit affichée correctement dans le composant PyQt5 (QLabel), nous avons développé une méthode `convert_cv_qt()` qui convertit la matrice numpy BGR en format lisible par Qt (`QImage.Format_BGR888` vers `QPixmap`). Nous avons également implémenté une fonction pour afficher les dimensions réelles de l'image.

> **[Insérez ici une capture d'écran de l'application avec une image chargée montrant ses dimensions]**

### B. Séparation des Canaux RVB (Onglet 1)
Nous avons utilisé le *slicing Numpy* pour isoler les composantes de l'image. 
Par exemple, pour extraire le rouge : 
```python
r_img = np.zeros_like(img_bgr)
r_img[:,:,2] = img_bgr[:,:,2] # Récupération de l'index 2 (Rouge en BGR)
```
> **[Insérez ici une capture d'écran montrant l'image originale et ses 3 canaux Rouge, Vert, Bleu extraits]**

### C. Histogrammes des Couleurs (Onglet 2)
Nous utilisons `cv2.calcHist()` itérativement sur les 3 canaux de base (Bleu, Vert, Rouge). Ensuite, `matplotlib` génère un graphique avec les 3 courbes empilées que l'on sauvegarde temporairement dans un fichier `.png` pour l'afficher dynamiquement dans l'interface PyQt5.

> **[Insérez ici une capture d'écran de l'histogramme des couleurs généré]**

### D. Transformation Niveaux de Gris, Contraste et Brillance (Onglet 3)
La modification de la dynamique de l'image est commandée par l'équation mathématique linéaire : `Image_Nouvelle = Image_Originale * alpha + beta`.
* **Alpha (Contraste)** et **Beta (Brillance)** sont récupérés depuis les zones de saisie.
* Nous utilisons `cv2.convertScaleAbs()` pour appliquer l'opération sans dépasser la valeur binaire (0-255).
* L'image obtenue est passée en niveaux de gris via `cv2.cvtColor(..., cv2.COLOR_BGR2GRAY)`. L'histogramme associé est calculé et affiché de la même manière.

> **[Insérez ici une capture d'écran des modifications de brillance/contraste avec son histogramme en gris]**

### E. Fonctionnalités Optionnelles & Créatives (Onglet 4)
Pour ajouter une touche de créativité à ce TP, nous avons développé un 4ème onglet avec plusieurs filtres avancés :
1. **Neon Effect (Canny)** : Détection de contours avec `cv2.Canny` appliquée sur un fond synthétique bleu/violet.
2. **Flou Artistique (Gaussien)** : Utilisation de `cv2.GaussianBlur` pour réduire le bruit et créer une profondeur de champ artificielle.
3. **Négatif** : Inversion des couleurs avec `cv2.bitwise_not()`.
4. **Sépia** : Transformation mathématique des matrices RVB pour un rendu photographique rétro.

> **[Insérez ici des captures d'écran démontrant un ou plusieurs effets du labo créatif]**

---

## 4. Lien vers le Dépôt GitHub

*(Si vous avez publié le code sur GitHub, mettez le lien ici)*
**Repository GitHub :** [Lien vers votre projet GitHub]

## 5. Conclusion
Ce travail pratique a permis d'assimiler concrètement la représentation matricielle spatiale et spectrale d'une image numérique. Le couplage de Python, OpenCV, et des éléments graphiques Qt a permis de structurer une application stable, interactive, et visuellement complète.
