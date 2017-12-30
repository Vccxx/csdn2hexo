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
## 通过两个rsa算法的实现代码初步认识RSA算法
### 程序bmrsa
### 程序rsa，源码：
源码分析：

RSA.cpp中的testRSA()函数流程图如下：

将结果中的n放到cap4中进行大素数分解：

#### a).format method只用了2秒就正确分解了这个大素数
#### b)pollard’s rho Test Progress 方法只用了1s
#### 3)pollard p-1 Progress 用了6秒
#### 4)最慢的continuous fractions progress也只用了1分26秒
可以看到，对于10位的公钥n，用密码分析算法可以很快的分解出质因数，所以p和q应该大一些，RSA建议p,q都在100位10进制数以上。
~~~
答：RSA算法通过产生两个大素数p,q，用他们计算出f = (p-1)*(q-1)作为私钥，产生一个大随机数e，若e和f互素，则用e作为公钥；接下来计算p*q和e在mod f下的乘法逆元d。
公布{e,n}作为公钥，保留{p,q,f,d}作为私钥。
公钥加密时私钥解密，私钥加密时公钥解密，原理是欧拉定理的推论：M^(kf + 1)mod n = M mod n。

C是密文，M是明文，则
加密：M^e mod n = C
d=e^(-1) mod f  => de = kf + 1
解密：C^d mod n = (M^e)^d mod n = M^(ed)mod n = M^(kf +1)mod n = M mod n
从而计算出明文M。
~~~

2.在上述算法中哪些模块是该算法的核心模块？
~~~
1)  产生大素数p，q的模块RandomPrime(16)
2)  判断是否素数的RM检测
3)  SteinGcd用于判断e，f是否互素，Eculid用于产生逆元d
4)  大数模乘和模幂函数MulMod，PowMod，这两个函数的处理数据的能力（防止乘法溢出的能力），直接决定了产生的密钥的安全性。
~~~

3.对于一个RSA加密算法的密文，要得到明文需要哪些要素？
~~~
要解密密文，最简单的方法是有私钥d，直接解密

或者通过分解大素数n得到p，q，从而计算f，用f和e算出d，再解密
~~~
