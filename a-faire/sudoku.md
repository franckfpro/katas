---
title: "Sudoku the concurrent resolver"
draft: false
date: "2022-04-26"
---

Inspired from [Thien Que Nguyen and Pascal Van Cauwenberghe](https://www.agilecoach.net/wp-content/uploads/2014/11/CSP-Presentation.pdf)

This kata whan to experience TDD and concurrent programming.

* Understand concurrent systems problems and solutions.
* Learn how you can apply Test Driven Design to concurrent code.
* Experience how a parallel computer works and is programmed.
* Discover how simple rules and collaboration can solve complicated problems

## Cell Specification

Build a Cell class or struct they follow this rules : 

* A Cell expresses which of the numbers 1..9 are possible
* By default every number is possible
* If there is more than one possible number, the value of the cell is unknown
* If exactly one number is possible, the value of the cell is known == number
* If there are no possible numbers there is a contradiction, this is impossible

A Cell can answer 1 question : 

* What is the value of the cell? unknown, number or impossible
* Is X is a possible value ?

And record one information :

* Number X it's not a possible value.

## Grid Specification

* A Grid has a name: A, B, C, D, E, F, G, H or I
* A Grid consists of 3x3 Cells
* Cells are addressed as (Row, Column), it's the grid column and row numbers.

Grid can record one information :

* **If** a Cell within a Grid has a known value **Then** no other Cell can have the same value

## Region Specification

* A Region contains a Grid
* A Region has 4 inputs: North, East, South, West
* A Region has 4 outputs: North, East, South, West
* A Region has an output Display

All regions are organized as follow :

| | | |
|-|-|-|
| A | B | C |
| D | E | F |
| G | H | I |

The North output of one region if connected with the South input of the corresponding region.

At west of last column it's the first column and at south of last line it's the first one.

For exemple

```
                         ^            |
                         |            |
                         |            |
                   /output/north  /input/north  
                         |            |
                         |            |
                         |            v
                    +----------------------+
                    |                      |
--- /input/west --->|                      |---- /output/east -->
                    |     Region grid C    |
<-- /output/west ---|                      |<--- /input/east ----
                    |                      |
                    +----------------------+
                         ^            |
                         |            |
                         |            |
                   /input/south  /output/south  
                         |            |
                         |            |
                         |            v

                         ^            |
                         |            |
                         |            |
                   /output/north  /input/north  
                         |            |
                         |            |
                         |            v
                    +----------------------+
                    |                      |
--- /input/west --->|                      |---- /output/east -->
                    |     Region grid F    |
<-- /output/west ---|                      |<--- /input/east ----
                    |                      |
                    +----------------------+
                         ^            |
                         |            |
                         |            |
                   /input/south  /output/south  
                         |            |
                         |            |
                         |            v

```

A region is a REST server with 2 routes:

POST `/input/[direction]` with direction in ("north", "east", "south", "west") and payload :

```json
{
    row:             // immutable
    column:          // immutable
    value:           // immutable
    uuid:            // immutable
    nb-of-msg:       // modified by last region
    path:            // modified by last region
}
```
- `nb-of-msg` corresponding to the number of received messages by region from start of compute.
- `path` corresponding to the list of regions that treated the message

POST `/init/` and payload :

```json
{
    row:
    column:
    value:
}
```

When a grid discover a value of a cell
* Send a message (payload)
* To the Display
* And to all output channels

When a grid receive a message from North or South
* The Grid can’t have Value in that column
* Send the message on the other side

When a grid receive a message from the East or West
* The Grid can’t have Value in that row
* And Send the message on to the other side

Exemple:

* Region-C receive the message on /input/south `{path: ["F"], row: 1, column: 1, value: 7, uuid: "UUID", nb-of-msg: 0}`
* notify all cells in the column 1 the Value 7 is not possible
* Send the message to Region-I on /input/south `{path: ["C"], row: 1, column: 1, value: 7, uuid: UUID, nb-of-msg: 9}`


Display server is a REST server with 1 route:

POST `/show` with payload :

```json
{
    row:             // immutable
    column:          // immutable
    value:           // immutable
    uuid:            // immutable
    nb-of-msg:       // modified by last region
    path:            // modified by last region
}
```

