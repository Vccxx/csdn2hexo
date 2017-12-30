---
title: 汽车安全：Adventures in Automotive Networks and Control Units 
date: 2017-06-29 00:43:39
tags:
- 安全
- 多媒体
- 电子
---
汽车网络和控制单元的探索摘要之前的研究已经表明，攻击者可能通过蓝牙和通讯单元等接口，对在汽车中的电子控制单元（ECU）进行远程执行代码攻击。这篇论文旨在讨论这类攻击会给汽车行为带来多大程度的影响。特别地，我们展示了如何在一些特定的环境下，在两个不同的汽车系统中，控制刹车、加速、驾驶和多媒体。我们还提出了一种用于检测这种攻击的机制。在这篇论文中，我们公开了所有的技术细节一遍读者复现和理解，包括源代码和
<!-- more -->
# 汽车网络和控制单元的探索
## 摘要
之前的研究已经表明，攻击者可能通过蓝牙和通讯单元等接口，对在汽车中的电子控制单元（ECU）进行远程执行代码攻击。这篇论文旨在讨论这类攻击会给汽车行为带来多大程度的影响。特别地，我们展示了如何在一些特定的环境下，在两个不同的汽车系统中，控制刹车、加速、驾驶和多媒体。我们还提出了一种用于检测这种攻击的机制。在这篇论文中，我们公开了所有的技术细节一遍读者复现和理解，包括源代码和一些必要的硬件描述。

## 介绍
汽车已经不再只是一些呆板的机械设备。现在的汽车包括许多通过不同网络连接在一起的不同电子部件，作为一个整体，负责监控和控制汽车的运行状态。从防抱死模块到仪表盘再到通讯模块…每一个模块都能够和附近的模块进行通信。现代汽车最多包括50个电子控制单元(以下简称ECU).汽车总体的安全性依赖于这些多种多样的ECU的实时交互通信。当和其他模块交流时，这些ECU负责预测崩溃、检测打滑、执行防抱死刹车等等操作。

当用电子网络连接的组件被添加到任何一个设备中时，在这些设备中运行的代码的鲁棒性和可靠性的问题就随之而来。如果像手机一样考虑物理安全，那么代码的可靠性甚至是一个更加重要和实际的问题。在像个人电脑这样的典型的计算环境下，写一个脚本来监控和调整计算机运行是一件比较容易的事。然而，在高度计算化的汽车中，没有一个比较简单的方法来写一个能够监控和控制各种各样嵌入式系统的应用。驾驶员和乘客都寄希望于汽车中跑的代码能给自己留条活路，这不是像web主页崩溃那样的问题，而是实实在在的物理威胁。

一些学术研究，特别是来自华盛顿大学和加州圣地亚哥大学的研究，已经表明：将代码驻留在汽车中并控制一些关键系统是完全可能的（例如计算化的显示器和车锁或者是汽车刹车）。不仅如此，它们还表明这样的恶意代码可能被一个攻击者通过物理方法甚至蓝牙或者通信模块远程注入。它们展示了威胁不仅存在于偶然性的电子系统故障，还存在于可以引起汽车安全问题的恶意行为中。然而，他们的研究之局限于证明这些威胁的存在性。它们没有给出任何的代码或者工具，事实上，他们甚至没有展现它们研究的汽车模型。

除了讨论新型的攻击，这篇论文旨在为汽车系统安全的研究者提供开放透明的方法。目前，没有简单的方法去写一个通用的软件来监控并且与现代汽车中的ECU交互。事实是：汽车系统暴露在被攻击的威胁下，但是安全研究人员面没有办法监控或者和有问题的系统交互。本论文将会提供一个允许为汽车打造这些工具的框架并且在两款现代交通工具上展示使用过程。这个框架将会允许研究者们用具体的方式展示汽车系统的威胁并且编写监控和控制软件来缓解这些威胁。

