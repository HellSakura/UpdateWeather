import inquirer
from PIL import Image, ImageFont, ImageDraw
import time
import sched
import zmkx


def get_device(features=[]):
    devices = zmkx.find_devices(features=features)

    if len(devices) == 0:
        print('未找到符合条件的设备')
        return None

    if len(devices) == 1:
        return devices[0]

    choice = inquirer.prompt([
        inquirer.List('device', message='有多个设备，请选择', choices=[
            (f'{d.manufacturer} {d.product} (SN: {d.serial})', d)
            for d in devices
        ]),
    ])

    if choice is None:
        return None

    return choice['device']

def update_time(scheduler):
    device = get_device(features=['eink'])
    if device is None:
        return

    canvas = Image.new('1', (128, 36), color=0xFF)

    draw = ImageDraw.Draw(canvas)
    #字体使用缝合像素字体 https://github.com/TakWolf/fusion-pixel-font
    font = ImageFont.truetype('img/fusion-pixel-10px-monospaced-zh_hans.ttf', 20)

    with device.open() as device:
        now = time.localtime()
        text = time.strftime("%H:%M", now)

        print(f'更新文字: {text}')

        # 多次局部刷新后会出现残影，因此每半小时全屏刷新一次，进行全刷似乎会把原本的图片也刷掉
        partial = False if now.tm_min % 30 == 0 else True

        _, _, w, _ = draw.textbbox((0, 0), text, font=font)
        draw.text((canvas.width // 2 - w // 2, 0),
                  text, font=font, fill=0x00, align='center')

        #此处坐标是图片在屏幕上的位置，不出意外应该是在星期与天气之间的空位上
        device.eink_set_image(canvas.tobytes(), 0, 64,
                              canvas.width, canvas.height, partial)

    scheduler.enter(60, 1, update_time, (scheduler, ))


if __name__ == '__main__':
    print('脚本运行中')
    scheduler = sched.scheduler(time.time, time.sleep)
    update_time(scheduler)
    scheduler.run()