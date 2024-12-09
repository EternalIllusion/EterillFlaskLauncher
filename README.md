# Eterill Flask App Launcher
## 一款带有WebGUI页面的Windows Flask应用管理器
### A Flask application manager for windows

# 使用 | Usage
一个项目的文件目录应该如图所示，其中`desc.json`为必须文件，它用于识别项目。
```bash
Project
- desc.json
- setup.py/setup.bat
- your-app.py
```
desc.json内容如下：
```json
{
    "info":{
        "name":"MyProject",
        "max_version":999,
        "author":"EterIll"
    },
    "splash":["{{name}}","by: {{author}}","{{applink}}"]
}
```
`info`部分存储项目信息。
- `name`：项目名称
- `max_version`：可接受的最大版本号
- `其他字段`：可以自定义，按需使用
`splash`存储项目说明的文字，每个项为一行。
- `{{applink}}`：项目链接，会读取`env.json`中`app_host_ip`和`app_host_port`作为IP和端口拼接，如果不存在`env.json`则使用默认：`本机IPV4`和端口`8000`
- `{{其他字段}}`：使用`info`中的字段值，如果不存在不会替换。
项目主文件：可以为任意文件名`.py`,文件前100字符需要出现`#@__core__=\d*\n`格式的注释，否则不会正确识别版本号。

合理的格式例如：
```python
# -*- coding: utf-8 -*-
#@__core__=114
print("版本号：114")
```
运行时会搜索当前目录的**所有子目录**，除了包含`AppData` `Program Files` `cache` `Cache`的目录。
后续在网页操作即可。