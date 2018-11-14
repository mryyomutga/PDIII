# -*- coding:utf-8 -*-
# Last Change : Wed 14 Nov 2018 14:19:31.
# データサイズを可変長にしてjsonにdump,plotする

import socket
import json
import threading
import pprint

import matplotlib.pyplot as plt
import numpy as np
import cv2

class Client(object):
    '''recv map data and draw map'''
    def __init__(self, origin={"x":0, "y":0}, mapping=False):
        '''constractor'''
        self.origin         = origin
        self.idx            = 0
        self.data_len       = 0
        self.current_data   = []
        self.max_data       = []
        self.mapping        = mapping
        self.json_dump_file = "./map_data/origin(" + str(origin["x"]) + "_" + str(origin["y"]) + ").json"

        self.recv_map_data_th = threading.Thread(target=self.recv_map_data)
        self.draw_map_th      = threading.Thread(target=self.draw_map)
        self.draw_cv_map_th   = threading.Thread(target=self.draw_cv_map)

        self.draw_map_th.setDaemon(True)
        self.draw_cv_map_th.setDaemon(True)

        self.lock = threading.Lock()

    def run(self):
        '''start task'''
        self.recv_map_data_th.start()
        self.recv_map_data_th.join(0.1)

    def recv_map_data(self):
        '''create UDP socket and recv map datas from server(Robot)'''
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 0)
            sock.bind(("0.0.0.0", 8888))



            def get_decoded_data():
                '''get data'''
                json_str, addr = sock.recvfrom(1024)
                json_str = json_str.decode("utf-8")

                if json_str == "END":
                    return json_str

                return json.loads(json_str)

            self.cx, self.cy = list(), list()
            self.mx, self.my = list(), list()

            ff = True
            while True:
                try:
                    res = get_decoded_data()
                    if res == "END":
                        break
                    # print("self.idx={}, self.current_data size={}, self.data_len={}".format(self.idx, len(self.current_data), self.data_len))


                    def append_data(mag=1.0):
                        self.cx.append(int(res["x"] / mag))
                        self.cy.append(int(res["y"] / mag))
                        self.mx.append(int(res["x"] / mag))
                        self.my.append(int(res["y"] / mag))

                    if res["idx"] < self.idx:  # 1周計測し終わった時
                        self.current_data = self.current_data[:self.idx]
                        self.max_data     = self.max_data[:self.idx]
                        self.lock.acquire()
                        self.data_len     = len(self.current_data)

                        self.cx           = self.cx[:self.idx]
                        self.cy           = self.cy[:self.idx]
                        self.mx           = self.mx[:self.idx]
                        self.my           = self.my[:self.idx]
                        self.lock.release()
                        if self.mapping and ff:
                            # self.draw_map_th.start()
                            self.draw_cv_map_th.start()
                            ff = False

                    # idxの更新
                    self.idx = res["idx"]

                    # 初回のデータを受け取っている時
                    if self.data_len == 0:
                        self.current_data.append(res.copy())
                        self.max_data.append(res.copy())

                        append_data(mag=6.0)

                    else:
                        if self.idx >= self.data_len:
                            self.current_data.append(res.copy())
                            self.max_data.append(res.copy())

                            append_data(mag=6.0)
                        else:
                            self.current_data[self.idx].update(res)

                            self.cx[self.idx] = int(res["x"] / 6.0)
                            self.cy[self.idx] = int(res["y"] / 6.0)
                            if res["range"] > self.max_data[self.idx]["range"]:
                                self.max_data[self.idx].update(res)

                                self.mx[self.idx] = int(res["x"] / 6.0)
                                self.mx[self.idx] = int(res["y"] / 6.0)

                except KeyboardInterrupt:
                    break

            with open(self.json_dump_file, "w") as f:
                json_dump_data = {"origin":self.origin, "data":self.max_data}
                json.dump(json_dump_data, f, indent=4)

    def draw_map_json(self, mapsize=[5000,5000], map_file="dummy.json"):
        '''load map data and draw map'''
        map_file = "./map_data/" + map_file
        with open(map_file) as f:
            map_data = json.load(f)
            pprint.pprint(map_data)
            plt.close("all")
            fig = plt.switch_backend('qt5agg')  # バックエンドをPyQt5に変更
            fig = plt.figure()

            plt.grid(color='#CCCCCC')
            plt.xlim(-mapsize[0], mapsize[0])
            plt.ylim(-mapsize[1], mapsize[1])
            plt.show(block=False)

            x, y = list(), list()
            for data in map_data["data"]:
                if data["range"] != 0:
                    x.append(data["x"])
                    y.append(data["y"])
            plt.plot(x, y, marker=".", markersize=2, linestyle="None", color="#7777FF")
            plt.show()

    def draw_cv_map(self, mapsize=[1000,1000]):
        cv2.namedWindow('demo', cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow('demo', 1500, 1100)

        color = {
                #         B    G    R
                "BLACK":(0  , 0  , 0  ),
                "WHITE":(255, 255, 255),
                "GRAY": (128, 128, 128),
                "RED":  (0  , 0  , 255)
                }

        image = np.full((mapsize[0], mapsize[1], 3), color["GRAY"][0], dtype=np.uint8)

        pt1 = (int(mapsize[0]/2), int(mapsize[1]/2))
        idx = 0
        midx = 0
        while True:
            # if idx == len(self.cx):

            self.lock.acquire()
            if idx >= self.data_len:
                idx = 0
            if midx >= len(self.mx):
                midx = 0
            self.lock.release()
            if idx == len(self.cx):
                pt2  = (self.cx[0] + pt1[0], self.cy[0] + pt1[1])
                pt3  = (self.cx[1] + pt1[0], self.cy[1] + pt1[1])
            elif idx + 1 == len(self.cx):
                pt2  = (self.cx[idx] + pt1[0], self.cy[idx] + pt1[1])
                pt3  = (self.cx[0]   + pt1[0], self.cy[0]   + pt1[1])
            else:
                pt2  = (self.cx[idx]     + pt1[0], self.cy[idx]     + pt1[1])
                pt3  = (self.cx[idx + 1] + pt1[0], self.cy[idx + 1] + pt1[1])

            if midx == len(self.mx):
                mpt2 = (self.mx[0] + pt1[0], self.my[0] + pt1[1])
                mpt3 = (self.mx[1] + pt1[0], self.my[1] + pt1[1])
            elif midx + 1 == len(self.mx):
                mpt2 = (self.mx[midx] + pt1[0], self.my[midx] + pt1[1])
                mpt3 = (self.mx[0]   + pt1[0], self.my[0]   + pt1[1])
            else:
                mpt2 = (self.mx[midx]     + pt1[0], self.my[midx]     + pt1[1])
                mpt3 = (self.mx[midx + 1] + pt1[0], self.my[midx + 1] + pt1[1])

            # cv2.circle(image, pt1, 10, (255,255,255), -1)
            # triangle_cnt = np.array( [pt1, mpt2, mpt3] , dtype=np.int32)

            # cv2.drawContours(image, [triangle_cnt], 0, color["WHITE"], -1)
            # cv2.line(image, mpt2, mpt3, color["BLACK"], 2)
            triangle_cnt = np.array([pt1, pt2, pt3], dtype=np.int32)

            cv2.drawContours(image, [triangle_cnt], 0, color["WHITE"], -1)
            cv2.line(image, pt1, pt2, (128, 255, 0), 1)
            if (pt1[0] == pt2[0] and pt1[1] == pt2[1]) or (pt1[0] == pt3[0] and pt1[1] == pt3[1]):
                pass
            else:
                cv2.line(image, pt2, pt3, color["RED"], 2)
            # cv2.drawContours(image, [triangle_cnt], 0, color["BLACK"], thickness=1)

            cv2.waitKey(1)
            cv2.imshow('demo', image)

            idx += 1
            midx += 1

        cv2.destroyAllWindows()

    def draw_map(self, mapsize=[5000,5000]):
        '''draw surrounding area'''
        plt.close("all")
        fig = plt.switch_backend('qt5agg')  # バックエンドをPyQt5に変更
        fig = plt.figure()
        line,  = plt.plot(self.cx, self.cy, label="now", marker=".", markersize=2, linestyle="None", color="#7777FF")
        # line2, = plt.plot(self.mx, self.my, label="max", marker="o", markersize=2, linestyle="None", color="#FF7777")
        # line, = plt.plot(0, marker=".", linestyle="None", color="#7777FF")

        plt.grid(color='#CCCCCC')
        plt.xlim(-mapsize[0], mapsize[0])
        plt.ylim(-mapsize[1], mapsize[1])
        plt.show(block=False)

        while True:
            try:
                line.set_xdata(self.cx)
                line.set_ydata(self.cy)
                # line2.set_xdata(self.mx)
                # line2.set_ydata(self.my)

                # plt.pause(0.01)
                fig.canvas.draw()
                fig.canvas.flush_events()
            except KeyboardInterrupt:
                break
        plt.close(fig)

if __name__ == "__main__":
    cli = Client(mapping=True)
    cli.run()

