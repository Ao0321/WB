"""
版本号：0.1.0
最后编辑时间：2022年3月24日20:49:38
"""
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from main import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox, QSystemTrayIcon, QApplication, QMenu, QAction, qApp, QMenu
from pykeyboard import PyKeyboard
from PyQt5.QtCore import QCoreApplication
import keyboard
import socket
import qrcode
import os
import threading
import sys
import re
import wmi

w = wmi.WMI()
list_wmi = []
# 获取本机电脑名
myname = socket.getfqdn(socket.gethostname())
# 获取本机ip
myaddr = socket.gethostbyname(myname)
# 按键绑定字典
Py_Key_Dictionary = {'0101': 'w', '0102': 'a', '0103': 's', '0104': 'd', '0105': 'u', '0106': 'k', '0107': 'h',
                     '0108': 'j', '0201': 'w', '0202': 's', '0203': 'k', '0204': 'a'}
# Py_Key_Dictionary = {}
# Py_Key_Dictionary_initial = {'0101': 'w', '0102': 'c', '0103': 's', '0104': 'v', '0105': 'u', '0106': 'd', '0107': 'a',
#                              '0108': 'j', '0201': 'w', '0202': 's', '0203': 'd', '0204': 'a'}
# 手机ip列表
cellphone_ip_List = ['0.0.0.0']
cellphone_ip_Dictionary = {'0.0.0.0': '无连接'}
keyboard_monitoring_key = 'esc'


