# sec-valve-backend
```
  一,简介

    本项目为上海电气阀门项目,用户鉴权/任务管理/阀门库等相关功能
    
    
二,项目环境
    python版本：python3.6
    系统：ubuntu16.04
    数据库：postgres11
    框架: flask
    其他涉及包以及版本参照requirement.txt
    
三,运行
    1,根据requirement建虚拟环境并安装包(pip install -r requirement.txt)
    
    2, 创建数据库表
    　　python manage.py db init
       python manage.py db migrate
       python manage.py db upgrade
    
    3, 初始化数据
       根据　manage.py 文件头部注释　依次运行脚本

    4,运行 python run.py
    
    5, 默认运行 域名127.0.0.1, 端口5000

三,api使用
   参见“docs/api.md”

四,　环境变量相关
　　
  
```
