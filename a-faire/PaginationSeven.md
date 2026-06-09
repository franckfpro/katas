---
title: "Pagination Seven"
date: "2020-06-26"
---
## Problem description

Pagination can be found in many websites on the Internet. Most of the time you can see the current page and going to the previous and the next page. Sometimes you can go to the first and the last page. Some information like total pages number can be shown.

Aware of the need for all these contraints, we found a lot of pagination example like:

Simple pagination:

```
< 42 >
```

Advanced pagination:

```
<< < Page 42 of 100 > >>
```

But the advanced pagination is really verbose, so we had an idea to represent first, last, next, previous and current page as the same time with less complexity, and we decided to use a "Pagination Seven" representation:

```
1 … 41 (42) 43 … 100
```

## Part I

First of all, we need to represent all pages until 7, the goal is to show the current page between `(` and `)`, as examples:


Page 2 of 5:

```
1 (2) 3 4 5
```

Page 6 of 7:

```
1 2 3 4 5 (6) 7
```

## Part II

Now we need to see first, last, previous and next page, but only using 7 slots when total pages number is above 7. So we need to replace group of pages with `…`, here are some examples:

Page 42 of 100 :

```
1 … 41 (42) 43 … 100
```

Page 5 of 9:

```
1 … 4 (5) 6 … 9
```

## Part III

Sometimes we don't need to show `…` because we are in the first part of the pagination, so we will have:

Page 2 of 9:

```
1 (2) 3 4 5 … 9
```

Page 4 of 9:

```
1 2 3 (4) 5 … 9
```

## Part IV

As you may notice, there is the same idea but for the last part of the pagination:

Page 8 of 9:

```
1 … 5 6 7 (8) 9
```

Page 6 of 9:

```
1 … 5 (6) 7 8 9
```

## Author's note

I wanted to propose this kata because most of the time in Front-End applications, we need to represent a pagination, and from my experience, I made a lot of them. So, from the large family of pagination, by working with designers, sometimes we decided to use "Pagination Seven" representation.
