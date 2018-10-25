# -*- coding:utf-8 -*-
# Last Change : Thu 25 Oct 2018 17:04:10.
import socket
import json
import threading
import matplotlib.pyplot as plt

import pickle

class SLAM(object):
    '''recv map data and draw map'''
    def __init__(self):
        self.x = [0 for i in range(360)]
        self.y = [0 for i in range(360)]
        self.start_flag = False

        self.recv_map_data_th = threading.Thread(target=self.recv_map_data)
        self.draw_map_th      = threading.Thread(target=self.draw_map)

    def run(self):
        self.recv_map_data_th.start()
        self.recv_map_data_th.join()

    def recv_map_data(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 0)
            sock.bind(("0.0.0.0", 8888))

            self.draw_map_th.start()

            while True:
                for i, _ in enumerate(self.x):
                    res, addr = sock.recvfrom(2048)
                    res = res.decode("utf-8")
                    res = json.loads(res)
                    self.x[i] = res["x"]
                    self.y[i] = res["y"]
            self.draw_map_th.join()

    def draw_map(self):
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
            # if self.start_flag:
            line.set_xdata(self.x)
            line.set_ydata(self.y)

            fig.canvas.draw()
            fig.canvas.flush_events()

if __name__ == "__main__":

    slam = SLAM()

    slam.run()
