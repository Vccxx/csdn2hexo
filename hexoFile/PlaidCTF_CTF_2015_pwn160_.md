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