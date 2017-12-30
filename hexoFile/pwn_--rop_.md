---
title: pwn --rop 
date: 2017-04-08 23:51:37
tags:
- pwn
- ctf
- rop
---
rop练习—Very Secure Systemrop 真爽。。题目链接：http://pan.baidu.com/s/1eSd0XTg 
注：.bak是原题，原题有个过10s自动退出程序的设置，不好调试，我用ida打了个patch，就是另一个文件，两个文件只有这一个区别漏洞分析：这个程序是静态加载的，所以got表没有用，顺带dynelf也不行，也没提供libc。但是有一个函数可以溢出，但是只溢出了
<!-- more -->