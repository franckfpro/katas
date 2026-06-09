---
title: "FizzBuzz"
draft: false
date: "2010-03-27T06:07:00"
aliases:
  - "/FizzBuzz"

---

This is the list of solutions to the [KataFizzBuzz](/kata/FizzBuzz).

# Java

This is a solution with the twist of supplying the filtering from the outside
of the [ClassUnderTest](/ClassUnderTest) .

``` Java
FizzBuzzTest.java:

import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;



public class FizzBuzzTest {

    private static final Object[] ARRAY_OF_2_FIZZ = {2, "Fizz"};
    private static final Object[] ARRAY_OF_1_2 = {1, 2};
    private static final Object[] ARRAY_OF_FIZZ_7_8_FIZZ = {"Fizz",
                                                            7, 8,
                                                            "Fizz"};
    private static final Object[] ARRAY_OF_BUZZ = {"Buzz"};
    private static final Object[] ARRAY_OF_FIZZBUZZ = {"FizzBuzz"};
    private static final Object[] ARRAY_OF_FIZZBUZZ_TO_FIZZ = { "FizzBuzz",
                                                                16, 17,
                                                                "Fizz",
                                                                19,
                                                                "Buzz", "Fizz",
                                                                22, 23,
                                                                "Fizz", "Buzz",
                                                                26,
                                                                "Fizz",
                                                                28, 29,
                                                                "FizzBuzz"};

    FizzBuzz fizzBuzz = new FizzBuzz();

    @Before
    public void addFilters() {
        fizzBuzz.addFilter(new FizzBuzzFilter() {
            public String filter(int integer) {
                return integer % 3 == 0? "Fizz" : "";
            }
        });
        fizzBuzz.addFilter(new FizzBuzzFilter() {
            public String filter(int integer) {
                return integer % 5 == 0? "Buzz" : "";
            }
        });
    }
    
    @Test
    public void shouldReturn1And2AsIs() throws Exception {
        assertArrayEquals(ARRAY_OF_1_2, fizzBuzz.filter(range(1, 2)));
    }
    

    @Test
    public void shouldConvertThreeToFizz() throws Exception {
        assertArrayEquals(ARRAY_OF_2_FIZZ, fizzBuzz.filter(range(2, 3)));
    }

    @Test
    public void shouldConvert6And9ToFizz() throws Exception {
        assertArrayEquals(ARRAY_OF_FIZZ_7_8_FIZZ,
                          fizzBuzz.filter(range(6, 9)));
    }
    
    @Test
    public void shouldConvert5ToBuzz() throws Exception {
        assertArrayEquals(ARRAY_OF_BUZZ, fizzBuzz.filter(range(5, 5)));
    }
    
    @Test
    public void shouldConvert15ToFizzBuzz() throws Exception {
        assertArrayEquals(ARRAY_OF_FIZZBUZZ,
                          fizzBuzz.filter(range(15, 15)));
    }
    
    @Test
    public void shouldConvert15To30Correctly() throws Exception {
        assertArrayEquals(ARRAY_OF_FIZZBUZZ_TO_FIZZ,
                          fizzBuzz.filter(range(15, 30)));
    }

    private int[] range(int start, int end) {
        int[] range = new int[end-start+1];
        for (int count = 0; count < range.length; count++)
          range[count] = start+count;
        return range;
    }
}
FizzBuzz.java:

import java.util.ArrayList;


public class FizzBuzz {

    private ArrayList<FizzBuzzFilter> filters = new ArrayList<FizzBuzzFilter>();

    public Object[] filter(int[] integers) {
        Object[] result = new Object[integers.length];
        for (int i = 0; i < integers.length; i++) {
            result[i] = convert(integers[i]);
        }
        return result;
    }

    private Object convert(int integer) {
        String converted = applyFilters(integer);
        return "".equals(converted) ? integer : converted;
    }

    private String applyFilters(int integer) {
        String converted = "";
        for (FizzBuzzFilter filter : filters) {
            converted += filter.filter(integer);
        }
        return converted;
    }

    public void addFilter(FizzBuzzFilter fizzBuzzFilter) {
        filters.add(fizzBuzzFilter);
    }
}
```

# Smalltalk

``` Smalltalk
    fb := [:counter| |rules|
       rules := {15->'FizzBuzz'. 5->'Buzz'. 3->'Fizz'. 1->counter}.
       rightRule := rules detect: [:aRule| counter \\ aRule key == 0].
       rightRule value].  

self assert: (fb value: 7) == 7.
self assert: (fb value: 3) == 'Fizz'.
self assert: (fb value: 5) == 'Buzz'.
self assert: (fb value: 15) == 'FizzBuzz'.

1 to: 100 do: [:counter | 
               Transcript 
                 show: (fb value: counter) asString;
                 cr]
```

# C++

This solution was made on Linux with the unit test framework [Catch2](https://github.com/catchorg/Catch2/tree/v2.x) placed at the same level as our "main", and compiled with `g++`:  

``` bash
g++ -o tests main.cpp
```

``` C++
#define CATCH_CONFIG_MAIN
#include <string>

#include "catch.hpp"

std::string fizzBuzz(int number) {
  std::string result = std::to_string(number);
  if (number > 0) {
    if (number % 3 == 0 && number % 5 == 0) {
      result = std::string("FizzBuzz");
    } else if (number % 3 == 0) {
      result = std::string("Fizz");
    } else if (number % 5 == 0) {
      result = std::string("Buzz");
    }
  }
  return result;
}

TEST_CASE("fizzBuzz return a number", "[fizzBuzz]") {
  REQUIRE(fizzBuzz(0) == "0");
  REQUIRE(fizzBuzz(1) == "1");
  REQUIRE(fizzBuzz(2) == "2");
  REQUIRE(fizzBuzz(4) == "4");
}

TEST_CASE("fizzBuzz return \"Fizz\" when its parameter can be divided by 3",
          "[fizzBuzz]") {
  REQUIRE(fizzBuzz(3) == "Fizz");
  REQUIRE(fizzBuzz(6) == "Fizz");
  REQUIRE(fizzBuzz(9) == "Fizz");
  REQUIRE(fizzBuzz(12) == "Fizz");
}

TEST_CASE("fizzBuzz return \"Buzz\" when its parameter can be divided by 5",
          "[fizzBuzz]") {
  REQUIRE(fizzBuzz(5) == "Buzz");
  REQUIRE(fizzBuzz(10) == "Buzz");
  REQUIRE(fizzBuzz(20) == "Buzz");
}

TEST_CASE("fizzBuzz return \"FizzBuzz\" when its parameter"
          "can be divided by 3 and by 5",
          "[fizzBuzz]") {
  REQUIRE(fizzBuzz(15) == "FizzBuzz");
  REQUIRE(fizzBuzz(30) == "FizzBuzz");
  REQUIRE(fizzBuzz(45) == "FizzBuzz");
  REQUIRE(fizzBuzz(60) == "FizzBuzz");
  REQUIRE(fizzBuzz(75) == "FizzBuzz");
  REQUIRE(fizzBuzz(90) == "FizzBuzz");
}
```
