---
title: "ORM"
draft: false
date: "2022-01-19"
---

## Kata

### Same object in database and business

Write a contacts program they use an ORM to read and write Persons from an sqlite3 database

Person has 3 attributes :

* Name
* Surname
* Birth date

### Tests DB and production DB

we want to have one test DB named `tests.db` and one production db file set by environment variable `DB_URL`

In production Data base we have all this contacts :

* Elon Musk: June 28, 1971
* Kamala Harris: October 20, 1964
* Joe Biden: November 20, 1942
* Greta Thunberg: January 3, 2003
* Donald Trump: June 14, 1946
* Angela Merkel: July 17, 1954
* Barack Obama: August 4, 1961
* Mark Zuckerberg: May 14, 1984
* Jeff Bezos: January 12, 1964

### Version of schema

add a version schema in your code and database

### Migration

Add attribute email and manage the production migration database. The migration should be automatic in 2 ways :
* if code version schema is under the production database schema the program can revert the migration
* if code version schema is upper the production database schema the program apply the migrations

### One object for database and one for business

Add a business Person value object they has an address attribute with these rules:

* The address in Business Person object is only the last address of person
* In database we want to keep the addresses history, to do that we will build a new table with 3 attributes, the id of person, the creation date and the address

### Relation one 2 one

A person has an unique National Identifier, add the national unique number structure build like in France with :

* gender
* year of birth
* month of birth
* id of city
* rank
* check sum

### Relation one to many

A Person can know have many phone numbers, add a collections of phones numbers as attribute to Person and a new table Phones in database

### Relation many To many

A person has 2 parents and 0 or more children, manage that in your business and in your database.

### Inheritance

We have now 2 types of persons:
* Student with attributes university, academic degree
* Employee with attributes office, date hired and salary

Student and Employee extends Person.

Save all this information in your database.

### Production database

Use a postgres or mysql as Production database.