class MyQLabel(QtWidgets.QLabel):
    # 自定义信号, 注意信号必须为类属性
    # button_clicked_signal = QtCore.pyqtSignal()
    label_mouse_release = QtCore.pyqtSignal()
    label_enter = QtCore.pyqtSignal()
    label_leave = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MyQLabel, self).__init__(parent)

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标点击松开事件
        self.label_mouse_release.emit()

    def enterEvent(self, QMouseEvent):  # 鼠标进入控件事件
        self.label_enter.emit()

    def leaveEvent(self, QMouseEvent):  # 鼠标进入控件事件
        self.label_leave.emit()

    def label_mouse_releaseconnect(self, func):  # 可在外部与槽函数连接
        self.label_mouse_release.connect(func)

    def label_enter_connect(self, func):  # 可在外部与槽函数连接
        self.label_enter.connect(func)

    def label_leave_connect(self, func):  # 可在外部与槽函数连接
        self.label_leave.connect(func)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow, QtWidgets.QSystemTrayIcon):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QIcon('images/WB_logo.png'))

        self.setupUi(self)
        self.image_00 = QPixmap()
        self.image_00.load('images/wx.png')
        new_image = self.image_00.scaled(120, 120)
        self.label_00.setPixmap(new_image)
        # self.label_00.setPixmap(QtGui.QPixmap('192.168.1.112.png'))

        self.label_17 = MyQLabel(self.tab_2)
        self.label_17.setGeometry(QtCore.QRect(120, 171, 41, 68))
        self.label_17.setText("")
        self.label_17.setPixmap(QtGui.QPixmap("images/上箭头.png"))
        self.label_17.setScaledContents(True)
        self.label_17.setObjectName("label_17")
        self.label_18 = MyQLabel(self.tab_2)
        self.label_18.setGeometry(QtCore.QRect(151, 230, 68, 41))
        self.label_18.setText("")
        self.label_18.setPixmap(QtGui.QPixmap("images/右箭头.png"))
        self.label_18.setScaledContents(True)
        self.label_18.setObjectName("label_18")
        self.label_19 = MyQLabel(self.tab_2)
        self.label_19.setGeometry(QtCore.QRect(63, 230, 68, 41))
        self.label_19.setText("")
        self.label_19.setPixmap(QtGui.QPixmap("images/左箭头.png"))
        self.label_19.setScaledContents(True)
        self.label_19.setObjectName("label_19")
        self.label_20 = MyQLabel(self.tab_2)
        self.label_20.setGeometry(QtCore.QRect(120, 260, 41, 68))
        self.label_20.setText("")
        self.label_20.setPixmap(QtGui.QPixmap("images/下箭头.png"))
        self.label_20.setScaledContents(True)
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.tab_2)
        self.label_21.setGeometry(QtCore.QRect(120, 229, 41, 41))
        self.label_21.setText("")
        self.label_21.setPixmap(QtGui.QPixmap("images/方向键中心.png"))
        self.label_21.setScaledContents(True)
        self.label_21.setObjectName("label_21")
        self.label_26 = MyQLabel(self.tab_2)
        self.label_26.setGeometry(QtCore.QRect(543, 163, 55, 55))
        self.label_26.setText("")
        self.label_26.setPixmap(QtGui.QPixmap("images/A.png"))
        self.label_26.setScaledContents(True)
        self.label_26.setObjectName("label_26")
        self.label_27 = MyQLabel(self.tab_2)
        self.label_27.setGeometry(QtCore.QRect(604, 223, 55, 55))
        self.label_27.setText("")
        self.label_27.setPixmap(QtGui.QPixmap("images/B.png"))
        self.label_27.setScaledContents(True)
        self.label_27.setObjectName("label_27")
        self.label_28 = MyQLabel(self.tab_2)
        self.label_28.setGeometry(QtCore.QRect(484, 224, 55, 55))
        self.label_28.setText("")
        self.label_28.setPixmap(QtGui.QPixmap("images/C.png"))
        self.label_28.setScaledContents(True)
        self.label_28.setObjectName("label_28")
        self.label_29 = MyQLabel(self.tab_2)
        self.label_29.setGeometry(QtCore.QRect(543, 283, 55, 55))
        self.label_29.setText("")
        self.label_29.setPixmap(QtGui.QPixmap("images/D.png"))
        self.label_29.setScaledContents(True)
        self.label_29.setObjectName("label_29")
        self.setFixedSize(self.width(), self.height())
        self.run()

    def run(self):
        self.PC_information()
        self.QR_code()
        # self.text_Edit()
        self.pc_wmi()
        self.login()
        self.thread_1 = threading.Thread(target=self.receive_udp_connection)
        self.thread_1.start()
        self.textEdit.setReadOnly(True)
        self.pushButton.clicked.connect(self.close_show)
        self.pushButton_2.clicked.connect(self.attention_show)
        # self.label_17.setToolTip('shang')
        self.label_17.label_enter_connect(lambda: self.key_enter('0101'))
        self.label_18.label_enter_connect(lambda: self.key_enter('0104'))
        self.label_19.label_enter_connect(lambda: self.key_enter('0102'))
        self.label_20.label_enter_connect(lambda: self.key_enter('0103'))
        self.label_26.label_enter_connect(lambda: self.key_enter('0105'))
        self.label_27.label_enter_connect(lambda: self.key_enter('0106'))
        self.label_28.label_enter_connect(lambda: self.key_enter('0107'))
        self.label_29.label_enter_connect(lambda: self.key_enter('0108'))
        self.label_17.label_leave_connect(self.key_leave)
        self.label_18.label_leave_connect(self.key_leave)
        self.label_19.label_leave_connect(self.key_leave)
        self.label_20.label_leave_connect(self.key_leave)
        self.label_26.label_leave_connect(self.key_leave)
        self.label_27.label_leave_connect(self.key_leave)
        self.label_28.label_leave_connect(self.key_leave)
        self.label_29.label_leave_connect(self.key_leave)
        self.label_17.label_mouse_releaseconnect(lambda: self.mouse_Release_Event('0101'))
        self.label_18.label_mouse_releaseconnect(lambda: self.mouse_Release_Event('0104'))
        self.label_19.label_mouse_releaseconnect(lambda: self.mouse_Release_Event('0102'))
        self.label_20.label_mouse_releaseconnect(lambda: self.mouse_Release_Event('0103'))
        self.label_26.label_mouse_releaseconnect(lambda: self.mouse_Release_Event('0105'))
        self.label_27.label_mouse_releaseconnect(lambda: self.mouse_Release_Event('0106'))
        self.label_28.label_mouse_releaseconnect(lambda: self.mouse_Release_Event('0107'))
        self.label_29.label_mouse_releaseconnect(lambda: self.mouse_Release_Event('0108'))
        # 此处编写业务逻辑代码

    def attention_show(self):
        """注意事项"""
        attention_QB = QMessageBox()
        attention_QB.setIconPixmap(QPixmap('images/WB_logo.png'))
        attention_QB.setWindowIcon(QIcon('images/WB_logo.png'))
        attention_QB.setWindowTitle('虽然没啥用')
        attention_QB.setText('1.本软件不允许任何人、任何组织以任何目的、以任何形式用作商业或非法活动。\n2.如需转载，请先获得作者(Ao0321)同意,'
                             '请尊重作者劳动成果。\n3.本软件只在github发布，从其他网站获取的资源均为盗版。\n4.该软件版本为'
                             '0.1.0试运行版本，因本人技术有限，所有bug有点多，还请大佬不吝赐教。\n5.最终解释权归作(Ao0321)者所有。\n6.我想'
                             '想还有啥···')
        attention_QB.setStandardButtons(QMessageBox.Ok | QMessageBox.Close)
        attention_QB.exec()

    def key_enter(self, key_i):
        """鼠标进入或悬停；如果为字典空，说明无连接，提示连接（0.1.0版本使用默认字典）"""
        if Py_Key_Dictionary == {}:
            # print('null')
            font = QtGui.QFont()
            font.setFamily("Arial")  # 括号里可以设置成自己想要的其它字体
            font.setPointSize(12)  # 括号里的数字可以设置成自己想要的字体大小
            self.label_31.setFont(font)
            self.label_31.setText('请先连接')

        else:
            # print(Py_Key_Dictionary)
            # print(key_i)
            key = Py_Key_Dictionary[key_i]
            font = QtGui.QFont()
            font.setFamily("Arial")  # 括号里可以设置成自己想要的其它字体
            font.setPointSize(12)  # 括号里的数字可以设置成自己想要的字体大小
            self.label_31.setFont(font)
            self.label_31.setText(key + '  键')

    def key_leave(self):
        """当鼠标离开在图片上时"""
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_31.setFont(font)
        self.label_31.setText('单击按钮更新绑定')

    # def mouse_Release_Event_null(self, key_i):
    #     if Py_Key_Dictionary == {}:
    #         QMessageBox.information(self, '连接', '请先连接手机', QMessageBox.Ok)
    #     else:
    #         self.mouse_Release_Event(self, key_i)

    def mouse_Release_Event(self, key_i):
        """当鼠标点击时，弹出窗口并监听一次键盘输入"""

        def keyboard_monitoring():
            global keyboard_monitoring_key
            keyboard_monitoring_key = keyboard.read_key()
            if len(keyboard_monitoring_key) != 'esc':
                listen_QB.setText('是否绑定' + keyboard_monitoring_key + '键')
            else:
                pass

        global keyboard_monitoring_key
        thread_2 = threading.Thread(target=keyboard_monitoring)
        thread_2.start()
        listen_QB = QMessageBox()
        # listen_QB.setIconPixmap(QPixmap('WB_logo.png'))
        listen_QB.setWindowIcon(QIcon('images/WB_logo.png'))
        listen_QB.setWindowTitle('按键绑定')
        listen_QB.setText('请在键盘上按下需要绑定的按钮')
        listen_QB.setStandardButtons(QMessageBox.Yes | QMessageBox.Close)
        button_key = listen_QB.exec()
        if thread_2.isAlive():
            pykey_board = PyKeyboard()
            pykey_board.press_key(pykey_board.escape_key)
            thread_2.join()
        else:
            pass
        if button_key == QMessageBox.Yes and keyboard_monitoring_key != 'esc':
            global Py_Key_Dictionary
            Py_Key_Dictionary[key_i] = keyboard_monitoring_key
            # information_txt = open("information\\%s.txt" % cellphone_ip_List[-1], "w+")
            # Py_Key_Dictionary_js = json.dumps(Py_Key_Dictionary)
            # information_txt.write(Py_Key_Dictionary_js)
            # # 关闭打开的文件
            # information_txt.close()
            # file = open("information\\%s.txt" % cellphone_ip_List[-1], 'r')
            # js = file.read()
            # Py_Key_Dictionary = json.loads(js)
            # file.close()
        else:
            pass

    def closeEvent(self, event):
        """点击窗口叉号触发，目的是终止udp无限循环，使线程正常关闭"""
        # 向本机发送接收udp通信信号
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        PORT = 8848
        msg = 'stop'
        msg = msg.encode("UTF-8")
        server_address = (myaddr, PORT)  # 接收方 服务器的ip地址和端口号
        client_socket.sendto(msg, server_address)  # 将msg内容发送给指定接收方
        qApp.quit()
        # event.accept()

    def PC_information(self):
        """在窗口上显示电脑信息"""
        self.label_7.setText(myname)
        self.label_8.setText(myaddr)

    def login(self):
        """点击链接后触发，显示手机ipcellphone_ip_List[-1];手机型号:name"""
        sj_ip = cellphone_ip_List[-1]
        sj_name = cellphone_ip_Dictionary[sj_ip]
        if sj_ip:
            self.label_3.setText(sj_ip)
            self.label_4.setText(sj_name)
            # self.pushButton_2.setEnabled(True)
        else:
            pass

    def QR_code(self):
        """生成包含电脑ip的二维码，保存到images文件夹下"""
        if os.path.exists('images/%s.png' % myaddr):
            self.label_10.setPixmap(QtGui.QPixmap('images/%s.png' % myaddr))
        else:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(myaddr)
            qr.make(fit=True)
            img = qr.make_image()
            img.save('images/%s.png' % myaddr)
            self.label_10.setPixmap(QtGui.QPixmap('images/%s.png' % myaddr))

    def text_Edit(self):
        """多行文本框"""
        # self.textEdit.append("------------------------------------------")
        # print('mousePressEvent')

    def Dialog_box(self, cellphone_ip_0):
        """连接请求弹窗（0.1.0版本问题：次线程不允许使用QMessageBox，使用System_tray.showMessage替代，并默认连接"""
        QMB_YN = QMessageBox.question(self, '连接', '收到来自%s的连接请求' % cellphone_ip_0, QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)
        print(QMB_YN)
        return QMB_YN

    def receive_udp_connection(self):
        """udp循环，当收到stop的信息终止循环
        stop：停止信号
        00000：请求连接信号"""
        # print("receive_udp_data")
        # 创建套接字
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 绑定一个本地信息
        localaddr = (myaddr, 8848)
        # 绑定自己电脑IP和port
        udp_socket.bind(localaddr)
        while True:
            recv_data = udp_socket.recvfrom(64)
            # recv_data存储元组（接收到的数据，（发送方的ip,port））
            recv_msg = recv_data[0]
            # 信息内容
            send_addr = recv_data[1]
            # 信息地址
            udp_data = recv_msg.decode("UTF-8")
            str_ip = str(send_addr)
            str_ip = re.findall(r"'(.*)'", str_ip)
            # print("信息来自:%s 内容是:%s" % (str_ip[0], recv_msg.decode("UTF-8")))
            # 打印接收到的数据

            if udp_data == 'stop':
                # print(udp_data)
                break
            elif udp_data[0:5] == '00000':
                print('self.Dialog_box(str_ip[0])')
                # QMB_YN = self.Dialog_box(str_ip[0])
                # if QMB_YN == QMessageBox.Yes:
                if True:
                    System_tray.showMessage('通知', '已连接到→%s' % str_ip[0])
                    print('yes')
                    cellphone_ip_List.append(str_ip[0])
                    cellphone_ip_Dictionary[str_ip[0]] = udp_data[5:]
                    # if os.path.isfile("information\\%s.txt" % str_ip[0]):
                    #     file = open("information\\%s.txt" % str_ip[0], 'r')
                    #     js = file.read()
                    #     global Py_Key_Dictionary
                    #     Py_Key_Dictionary = json.loads(js)
                    #     print(Py_Key_Dictionary)
                    #     file.close()
                    # else:
                    #     information_txt = open("information\\%s.txt" % str_ip[0], "w+")
                    #     print(os.path.isfile("information\\%s.txt" % str_ip[0]))
                    #     Py_Key_Dictionary_js = json.dumps(Py_Key_Dictionary_initial)
                    #     information_txt.write(Py_Key_Dictionary_js)
                    #     js = information_txt.read()
                    #     Py_Key_Dictionary = json.loads(js)
                    #     # 关闭打开的文件
                    #     information_txt.close()
                    self.login()
                # else:
                #     # print('no')
                #     break
            elif cellphone_ip_List[-1] == str_ip[0]:
                self.receive_udp_data(udp_data)
            else:
                pass
        # print("close")
        udp_socket.close()

    def receive_udp_data(self, udp_data):
        """udp数据处理，调用按键绑定字典"""
        udp_data_1_5 = udp_data[1:5]
        key_data = Py_Key_Dictionary[udp_data_1_5]
        # print(key_data)
        if len(key_data) == 1:
            self.Py_Key(udp_data, key_data)
        else:
            self.Py_Key_Special(udp_data, key_data)

    def Py_Key_Special(self, udp_data, key_data):
        """特殊字符和按键响应"""
        py_key_special = PyKeyboard()
        if udp_data[0] == '1':
            if key_data == 'tab':
                py_key_special.press_key(py_key_special.tab_key)
            elif key_data == 'shift':
                py_key_special.press_key(py_key_special.shift_l_key)
            elif key_data == 'right shift':
                py_key_special.press_key(py_key_special.shift_r_key)
            elif key_data == 'caps lock':
                py_key_special.press_key(py_key_special.caps_lock_key)
            elif key_data == 'ctrl':
                py_key_special.press_key(py_key_special.control_l_key)
            elif key_data == 'right ctrl':
                py_key_special.press_key(py_key_special.control_r_key)
            elif key_data == 'left windows':
                py_key_special.press_key(py_key_special.windows_l_key)
            elif key_data == 'right windows':
                py_key_special.press_key(py_key_special.windows_r_key)
            elif key_data == 'alt':
                py_key_special.press_key(py_key_special.alt_l_key)
            elif key_data == 'right alt':
                py_key_special.press_key(py_key_special.alt_r_key)
            elif key_data == 'space':
                py_key_special.press_key(py_key_special.space_key)
            elif key_data == 'backspace':
                py_key_special.press_key(py_key_special.backspace_key)
            elif key_data == 'enter':
                py_key_special.press_key(py_key_special.enter_key)
            elif key_data == 'up':
                py_key_special.press_key(py_key_special.up_key)
            elif key_data == 'left':
                py_key_special.press_key(py_key_special.left_key)
            elif key_data == 'right':
                py_key_special.press_key(py_key_special.right_key)
            elif key_data == 'down':
                py_key_special.press_key(py_key_special.down_key)
            else:
                pass

        elif udp_data[0] == '0':
            if key_data == 'tab':
                py_key_special.release_key(py_key_special.tab_key)
            elif key_data == 'shift':
                py_key_special.release_key(py_key_special.shift_l_key)
            elif key_data == 'right shift':
                py_key_special.release_key(py_key_special.shift_r_key)
            elif key_data == 'caps lock':
                py_key_special.release_key(py_key_special.caps_lock_key)
            elif key_data == 'ctrl':
                py_key_special.release_key(py_key_special.control_l_key)
            elif key_data == 'right ctrl':
                py_key_special.release_key(py_key_special.control_r_key)
            elif key_data == 'left windows':
                py_key_special.release_key(py_key_special.windows_l_key)
            elif key_data == 'right windows':
                py_key_special.release_key(py_key_special.windows_r_key)
            elif key_data == 'alt':
                py_key_special.release_key(py_key_special.alt_l_key)
            elif key_data == 'right alt':
                py_key_special.release_key(py_key_special.alt_r_key)
            elif key_data == 'space':
                py_key_special.release_key(py_key_special.space_key)
            elif key_data == 'backspace':
                py_key_special.release_key(py_key_special.backspace_key)
            elif key_data == 'enter':
                py_key_special.release_key(py_key_special.enter_key)
            elif key_data == 'up':
                py_key_special.release_key(py_key_special.up_key)
            elif key_data == 'left':
                py_key_special.release_key(py_key_special.left_key)
            elif key_data == 'right':
                py_key_special.release_key(py_key_special.right_key)
            elif key_data == 'down':
                py_key_special.release_key(py_key_special.down_key)
        else:
            pass

    def Py_Key(self, udp_data, key_data):
        """
        首位数字0和1
        0:松开
        1：按下
        """
        py_key = PyKeyboard()
        if udp_data[0] == '1':
            py_key.press_key(key_data)
        elif udp_data[0] == '0':
            py_key.release_key(key_data)
        else:
            pass

    def pc_wmi(self):
        """电脑硬件检测"""
        for BIOSs in w.Win32_ComputerSystem():
            list_wmi.append("电脑名称: %s" % BIOSs.Caption)
            list_wmi.append("使 用 者: %s" % BIOSs.UserName)
        for address in w.Win32_NetworkAdapterConfiguration(ServiceName="e1dexpress"):
            list_wmi.append("IP地址: %s" % address.IPAddress[0])
            list_wmi.append("MAC地址: %s" % address.MACAddress)
        for BIOS in w.Win32_BIOS():
            list_wmi.append("使用日期: %s" % BIOS.Description)
            list_wmi.append("主板型号: %s" % BIOS.SerialNumber)
        for processor in w.Win32_Processor():
            list_wmi.append("CPU型号: %s" % processor.Name.strip())
        for memModule in w.Win32_PhysicalMemory():
            totalMemSize = int(memModule.Capacity)
            list_wmi.append("内存厂商: %s" % memModule.Manufacturer)
            list_wmi.append("内存型号: %s" % memModule.PartNumber)
            list_wmi.append("内存大小: %.2fGB" % (totalMemSize / 1024 ** 3))
        for disk in w.Win32_DiskDrive():
            diskSize = int(disk.size)
            list_wmi.append("磁盘名称: %s" % disk.Caption)
            list_wmi.append("磁盘大小: %.2fGB" % (diskSize / 1024 ** 3))
        for xk in w.Win32_VideoController():
            list_wmi.append("显卡名称: %s" % xk.name)
        for i in list_wmi:
            self.textEdit.append(i)

    def close_show(self):
        self.hide()


