---
title: "RSA Cheatsheet"
date: 2022-12-20T03:22:24-08:00
description: "I made a RSA cheatsheet so I don't have to search up about it every time."
tags: [cryptography]
---

I made a RSA cheatsheet so I don't have to search up about it every time.

## To generate a private key

```bash
openssl genrsa 2024 > secret.key
```

## To generate a public key

```bash
openssl rsa -pubout < secret.key > public.key
```

## To encrypt a plaintext

```bash
openssl pkeyutl -encrypt -pubin -inkey public.key -in plaintext -out ciphertext
```

## To decrypt a ciphertext

```bash
openssl pkeyutl -decrypt -inkey secret.key -in ciphertext -out plaintext
```

