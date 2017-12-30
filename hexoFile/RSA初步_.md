---
title: RSA初步 
date: 2017-03-26 10:34:13
tags:
- rsa
- 算法
- 源码
- 注释
---
通过两个rsa算法的实现代码初步认识RSA算法程序bmrsa，源码：先看看第一个程序bmrsa.exe的流程图： 
 
 
 
Bmrsa的demo.bat运行截图及注释： 
1.产生第一个大素数p,用时3.1s 
 
2.产生第二个大素数q（用时5s），以及一个与f(n) = (p-1) * (q - 1)互素的e 
 
可以看到密文被公钥加密了： 
 
加密结果在encrypted.txt中可以
<!-- more -->