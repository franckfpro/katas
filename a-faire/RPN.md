---
title: "RPN Calculator"
date: 2018-03-19
---

An RPN calculator computes expressions written in Reverse Polish Notation.

An RPN expression or postfix expression is one of the following :

* a number `X`, in wich case the value of the expression is that of X,
* a sequence of form `E1 E2 OP` where `E1` and `E2` are RPN expressions and `OP` is an arithmetic operation.

Samples :

    20 5 /        => 20/5 = 4
    4 2 + 3 -     => (4+2)-3 = 3
    3 5 8 * 7 + * => ((5*8)+7)*3 = 141

Add the SQRT operation :

    9 SQRT => √9 = 3

Add the MAX operation :

    5 3 4 2 9 1 MAX => MAX(5, 3, 4, 2, 9, 1) = 9
    4 5 MAX 1 +     => MAX(4, 5) + 1 = 6

It's important to have the discussion about absorbing property of MAX operator. With Reverse Polish Notation we must have a fixed number of operands by operator to avoid parentesis. For example : `4 5 MAX 1 2 MAX *` could be replace in first step by `5 1 2 MAX *` and in second step by `5 *` but it's not a valid expression. With a fixed number of operands by operator for example 2, `4 5 MAX 1 2 MAX *` is a valid expression but `5 3 4 2 9 1 MAX` not.

