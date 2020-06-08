# -*- coding:utf-8 -*-
import sys
from time import sleep, time
import game_log
import cv2
from adb import click, swipe, click_s
from image import cut_image, mathc_img
from sub import get_img
from gameerror import OvertimeError
from universe import search
from universe import remove_same

LV = cv2.imread(sys.path[0] + "\\IMG\\lv.jpg", 0)  # 远征检测
MARCHPAGE = cv2.imread(sys.path[0] + "\\IMG\\marchpage.jpg")
DONE = cv2.imread(sys.path[0] + "\\IMG\\done.jpg", 0)  # 远征完成
WORKING = cv2.imread(sys.path[0] + "\\IMG\\working.jpg", 0)  # 远征中
YES = cv2.imread(sys.path[0] + "\\IMG\\yes.jpg", 0)  # 决定
ADD = cv2.imread(sys.path[0] + "\\IMG\\add.jpg", 0)  # 远征加人物

BOOK = cv2.imread(sys.path[0] + "\\IMG\\l1.jpg", 0)
GOLD1 = cv2.imread(sys.path[0] + "\\IMG\\l2.jpg", 0)
CARD = cv2.imread(sys.path[0] + "\\IMG\\l3.jpg", 0)
POWER = cv2.imread(sys.path[0] + "\\IMG\\l4.jpg", 0)
GOLD2 = cv2.imread(sys.path[0] + "\\IMG\\l5.jpg", 0)

ADDGIRL = cv2.imread(sys.path[0] + "\\IMG\\addgirl.jpg", 0)

MARCHDONE = cv2.imread(sys.path[0] + "\\IMG\\marchdone.jpg", 0)
STEP = 0.5

OFFLINE = cv2.imread(sys.path[0] + "\\IMG\\offline.jpg")


def offlinefind(img=get_img):
    """断网判定"""
    if search(390, 485, 626, 960, img, OFFLINE, 0.9):
        click(963, 632)  # 断网重连操作
        game_log.warning("offline")
        sleep(10)
        return True
    else:
        return False


FIRST = cv2.imread(sys.path[0] + "\\IMG\\first.jpg")  # 开始界面


def firstpagefind(img=get_img):
    "初始界面判断"
    return search(839, 884, 12, 774, img, FIRST, 0.5)


def marchfind(img=get_img):
    """远征界面判断"""
    return search(13, 48, 89, 231, img, MARCHPAGE, 0.8)


MARCH = cv2.imread(sys.path[0] + "\\IMG\\march.jpg")  # 远征红点


def mainpage_marchfind(img=get_img):
    """主界面远征判断"""
    return search(480, 502, 1415, 1445, img, MARCH, 0.8)


MAIN = cv2.imread(sys.path[0] + "\\IMG\\main.jpg")  # 主界面


def mainpagefind(img=get_img):
    """主界面判断"""
    return search(696, 737, 1424, 1521, img, MAIN, 0.8)


BUILDING = cv2.imread(sys.path[0] + "\\IMG\\building.jpg")


def mainpage_buildingfind(img=get_img):
    """设施红点判断"""
    return search(754, 770, 880, 900, img, BUILDING, 0.8)


SKILLROOM = cv2.imread(sys.path[0] + "\\IMG\\skillpoint.jpg")


def mainpage_building_skill_room_point(img=get_img):
    """道场红点判断"""
    return search(238, 260, 1418, 1430, img, SKILLROOM, 0.8)


SKILLPOINT = cv2.imread(sys.path[0] + "\\IMG\\skillyes.jpg")


def mainpage_building_skill_room_find(img=get_img):
    """道场确定判断"""
    return search(608, 656, 914, 1026, img, SKILLPOINT, 0.8)


M3 = cv2.imread(sys.path[0] + "\\IMG\\3m.jpg")


def fullfind(img=get_img):
    """三个远征满了判断"""
    return search(812, 854, 122, 146, img, M3, 0.75)


EXP = cv2.imread(sys.path[0] + "\\IMG\\150exp.jpg", 0)

TEAM4 = cv2.imread(sys.path[0] + "\\IMG\\4team.jpg")
TEAM5 = cv2.imread(sys.path[0] + "\\IMG\\5team.jpg")


def number_find(img=get_img):
    """远征个数判断"""
    if search(761, 781, 1553, 1564, img, TEAM4, 0.8):
        return 4
    elif search(632, 646, 1552, 1564, img, TEAM5, 0.8):
        return 5
    else:
        up_swipe()
        return number_find()


