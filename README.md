> ### ⚠️ 警告：该分支为Dev分支，当前仅支持JWT认证，wiki内容待完善
# UpdateWeather      [![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/hellsakura/UpdateWeather/main.yml?color=%2346c018&logo=github&style=flat-square)](https://github.com/HellSakura/UpdateWeather/actions)
调用和风天气api，为瀚文75扩展模块生成天气图片

[![python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=ffffff)](https://www.python.org/)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/hellsakura/UpdateWeather?style=flat-square&logo=github)](https://github.com/HellSakura/UpdateWeather/releases/latest)
[![GitHub all releases](https://img.shields.io/github/downloads/hellsakura/UpdateWeather/total?color=brightgreen&style=flat-square&logo=github)](https://github.com/HellSakura/UpdateWeather/releases/latest)

## 使用说明

>⚠注意：扩展模块需要刷入 xingrz 的[扩展固件](https://github.com/xingrz/zmk-config_helloword_hw-75/tree/master/config/boards/arm/hw75_dynamic)，才能正常工作

* 参见[快速开始](https://github.com/HellSakura/UpdateWeather/wiki/%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)

### 🔑 JWT 认证使用指南 (Dev 分支)

本分支使用和风天气最新的 **JWT (EdDSA)** 认证方式，安全性更高，推荐进阶用户使用。

#### 1. 生成密钥对
运行脚本生成所需的 Ed25519 密钥对：
```bash
pip install -r requirements.txt
python generate_key.py
```
运行后会生成两个文件：
*   `public_key.txt`: 公钥（纯 Base64 字符串）。请将内容复制并填入 [和风天气控制台](https://console.qweather.com/) 的项目设置中。[参考官方教程](https://dev.qweather.com/docs/configuration/project-and-key/)，建议验证JWT以确保正确。  
*   `private_key.pem`: 私钥（PEM 格式）。

#### 2. 配置 `config.ini`
将相关参数填入配置文件：
*   `publicid`: 和风控制台生成的 Key ID。
*   `projectid`: 和风控制台中的项目 ID。
*   `privatekey`: 从 `private_key.pem` 中提取的 Base64 字符串（即 `-----BEGIN...` 之后的内容）。
*   `apihost`: 您的自定义 API 域名。

#### 3. 构建
*   **手动构建**: 请fork本仓库，然后在 Actions 页面手动运行 `Dev Build and Release (JWT)`。
