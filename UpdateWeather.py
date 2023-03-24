import configparser
import os
import requests
import datetime
import binascii
import re
import hid
import tkinter as tk
from PIL import Image
from tkinter import messagebox

#读取config.ini文件

config = configparser.ConfigParser()
config_file = os.path.join(os.getcwd(), 'config.ini')
config.read(config_file)

if not config.has_option('DEFAULT', 'key'):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "配置文件中缺少必要参数 'key'")
    exit()

if not config.has_option('DEFAULT', 'location'):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "配置文件中缺少必要参数 'location'")
    exit()

key = config.get('DEFAULT', 'key')
if not key:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "未填写 'key' 参数")
    exit()

location = config.get('DEFAULT', 'location')
if not location:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "未填写 'location' 参数")
    exit()


# 使用和风天气api
params = {
    'key': key,
    'location': location,
    'language': 'zh',
    'unit': 'm'
}

session = requests.Session()

url = 'https://devapi.qweather.com/v7/weather/3d'
url_today = 'https://devapi.qweather.com/v7/weather/now'

try:
    with session.get(url, params=params) as r, session.get(url_today, params=params) as t:
        r.raise_for_status()
        t.raise_for_status()

        data = r.json()['daily']
        data_today = t.json()['now']

        today = data[0]['fxDate']
        
        tempmin = data[0]['tempMin']
        tempmax = data[0]['tempMax']

        textDay = data[0]['textDay']
        textNight = data[0]['textNight']

        tempnow = data_today['temp']

        iconDay = data[0]['iconDay']
        iconNight = data[0]['iconNight']

        print('获取当前天气'+today)

except requests.exceptions.RequestException as e:
    print(f'An error occurred: {e}')

# 定义数字图片和线条图片的路径
image_path = "./img/"
line_path = "./img/line.png"
chinese_path = "./img/"
nowtemp_path = "./img/nowtemp.png"
wave_path = "./img/wave.png"

# 定义要解析的日期字符串和中文字符串
date_str = today
iconDay_str = iconDay
iconNight_str  = iconNight
textDay_str = textDay
textNight_str = textNight

# 获取当前是星期几
year, month, day = map(int, date_str.split('-'))
date = datetime.date(year, month, day)
weekday = date.strftime("%A")

# 将日期字符串解析成数字列表和线条数量
digits = [int(d) if d.isdigit() else "-" for d in date_str]
num_lines = date_str.count("-")

# 将温度值转换为带有符号的字符串
tempmin_digits = [d for d in tempmin if d.isdigit() or d == "-"]
tempmin_int = int("".join(tempmin_digits))
tempmin_str = "{:d}".format(tempmin_int)

tempmax_digits = [d for d in tempmax if d.isdigit() or d == "-"]
tempmax_int = int("".join(tempmax_digits))
tempmax_str = "{:d}".format(tempmax_int)

tempnow_digits = [d for d in tempnow if d.isdigit() or d == "-"]
tempnow_int = int("".join(tempnow_digits))
tempnow_str = "{:d}".format(tempnow_int)

# 计算温度值字符串的长度
tempmin_str_len = len(tempmin_str)
tempmax_str_len = len(tempmax_str)
tempnow_str_len = len(tempnow_str)

# 计算温度值字符串在新图片上的水平偏移量
if tempmin_str_len == 3:
    tempmin_offset_x =(64 - (12 * 3 + 8)) // 2
else:
    tempmin_offset_x = (64 - (12 * 2 + 8)) // 2

if tempmax_str_len == 3:
    tempmax_offset_x = 64 + (64 - (12 * 3 + 8)) // 2
else:
    tempmax_offset_x = 64 + (64 - (12 * 2 + 8)) // 2

if tempnow_str_len == 3:
    tempnow_offset_x = (128 - (12 * 3 + 8)) // 2
else:
    tempnow_offset_x = (128 - (12 * 2 + 8)) // 2

# 创建一张128x296的新图片
new_image = Image.new("RGB", (128, 296), color=(255, 255, 255))

# 将数字图片和线条图片拼接到新图片上
x_offset = (128 - 120) // 2
y_offset = (32 - 14) // 2
for digit in digits:
    if digit == "-":
        # 加载线条图片
        line_image = Image.open(line_path)

        # 将线条图片粘贴到新图片上
        new_image.paste(line_image, (x_offset, y_offset))

        # 更新线条图片在新图片中的水平偏移量
        x_offset += line_image.width
    else:
        # 加载数字图片
        digit_image = Image.open(image_path + str(digit) + ".png")

        # 将数字图片粘贴到新图片上
        new_image.paste(digit_image, (x_offset, y_offset))

        # 更新数字图片在新图片中的水平偏移量
        x_offset += digit_image.width

# 将星期粘贴到新图片上
weekday_image = Image.open(chinese_path + str(weekday) + ".png")
new_image.paste(weekday_image, (0, 32))

