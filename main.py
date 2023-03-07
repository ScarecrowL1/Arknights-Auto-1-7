import time
from ctypes import windll

from win32con import SWP_NOMOVE, SWP_NOZORDER
from win32gui import SetWindowPos

import reconize
import click

OPRA_COMP_PATH = './image/opra_comp.png'
OPRA_STAR_PATH = './image/opra_start.png'
START_PATH = './image/start.png'

if __name__ == "__main__":
    import sys

    if not windll.shell32.IsUserAnAdmin():
        # 不是管理员就提权
        windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)

    try:
        handle = windll.user32.FindWindowW(None, "明日方舟 - MuMu模拟器")
    except:
        print("找不到明日方舟 - MuMu模拟器")
        sys.exit(1)
    # 将模拟器的窗口大小设置为程序可执行的大小 1440*899 使得游戏框为1440*810
    SetWindowPos(handle, 0, 0, 0, 1440, 899, SWP_NOMOVE | SWP_NOZORDER)
    print("请输入执行次数:")
    cnt = int(input())
    i = 0
    # 查找开始按钮并按下
    while i < cnt:
        while 1:
            image = reconize.capture(handle)
            loc = reconize.match(image, START_PATH)
            if loc is not None:
                click.click(handle, loc[0], loc[1])
                break
            print("未找到开始按钮，请点开1-7")
            time.sleep(1)
        print("已找到开始按钮")
        loc = None

        while 1:
            image = reconize.capture(handle)
            loc = reconize.match(image, OPRA_STAR_PATH)
            if loc is not None:
                click.click(handle, loc[0], loc[1])
                break
            print("未找到")
            time.sleep(1)
        print("已找到")
        loc = None

        print("正在等待代理指挥结束")
        time.sleep(70)
        while 1:
            image = reconize.capture(handle)
            loc = reconize.match(image, OPRA_COMP_PATH)
            if loc is not None:
                click.click(handle, loc[0], loc[1])
                break
            print("寻找结束标志中")
            time.sleep(1)
        loc = None
        # 为了防止升级等提示，要看到开始按钮才结束大循环

        while 1:
            image = reconize.capture(handle)
            loc = reconize.match(image, START_PATH)  # 查看结束后是否已跳转到最初页面
            if loc is not None:  # 如果没有看到开始按钮，就继续点击屏幕中央
                break
            print("正在等待跳转到开始按钮")
            click.click(handle, int(image.shape[1] / 2), int(image.shape[0] / 2))
            time.sleep(1)
        print("已找到开始按钮")
        loc = None
        i = i + 1
        print("第", i, "次代理已结束")
    print("代理已经结束，按任意键退出,完成了", i, "次代理")
    input()
