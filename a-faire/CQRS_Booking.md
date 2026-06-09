---
title: "CQRS Booking"
draft: false
date: "2020-05-19T13:23:00"
---

You should implement a simple booking solution in CQRS architecture.

## About CQRS

CQRS for Command Query Responsibility Segregation Pattern.

A query returns data and does not alter the state of the object. 
A command changes the state of an object but does not return any data.

We will split our code in read and write code to really live this pattern.

## Booking subject

We want to make a booking solution for one hotel. 

The first 2 user stories are :

* As a user I want to see all free rooms.
* As a user I want to book a room.

They want to use the CQRS pattern. To do that we will have : 

* One Command Service with a function `bookARoom(Booking)`
    * that calls the `WriteRegistry`
    * that notifies the `ReadRegistry` called by the Query Service
* One Query Service with function `Room[] freeRooms(arrival: Date, departure: Date)`

The Booking struct contains

* client id
* room name
* arrival date
* departure date

And the Room struct contain only

* room name

## Source

*  inspiration source of this kata : https://github.com/tpierrain/CQRS/
*  explanation of CQRS by Microsoft https://docs.microsoft.com/en-us/previous-versions/msp-n-p/jj591573(v=pandp.10)