# 将天气图标粘贴到新图片上
weather_image = Image.open(image_path + iconDay + ".jpg")
new_image.paste(weather_image, (6, 96))
weather_image = Image.open(image_path + iconNight + ".jpg")
new_image.paste(weather_image, (70, 96))

# 将温度值字符串中的每个字符分别加载对应的图片，并粘贴到新图片上
tempmin_y_offset = 196
for min, ch in enumerate(tempmin_str):
    if ch == "-":
        # 加载减号图片
        minus_image = Image.open(image_path + "minus.png")
        new_image.paste(minus_image, (tempmin_offset_x, tempmin_y_offset))
    else:
        # 加载对应数字图片
        digit_image = Image.open(image_path + ch + ".png")
        new_image.paste(digit_image, (tempmin_offset_x + min * 12, tempmin_y_offset))

tempmax_y_offset = 196
for max, ch in enumerate(tempmax_str):
    if ch == "-":
        minus_image = Image.open(image_path + "minus.png")
        new_image.paste(minus_image, (tempmax_offset_x, tempmax_y_offset))
    else:
        digit_image = Image.open(image_path + ch + ".png")
        new_image.paste(digit_image, (tempmax_offset_x + max * 12, tempmax_y_offset))

tempnow_y_offset = 261
for now, ch in enumerate(tempnow_str):
    if ch == "-":
        minus_image = Image.open(image_path + "minus.png")
        new_image.paste(minus_image, (tempnow_offset_x, tempnow_y_offset))
    else:
        digit_image = Image.open(image_path + ch + ".png")
        new_image.paste(digit_image, (tempnow_offset_x + now * 12, tempnow_y_offset))


# 将中文图片粘贴到新图片上
weather_image = Image.open(image_path + textDay + ".png")
new_image.paste(weather_image, (0, 158))
weather_image = Image.open(image_path + textNight + ".png")
new_image.paste(weather_image, (64, 158))

# 将温度单位图片粘贴到新图片上
temp_unit_image = Image.open(image_path + "temp_unit.png")
new_image.paste(temp_unit_image, (tempmin_offset_x + min * 12 + 12, tempmin_y_offset))
new_image.paste(temp_unit_image, (tempmax_offset_x + max * 12 + 12, tempmax_y_offset))
new_image.paste(temp_unit_image, (tempnow_offset_x + now * 12 + 12, tempnow_y_offset))

# 将其他图片粘贴到新图片上
nowtemp_image = Image.open(nowtemp_path)
new_image.paste(nowtemp_image, (0, 220))
wave_image = Image.open(wave_path)
new_image.paste(wave_image, (58, 158))
new_image.paste(wave_image, (58, 190))


# 保存新图片
new_image.save("output.png")
print('创建图片')

# 刷新墨水屏
if __name__ == '__main__':
    img = Image.open('./output.png')

    black_img = img.convert("L")  # 转化为黑白图片#进行灰度处理
    bdata_list = list(black_img.getdata())

    threshold = 128
    bvalue_list = [0 if i < threshold else 1 for i in bdata_list]
    # 将8位一组放在一起
    ob_list = []
    s = "0b"
    for i in range(1, len(bvalue_list) + 1):
        s += str(bvalue_list[i - 1])
        if i % 8 == 0:
            ob_list.append(s)
            s = "0b"
    # 转换为16进制字符串 格式定位两位
    ox_list = ['%02x' % int(i, 2) for i in ob_list]
    j = 0
    firstPackage = '013e8d2508072a8825080b1080251a8025'
    nextPackage = '013e'
    lastPackage = '0128'
    hexStr = ''
    hexStr += firstPackage
    for i in range(0, 47):
        hexStr += ox_list[j]
        j += 1
    packCount = int((len(ox_list) - 47) / 62)
    for i in range(0, packCount):
        hexStr += nextPackage
        for k in range(0, 62):
            if j >= len(ox_list):
                hexStr += '00'
            else:
                hexStr += ox_list[j]
            j += 1
    hexStr += lastPackage
    for k in range(0, 62):
        if j >= len(ox_list):
            hexStr += '00'
        else:
            hexStr += ox_list[j]
        j += 1
    st2 = re.findall(r'.{128}', hexStr)
    st2.append(hexStr[int(int(len(hexStr) / 128) * 128):])
    h = hid.enumerate(vid=0x1d50, pid=0x615e)
    d = hid.Device(path=h[2]['path'])
    d.write(binascii.unhexlify(
        '01050408011200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))
    pack = d.read(1000).decode()
    print('Zephyr 版本:' + pack[9:16])
    print('ZMK 版本:' + pack[18:25])
    print('固件版本:' + pack[27:34])
    for i in st2:
        if i == '':
            continue
        d.write(binascii.unhexlify(i))
    print('图片刷新完成')
