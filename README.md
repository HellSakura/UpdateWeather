# UpdateWeather  [![.github/workflows/main.yml](https://github.com/HellSakura/UpdateWeather/actions/workflows/main.yml/badge.svg)](https://github.com/HellSakura/UpdateWeather/actions/workflows/main.yml)
调用和风天气api，为瀚文75扩展模块生成天气图片

![GitHub all releases](https://img.shields.io/github/downloads/hellsakura/UpdateWeather/total?color=brightgreen)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/hellsakura/UpdateWeather)
## 使用说明
* 申请和风天气api，获取`key`和`location`，并填入`config.ini`中

`location` 即 LocationID 可通过[城市搜索服务](https://dev.qweather.com/docs/api/geoapi/city-lookup/)获取
```
[DEFAULT]
key = 
location = 
```
运行`UpdateWeather.py`即可在当前目录下生成`output.png`天气图片，并自动刷入墨水屏
>需要将`hidapi-win.zip`中对应架构的`hidapi.pdb` `hidapi.lib` `hidapi.dll` 放置在相应的目录中。   
例如64位系统电脑请使用X64文件夹下的文件，放置于`C:\Windows\System32`中

* 现在可以直接从release里下载打包好的exe文件直接运行了（仍需要放置`hidapi-win.zip`中的文件）

## 效果预览
![图片预览](docs/output.png#pic_center)
<img src="./docs/Actual%20picture.png#pic_center" width = "128" height = "296"  />


## 如何刷入墨水屏
* 直接运行`UpdateWeather.py`，会自动刷入墨水屏
* 运行`picUpdate.py` 即可    
     >`picUpdate.py`和`hidapi-win.zip`来自群友`[GNX-Susanoo]`，感谢！

* 使用[xingrz](https://github.com/xingrz/zmk-config_helloword_hw-75)开发的  [zmkx.app](https://zmkx.app/)   上位机驱动刷入

>⚠注意：无论使用哪种方式，扩展模块都需要刷入 xingrz 的[固件](https://github.com/xingrz/zmk-config_helloword_hw-75/tree/master/config/boards/arm/hw75_dynamic)，才能正常工作
