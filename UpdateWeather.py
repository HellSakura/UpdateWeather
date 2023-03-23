import requests
from PIL import Image

# 使用和风天气api
params = {
    'key': '',  # 和风天气，其中填写自己的密钥
    'location': '',
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
        # 加载减号图片
        minus_image = Image.open(image_path + "minus.png")
        new_image.paste(minus_image, (tempmax_offset_x, tempmax_y_offset))
    else:
        # 加载对应数字图片
        digit_image = Image.open(image_path + ch + ".png")
        new_image.paste(digit_image, (tempmax_offset_x + max * 12, tempmax_y_offset))

tempnow_y_offset = 261
for now, ch in enumerate(tempnow_str):
    if ch == "-":
        # 加载减号图片
        minus_image = Image.open(image_path + "minus.png")
        new_image.paste(minus_image, (tempnow_offset_x, tempnow_y_offset))
    else:
        # 加载对应数字图片
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