这篇研究的核心是为两种新型汽车模型建造框架。我们讨论装备有停车辅助系统和其他科技部件的Toyota Peius和Ford Escape(都是2010年的模型)。不像之前的研究，这些技术的增添使我们的框架不仅能够获得一些刹车和多媒体信息，而且能够获得驾驶系统的信息。我们选择两款汽车以便于尽可能地建立通用的框架，并阐述两种不同汽车的不同。我们希望公开所有被使用的数据和工具，让我们的研究结果能够简单地被其他研究人员复现和拓展。

## 电子控制单元（ECU）
一般地，ECU单元被网络连接在一个或多个基于CAN(Controller Area Network)标准的总线上。ECU之间依靠发送CAN包来交流数据。这些包具有如下特点：

由于以上两个事实，不论是对CAN网络进行嗅探还是伪装成另一个ECU来发送CAN包都是很简单的。这也让对数据包的逆向分析更加困难，因为先验地推出那个CAN报文是由那个ECU发出和接收是不可能的。

通过检测ECU单元之间用于通信的CAN总线，就有可能发送合适的消息给ECU来指示它们做一些操作，或者甚至重写整个ECU（喵喵喵？），ECU本质上是嵌入式的设备，被网络连接在CAN总线上。每一个都有独立电源并且连接着大量传感器和执行机构。如下图

这些传感器为ECU提供输入，以便ECU判断当前该采取怎样的行动。执行机构是ECU能够执行这些动作。这些执行机构被频繁地使用来启动和停止汽车运动。总的来说，ECU是特殊的带有特定目的来感知周围环境，并采取行动来辅助汽车运行的嵌入式设备。

每一个ECU有一个特定的目的和自己的实现，但是他们必须互相交流数据来互相协作。为了实现这个功能，我们的汽车使用了CAN消息。一些ECU是间隔性地发送广播数据，例如传感器数据，然而有些其他ECU需要其周围的ECU相互协作来采取行动。其他的CAN信息也被制造商和经销商开发的软件用来在多样的汽车系统中进行诊断。

## 一般的CAN报文
在应用层，CAN报文包括ID段和数据段。虽然我们研究的汽车的ID字段长度都是11比特，实际ID段长度可以为11或29比特。紧跟ID段之后的是0到8字节的数据字段。数据字段包含多个组成成分，例如长度字段和下层协议的校验和字段（但是我们只关心应用层）。数据段中还可能包含应用层的校验和或者其他机制代码，但是这些没有在CAN标准中定义。正如我们将会看到的，有一个标准的方法来使用CAN报文一次发送超过8字节的数据。

除了标识设备，ID的另一个作用是标识设备优先级，设备ID的值越小，设备的优先级就越高。这个机制帮助ECU决策是否执行当前优先级的指令。在CAN的广播传输方式中，这种机制是很有必要的。

在CAN汽车网络中，有两种主要的CAN报文类型：正常类型和诊断类型。正常的报文从ECU发出，并且在任何时刻都能在总线网络上看到。正常报文可能是ECU广播给其他ECU的数据，或者可能是能够被其他ECU译码执行的指令。每时每刻都有大量这样的包被发送，准确的说是每几个毫秒。  
~~~
An example of such a packet with identifier 03B1 from the Ford Escape MS bus looks like: 

IDH: 03, IDL: B1, Len: 08, Data: 80 00 00 00 00 00 00 00  

An example of a packet transmitted by the Toyota with the identifier 00B6, broadcasting 
the current speed, with a checksum at the last data byte looks like:

IDH: 00, IDL: B6, Len: 04, Data: 33 A8 00 95  
~~~

注意：

上述的报文格式是本论文的作者为了方便读者阅读并且方便我们开发的API解析而构造的。11比特的CAN ID字段可能被分解为高字节和低字节或者整合为单个的ID。例如上面得到例子中的IDH为03，IDL为B1。因此这个ID为03B1。两种报文格式可相互转化。

