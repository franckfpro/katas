---
title: "RSA"
draft: false
date: "2021-12-17"
---

## Origin

RSA (Rivest–Shamir–Adleman) is a public-key cryptosystem that is widely used for secure data transmission. It is also one of the oldest.

## Kata

In this kata we will encrypt and decrypt a message with RSA algorythm.

### Build keys

* Find 2 primes numbers `p` and `q` such that `(2^24 + 1) < p × q < 2^32`
* Compute `N = p × q`
* Compute `n = (p − 1) × (q − 1)`
* Choose `c` a coprime number with `n` such that `1 < c < n`

`(N, c)` is the public key

* Determine `d` as `d ≡ c^−1 (mod n)` that is, `d` is the modular multiplicative inverse of `c modulo n` i.e. `c*d mod n == 1`. `d` can be computed efficiently by using the Extended Euclidean algorithm.

`(N, d)` is the private key

### Encrypt the message

Make a function they:

* take a message in input
* slice the message in peaces of exactly 3 bytes
* for each peaces as integer `a` compute `a^c mod N`, you will obtain a 4 bytes integer
* the concatenation of each of this numbers is the encrypted message

### Decrypt the message

Make a function they:

* take an encrypted message in input
* slice the message in peaces of exactly 4 bytes
* for each peaces as integer `a` compute `a^d mod N`, you will obtain a 3 bytes integer
* the concatenation of each of this numbers is the original message

### Transmit the message

For transmition using mail or other messaging tools, we must have a function they encode the encrypted message in a readable message.

Make a function they take an encrypted message in input and they output a string with only readable chars like base64 encode. Do the revert function.

### Sample 

* p = 51581, q = 60101
* N = 3100069681
* n = 3099958000
* c = 66797

Public key : (3100069681, 66797)

* d = 1336940133

Private key : (3100069681, 1336940133)

* Message = "Hello world!": `0x48 0x65 0x6c 0x6c 0x6f 0x20 0x77 0x6f 0x72 0x6c 0x64 0x21`
* Sliced hexadecimal: `0x48656c 0x6c6f20 0x776f72 0x6c6421`
* Sliced decimal: `4744556 7106336 7827314 7103521`
* Encoded message decimal: `352431401 2267192425 538638606 1131048795`
* Encoded message hexadecimal: `0x1501AD29 0x87229C69 0x201AF90E 0x436A6F5B`
* Encoded message in base64: `FQGtKYcinGkgGvkOQ2pvWw==`

