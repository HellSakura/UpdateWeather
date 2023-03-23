import binascii
import re

import hid
from PIL import Image

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
