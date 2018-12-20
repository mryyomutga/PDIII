# -*- coding:utf-8 -*-
# Last Change : Fri 02 Nov 2018 16:40:31.
import socket
import json
import threading
import matplotlib.pyplot as plt

import pickle

# {"range":float,"angle":float,"x":float,"y":float,"radian":float}
class SLAM(object):
    '''recv map data and draw map'''
    def __init__(self, origin=[0, 0]):
        '''constractor'''
        self.origin       = origin
        self.idx          = 0
        self.data_len     = 0
        self.current_data = []
        self.max_data     = []

        self.recv_map_data_th = threading.Thread(target=self.recv_map_data)
        # self.draw_map_th      = threading.Thread(target=self.draw_map)

        # self.draw_map_th.setDaemon(True)

    def run(self):
        '''start task'''
        self.recv_map_data_th.start()
        self.recv_map_data_th.join(0.1)
        print(self.max_data)
        # with open("./map_data.json", "w") as f:
        #     json_dump_data = {"origin":self.origin, "data":self.max_data}
        #     json.dump(json_dump_data, f, indent=4)

    def recv_map_data(self):
        '''create UDP socket and recv map datas from server(Robot)'''
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 0)
            sock.bind(("0.0.0.0", 8888))

            # self.draw_map_th.start()

            def get_decoded_data():
                '''get data'''
                json_str, addr = sock.recvfrom(2048)
                json_str = json_str.decode("utf-8")

                if json_str == "END":
                    return json_str

                return json.loads(json_str)

            while True:
                # try:
                res = get_decoded_data()
                if res == "END":
                    break
                print("self.idx={}, self.current_data size={}, self.data_len={}".format(self.idx, len(self.current_data), self.data_len))
                if res["idx"] < self.idx:  # 1周計測し終わった時
                    self.current_data = self.current_data[:self.idx]
                    self.max_data     = self.max_data[:self.idx]
                    self.data_len     = self.idx

                # idxの更新
                self.idx = res["idx"]

                # 初回のデータを受け取っている時
                if self.data_len == 0:
                    self.current_data.append(res.copy())
                    self.max_data.append(res.copy())
                else:
                    if self.idx >= self.data_len:
                        self.current_data.append(res.copy())
                        self.max_data.append(res.copy())
                    else:
                        self.current_data[self.idx].update(res)
                        if res["range"] > self.max_data[self.idx]["range"]:
                            self.max_data[self.idx].update(res)

                # except KeyboardInterrupt:
                #     break

            with open("./map_data.json", "w") as f:
                json_dump_data = {"origin":self.origin, "data":self.max_data}
                json.dump(json_dump_data, f, indent=4)

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

if __name__ == "__main__":
    slam = SLAM()
    slam.run()
