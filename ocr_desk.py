import paddlehub as hub
import cv2
from PIL import ImageGrab
import time
import numpy as np
from tkinter import *

ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")

# 设定提取的文字所存储的位置
log_f = open("./log.txt", mode="w")
global temp
temp = [ ]  # 初始化暂存空间
break_program = False
global left_up
global right_down
left_up = (0,0)
right_down = (1,1)  # 避免空区域，所以初始化右下角的坐标比左上角稍大一些

def save_to_log(data):
    local_t = time.localtime(time.time())  # 本地时间
    t = time.asctime(local_t)  # 转化显示形式

    data_set = set()
    for item in data:
        data_set.add(item[ 'text' ])

    log_f.write(str(t) + str(data_set) + "\n")  # 记录到 log 文件中


def text_detect(temp):

    img = ImageGrab.grab((2 * left_up[ 0 ], 2 * left_up[ 1 ], 2 * right_down[ 0 ], 2 * right_down[ 1 ]))
    # img = ImageGrab.grab() 使用的坐标范围是（1880，800），鼠标监听（1440，400），所以需要*2来换算

    imm = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    result = ocr.recognize_text(images=[ imm ],
                                visualization=False,
                                output_dir='ocr_result')


    # 如果当前画面里出现了文字，并且文字和前以帧不同
    if result[ 0 ][ 'data' ] != [ ]:
        if temp == [ ]:  # 前面的为空，表示现在刚探测到文字，所以要存储
            save_to_log(result[ 0 ][ 'data' ])
        else:  # 前面不为空，要检测是否和前面的文字相同，不同则进行存储
            before_words_set = set()
            this_words_set = set()
            for item in temp:
                before_words_set.add(item[ 'text' ])
            for item in result[ 0 ][ 'data' ]:
                this_words_set.add(item[ 'text' ])
            if this_words_set != before_words_set:
                save_to_log(result[ 0 ][ 'data' ])

    temp = result[ 0 ][ 'data' ]  # 将当前的数据暂存

    # 同步显示文字读取情况
    print(result)
    return temp


# 选定桌面上需要监测的区域
def go():
    global left_up
    global right_down
    if root.winfo_y()==0:
        left_up = (root.winfo_x(), root.winfo_y())
    else:
        left_up = (root.winfo_x(), root.winfo_y()+20)  # 修正，对话框的标题部分不设置为探测区域
    right_down = (root.winfo_x() + root.winfo_width(),
                  root.winfo_y() + root.winfo_height()+20)

    global temp
    temp = text_detect(temp)
    root.after(1, go)

root = Tk()
root.geometry("300x200+100+50")
label1 = Label(root)
label1.pack(expand=YES)
go()
root.attributes("-alpha",0.4)
root.title("把窗口覆盖到想要探测的区域即可！")
root.mainloop()