当试图模拟CAN总线上的通信时，将会产生一个矛盾，就是CAN网络天生就是广播的。每个CAN报文确实有个CAN ID和它们绑定，但是对于正常的CAN报文，每个ECU独立的决策是否响应收到的报文。不仅如此，没有任何信息显示某个报文是哪个ECU发送的。这些特性导致了在我们没有任何先验知识的条件下，嗅探CAN网络时我们无法分辨每个报文的源和目的。唯一的例外就是诊断类型的CAN报文，对于这些报文来说，报文的目的可以简单的由CAN ID确定，而源一般是诊断工具。
~~~
Checksum - Toyota 
Many CAN messages implemented by the Toyota Prius contain a message checksum in the last byte of the data.
While not all messages have a checksum, a vast majority of important CAN packets contain one. 
The algorithm below is used to calculate the checksum. 

Checksum = (IDH + IDL + Len + Sum(Data[0] – Data[Len-2])) & 0xFF 

The checksum value is then placed in Data[Len - 1] position.  
For example, the following Lane Keep Assist (LKA) packet has a check sum of 0xE3, 
which is derived by summing 02,E4, 05, F8, 00, 00, 00: 

IDH: 02, IDL: E4, Len: 05, Data: F8 00 00 00 E3. 

Packets that do NOT have a correct checksum will be completely ignored by the ECUs on the CAN Bus for which the message is intended.  
~~~

## 诊断报文
另一种可以在汽车系统中看到的CAN报文是诊断报文。这些报文被机械师使用的诊断工具发送，用于和ECU的通信和质询。这些报文在汽车的正常运行过程中不会出现。作为一个例子，下面的报文是诊断工具和ABS系统的ECU交互报文，用于清除诊断工具和ABS ECU之间的默认编码：
~~~
IDH: 07, IDL: 60, Len: 08, Data: 03 14 FF 00 00 00 00 00 
IDH: 07, IDL: 68, Len: 08, Data: 03 7F 14 78 00 00 00 00 
IDH: 07, IDL: 68, Len: 08, Data: 03 54 FF 00 00 00 00 00 
~~~

在诊断报文发送时，每个ECU有一个特定的与之绑定的ID。就像在上面的例子中提到的，0760就是ABS ECU的ID（大多数的福特汽车都是如此）。响应报文的ID通常比被响应的报文的ID大8或者更多，在这个例子中是0768（比0760大8）。正常的报文没有类似的约定，并且是完全专有的。诊断报文格式一般遵循十分严格的标准，但是ECU实际上会以不同的方式遵循这些标准。接下来我们将会讨论诊断报文的有关标准。

### ISO-TP
ISO-TP（也称为ISO 15765-2）是一个在CAN总线上发送数据报文的国际标准。它定义了一种在总线上发送任意长度报文的方式。ISO-TP在每个CAN报文的开头增添了预置了一个或多个元数据字节。这些附加的字节被称为协议控制信息（PCI）。第一个字节的前半字节标识了PCI的类型。有四种可能的值：
~~~
0 - Single frame.  
Contains the entire payload.  
The next nibble is how much data is in the packet.

1 - First frame.  （第一帧，标识其后有其他的帧）
The first frame of a multi-packet payload. 
The next 3 nibbles 
indicate the size of the payload.

2 - Consecutive frame.  （连续帧，报文的中间一部分）
This contains the rest of a multi-packet payload.  
The next nibble serves as an index to sort out the order of received packets. 

3 - Flow control frame.  （流控制帧，规定报文传输速率等）
Serves as an acknowledgement of first frame packet.  
Specifies parameters for the transmission of additional packets such as their rate of delivery.
~~~

作为一个例子，上述内容中的第一种类型的包如下：
~~~
IDH: 07, IDL: 60, Len: 08, Data: 03 14 FF 00 00 00 00 00 
~~~
