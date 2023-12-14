# Xray-Gui

该项目参考了[super-xray](https://github.com/4ra1n/super-xray)

## 介绍
[xray](https://github.com/chaitin/xray) 是长亭科技研发的 一款功能强大的安全评估工具，由多名经验丰富的一线安全从业者呕心打造而成。

目前该工具是用命令行来实现扫描，为了方便快捷配置config.yaml文件以及帮助新人快速入手而写的GUI界面。
- 目前版本
- Version: 1.9.11（该版本使用xray 1.9.11和rad 1.0，不兼容老版本）
- 使用时把xray和rad放在Xray-Gui.exe同目录下
  

## 选择xray文件
<img src="/PNG/png1.png" alt="image" style="width:700px;height:700px;">

## 主动扫描

输入url后点击开启主动扫描，扫完后可以点击查看扫描结果。比命令行模式方便一点
<img src="/PNG/png2.png" alt="image" style="width:700px;height:700px;">

## 被动扫描
输入ip，端口，开启被动扫描
<img src="/PNG/png3.png" alt="image" style="width:700px;height:700px;">

## 高级设置
<img src="/PNG/png4.png" alt="image" style="width:700px;height:700px;">

## 编写poc
点击后跳转到[https://poc.xray.cool/](https://poc.xray.cool/)
<img src="/PNG/png5.png" alt="image" style="width:700px;height:700px;">

## rad界面
<img src="/PNG/png7.png" alt="image" style="width:700px;height:700px;">

## 查看rad_config文件
可以在配置文件里面修改后保存
<img src="/PNG/png8.png" alt="image" style="width:700px;height:700px;">

## rad主动扫描
输入url后点击自动扫描
<img src="/PNG/png9.png" alt="image" style="width:700px;height:700px;">

## rad需要手动登录的情况
输入url后勾选，点击主动扫描，弹出谷歌浏览器窗口，登入后点击确定
<img src="/PNG/png10.png" alt="image" style="width:700px;height:700px;">

## 与xray联动
在xray界面点击被动扫描后，再在rad界面输入目标url然后点击被动扫描
<img src="/PNG/png11.png" alt="image" style="width:700px;height:700px;">
<img src="/PNG/png12.png" alt="image" style="width:700px;height:700px;">
## 加解密
输入自动加密，解密的md5是通过内置的表来实现的。
<img src="/PNG/png6.png" alt="image" style="width:700px;height:700px;">




## 后续
后面再看一下xpoc的

## 更新日志
```
- 【2023.12.4】 修复第二次扫描时候，无法生成扫描文件的bug
- 【2023.12.14】 更新rad模块的ui界面
```

