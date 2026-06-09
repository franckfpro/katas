---
title: "Manhattan Distance"
draft: false
date: "2021-12-10"
---

[Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry) is the distance between two points in a grid (like the grid-like street geography of the New York borough of Manhattan) calculated by only taking a vertical and/or horizontal path.

Write a function `int manhattanDistance(Point, Point)` that returns the Manhattan Distance between the two points.

## Potential constraints

* The class Point is immutable
* The class Point has no Getters, no Setters
* The class Point has no public properties (i.e. the internal state cannot be read from outside the class).

## Suggested tests

* `manhattanDistance( Point(1, 1), Point(1, 1) )` should returns `0`
* `manhattanDistance( Point(5, 4), Point(3, 2) )` should returns `4`
* `manhattanDistance( Point(1, 1), Point(0, 3) )` should returns `3`

