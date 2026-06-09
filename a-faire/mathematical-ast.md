---
title: "Mathematical AST"
draft: false
date: "2021-12-17"
---

## Origin

This kata was originaly write to implement the visitor pattern

## Kata

### Step 1

Write a program they build and Abstract Syntax Tree of a RPN mathematical expression from a string like: 

                                               (+)
    Mathematical.parse("3 6 +") be produce     / \
                                              /   \
                                             3     6

and

                                                       (+)
                                                       / \
                                                      /   \
                                                     3    (×)
    Mathematical.parse("3 6 -6 * +") be produce           / \
                                                         /   \
                                                        6    -6


For the first test You must chose objects or structs you will have in your AST.

Possible solutions are : 

    new Addition(new Operand(3), new Operand(6))

    new Operation(new Add(), new Operand(3), new Operand(6))

    new Addition().setLeft(new Operand(3))
    new Addition().setRight(new Operand(6))

    ...

### Step 2

Make a method or function they build the RPN representation of AST

For exemple, 

      (+)
      / \
     /   \
    3    (×)    should be represented by 3 6 -6 × +
         / \
        /   \
       6    -6

Make a method or function they build the infix representation of AST

For exemple, 

      (+)
      / \                               
     /   \                               3 + 6 × -6
    3    (×)    could be represented by       or 
         / \                             3 + (6 × -6)
        /   \                           
       6    -6

Make a method or function they evaluate the AST

      (+)
      / \
     /   \
    3    (×)    = -33
         / \
        /   \
       6    -6

### Step 3

Build the infix representation with the minimum of parenthesis.

### Step 4

Implement operations:

* Exponent (^)
* Knuth's up-arrow (↑) 
