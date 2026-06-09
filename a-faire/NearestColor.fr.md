---
title: "Nearest color"
date: "2022-08-19"
---
## Introduction

Une couleur est composée d'une quantité de _rouge_, _vert_ et _bleu_.

En informatique, une façon de représenter une couleur est de composer ces trois quantités de couleurs.

Chaque quantité de couleur a une présence entre `O` (la couleur est absente) et `255` (la couleur est totalement présente).

Mais, parce que certains développeurs aiment l'hexadécimal, ils ont décidé d'utiliser des nombres compris entre `0` et `F`. Ainsi `00` désigne `0` en décimal et `FF`  désigne `255` en décimal.

Pour la composition d'une couleur, la première paire de caractères est utilisée pour le rouge, la deuxième paire pour le vert et la dernière paire pour le bleu.

La représentation hexadécimale des couleurs donne donc :

* `FF0000` pour __red__
* `00FF00` pour __green__
* `0000FF` pour __blue__

Cependant, pour l'exercice, nous utiliserons seulement 3 caractères, on aura donc les alias suivants :

* `F00` pour `FF0000`
* `0F0` pour `00FF00`
* `00F` pour `0000FF`

## Partie 1 : la couleur la plus proche

L'idée est d'utiliser un ensemble de couleurs (`F00`, `0F0`, `00F`) et de deviner la couleur la plus proche parmi cet ensemble.

Exemple : la couleur la plus proche de `F42` est `F00`.

## Partie 2 : en cas d'égalité

L'idée est de lister toutes les couleurs en cas d'égalité, puisque, parfois, il arrive que plus d'une couleur soit la plus proche.

Exemple : parce que le jaune `FF0` est composé de rouge `F00` et de vert `0F0`, les couleurs les plus proches sont ces deux dernières.

## Bonus

- Faire de même avec une représentation colorimétrique hexadécimale à 6 caractères
- Trouver la couleur la plus éloignée
- Comparer avec les [color keywords](https://www.w3.org/TR/css-color-3/#html4)
