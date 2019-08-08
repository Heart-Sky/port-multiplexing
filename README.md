# port-multiplexing
端口复用相关思路和工具

## 简介
* 通过 setsockopt 函数实现对端口的重绑定，从而实现端口复用
    * 适用于 apache、nginx、iis(<6.0) 等
    * `python lcx.py -l 192.168.1.222 -p 80 -r 127.0.0.1 -P 3389`
* ......

## 应用场景
* 防火墙只开放 80 或者其他 web 服务端口
* 增加隐蔽性，降低被管理员发现的风险
* ......

## 效果
<img src=./pics/pic1.png>

ps: 持续更新中