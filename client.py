# -*- coding:utf-8 -*-
# Last Change: Wed 17 Oct 2018 16:16:57.
import sys
import socket
import json
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

lidar_datas = list()

px, py = [0 for i in range(360)], [0 for i in range(360)]
length = 0
theta  = 0

start_flag = False

def get_data():
    """ロボットからデータをUDPのソケット通信で受信"""
    global mapping_th, start_flag
    global px, py, length, theta

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 0)
        sock.bind(("0.0.0.0", 8888))

        mapping_th.start()

        cnt = 0
        # try:
        while True:
            if cnt > 359:
                cnt = 0
            res, addr = sock.recvfrom(2048)
            res = res.decode("utf-8")
            res = json.loads(res)

            # px.append(res["x"])
            # py.append(res["y"])

            px[cnt] = res["x"]
            py[cnt] = res["y"]

            length = res["length"]
            theta = res["theta"]
            rad = res["rad"]
            start_flag = res["begin"]
            # print(start_flag)
            cnt += 1


def mapping():
    """LIDARのデータをmatplotlibで描画"""

    global px, py, start_flag, length, theta
    # lock = threading.Lock()

    plt.close("all")
    fig = plt.switch_backend('qt5agg')  # バックエンドをPyQt5に変更
    fig = plt.figure()
    line, = plt.plot(0, marker=".", markersize=2, linestyle="None", color="#7777FF")
    # line, = plt.plot(0, marker=".", linestyle="None", color="#7777FF")
    plt.grid(color="gray")
    plt.xlim([-5000,5000])
    plt.ylim([-5000,5000])
    plt.show(block=False)

    while True:
        # print(start_flag)
        # print(len(px))
        # print("")
        # if start_flag:
        # sys.stdout.flush()
        # if len(px) > 360:
            # x = np.array(px)
            # y = np.array(py)
            line.set_xdata(px)
            line.set_ydata(py)

            fig.canvas.draw()
            fig.canvas.flush_events()

            # px.clear()
            # py.clear()
        # px.append(length * np.cos(np.radians(theta)))
        # py.append(length * np.sin(np.radians(theta)))

if __name__ == "__main__":

    get_data_th = threading.Thread(target=get_data)
    mapping_th  = threading.Thread(target=mapping)
    # mapping_th.setDaemon(True)

    get_data_th.start()
    # mapping_th.start()


    # get_data_th.setDaemon(True)
    # mapping_th.join()

    while True:
        print("")

    get_data_th.join()
