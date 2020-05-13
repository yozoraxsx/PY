# -*- coding:utf-8 -*-
import sys
import threading
import time

import cv2

import functions


class event:
    flag = threading.Event()  # 子程序开关
    end = threading.Event()  # 子程序结束主程序开始事件

    class fight:  # 战斗子程序事件
        flag = threading.Event()  # 战斗类事件筛选
        end = threading.Event()  # 子程序完成事件
        boost = threading.Event()  # boost事件
        full = threading.Event()  # 满血事件

    class select:  # 选择子程序事件
        flag = threading.Event()  # 选择类事件筛选
        start = threading.Event()  # 开始界面事件
        go = threading.Event()  # 出发界面事件


BOOST = cv2.imread(sys.path[0] + '\\IMG\\boost.jpg')
END = cv2.imread(sys.path[0] + '\\IMG\\end.jpg')
FIGHT = cv2.imread(sys.path[0] + '\\IMG\\fight.jpg')
GO = cv2.imread(sys.path[0] + '\\IMG\\go.jpg')
OFFLINE = cv2.imread(sys.path[0] + '\\IMG\\offline.jpg')
FULL = cv2.imread(sys.path[0] + '\\IMG\\full.jpg')


def startfind(img):  # 选关界面判断
    # y0   y1   x0   x1
    # 791, 835, 737, 969 (1600x900)
    # 0.878,0.927,0.46,0.6
    img = functions.cut_image(791, 835, 737, 969, img)
    x = functions.compare_image(img, FIGHT)
    if x >= 0.8:
        event.select.start.set()
    else:
        event.select.start.clear()
    # print(x)


def gofind(img):  # 开始界面判断
    # y0   y1   x0   x1
    # 754, 830, 1220, 1465
    #
    img = functions.screenshot()
    img = functions.cut_image(754, 830, 1220, 1465, img)
    x = functions.compare_image(img, GO)
    if x >= 0.8:
        event.select.go.set()
    else:
        event.select.go.clear()
    # print(x)


def boostfind(img):  # 找boost
    # y0   y1   x0   x1
    # 753, 790, 1259, 1410
    #
    img = functions.cut_image(753, 790, 1259, 1410, img)
    x = functions.compare_image(img, BOOST)
    if x >= 0.7:  # boost 找到了
        event.fight.boost.set()
    else:
        event.fight.boost.clear()
    # print(x)


def endfind(img):  # 结束判断
    # y0   y1   x0   x1
    # 158, 216, 690, 907
    #
    img = functions.cut_image(158, 216, 690, 907, img)
    # cv2.imwrite('x.jpg', img)
    x = functions.compare_image(img, END)
    if x >= 0.7:
        event.fight.end.set()
    else:
        event.fight.end.clear()
    # print(x)


def fullfind(img):  # 残血判定
    # y0   y1   x0   x1
    # 140, 150, 529, 534
    #
    img = functions.cut_image(140, 150, 529, 534, img)
    x = functions.compare_image(img, FULL)
    if x >= 0.8:
        event.fight.full.set()
    else:
        event.fight.full.clear()
    # print(x)


def offlinefind(img):  # 断网判定
    # y0   y1   x0   x1
    # 390, 485, 626, 960
    #
    img = functions.cut_image(390, 485, 626, 960, img)
    x = functions.compare_image(img, OFFLINE)
    if x >= 0.9:
        functions.adb.click(1424, 765)  # 断网重连操作
    # print(x)


def backstage():  # 子线程
    event.fight.boost.clear()
    event.fight.full.clear()
    event.fight.end.clear()
    event.select.start.clear()
    event.select.go.clear()

    event.flag.clear()
    event.select.flag.clear()
    event.fight.flag.clear()
    time.sleep(2)
    while True:  # 子线程
        event.flag.wait()  # 等待后台允许事件
        img = functions.screenshot()
        if event.select.flag.is_set():  # 选择类事件检测
            offlinefind(img)
            startfind(img)
            gofind(img)
        if event.fight.flag.is_set():  # 战斗类事件检测
            offlinefind(img)
            boostfind(img)
            fullfind(img)
            endfind(img)
            if event.fight.boost.is_set():
                event.end.set()
            elif event.fight.end.is_set():
                event.end.set()
            else:
                event.end.clear()
        time.sleep(1)


