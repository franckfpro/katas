---
title: "Eight Queens"
draft: false
date: "2021-12-16"
---

## Kata

This kata is based on the classic chess rules. You must put eight chess queens on an 8×8 chessboard such that none of them is able to capture any other using the standard chess queen's moves.

Tips: you could have only one queen by row and column.

### Step 1

Use multiple TDD loops to build a programm they find all solutions.


### Tree traversal

* Rewrite a new programm to use a Depth-first walk.
* Rewrite a new programm to use a Breadth-first walk.
* Compare performances and lisibility

### Nontraditional approaches

In this part we whant to find only one solution.

* Use a genetic algorithms to solve this puzzle.
* Use a minimum-conflicts heuristic to solve this puzzle.
* Use other metaheuristic algorithms like Simulated annealing or random to solve this puzzle.
* Compare performances

### Brute-force

* Build a programm they use brute-force and compare performances

## ⚠️  Spoiler: the next part is a technical solution ⚠️

### Brute-force

#### Vertical and horizontal rules

Given a chessboard, you can code each line of board by one byte of 8 bits, with 0 for empty cell and 1 for a queen.

```
+---+---+---+---+---+---+---+---+
| ♛ |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
```
Could be encoded by 10000000 i.e 128. To know if 2 row contains 2 quens, it's possible to use the OR operator. For a 8×8 chessboard, you must have only 1 in the result i.e. 255.


Sample with a 4×4 board
```
+---+---+---+---+
|   | ♛ |   |   |
+---+---+---+---+
|   |   |   | ♛ |
+---+---+---+---+
| ♛ |   |   |   |
+---+---+---+---+
|   |   | ♛ |   |
+---+---+---+---+
```
0100 OR 0001 OR 1000 OR 0010 = 1111

#### Diagonals rules

Diagonals could be check with 16bits with one shift by line :

```
+---+---+---+---+                    +---+---+---+---++---+---+---+---+
|   |   |   | ♛ | Line 0 => no shift |   |   |   |   ||   |   |   | ♛ |
+---+---+---+---+                    +---+---+---+---++---+---+---+---+
|   | ♛ |   |   | Line 1 => 1 shift  |   |   |   |   || ♛ < . |   |   |
+---+---+---+---+                    +---+---+---+---++---+---+---+---+
|   |   | ♛ |   | Line 2 => 2 shifts |   |   |   |   || ♛ <   < . |   |
+---+---+---+---+                    +---+---+---+---++---+---+---+---+
| ♛ |   |   |   | Line 3 => 3 shifts |   | ♛ <   <   << . |   |   |   |
+---+---+---+---+                    +---+---+---+---++---+---+---+---+
```
Could be test with :

00000001 OR 00001000 OR 00001000 OR 01000000 = 01001001

* Implement a programm they use this optimized check solution to find all solutions by brute-force.
* Compare performance with others implementations