def skill_room():
    """道场续书"""
    # 设施有红点吗
    if not mainpage_buildingfind():
        return
    click(800, 800)
    sleep(5)
    # 道场有红点吗
    if not mainpage_building_skill_room_point():
        click(792, 772)
        return
    else:
        click(1316, 464)
    start = time()
    while 1:
        sleep(5)
        x, y = mathc_img(get_img(), EXP, 0.9)
        if time() - start > 30:
            break
            # raise OvertimeError("skill_room")
        elif mainpage_building_skill_room_find():
            click(1342, 762)
            sleep(3)
            continue
        elif x:
            x, y = remove_same(x, y)
            click(x[1], y[1] + 20, 2)
            click(1322, 764, 1)
            click(992, 632, 1)
            sleep(3)
            continue


def down_swipe():
    """下滑"""
    swipe(1557, 261, 1560, 615, 200)
    sleep(1)


def up_swipe():
    """上滑"""
    swipe(1560, 615, 1557, 261, 200)
    sleep(1)


def go_to_main():
    """进入远征界面"""
    click(1387, 543)
    sleep(3)
    start = time()
    while 1:
        if time() - start > 60:
            raise OvertimeError("go")
        marchfind()
        offlinefind()
        if marchfind():
            break
        sleep(STEP * 2)


def exit_to_main():
    """返回主界面"""
    click_s(1559, 35)
    start = time()
    while 1:
        if time() - start > 60:
            raise OvertimeError("exit")
        offlinefind()
        if mainpagefind():
            break
        if time() - start > 10:
            click_s(1559, 35)
            sleep(5)
        sleep(STEP * 2)


