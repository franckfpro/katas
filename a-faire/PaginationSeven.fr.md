---
title: "Pagination Seven"
date: "2020-06-26"
---
## Description du problème

La pagination se retrouve dans de nombreux sites web sur internet. La plupart du temps, nous retrouvons la page courante ainsi que la navigation précédente et suivante. Parfois il est possible de retourner à la première ou la dernière page. Quelques informations peuvent compléter la pagination pour afficher le nombre total de pages.

Conscient de cet ensemble de besoins, nous avons trouvé un grand nombre d'exemples de paginations, les voici :

Pagination simple :

```
< 42 >
```

Pagination avancée :

```
<< < Page 42 sur 100 > >>
```

Cependant, la pagination avancée est assez verbeuse, nous avons donc décidé de représenter le numéro de la première page, la dernière, précédente et suivante sur une même fenêtre de sept entrées, c'est pourquoi nous avons décidé d'utiliser la représentation "Pagination Seven" :

```
1 … 41 (42) 43 … 100
```

## Partie I

Premièrement, nous avons besoin de représenter toutes les pages jusqu'à la page 7, le but est d'afficher la page courante entre `(` et `)`, par exemple :


Page 2 sur 5 :

```
1 (2) 3 4 5
```

Page 6 sur 7 :

```
1 2 3 4 5 (6) 7
```

## Partie II

Maintenant, nous aimerions afficher la première page, la dernière, précédente et suivante mais seulement sur 7 entrées même si le nombre de pages excède 7. Pour représenter les pages groupées, nous utiliserons `…`, voici quelques exemples :

Page 42 sur 100 :

```
1 … 41 (42) 43 … 100
```

Page 5 sur 9 :

```
1 … 4 (5) 6 … 9
```

## Partie III

Parfois, nous n'avons pas besoin d'utiliser `…` parce que nous sommes au début de la pagination, nous aurions donc :

Page 2 sur 9 :

```
1 (2) 3 4 5 … 9
```

Page 4 sur 9 :

```
1 2 3 (4) 5 … 9
```

## Partie IV


Comme vous l'avez peut-être constaté, cette règle peut s'appliquer à la fin de la pagination :

Page 8 sur 9 :

```
1 … 5 6 7 (8) 9
```

Page 6 sur 9 :

```
1 … 5 (6) 7 8 9
```

## Note de l'auteur

Je souhaitais proposer ce kata parce que, la plupart du temps dans le développement Front-End, nous avons besoin de représenter une pagination, et, avec mon expérience, j'ai pu en coder de nombreuses versions différentes. Cependant, avec la grande famille de paginations, en travaillant avec des designers, il nous arrivait d'utiliser la représentation "Pagination Seven".
