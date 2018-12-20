# -*- coding:utf-8 -*-
# Last Change : Mon 05 Nov 2018 17:33:35.
# データサイズを可変長にしてjsonにdump,plotする

import socket
import json
import threading
import pprint

import matplotlib.pyplot as plt

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

            if self.mapping:
                self.draw_map_th.start()

            def get_decoded_data():
                '''get data'''
                json_str, addr = sock.recvfrom(1024)
                json_str = json_str.decode("utf-8")

                if json_str == "END":
                    return json_str

                return json.loads(json_str)

            self.cx, self.cy = list(), list()
            self.mx, self.my = list(), list()

            while True:
                try:
                    res = get_decoded_data()
                    if res == "END":
                        break
                    print("self.idx={}, self.current_data size={}, self.data_len={}".format(self.idx, len(self.current_data), self.data_len))
                    if res["idx"] < self.idx:  # 1周計測し終わった時
                        self.current_data = self.current_data[:self.idx]
                        self.max_data     = self.max_data[:self.idx]
                        self.data_len     = len(self.current_data)

                        self.cx           = self.cx[:self.idx]
                        self.cy           = self.cy[:self.idx]
                        self.mx           = self.mx[:self.idx]
                        self.my           = self.my[:self.idx]

                    # idxの更新
                    self.idx = res["idx"]

                    # 初回のデータを受け取っている時
                    if self.data_len == 0:
                        self.current_data.append(res.copy())
                        self.max_data.append(res.copy())

                        self.cx.append(res["x"])
                        self.cy.append(res["y"])
                        self.mx.append(res["x"])
                        self.my.append(res["y"])
                    else:
                        if self.idx >= self.data_len:
                            self.current_data.append(res.copy())
                            self.max_data.append(res.copy())

                            self.cx.append(res["x"])
                            self.cy.append(res["y"])
                            self.mx.append(res["x"])
                            self.my.append(res["y"])
                        else:
                            self.current_data[self.idx].update(res)

                            self.cx[self.idx] = res["x"]
                            self.cy[self.idx] = res["y"]
                            if res["range"] > self.max_data[self.idx]["range"]:
                                self.max_data[self.idx].update(res)

                                self.mx[self.idx] = res["x"]
                                self.mx[self.idx] = res["y"]

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