class March:
    """远征类"""

    def __init__(self, img, number):
        """初始化远征

        :img:远征的小图
        :number:远征编号
        :mode: 模式 材料、灵力、钱、两种结晶
        :name: 远征名字，选择合适队员用
        :situation: 情况 进行中 结束 可用
        """

        def get_mode(img):
            """获取类别"""
            x, y = mathc_img(img, BOOK, 0.8)
            x, y = remove_same(x, y)
            # print(x)
            string = "nothing"
            if x:
                string = "book"  # 指南书
            x, y = mathc_img(img, GOLD1, 0.9)
            x, y = remove_same(x, y)
            # print(x)
            if x:
                string = "gold1"  # 封结晶
            x, y = mathc_img(img, GOLD2, 0.9)
            x, y = remove_same(x, y)
            # print(x)
            if x:
                string = "gold2"  # 神结晶
            x, y = mathc_img(img, CARD, 0.8)
            x, y = remove_same(x, y)
            # print(x)
            if x:
                string = "card"  # 绘扎
            x, y = mathc_img(img, POWER, 0.8)
            x, y = remove_same(x, y)
            # print(x)
            if x:
                string = "power"  # 灵力
            return string

        def get_name(img):
            """获取名字"""
            return 1

        def get_situation(img):
            """获取状态"""
            x1, y1 = mathc_img(img, DONE, 0.9)
            x2, y2 = mathc_img(img, WORKING, 0.9)
            if x1:
                return "done"  # 状态为完成
            elif x2:
                return "doing"  # 状态为进行中
            else:
                return "available"  # 状态为可选

        # cv2.imwrite('march%d.jpg' % number, img)
        self.img = img
        self.number = number
        self.mode = get_mode(img)
        self.name = get_name(img)
        self.situation = get_situation(img)
        # print(number, self.mode, self.situation)

    @classmethod
    def initialize(cls, get_img=get_img):
        """初始化

        需要处在远征界面
        """

        def cut(img):
            """切出每个远征的小图"""
            # 找到所以基准点
            x, y = mathc_img(img, LV, 0.7)
            x, y = remove_same(x, y)
            # 图片切片
            piclist = []
            for num in range(0, len(x)):
                y0 = y[num] - 34
                y1 = y[num] + 186
                x0 = x[num] - 296
                x1 = x[num] + 907
                piclist.append(cut_image(y0, y1, x0, x1, img))
            return piclist

        # 普通远征
        click(73, 179)
        up_swipe()
        sleep(1)
        piclist = cut(get_img())
        piclist.pop()
        down_swipe()

        sleep(1)
        pic2list = cut(get_img())
        pic2list.pop(0)
        piclist = piclist + pic2list
        sleep(1)
        march_list = []
        for number in range(0, 5):
            march_list.append(cls(piclist[number], number))
        # 特殊远征
        click(73, 329)
        sleep(1)
        up_swipe()
        sleep(1)
        piclist = cut(get_img())
        if piclist:
            # 限时远征少于3个，一次搞定
            if len(piclist) <= 3:
                for number in range(0, len(piclist)):
                    march_list.append(cls(piclist[number], number + 5))
            # 限时远征多于3个
            else:
                # 限时远征个数判断
                n = number_find()
                piclist.pop()
                down_swipe()
                sleep(1)
                pic2list = cut(get_img())
                if n == 5:
                    pic2list.pop(0)
                if n == 4:
                    pic2list.pop(0)
                    pic2list.pop(0)
                piclist = piclist + pic2list
                for number in range(0, len(piclist)):
                    march_list.append(cls(piclist[number], number + 5))
        return march_list[0:9]

    def send(available_list, modelist):
        """发远征"""

        def select_player():
            # 选人
            start = time()
            while 1:
                if time() - start > 60:
                    raise OvertimeError("select_player1")
                x, y = mathc_img(get_img(), ADDGIRL, 0.8)
                x, y = remove_same(x, y)
                if x:
                    click(x[0], y[0])
                    break
            # 确定
            start = time()
            while 1:
                if time() - start > 60:
                    raise OvertimeError("select_player2")
                x, y = mathc_img(get_img(), YES, 0.8)
                x, y = remove_same(x, y)
                if x:
                    click(x[0], y[0])
                    break
            sleep(2)
            click(75, 186)
            up_swipe()

        def send_done(march):
            """做远征"""
            num = march.number + 1
            # print(num)
            click(75, 186)
            up_swipe()
            # 普通远征
            if num == 1:
                click(576, 207)
                return
            elif num == 2:
                click(560, 440)
                return
            elif num == 3:
                click(599, 666)
                return
            else:
                down_swipe()
            if num == 4:
                click(846, 520)
                return
            elif num == 5:
                click(866, 762)
                return
            # 限时远征 前三个
            else:
                click(72, 336)
            if num == 6:
                click(576, 207)
                return
            elif num == 7:
                click(560, 440)
                return
            elif num == 8:
                click(599, 666)
                return
            else:
                down_swipe()
            # 限时远征 后三个
            if num == 9:
                click(570, 306)
                return
            elif num == 10:
                click(600, 540)
                return
            elif num == 11:
                click(756, 770)
                return

        # 反转list
        available_list.reverse()
        # 按模式list的顺序发远征
        for string in modelist:
            # 按先限时后普通的顺序选择远征
            for march in available_list:
                # 三个远征满了就返回
                if fullfind():
                    return
                # march 必须为可用 且为当前选择的mode
                if march.situation == "available" and string in march.mode:
                    send_done(march)
                    select_player()
                    march.situation = "doing"
                sleep(1)

    def receive():
        def receive_done_sub(get_img=get_img):
            """收远征完成"""
            sleep(1)
            for num in range(0, 3):
                # 找完成的远征
                x, y = mathc_img(get_img(), DONE, 0.9)
                x, y = remove_same(x, y)
                # 找到可以收的远征
                if x:
                    game_log.info("RECEIVE")
                    click(x[0], y[0])
                    x = []
                    y = []
                    sleep(1)
                    # 找MARCHDONE
                    start = time()
                    while 1:
                        if time() - start > 60:
                            raise OvertimeError("receive1")
                        x, y = mathc_img(get_img(), MARCHDONE, 0.9)
                        if x:
                            x = []
                            y = []
                            break
                        sleep(STEP * 2)
                    # 在回到远征界面前一直点
                    start = time()
                    while 1:
                        if time() - start > 60:
                            raise OvertimeError("receive2")
                        if marchfind():
                            break
                        click(792, 818)
                        sleep(2)
                # 没远征可收
                else:
                    return

        def receive_done_main():
            """收远征"""

            sleep(5)
            receive_done_sub()
            down_swipe()
            receive_done_sub()
            click(73, 329)
            receive_done_sub()
            down_swipe()
            receive_done_sub()

        exit_to_main()
        go_to_main()
        receive_done_main()

    def start(sel="all"):
        """远征全家桶"""
        try:
            exit_to_main()
            # 道场续书
            skill_room()
            # 收远征
            March.receive()
            if sel == "receive":
                return
            # 初始化
            march_list = March.initialize()
            # 远征优先级
            modelist = ["gold2", "gold1", "power", "card", "book", "nothing"]
            # 做远征
            March.send(march_list, modelist)
            game_log.info("march done")
            exit_to_main()
            click(1472, 717)
            sleep(3)
        except OvertimeError as err:
            game_log.error(err.type)
            March.start()


if __name__ == "__main__":
    pass
