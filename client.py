# -*- coding:utf-8 -*-
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
data = {"begin":False, "theta":0, "length":0}        # LIDARデータ
# data = dict()
# queue = list()
def get_data():
    lock = threading.Lock()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("0.0.0.0",8888))
        print(sock)

        cnt = 0
        success_recv_data = True
        # print("a")

        mapping_th  = threading.Thread(target=mapping)
        mapping_th.start()
        while True:
            res, addr = sock.recvfrom(1024)
            res = res.decode("utf-8")
            res = json.loads(res)
            print(res, type(res))
            # lock.acquire()
            data["begin"] = res["begin"]
            data["theta"] = res["theta"]
            data["length"] = res["length"]
            # print("response : ", res)
            # print("data     : ", data)
            # if res["begin"]:
            #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            # print("-" * 55)
            # print(res == data)

            # lock.release()
            # data.clear()
            # queue.append(res)
            # print(type(res))
            # print(data)
            # start_flag = res["begin"]
            # redumps = {"theta":res["theta"], "len":res["len"]}
            # data.update({"begin":res["begin"], "length":res["len"], "theta":res["theta"]})
            # if start_flag:
            #     data.append(redumps)
            # data.append(json.loads(res))
            # if success_recv_data:

            # cnt += 1
            # print(res)
            # time.sleep(0.1)
            del res, addr

        # begin = [v.get("begin") for v in data]
        # print(begin)

x, y = list(), list()

def mapping():
    lock = threading.Lock()
    # time.sleep(3)
    fig = plt.figure()
    # print(data, type(data))
    # print(queue)
    # data = queue.pop(0)
    # print(data)
    while True:
        # print(data)
        # print(data,data["begin"])
        # lock.acquire()
        # print(data)
        if data["begin"]:
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



if __name__ == "__main__":

    get_data_th = threading.Thread(target=get_data)


    # get_data_th.setDaemon(True)
    # mapping_th.setDaemon(True)
    get_data_th.start()

    # if connect_success:
    # get_data_th.join()
    # mapping_th.join()
    # executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    # executor.submit(get_data)
    # executor.submit(mapping)
