import sys
import configparser
import os
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # 禁用https警告
import datetime
import binascii
import re
import tkinter as tk
from PIL import Image
from tkinter import messagebox
import logging
import time
import jwt

# 读取config.ini文件
config = configparser.ConfigParser()
config_file = os.path.join(os.getcwd(), 'config.ini')
config.read(config_file)

# 设置日志记录器
logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 尝试导入 hid 库
hid_available = False
try:
    import hid
    hid_available = True
    logging.info("hid library imported successfully.")
except ImportError as e:
    logging.warning(f"Failed to import hid library: {e}. E-ink screen refresh will be unavailable.")

if not config.has_option('DEFAULT', 'key'):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "配置文件中缺少必要参数 'key'")
    sys.exit()

if not config.has_option('DEFAULT', 'publicid'):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "配置文件中缺少必要参数 'publicid'")
    sys.exit()

if not config.has_option('DEFAULT', 'privatekey'):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "配置文件中缺少必要参数 'privatekey'")
    sys.exit()

if not config.has_option('DEFAULT', 'location'):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "配置文件中缺少必要参数 'location'")
    sys.exit()

publicid = config.get('DEFAULT', 'publicid')
if not publicid:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "未填写 'publicid' 参数")
    sys.exit()

projectid = config.get('DEFAULT', 'projectid', fallback=None)
if not projectid:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "配置文件中缺少 'projectid' 参数")
    sys.exit()

privatekey_core = config.get('DEFAULT', 'privatekey') # 用户现在只填写核心内容
if not privatekey_core:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "配置文件中未填写 'privatekey' 的核心内容")
    sys.exit()
# 清理用户可能意外粘贴的空白字符（包括换行），并确保是单行
privatekey_core_cleaned = "".join(privatekey_core.strip().split())
# 重建完整的PEM格式密钥
privatekey = f"-----BEGIN PRIVATE KEY-----\n{privatekey_core_cleaned}\n-----END PRIVATE KEY-----"


location = config.get('DEFAULT', 'location')
if not location:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "未填写 'location' 参数")
    sys.exit()

def generate_jwt(key_id, project_id, private_key_str):
    """生成和风天气 API 使用的 JWT"""
    # Header
    headers = {
        'alg': 'EdDSA',
        'kid': key_id
        # 'typ': 'JWT' 和风天气建议移除，但PyJWT库默认会添加 "typ":"JWT"
    }
    # Payload
    payload = {
        # 'publicid': key_id, # 移除api key
        'sub': project_id,
        'iat': int(time.time()),
        'exp': int(time.time()) + 30 * 60
    }
    try:
        private_key_bytes = private_key_str.encode('utf-8')
        token = jwt.encode(payload, private_key_bytes, algorithm='EdDSA', headers=headers)
        print(f"创建 JWT: {token}")
        return token
    except Exception as e:
        logging.exception(f"Error generating JWT: {e}")
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror('错误', f"生成JWT时出错: {e}")
        sys.exit()

params = {
    'location': location,
    'language': 'zh',
    'unit': 'm'
}

session = requests.Session()

url = 'https://nn3jpbqfmg.re.qweatherapi.com/v7/weather/3d'
url_today = 'https://nn3jpbqfmg.re.qweatherapi.com/v7/weather/now'

try:
    jwt_token = generate_jwt(publicid, projectid, privatekey)
    auth_headers = {
        'Authorization': f'Bearer {jwt_token}'
    }
    # verify=False 临时禁用SSL证书验证
    with session.get(url, params=params, headers=auth_headers, verify=False) as r, \
         session.get(url_today, params=params, headers=auth_headers, verify=False) as t:
        r.raise_for_status()
        t.raise_for_status()

        try:
            data = r.json()['daily']
        except KeyError:
            raise ValueError(r.text)
        
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
    error_message = str(e)
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', f"网络请求错误: {error_message}")
    logging.exception(error_message)
    sys.exit()

except (KeyError, ValueError) as e:
    error_message = str(e)
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "请检查API凭据或location输入是否正确\n" + error_message)
    logging.exception(error_message)
    sys.exit()


image_path = "./img/"
line_path = "./img/line.png"
chinese_path = "./img/"
nowtemp_path = "./img/nowtemp.png"
wave_path = "./img/wave.png"

date_str = today
iconDay_str = iconDay
iconNight_str  = iconNight
textDay_str = textDay
textNight_str = textNight

year, month, day = map(int, date_str.split('-'))
date_obj = datetime.date(year, month, day) 
weekday = date_obj.strftime("%A")

digits = [int(d) if d.isdigit() else "-" for d in date_str]
num_lines = date_str.count("-")

