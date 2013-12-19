简化的有道网页搜索。
======

功能：
--------
1. 清理页面，让网页更加干净
2. 独立窗口，不需要在浏览器标签页之间来回切换。针对我个人使用更加方便。配合i3 wm的scratchpad使用。
3. 简单的快捷键设置，不需要使用鼠标来配合输入跟基本操作。

不足：
----
依赖于网页结构，网页发生变化，必须修改相应源代码。但是我又不想使用有道api，然后自己呈现搜索结果，有道api也不提供个人账信息的获取，对于保存单词等功能还欠缺。

目前还不能发音，待解决。

快捷键：
------
j，k, gg, G：	类vim导航

ctrl-f, ctrl-b：下一页，上一页

0,1,2,3: 搜索结果导航

':':	进入命令模式，下方出现输入框

直接输入单词：搜索单词

login: 	登陆

add：	加入到单词本（只有登陆后）

q/quit：推出

![Start Page](screenshot/startpage.png "")
![Main Window](screenshot/main_window.png "")
![Login Window](screenshot/login.png "")
![Window](screenshot/mw-login.png "")
