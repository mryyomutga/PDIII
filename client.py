# -*- coding:utf-8 -*-
# Last Change: Mon 01 Oct 2018 09:27:44.
import sys
import socket
import json
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
import concurrent.futures
# from collections import OrderedDict as Dict
import csv

success_recv_data = False  # 接続成功フラグ
# data = {"begin":False, "theta":0, "length":0}        # LIDARデータ
lidar_datas = list()
queue = list()


get_data_th = threading.Thread(target=get_data)
# mapping_th  = threading.Thread(target=mapping)
# print_data_th = threading.Thread(target=print_data)

def get_data():
    """ロボットからデータをUDPのソケット通信で受信"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 0)
        sock.bind(("0.0.0.0", 8888))
        print(sock)

        # print_data_th.setDaemon(True)
        # print_data_th.start()

        try:
            while True:
                res, addr = sock.recvfrom(2048)
                res = res.decode("utf-8")
                res = json.loads(res)
                # print(res, type(res))
                lidar_datas.append(np.array([res["begin"], res["theta"], res["length"]]))
                queue.append(res["begin"])
        except KeyboardInterrupt:
            pass

# LIDARからランドマークまでの距離の成分
pos = [[]]

def mapping():
    """LIDARのデータをmatplotlibで描画"""

    lock = threading.Lock()
    fig = plt.figure()
    try:
        while True:
            if len(queue) > 0 and queue[0] == True:
                plt.cla()
                plt.scatter(x, y, marker=".", color="#7777FF")
                x.clear()
                y.clear()
                plt.grid(color="gray")
                plt.xlim([-2000,2000])
                plt.ylim([-2000,2000])

                plt.pause(0.1)
            else:
                # data = queue.pop(0)
                # print(data)
                v = data["length"]
                radius = (np.pi / 180) * data["theta"]
                x.append(v * np.cos(radius))
                y.append(v * np.sin(radius))
                # plt.draw()
            lock.acquire()
            queue.pop(0)
            lock.release()
    except KeyboardInterrupt:
        pass

def print_data():
    """データの確認スレッド"""
    try:
        while True:
            print(lidar_datas)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    # get_data_th.setDaemon(True)
    # mapping_th.setDaemon(True)

    get_data_th.start()
    # mapping_th.start()

    get_data_th.join()
    # mapping_th.join()
    # print_data_th.join()
    # executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    # executor.submit(get_data)
    # executor.submit(mapping)
