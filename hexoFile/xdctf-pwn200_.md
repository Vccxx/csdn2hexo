---
title: xdctf-pwn200 
date: 2017-04-08 18:09:04
tags:
- 栈
- pwn
- ctf
---
XDCTF (哪一年的忘了)中的一道pwn题题目地址http://pan.baidu.com/s/1hszHtwo解题思路：缓冲区溢出->泄露ebp->覆盖got表->执行shellcode首先用ida分析这题的反汇编：这里是一个关键的缓冲区溢出点，这里虽然v2的长度和读入的最大长度一致，但是我们知道对于printf函数，如果后面的地址中（这里是v2的栈地址）的内容没有”/x00”这样的结束符，就会
<!-- more -->