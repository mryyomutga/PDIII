# -*- coding:utf-8 -*-
# Last Change : Fri 26 Oct 2018 17:41:36.
import socket
import json
import threading
import matplotlib.pyplot as plt

import pickle

# {"range":float,"angle":float,"x":float,"y":float,"radian":float}
class SLAM(object):
    '''recv map data and draw map'''
    def __init__(self):
        '''constractor'''
        self.x = [0 for i in range(360)]
        self.y = [0 for i in range(360)]

        self.recv_map_data_th = threading.Thread(target=self.recv_map_data)
        self.draw_map_th      = threading.Thread(target=self.draw_map)

        self.draw_map_th.setDaemon(True)

    def run(self):
        '''start task'''
        self.recv_map_data_th.start()
        self.recv_map_data_th.join(0.1)

    def recv_map_data(self):
        '''create UDP socket and recv map datas from server(Robot)'''
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 0)
            sock.bind(("0.0.0.0", 8888))

            self.draw_map_th.start()

            def recv_data():
                '''get data'''
                for i, _ in enumerate(self.x):
                    res, addr = sock.recvfrom(2048)
                    res = res.decode("utf-8")
                    res = json.loads(res)
                    self.x[i] = res["x"]
                    self.y[i] = res["y"]

            while True:
                try:
                    recv_data()
                except KeyboardInterrupt:
                    break

    def draw_map(self):
        '''draw surrounding area'''
        plt.close("all")
        fig = plt.switch_backend('qt5agg')  # バックエンドをPyQt5に変更
        fig = plt.figure()
        line, = plt.plot(0, marker=".", markersize=2, linestyle="None", color="#7777FF")
        # line, = plt.plot(0, marker=".", linestyle="None", color="#7777FF")
        plt.grid(color='#CCCCCC')
        plt.xlim([-5000,5000])
        plt.ylim([-5000,5000])
        plt.show(block=False)

        while True:
            try:
                line.set_xdata(self.x)
                line.set_ydata(self.y)

                fig.canvas.draw()
                fig.canvas.flush_events()
            except KeyboardInterrupt:
                break
        plt.close(fig)


class Point(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.nx = 0
        self.ny = 0

if __name__ == "__main__":

    slam = SLAM()
    slam.run()
