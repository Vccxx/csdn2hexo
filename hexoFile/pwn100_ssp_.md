---
title: pwn100 ssp 
date: 2017-04-08 19:34:10
tags:
- ssp
- pwn
- ctf
---
ssp–利用栈溢出保护来泄露内存这payload贼短。。题目链接：sspStack-smashing Protection (SSP，又名 ProPolice），是在函数的栈底插入一个随机数，这个随机数在函数调用结束后会被检测，如果与预设的不同，就会直接退出程序并打印如下的错误提示:    *** stack smashing detected ***: ./pwn100 terminated
<!-- more -->