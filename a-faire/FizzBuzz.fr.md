---
title: "FizzBuzz"
draft: false
date: "2018-01-28"
---

## A propos

Difficulté : Simple  
Intérêt : Apprentissage [TDD](/TestDrivenDevelopment) et [BabySteps](/BabySteps).

## Règles

## Description du problème

Imaginez la scène. Vous avez onze ans et cinq minutes avant la fin de la leçon de mathématique, votre professeur décide soudain de rendre son cours plus "fun" en vous faisant jouer à ce qu'il qualifie de "jeu". Il vous explique qu'il va intérroger chacun d'entre-vous l'un après l'autre et lui demander de dire le prochain nombre de la séquence en commençant par 1. La partie "fun" est que si le nombre est un multiple de 3 alors vous devrez dire "Fizz", et s'il est un multiple de 5, vous devrez dire "Buzz".  
Votre professeur commence à vous interroger les uns à la suite des autres. Vos camarades entonnent joyeusement "un!", "deux!", "Fizz!", "quatre!", "Buzz!"... Jusqu'à ce qu'il décide de son plein gré de vous pointer, vous. En vous fixant de son regard d'acier... Le temps retient son souffle, votre bouche s'assèche et vos mains sont de plus en plus moites. Vous finissez tant bien que mal par articuler "Fizz!".  
Vous échappez de peu à une mort tragique, et l'implacable main du maître vient pointer un autre élève.

Biensûr, pour éviter d'avoir honte devant toute votre classe, vous devez vous procurer la séquence complète pour savoir quoi dire. Vous êtes dans une classe de 33 élèves, et le professeur à le temps d'interroger chaque élève trois fois avant que la sonnerie ne retentisse. La prochaine leçon est Vendredi. Vous n'avez pas de temps à perdre.

Vous devez écrire un programme affichant les nombres de 1 à 100.

## Étape 1

Vous devez construire une fonction `fizzBuzz` qui retourne un nombre ou une chaîne de caractère selon les règles suivantes :
  - Si le nombre est divisible par 3, on le remplace par "Fizz" ;
  - Si le nombre est divisible par 5, on le remplace par "Buzz" ;
  - Si le nombre est divisible par 3 et 5, alors on le remplace par "FizzBuzz" ;
  - Par défaut, retourner le nombre.

### Exemples

    1 => 1
    2 => 2
    3 => Fizz
    4 => 4
    5 => Buzz
    6 => Fizz
    15 => FizzBuzz

## Étape 2

Vous aurez la peau de ce professeur :
  - La fonction retourne "Fizz" si le nombre est un multiple de 3 ou s'il contient un 3 ;
  - La fonction retourne "Buzz" si le nombre est un multiple de 5 ou s'il contient un 5.

### Exemples

    1 => 1
    2 => 2
    3 => Fizz
    4 => 4
    5 => Buzz
    6 => Fizz
    10 => Buzz
    11 => 11
    12 => Fizz
    13 => Fizz
    15 => FizzBuzz
    51 => Fizz
    52 => Buzz

## Étape 3

Construire une fonction `compute` qui affiche la suite de correspondance de 1 à 100.

