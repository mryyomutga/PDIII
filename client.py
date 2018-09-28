# -*- coding:utf-8 -*-
# Last Change: Fri 28 Sep 2018 17:02:52.
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
# queue = list()

def get_data():

    # addr = sys.argv[1]
    # print(addr)
    # lock = threading.Lock()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 0)
        sock.bind(("0.0.0.0", 8888))
        print(sock)

        # cnt = 0
        success_recv_data = True
        # print("a")

        # print_data_th = threading.Thread(target=print_data)
        # print_data_th.setDaemon(True)
        # print_data_th.start()

        while True:
            res, addr = sock.recvfrom(2048)
            res = res.decode("utf-8")
            res = json.loads(res)
            # print(res, type(res))
            lidar_datas.append(np.array([res["begin"], res["theta"], res["length"]]))

x, y = list(), list()

def mapping():
    fig = plt.figure()
    while True:
        if len(a):
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
        # lock.release()

# while True:
            # print(data["begin"])
            # print(data["len"])
            # print(data["theta"])
            # print(data)
            # time.sleep(0.1)


def print_data():
    while True:
        print(lidar_datas)

if __name__ == "__main__":

    get_data_th = threading.Thread(target=get_data)
    # mapping_th  = threading.Thread(target=mapping)


    # get_data_th.setDaemon(True)
    # mapping_th.setDaemon(True)


    get_data_th.start()
    # mapping_th.start()


    # if connect_success:
    # get_data_th.join()
    # mapping_th.join()
    # executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    # executor.submit(get_data)
    # executor.submit(mapping)
