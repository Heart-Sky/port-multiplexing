# port-multiplexing
端口复用相关思路和工具

## 简介
* 通过 setsockopt 函数实现对端口的重绑定，从而实现端口复用
    * 适用于 apache、nginx、iis(<6.0) 等
    * `python lcx.py -l 192.168.1.222 -p 80 -r 127.0.0.1 -P 3389`
* 通过 NET.TCP Port Sharing 服务
    * iis 6.0 后微软提供的原生机制，适用于 iis(>6.0)
    * 在 HTTP.sys 驱动上注册的 URL 前缀不同即可
    * WinRM 注册了 wsman 的 URL 前缀
        * 开启 WinRM 服务 `winrm quickconfig -q`
        * 原本没有开启 WinRM 服务，修改端口为 Web 服务端口 `winrm set winrm/config/Listener?Address=*+Transport=HTTP @{Port="80"}`
        * 原本开启了 WinRM 服务，新增 Web 服务端口监听 `winrm set winrm/config/service @{EnableCompatibilityHttpListener="true"}`
        * 远程连接 WinRM 服务，需要本机先开启服务，`winrm quickconfig -q`，且设置信任连接的主机，`winrm set winrm/config/Client @{TrustedHosts="*"}`
        * 使用 CMD 进行连接 `winrs -r:http://x.x.x.x -u:administrator -p:pass cmd`
        * 使用 PowerShell 进行连接 `Enter-PSSession -ComputerName http://x.x.x.x -Credential administrator`
        * 因为是类似 Linux 下的 SSH 进行远程操作，项目比较多，可以参考：https://github.com/diyan/pywinrm

* ......

## 应用场景
* 防火墙只开放 80 或者其他 web 服务端口
* 增加隐蔽性，降低被管理员发现的风险
* ......

## 效果
<img src=./pics/pic1.png>

ps: 持续更新中