tempmin_digits = [d for d in tempmin if d.isdigit() or d == "-"]
tempmin_int = int("".join(tempmin_digits))
tempmin_str = "{:d}".format(tempmin_int)

tempmax_digits = [d for d in tempmax if d.isdigit() or d == "-"]
tempmax_int = int("".join(tempmax_digits))
tempmax_str = "{:d}".format(tempmax_int)

tempnow_digits = [d for d in tempnow if d.isdigit() or d == "-"]
tempnow_int = int("".join(tempnow_digits))
tempnow_str = "{:d}".format(tempnow_int)

tempmin_str_len = len(tempmin_str)
tempmax_str_len = len(tempmax_str)
tempnow_str_len = len(tempnow_str)

if tempmin_str_len == 3:
    tempmin_offset_x =(64 - (12 * 3 + 8)) // 2
elif tempmin_str_len == 2:
    tempmin_offset_x = (64 - (12 * 2 + 8)) // 2
else:
    tempmin_offset_x = (64 - (12 * 1 + 8)) // 2

if tempmax_str_len == 3:
    tempmax_offset_x = 64 + (64 - (12 * 3 + 8)) // 2
elif tempmax_str_len == 2:
    tempmax_offset_x = 64 + (64 - (12 * 2 + 8)) // 2
else:
    tempmax_offset_x = 64 + (64 - (12 * 1 + 8)) // 2

if tempnow_str_len == 3:
    tempnow_offset_x = (128 - (12 * 3 + 8)) // 2
elif tempnow_str_len == 2:
    tempnow_offset_x = (128 - (12 * 2 + 8)) // 2
else:
    tempnow_offset_x = (128 - (12 * 1 + 8)) // 2

new_image = Image.new("RGB", (128, 296), color=(255, 255, 255))

x_offset = (128 - 120) // 2
y_offset = (32 - 14) // 2
for digit in digits:
    if digit == "-":
        line_image = Image.open(line_path)
        new_image.paste(line_image, (x_offset, y_offset))
        x_offset += line_image.width
    else:
        digit_image = Image.open(image_path + str(digit) + ".png")
        new_image.paste(digit_image, (x_offset, y_offset))
        x_offset += digit_image.width

weekday_image = Image.open(chinese_path + str(weekday) + ".png")
new_image.paste(weekday_image, (0, 32))

weather_image_day = Image.open(image_path + iconDay + ".jpg")
new_image.paste(weather_image_day, (6, 96))
weather_image_night = Image.open(image_path + iconNight + ".jpg")
new_image.paste(weather_image_night, (70, 96))

tempmin_y_offset = 196
for idx, ch in enumerate(tempmin_str):
    if ch == "-":
        minus_image = Image.open(image_path + "minus.png")
        new_image.paste(minus_image, (tempmin_offset_x, tempmin_y_offset))
    else:
        digit_image = Image.open(image_path + ch + ".png")
        new_image.paste(digit_image, (tempmin_offset_x + idx * 12, tempmin_y_offset))

tempmax_y_offset = 196
for idx, ch in enumerate(tempmax_str):
    if ch == "-":
        minus_image = Image.open(image_path + "minus.png")
        new_image.paste(minus_image, (tempmax_offset_x, tempmax_y_offset))
    else:
        digit_image = Image.open(image_path + ch + ".png")
        new_image.paste(digit_image, (tempmax_offset_x + idx * 12, tempmax_y_offset))

tempnow_y_offset = 261
for idx, ch in enumerate(tempnow_str):
    if ch == "-":
        minus_image = Image.open(image_path + "minus.png")
        new_image.paste(minus_image, (tempnow_offset_x, tempnow_y_offset))
    else:
        digit_image = Image.open(image_path + ch + ".png")
        new_image.paste(digit_image, (tempnow_offset_x + idx * 12, tempnow_y_offset))


weather_text_day = Image.open(image_path + textDay + ".png")
new_image.paste(weather_text_day, (0, 158))
weather_text_night = Image.open(image_path + textNight + ".png")
new_image.paste(weather_text_night, (64, 158))

temp_unit_image = Image.open(image_path + "temp_unit.png")
# Corrected logic for positioning temp_unit_image
tempmin_last_char_idx = len(tempmin_str) - 1
tempmax_last_char_idx = len(tempmax_str) - 1
tempnow_last_char_idx = len(tempnow_str) - 1

new_image.paste(temp_unit_image, (tempmin_offset_x + tempmin_last_char_idx * 12 + 12 if tempmin_str and tempmin_str[0] != '-' else tempmin_offset_x + 12, tempmin_y_offset))
new_image.paste(temp_unit_image, (tempmax_offset_x + tempmax_last_char_idx * 12 + 12 if tempmax_str and tempmax_str[0] != '-' else tempmax_offset_x + 12, tempmax_y_offset))
new_image.paste(temp_unit_image, (tempnow_offset_x + tempnow_last_char_idx * 12 + 12 if tempnow_str and tempnow_str[0] != '-' else tempnow_offset_x + 12, tempnow_y_offset))


