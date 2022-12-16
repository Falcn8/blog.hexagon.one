---
title: "NO_PUBKEY when running sudo apt-get update"
date: 2022-12-16T16:21:26+09:00
description: "I've tried a lot of solutions on the internet, but none of them worked for me. So I'm writing this post to help others who are having the same problem."
tags: [ubuntu, linux]
---

I've tried a lot of solutions on the internet, but none of them worked for me. So I'm writing this post to help others who are having the same problem. *Btw, this is my first post!*

## What did I do?

I wanted to update my Ubuntu 18.04 droplet on DigitalOcean, so I ran `sudo apt-get update` and the result I got was:

```shell
root@ubuntu:~# sudo apt-get update
Hit:1 https://repos.insights.digitalocean.com/apt/do-agent main InRelease
Get:2 http://mirrors.digitalocean.com/ubuntu bionic InRelease [242 kB]
Get:3 https://cli.github.com/packages stable InRelease [3917 B]
Hit:4 https://deb.nodesource.com/node_12.x bionic InRelease
Get:5 http://mirrors.digitalocean.com/ubuntu bionic-updates InRelease [88.7 kB]
Get:6 http://mirrors.digitalocean.com/ubuntu bionic-backports InRelease [83.3 kB]
Err:3 https://cli.github.com/packages stable InRelease
The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 23F3D4EA75716059
Get:7 https://repos-droplet.digitalocean.com/apt/droplet-agent main InRelease [5518 B]
Hit:8 http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease
Get:9 http://security.ubuntu.com/ubuntu bionic-security InRelease [88.7 kB]
Hit:10 http://ppa.launchpad.net/linuxuprising/java/ubuntu bionic InRelease
Err:7 https://repos-droplet.digitalocean.com/apt/droplet-agent main InRelease
The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 35696F43FC7DB4C2
Get:11 http://security.ubuntu.com/ubuntu bionic-security/universe amd64 Packages [1250 kB]
Get:12 http://security.ubuntu.com/ubuntu bionic-security/universe Translation-en [289 kB]
Fetched 2048 kB in 2s (1122 kB/s)
Reading package lists... Done
W: An error occurred during the signature verification. The repository is not updated and the previous index files will be used. GPG error: https://cli.github.com/packages stable InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 23F3D4EA75716059
W: An error occurred during the signature verification. The repository is not updated and the previous index files will be used. GPG error: https://repos-droplet.digitalocean.com/apt/droplet-agent main InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 35696F43FC7DB4C2
W: Failed to fetch https://repos-droplet.digitalocean.com/apt/droplet-agent/dists/main/InRelease The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 35696F43FC7DB4C2
W: Failed to fetch https://cli.github.com/packages/dists/stable/InRelease The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 23F3D4EA75716059
W: Some index files failed to download. They have been ignored, or old ones used instead.
```

## What's the problem?

In the above output, I got `NO_PUBKEY 23F3D4EA75716059` and `NO_PUBKEY 35696F43FC7DB4C2` error. I searched for this error on the internet and found a lot of solutions, but none of them fixed this problem.

## ⭐ The solution

I found the solution on this [StackExchange post](https://superuser.com/questions/1744040/the-following-signatures-couldnt-be-verified-because-the-public-key-is-not-ava/1744043#1744043). The solution is to run the following commands:

```shell
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh -y
```

This will fix the `NO_PUBKEY 23F3D4EA75716059` error, but I still saw the `NO_PUBKEY 35696F43FC7DB4C2` error.

To fix this error, I needed to run the following command:

```shell
wget -qO- https://repos-droplet.digitalocean.com/install.sh | sudo bash
```

and this should fix the `NO_PUBKEY 35696F43FC7DB4C2` error.

## Result

Now you can run `sudo apt-get update` and it should work like this:

```shell
root@ubuntu:~# sudo apt-get update
Hit:1 https://cli.github.com/packages stable InRelease
Hit:2 https://repos.insights.digitalocean.com/apt/do-agent main InRelease
Get:3 http://mirrors.digitalocean.com/ubuntu bionic InRelease [242 kB]
Hit:4 https://deb.nodesource.com/node_12.x bionic InRelease
Hit:5 https://repos-droplet.digitalocean.com/apt/droplet-agent main InRelease
Hit:6 http://mirrors.digitalocean.com/ubuntu bionic-updates InRelease
Hit:7 http://mirrors.digitalocean.com/ubuntu bionic-backports InRelease
Hit:8 http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease
Hit:9 http://security.ubuntu.com/ubuntu bionic-security InRelease
Hit:10 http://ppa.launchpad.net/linuxuprising/java/ubuntu bionic InRelease
Fetched 242 kB in 1s (293 kB/s)
Reading package lists... Done
```
