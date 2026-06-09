---
title: Movie Rental
draft: false
date: "2020-06-16"
tags:
  - refactoring
---

The Martin Fowler's book "Refactoring, Improving the Design of Existing Code" start with a (very) simple example of refactoring of code.

Actualy the `statement` method prints out a simple text output of a rental statement
```
Rental Record for martin
  Ran 3.5
  Trois Couleurs: Bleu 2
Amount owed is 5.5
You earned 2 frequent renter points
```

We want to write an HTML version of the statement method :
```
<h1>Rental Record for <em>martin</em></h1>
<table>
  <tr><td>Ran</td><td>3.5</td></tr>
  <tr><td>Trois Couleurs: Bleu</td><td>2</td></tr>
</table>
<p>Amount owed is <em>5.5</em></p>
<p>You earned <em>2</em> frequent renter points</p>
```

First refactor the program to make it easy to add the feature, then add the feature.

The original code was in java. You will find implementations in different languages (java, python, typescript, php, etc.) at this address: https://gitlab.com/azae/craft/movie-rental

## Links

* [French live coding](https://video.ploud.fr/videos/watch/4b8bad98-cf4f-40a5-976c-d7b825f79d30)
* [Sources starting point for different languages](https://gitlab.com/azae/craft/movie-rental)
