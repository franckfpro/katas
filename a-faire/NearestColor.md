---
title: "Nearest color"
date: "2022-08-19"
---
## Introduction

A color is composed by an amount of _red_, _green_ and _blue_.

In computer science, a way to represent a color is to compose between these three amount of colors.

Each amount of color have a presence from `0` (the color is absent) to `255` (full presence of color).

But, because some developers love hexadecimal, they decided to use numbers between `0` and `F`. So, `00` means `0` in decimal and `FF` means `255` in decimal.

For color composition, the first pair of digits are used for the red, the second pair for the green and last pair for the blue.

The hexadecimal representation of the colors looks like:

* `FF0000` for __red__
* `00FF00` for __green__
* `0000FF` for __blue__

But, for the exercice we decided to represent colors with only 3 digits, so the alias will be:

* `F00` for `FF0000`
* `0F0` for `00FF00`
* `00F` for `0000FF`

## Part 1: nearest color

The idea is to use a set of colors (`F00`, `0F0`, `00F`) and guess the nearest color from the set.

Example: the nearest color of `F42` is `F00`.

## Part 2: equality

The idea is to list all the colors in equality cases, because, sometimes, more than one color is the nearest color.

Example: because yellow `FF0` is composed by red `F00` and green `0F0`, the nearest colors are both of them.

## Bonus

- Do the same with 6 digit hexadecimal colors
- Find the farthest color
- Compare with [color keywords](https://www.w3.org/TR/css-color-3/#html4)
