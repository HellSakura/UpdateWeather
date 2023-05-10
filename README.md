# UpdateWeather      [![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/hellsakura/UpdateWeather/main.yml?color=%2346c018&logo=github&style=flat-square)](https://github.com/HellSakura/UpdateWeather/actions)
调用和风天气api，为瀚文75扩展模块生成天气图片

[![python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=ffffff)](https://www.python.org/)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/hellsakura/UpdateWeather?style=flat-square&logo=github)](https://github.com/HellSakura/UpdateWeather/releases/latest)
[![GitHub all releases](https://img.shields.io/github/downloads/hellsakura/UpdateWeather/total?color=brightgreen&style=flat-square&logo=github)](https://github.com/HellSakura/UpdateWeather/releases/latest)

## 使用说明
* 申请和风天气api，获取`key`和`location`，并填入`config.ini`中

`location` 即 LocationID 可通过[城市搜索服务](https://dev.qweather.com/docs/api/geoapi/city-lookup/)获取
```
[DEFAULT]
key = 
location = 
```
~~安装好依赖库后，运行`UpdateWeather.py`即可在当前目录下生成`output.png`天气图片，并自动刷入墨水屏~~

* 现在可以直接从release里下载打包好的exe文件直接运行了（仍需要放置`hidapi-win.zip`中的文件）

>需要将`hidapi-win.zip`中对应架构的`hidapi.pdb` `hidapi.lib` `hidapi.dll` 放置在相应的目录中。   
例如64位系统电脑请使用X64文件夹下的文件，放置于`C:\Windows\System32`中



## 效果预览
![图片预览](docs/output.png#pic_center)
<img src="./docs/Actual%20picture.png#pic_center" width = "128" height = "296"  />


## 如何刷入墨水屏（任选其一）
* ~~直接运行`UpdateWeather.py`，会自动刷入墨水屏~~

* 现在直接运行打包好的exe程序并配置好`config.ini`即可
* ~~运行`picUpdate.py` 即可~~    
     >`picUpdate.py`和`hidapi-win.zip`来自群友`[GNX-Susanoo]`，感谢！

* 使用[xingrz](https://github.com/xingrz/zmk-config_helloword_hw-75)开发的  [zmkx.app](https://zmkx.app/)   上位机驱动刷入

>⚠注意：无论使用哪种方式，扩展模块都需要刷入 xingrz 的[固件](https://github.com/xingrz/zmk-config_helloword_hw-75/tree/master/config/boards/arm/hw75_dynamic)，才能正常工作
## Tips        
* 如果想实现后台自动刷新，最好在自己系统配置python3.8环境，并在win计划任务中添加python程序
![Alt text](docs/task1.png)         
* 当然你也可以直接在计划任务中选择添加打包好的程序，在起始于中填入`UpdateWeather.exe`所在完整路径即可
![Alt text](docs/task2.png)
     >这会在每次刷新时弹窗
## Todolist    ![咕咕咕](https://img.shields.io/badge/-%E5%92%95%E5%92%95%E5%92%95-blue?style=flat-square)
- [ ] [更多](https://dev.qweather.com/docs/resource/icons/) 的中文天气矢量图 
- [ ] `location`直接填入城市名称即可
- [ ] 无需填写`loccation`，自动获取当前位置
