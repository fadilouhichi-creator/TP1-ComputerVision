# Rapport de TP 1 : Introduction aux images numériques (Computer Vision)

**Date limite :** 27/02/2026
**Matière :** Computer Vision 1
**Étudiant :** FADI LOUHICHI
**Section :** S4

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

## 3. Démonstration des Fonctionnalités Réalisées

Afin de présenter au mieux l'ensemble des fonctionnalités développées (chargement des images au format correct BGR/RGB, séparation des canaux, création dynamique d'histogrammes couleurs et niveaux de gris, modification de la luminance, ainsi que les filtres de notre **Labo Créatif** exclusif), nous avons opté pour une démonstration vidéo interactive.

> 🎥 **[Cliquez ici pour visionner la vidéo de démonstration complète de l'application (Demo_TP1.mkv)](https://github.com/fadilouhichi-creator/TP1-ComputerVision/blob/master/Demo_TP1.mkv)**

---

## 4. Lien vers le Dépôt GitHub

**Repository GitHub :** https://github.com/fadilouhichi-creator/TP1-ComputerVision

## 5. Conclusion
Ce travail pratique a permis d'assimiler concrètement la représentation matricielle spatiale et spectrale d'une image numérique. Le couplage de Python, OpenCV, et des éléments graphiques Qt a permis de structurer une application stable, interactive, et visuellement complète.