def actionextra():  # 战斗判断函数
    time.sleep(8)
    event.flag.set()  # 开始子线程
    event.end.wait(timeout=None)  # 等待后台发出开始命令
    event.end.clear()
    event.flag.clear()  # 停止子线程，开始判断
    if event.fight.boost.is_set():  # 有boost
        if event.fight.full.is_set():  # 满血
            return 1
        if not event.fight.full.is_set():  # 残血
            print('extra')
            functions.game.attack(2)
            functions.game.attack(2)
            functions.game.attack(1)
            event.fight.boost.clear()
            x = actionextra()
            return x
    if event.fight.end.is_set():  # 结束
        return 0


def end():
    print('end')
    functions.adb.click(500, 500)
    time.sleep(0.5)
    functions.adb.click(500, 500)
    functions.adb.click(500, 500)
    event.fight.end.clear()
    event.fight.boost.clear()
    event.fight.full.clear()


def actionselect(n):  # 选择函数
    event.flag.set()  # 开始子线程
    event.select.start.wait()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    selection(n)  # 选择内容函数

    event.select.go.wait()

    # 队伍选择待写
    go()

    #
    #
    #
    functions.adb.click(1338, 796)  # 出发操作
    event.flag.clear()  # 结束子线程


def go():
    pass


def action(n, style):

    back_stage = threading.Thread(target=backstage, args=())
    back_stage.setDaemon(True)
    back_stage.start()
    while True:

        event.select.flag.set()  # 选择事件开始
        actionselect(n)  # 选择
        event.select.flag.clear()  # 选择事件结束

        event.fight.flag.set()  # 战斗事件开始
        if actionextra():
            fight1(style)  # 操作1
        else:
            end()
            continue
        if actionextra():
            fight2(style)  # 操作2
        else:
            end()
            continue
        if actionextra():
            fight3(style)  # 操作3
        else:
            end()
            continue
        if actionextra():
            print('end error')
        else:
            event.fight.flag.clear()  # 战斗事件结束
            end()


def selection(n):
    #
    #
    #
    if n == 1:
        functions.adb.click(1105, 231)  # 选关1
    elif n == 2:
        functions.adb.click(1105, 426)  # 选关2
    elif n == 3:
        functions.adb.click(1105, 612)  # 选关3
    elif n == 4:
        functions.adb.order('adb shell input swipe 1105 612  1105 420 2500')
        time.sleep(1)
        functions.adb.click(1105, 612)
    elif n == 5:
        functions.adb.order('adb shell input swipe 1105 612  1105 420 2500')
        time.sleep(3)
        functions.adb.order('adb shell input swipe 1105 612  1105 420 2500')
        time.sleep(3)
        functions.adb.click(1105, 612)
    elif n == 'last':
        functions.adb.order('adb shell input swipe 1105 612  1105 256 2500')
        time.sleep(0.5)
        functions.adb.order('adb shell input swipe 1105 612  1105 256 2500')
        functions.adb.click(1105, 682)


# 第一波战斗
def fight1(style):
    print("WAVE 1")
    if style == 1:
        functions.game.skill([2.2])
        functions.game.card(1)
        functions.game.card(1)


# 第二波战斗
def fight2(style):
    print("WAVE 2")
    if style == 1:
        functions.game.skill([2.1])
        functions.game.card(3)
        functions.game.card(2)


# 第三波战斗
def fight3(style):
    print("WAVE 3")
    if style == 1:
        functions.game.attack(1)
        functions.game.boost(2)
        functions.game.card(3)
