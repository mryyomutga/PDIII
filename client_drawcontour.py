# -*- coding:utf-8 -*-
# Last Change : Thu 01 Nov 2018 01:31:15.
import socket
import json
import threading

import cv2

# {"range":float,"angle":float,"radian":float,"x":float,"y":float}
class MapDrawCoutours(object):
    '''recv map data and draw map'''
    def __init__(self):
        '''constractor'''
        # self.x = [0 for i in range(360)]
        # self.y = [0 for i in range(360)]
        self.current_data = [{"idx":0, "range":0, "angle":0, "radian":0, "x":0, "y":0}]
        self.max_data     = [{"idx":0, "range":0, "angle":0, "radian":0, "x":0, "y":0}]

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

            prev_idx = -1

            def recv_data():
                '''get data'''
                res, addr = sock.recvfrom(2048)
                res = res.decode("utf-8")
                res = json.loads(res)
                if res["idx"] > prev_idx:
                    current_data

            while True:
                try:
                    # recv_data()
                    # '''get data'''
                    for current, md in zip(current_data, max_data):
                        res, addr = sock.recvfrom(2048)
                        res = res.decode("utf-8")
                        res = json.loads(res)
                except KeyboardInterrupt:
                    break

    def draw_map(self):
        '''draw surrounding area'''


if __name__ == "__main__":

    slam = SLAM()
    slam.run()
