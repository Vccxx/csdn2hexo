---
title: HITCTF PWN300--dynelf 
date: 2017-04-08 18:26:11
tags:
- CTF
- PWN
- PWNTOOLS
---
第一次用Dynelf，脚本调了一下午。。hitctf pwn300题目链接：http://pan.baidu.com/s/1eSCCOE2漏洞分析：三个write之前的一个函数调用了read来读入字符，而这里存在明显的缓冲区溢出，可以覆盖main函数的栈地址，这个题没给libc，got表里没有system之类的函数，于是考虑用dynelf。攻击脚本：from pwn import *
io = pr
<!-- more -->