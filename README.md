# UpdateWeather
调用和风天气api，为瀚文75扩展模块生成天气图片

## 使用说明
* 申请和风天气api，获取`key`和`location`，并填入`UpdateWeather.py`中

`location` 即 LocationID 可通过[城市搜索服务](https://dev.qweather.com/docs/api/geoapi/city-lookup/)获取
```params = {
    'key': '',  # 密钥
    'location': '',  # 城市代码
    'language': 'zh',
    'unit': 'm'
}
```
运行`UpdateWeather.py`即可在当前目录下生成`output.png`天气图片
## 效果预览
![图片预览](docs/output.png#pic_center)
<img src="./docs/Actual%20picture.png#pic_center" width = "128" height = "296"  />


## 如何刷入墨水屏
* 运行`picUpdate.py` 即可     
    >`picUpdate.py`和`hidapi-win.zip`来自群友`[GNX-Susanoo]`，感谢！
* 使用[xingrz](https://github.com/xingrz/zmk-config_helloword_hw-75)开发的  [zmkx.app](https://zmkx.app/)   上位机驱动刷入

>⚠注意：无论使用哪种方式，扩展模块都需要刷入 xingrz 的[固件](https://github.com/xingrz/zmk-config_helloword_hw-75/tree/master/config/boards/arm/hw75_dynamic)，才能正常工作
