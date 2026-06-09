---
title: "FizzBuzz Java"
draft: false
date: "2022-01-05"
---

/*
 * @ProjectName:mianshi
 * @Package:PACKAGE_NAME
 * @ClassName:MianShi
 * @Author:Rain
 * @Date:2022-01-05 10:17
 * @Description:
 */
public class MianShi {
    public static void main(String[] args) {

        m1();
        System.out.println("********************");
        m2();

    }

    public static void m1() {
        for (int i = 1; i <= 100; i++) {
            if (i % 3 == 0 && i % 5 == 0) {
                System.out.println("FizzBuzz");
            } else if (i % 3 == 0) {
                System.out.println("Fizz");
            } else if (i % 5 == 0) {
                System.out.println("Buzz");
            } else {
                System.out.println(i);
            }
        }
    }

    public static void m2() {
        for (int i = 1; i <= 100; i++) {
            if (i % 3 == 0 && i % 5 == 0) {
                System.out.println("FizzBuzz");
            } else if (i % 3 == 0 && String.valueOf(i).contains("3")) {
                System.out.println("fizz");
            } else if (i % 5 == 0 && String.valueOf(i).contains("5")) {
                System.out.println("buzz");
            } else {
                System.out.println(i);
            }
        }
    }
}



