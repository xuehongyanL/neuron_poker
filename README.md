# 人工智能课程大作业-无限注德州扑克机器人

## 组员

薛泓彦 负责python端的接口设计和适配 以及C++代码的整合

胡景佩 C++牌型评估方面尝试编写

孔维浩 决策部分的设计 编写报告

高云聪 调研和优化设计

## 环境说明

AI的主体部分是一个动态库，用C++编写。

所有C++代码位于neuron_poker\ai目录，用Makefile组织。

agent的python代码位于neuron_poker\agents\agent_custom_ai.py。

AI与随机agent对局的环境在neuron_poker\main.py中有所修改。

所有的这些改动可以在git中查看。

## 运行测试

首先安装环境。安装过程见环境开发者编写的readme.rst。

进入neuron_poker\ai目录，根据操作系统执行'make windows'或'make linux'，确保当前目录出现了'ai.dll'(Win)或'ai.so'(Linux)。

然后回到项目根目录，执行'python3 main.py ai_vs_random --ai_num=X'，其中'X'是随机agent的个数，可以取1到6。

## 致谢

C++的牌型评估函数由胡景佩撰写，他做了有益的尝试，但效果并不理想，于是尝试使用了一个现成的库：[SKPokerEval](https://github.com/kennethshackleton/SKPokerEval/tree/master)，在此说明。