nowtemp_image = Image.open(nowtemp_path)
new_image.paste(nowtemp_image, (0, 220))
wave_image = Image.open(wave_path)
new_image.paste(wave_image, (58, 158))
new_image.paste(wave_image, (58, 190))


new_image.save("output.png")
print('创建图片')

# 刷新墨水屏 (以下代码保持注释状态)
# if __name__ == '__main__':
#     # img = Image.open('./output.png')
#
#     # black_img = img.convert("L")  # 进行灰度处理
#     # bdata_list = list(black_img.getdata())
#
#     # threshold = 128
#     # bvalue_list = [0 if i < threshold else 1 for i in bdata_list]
#     # # 将8位一组放在一起
#     # ob_list = []
#     # s = "0b"
#     # for i in range(1, len(bvalue_list) + 1):
#     #     s += str(bvalue_list[i - 1])
#     #     if i % 8 == 0:
#     #         ob_list.append(s)
#     #         s = "0b"
#     # # 转换为16进制字符串 格式定位两位
#     # ox_list = ['%02x' % int(i, 2) for i in ob_list]
#     # j = 0
#     # firstPackage = '013e8d2508072a8825080b1080251a8025'
#     # nextPackage = '013e'
#     # lastPackage = '0128'
#     # hexStr = ''
#     # hexStr += firstPackage
#     # for i in range(0, 47):
#     #     hexStr += ox_list[j]
#     #     j += 1
#     # packCount = int((len(ox_list) - 47) / 62)
#     # for i in range(0, packCount):
#     #     hexStr += nextPackage
#     #     for k in range(0, 62):
#     #         if j >= len(ox_list):
#     #             hexStr += '00'
#     #         else:
#     #             hexStr += ox_list[j]
#     #         j += 1
#     # hexStr += lastPackage
#     # for k in range(0, 62):
#     #     if j >= len(ox_list):
#     #         hexStr += '00'
#     #     else:
#     #         hexStr += ox_list[j]
#     #         j += 1
#     # st2 = re.findall(r'.{128}', hexStr)
#     # st2.append(hexStr[int(int(len(hexStr) / 128) * 128):])
#
#     # # HID命令: 获取设备版本信息 (总共64字节)
#     # # 命令前缀 (6字节, 12个十六进制字符)
#     # HID_COMMAND_GET_VERSION_PREFIX_HEX = "010504080112"
#     # # 剩余字节用 "00" 填充 (64字节命令 - 6字节前缀 = 58字节填充)
#     # HID_COMMAND_GET_VERSION_PADDING_HEX = "00" * 58
#     # HID_COMMAND_GET_VERSION_HEX = HID_COMMAND_GET_VERSION_PREFIX_HEX + HID_COMMAND_GET_VERSION_PADDING_HEX
#
#     # if hid_available:
#     #     h = hid.enumerate(vid=0x1d50, pid=0x615e)
#     #     path = None
#     #     for device_info in h:
#     #         if device_info['usage_page'] == 65300: # 用usage_page选择设备
#     #             path = device_info['path']
#     #             break
#     #     if path:
#     #         try:
#     #             d = hid.Device(path=path)
#     #             #   d = hid.Device(path=h[2]['path']) # 原始代码中的备选方案
#     #             d.write(binascii.unhexlify(HID_COMMAND_GET_VERSION_HEX))
#     #             pack = d.read(1000).decode("utf8", "ignore")
#     #             print('Zephyr 版本:' + pack[9:16])
#     #             print('ZMK 版本:' + pack[18:25])
#     #             print('固件版本:' + pack[27:34])
#     #             for i in st2:
#     #                 if i == '':
#     #                     continue
#     #                 d.write(binascii.unhexlify(i))
#     #             print('图片刷新完成')
#     #             d.close() # 关闭设备
#     #         except Exception as e_hid:
#     #             logging.error(f"Error during HID operation: {e_hid}")
#     #             print(f"HID操作出错: {e_hid}")
#     #     else:
#     #         print("未找到兼容的HID设备，跳过墨水屏刷新。")
#     #         logging.warning("Compatible HID device not found, skipping e-ink refresh.")
#     # else:
#     #     print("hid库不可用，跳过墨水屏刷新。")
#     #     logging.warning("hid library not available, skipping e-ink refresh.")

if __name__ == '__main__':
    if not hid_available:
        print("警告: hid库未能成功加载，墨水屏刷新功能将不可用。")
    print("墨水屏刷新代码已注释，仅生成图片。")
