from PIL import Image

# 定义数字图片和线条图片的路径
image_path = "./img/"
line_path = "./img/line.png"
chinese_path = "./img/"
temp_path = "./img/temp.png"
wave_path = "./img/wave.png"

# 定义要解析的日期字符串和中文字符串
date_str = "2023-03-23"
weather_str = "暴雨"
tempmin = "-16"


# 将日期字符串解析成数字列表和线条数量
digits = [int(d) if d.isdigit() else "-" for d in date_str]
num_lines = date_str.count("-")


# 加载中文图片
weather_image = Image.open(image_path + weather_str + ".png")

temp_image = Image.open(temp_path)
wave_image = Image.open(wave_path)


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

# 将中文图片粘贴到新图片上
new_image.paste(weather_image, (0, 158)) 
new_image.paste(temp_image, (0, 220))
new_image.paste(wave_image, (58, 158))


# 保存新图片
new_image.save("output.png")