def act(reason):
    """设置托盘图标对鼠标点击的响应"""
    # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
    if reason == 2 or reason == 3:
        mainWindow.show()
    # print("系统托盘的图标被点击了")


def main_quit():
    """结束信号"""
    # 向本机发送接收udp通信信号
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    PORT = 8848
    msg = 'stop'
    msg = msg.encode("UTF-8")
    server_address = (myaddr, PORT)  # 接收方 服务器的ip地址和端口号
    client_socket.sendto(msg, server_address)  # 将msg内容发送给指定接收方
    QCoreApplication.instance().quit()
    # 在应用程序全部关闭后，TrayIcon其实还不会自动消失，
    # 直到你的鼠标移动到上面去后，才会消失，
    # 这是个问题，（如同你terminate一些带TrayIcon的应用程序时出现的状况），
    # 这种问题的解决我是通过在程序退出前将其setVisible(False)来完成的。
    System_tray.setVisible(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # 关闭所有窗口,也不关闭应用程序
    QApplication.setQuitOnLastWindowClosed(False)
    mainWindow = MainWindow()
    mainWindow.show()
    # 在系统托盘处显示图标
    System_tray = QSystemTrayIcon(mainWindow)
    System_tray.setIcon(QIcon('images/WB_logo.png'))
    # 设置系统托盘图标的菜单
    a1 = QAction('&显示(Show)', triggered=mainWindow.show)
    a2 = QAction('&退出(Exit)', triggered=main_quit)
    tpMenu = QMenu()
    tpMenu.addAction(a1)
    tpMenu.addAction(a2)
    System_tray.setContextMenu(tpMenu)
    System_tray.show()
    System_tray.activated.connect(act)
    sys.exit(app.exec_())
