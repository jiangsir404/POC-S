
您正处于项目源代码目录，该目录仅对开发者提供。

如需使用说明请访问：
https://github.com/Xyntax/POC-T/blob/master/README.md

===

You are in the main POC-T source folder. This page is ONLY for developers.

If you are looking for the user manual, please follow this link:
https://github.com/Xyntax/POC-T/blob/master/README.md

===


cli.py                      主函数

api
    zoomeye                 ZoomEye接口
controller
    api.py                  处理第三方接口
    engine.py               多线程&协程引擎
    loader.py               加载插件和目标
core
    common.py               基础函数库
    convert.py              编码转换
    data.py                 全局数据存储
    datatype.py             数据结构类
    enums.py                枚举类
    exception.py            错误类
    log.py                  日志与消息
    revision.py             检查版本(用于更新)
    settings.py             系统信息
parse
    cmdline.py              命令参数
    handler.py              参数处理
utils
    cnhelp.py               中文帮助
    console.py              运行时命令行输出
    update.py               自动升级功能
    versioncheck.py         Python版本检查
