# -*- coding:utf-8 -*-
# Last Change : Thu 29 Nov 2018 00:49:59.
# データサイズを可変長にしてjsonにdump,plotする

import os
import sys
import glob
import argparse

import json
import pprint
import socket
import threading

import cv2
import matplotlib.pyplot as plt
import numpy as np


class Client(object):
    '''recv map data and draw map'''

    def __init__(self, origin={"x": 0, "y": 0}, scale=6, mapping=False):
        '''constractor'''
        self.origin = origin
        self.idx = 0
        self.data_len = 0
        self.current_data = []
        self.max_data = []
        self.mapping = mapping

        self.color = {
            #         B    G    R
            "BLACK": (0, 0, 0),
            "WHITE": (255, 255, 255),
            "GRAY":  (128, 128, 128),
            "BLUE":  (255, 96, 16),
            "RED":   (0, 0, 255)
        }
        self.scale = scale

        self.recv_map_data_th = threading.Thread(target=self.recv_map_data)
        self.draw_mat_map_th = threading.Thread(target=self.draw_mat_map)
        self.draw_cv_map_th = threading.Thread(target=self.draw_cv_map)

        self.draw_mat_map_th.setDaemon(True)
        self.draw_cv_map_th.setDaemon(True)

        self.lock = threading.Lock()

        os.chdir(os.getcwd() + "/map_data")

        fl = glob.glob("map_data[0-9]*.json")
        number = len(fl)
        self.block = 50 # 30cm = 50px

        self.json_dump_file = "map_data{0:02d}.json".format(number)

    def run(self):
        '''start task'''
        self.recv_map_data_th.start()
        self.recv_map_data_th.join(0.1)

    def recv_map_data(self):
        '''create UDP socket and recv map datas from server(Robot)'''
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                           socket.IPPROTO_UDP) as sock:
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
                        self.max_data = self.max_data[:self.idx]
                        self.lock.acquire()
                        self.data_len = len(self.current_data)

                        self.cx = self.cx[:self.idx]
                        self.cy = self.cy[:self.idx]
                        self.mx = self.mx[:self.idx]
                        self.my = self.my[:self.idx]
                        self.lock.release()
                        if self.mapping and ff:
                            # self.draw_map_th.start()
                            self.draw_cv_map_th.start()
                            ff = False

                    # idxの更新
                    self.idx = res["idx"]

                    print(len(self.max_data))
                    # 初回のデータを受け取っている時
                    if self.data_len == 0:
                        self.current_data.append(res.copy())
                        self.max_data.append(res.copy())

                        append_data(mag=10.0)

                    else:
                        if self.idx >= self.data_len:
                            self.current_data.append(res.copy())
                            self.max_data.append(res.copy())

                            append_data(mag=10.0)
                        else:
                            self.current_data[self.idx].update(res)

                            self.cx[self.idx] = int(res["x"] / 10.0)
                            self.cy[self.idx] = int(res["y"] / 10.0)
                            if res["range"] > self.max_data[self.idx]["range"]:
                                self.max_data[self.idx].update(res)

                                self.mx[self.idx] = int(res["x"] / 10.0)
                                self.mx[self.idx] = int(res["y"] / 10.0)

                except KeyboardInterrupt:
                    break

            with open(self.json_dump_file, "w") as f:
                json_dump_data = {"origin": self.origin, "data": self.max_data}
                json.dump(json_dump_data, f, indent=4)

    def draw_map_json(self, mapsize=[5000, 5000], mapfile="dummy.json"):
        '''load map data and draw map'''
        map_file = mapfile
        with open(mapfile) as f:
            mapdata = json.load(f)
            pprint.pprint(mapdata)
            plt.close("all")
            fig = plt.switch_backend('qt5agg')  # バックエンドをPyQt5に変更
            fig = plt.figure()

            plt.grid(color='#CCCCCC')
            plt.xlim(-mapsize[0], mapsize[0])
            plt.ylim(-mapsize[1], mapsize[1])
            plt.show(block=False)

            x, y = list(), list()
            for data in mapdata["data"]:
                if data["range"] != 0:
                    x.append(data["x"])
                    y.append(data["y"])
            plt.plot(x, y, marker=".", markersize=2, linestyle="None", color="#7777FF")
            plt.show()

    def draw_cv_map_json(self, mapsize=[1500,1500]):
        '''loads json file and drawing map by opencv'''
        cv2.namedWindow('demo', cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow('demo', 1500, 1250)

        # 縮小倍率
        # self.scale = 30

        image = np.full((mapsize[0], mapsize[1], 3),
                        self.color["GRAY"][0],
                        dtype=np.uint8)

        # マップの中心点
        pt0 = (int(mapsize[0] / 2), int(mapsize[1] / 2))

        maplist = glob.glob("map_data[0-9]*.json")
        lw, lh = 500, 500

        # レイヤーの数
        tiles = (int(mapsize[0] / lw), int(mapsize[1] / lh))
        # 各レイヤー情報を退避させるリスト
        layers = list()

        # 複数のマップデータを読み込む
        for filename in maplist:
            # 部分領域のイメージ
            layer = np.full((lw, lh, 3),
                            self.color["GRAY"][0],
                            dtype=np.uint8)

            po = (int(lw / 2), int(lh / 2))

            # 1レイヤーにおけるマップデータのロード
            with open(filename, "r") as f:
                cv2.namedWindow('test', cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
                cv2.resizeWindow('test', 500, 500)
                mapdata = json.load(f)
                po = (int(mapdata["origin"]["x"] / self.scale) + po[0], int(mapdata["origin"]["y"] / self.scale) + po[1])
                max_idx = len(mapdata["data"]) - 1
                data = mapdata["data"]

                for idx in range(len(data)):
                    if idx == max_idx:
                        pt2 = (int(data[idx]["x"] / self.scale) + po[0], int(data[idx]["y"] / self.scale) + po[1])
                        pt3 = (int(data[0]["x"]   / self.scale) + po[0], int(data[0]["y"]   / self.scale) + po[1])
                    else:
                        pt2 = (int(data[idx]["x"]     / self.scale) + po[0], int(data[idx]["y"]     / self.scale) + po[1])
                        pt3 = (int(data[idx + 1]["x"] / self.scale) + po[0], int(data[idx + 1]["y"] / self.scale) + po[1])

                    triangle_cnt = np.array([po, pt2, pt3], dtype=np.int32)

                    cv2.drawContours(layer, [triangle_cnt], 0, self.color["WHITE"], -1)
                    # cv2.line(layer, po, pt2, (128, 255, 0), 1)
                    if (po[0] == pt2[0]
                            and po[1] == pt2[1]) or (po[0] == pt3[0]
                                                      and po[1] == pt3[1]):
                        pass
                    # else:
                        # cv2.line(layer, pt2, pt3, self.color["RED"], 2)
                cv2.imshow("test", layer)
                layers.append(layer)

        def concat_tile(im):
            return cv2.vconcat([cv2.hconcat(im_h) for im_h in im])

        img = layers[0]
        cv2.waitKey(0)
        image = concat_tile([[img, img, img],
                             [img, img, img],
                             [img, img, img]]
                            )

        print(image, type(image))
        cv2.imshow('demo', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def draw_cv_map2_json(self, mapsize=[1500,1500], rot_deg=0):
        '''
            Description : OpenCVを用いてjson形式で保存された地図データをもとに地図生成する
            args : 
                degree : センサー座標を中心にPnをrot_deg(deg)回転
        '''
        cv2.namedWindow("demonstration", cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL) 
        cv2.resizeWindow("demonstration", 800, 800)

        image = np.full((mapsize[0], mapsize[1], 3),
                        self.color["GRAY"][0],
                        dtype=np.uint8
                        )

        # 地図の原点
        pt0 = (int(mapsize[0] / 2), int(mapsize[1] / 2))

        # x,y軸に対して50px毎に線を引く
        # for _line in range(0, 1500, 50):
        #     cv2.line(image, (0, _line), (mapsize[0], _line), (160,160,160), 1)
        #     cv2.line(image, (_line ,0), (_line, mapsize[1]), (160,160,160), 1)

        # 地図データのファイルリストを取得
        maplist = glob.glob("map_data[0-9]*.json")
        maplist.sort()
        print(maplist)

        cv2.rectangle(image, (pt0[0] + int(2   * self.block), pt0[1] - int(5  * self.block)), (pt0[0] + int(16 * self.block), pt0[1] - int(-15 * self.block)), (192,192,192), thickness=2, lineType=cv2.LINE_AA)
        cv2.rectangle(image, (pt0[0] + int(-13 * self.block), pt0[1] - int(5  * self.block)), (pt0[0]                       , pt0[1] - int(-15 * self.block)), (192,192,192), thickness=2, lineType=cv2.LINE_AA)
        cv2.rectangle(image, (0                             , pt0[1] - int(14 * self.block)), (mapsize[0]                   , pt0[1] - int(7   * self.block)), (192,192,192), thickness=2, lineType=cv2.LINE_AA)

        # センサーの計測位置表示用座標リスト
        senser_points = list()

        for filename in maplist:
            with open(filename, "r") as f:
                mapdata = json.load(f)
                # センサー座標系の原点を地図座標系に変換
                pt1 = (int(mapdata["origin"]["x"] * self.block) + pt0[0], int(-mapdata["origin"]["y"] * self.block) + pt0[1])
                print(pt1)
                senser_points.append(pt1)

                data = mapdata["data"]   # 座標Pにおけるセンサーデータの取得
                max_idx = len(data) - 1

                def rotate_pos(pos, deg):
                    radian = np.radians(deg)
                    rc = np.cos(radian)
                    rs = np.sin(radian)
                    # 回転行列の生成
                    rot_mat = np.array([[rc, -rs], [rs, rc]])
                    ret = np.dot(rot_mat, pos)
                    return ret

                # 各偏角とセンサー座標を頂点とする三角形を描画する
                for idx in range(len(data)):
                    if idx == max_idx:
                        p2_pos = np.array([[ data[idx]["x"] ], [ data[idx]["y"] ]])
                        p3_pos = np.array([[ data[0]["x"]   ], [ data[0]["y"]   ]])
                        p2 = rotate_pos(p2_pos, rot_deg)
                        p3 = rotate_pos(p3_pos, rot_deg)

                        pt2 = [int(p2[0] / self.scale) + pt1[0], -int(p2[1] / self.scale) + pt1[1]]
                        pt3 = [int(p3[0] / self.scale) + pt1[0], -int(p3[1] / self.scale) + pt1[1]]
                    else:
                        p2_pos = np.array([[ data[idx]["x"]     ], [ data[idx]["y"]     ]])
                        p3_pos = np.array([[ data[idx + 1]["x"] ], [ data[idx + 1]["y"] ]])
                        p2 = rotate_pos(p2_pos, rot_deg)
                        p3 = rotate_pos(p3_pos, rot_deg)
                        pt2 = [int(p2[0] / self.scale) + pt1[0], -int(p2[1] / self.scale) + pt1[1]]
                        pt3 = [int(p3[0] / self.scale) + pt1[0], -int(p3[1] / self.scale) + pt1[1]]

                        # pt2 = [int(data[idx]["x"]     / self.scale) + pt1[0], -int(-data[idx]["y"] / self.scale)     + pt1[1]]
                        # pt3 = [int(data[idx + 1]["x"] / self.scale) + pt1[0], -int(-data[idx + 1]["y"] / self.scale) + pt1[1]]

                    def convert_data(point):
                        '''データを地図に合わせる
                           convert list to tuple
                        '''
                        # if point[0] > mapsize[0]:
                        #     point[0] = mapsize[0]
                        # if point[1] > mapsize[1]:
                        #     point[1] = mapsize[1]
                        return tuple(point)

                    pt2 = convert_data(pt2)
                    pt3 = convert_data(pt3)

                    triangle_cnt = np.array([pt1, pt2, pt3], dtype=np.int32)

                    cv2.drawContours(image, [triangle_cnt], 0, self.color["WHITE"], -1)

                    # if (pt1[0] == pt2[0] and pt1[1] == pt2[1]) or (pt1[0] == pt3[0] and pt1[1] == pt3[1]):
                    #     pass
                    # else:
                    #     cv2.line(image, pt2, pt3, self.color["RED"], 2)

        cv2.drawMarker(image, (pt0[0], pt0[1]), self.color["BLUE"], markerType=cv2.MARKER_STAR, markerSize=20, thickness=1, line_type=cv2.LINE_AA)
        for _line in range(0, 1500, 50):
            cv2.line(image, (0, _line), (mapsize[0], _line), (160,160,160), 1)
            cv2.line(image, (_line ,0), (_line, mapsize[1]), (160,160,160), 1)
        cv2.rectangle(image, (pt0[0] + int(2   * self.block), pt0[1] - int(5  * self.block)), (pt0[0] + int(16 * self.block), pt0[1] - int(-15 * self.block)), (192,192,192), thickness=3, lineType=cv2.LINE_AA)
        cv2.rectangle(image, (pt0[0] + int(-13 * self.block), pt0[1] - int(5  * self.block)), (pt0[0]                       , pt0[1] - int(-15 * self.block)), (192,192,192), thickness=3, lineType=cv2.LINE_AA)
        cv2.rectangle(image, (0                             , pt0[1] - int(14 * self.block)), (mapsize[0]                   , pt0[1] - int(7   * self.block)), (192,192,192), thickness=3, lineType=cv2.LINE_AA)
        # センサーの中心を表示
        for p in senser_points:
            cv2.drawMarker(image, p, (128,255,64), markerType=cv2.MARKER_TILTED_CROSS, markerSize=30, thickness=2, line_type=cv2.LINE_AA)

        cv2.imshow("demonstration", image)
        sf = "map_{0}.png".format(mapsize[0])
        cv2.imwrite(sf, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def draw_cv_map3_json(self, mapsize=[1500,1500]):
        cv2.namedWindow("demonstration", cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL) 
        cv2.resizeWindow("demonstration", 800, 800)

        image = np.full((mapsize[0], mapsize[1], 3),
                        self.color["GRAY"][0],
                        dtype=np.uint8
                        )

        # 地図の原点
        pt0 = (int(mapsize[0] / 2), int(mapsize[1] / 2))

        # 地図データのファイルリストを取得
        maplist = glob.glob("map_data[0-9]*.json")
        maplist.sort()
        print(maplist)

        # 5,2
        cv2.rectangle(image, (pt0[0] + int(2   * self.block), pt0[1] - int(5  * self.block)), (pt0[0] + int(16 * self.block), pt0[1] - int(-15 * self.block)), (192,192,192), thickness=1, lineType=cv2.LINE_AA)
        cv2.rectangle(image, (pt0[0] + int(-13 * self.block), pt0[1] - int(5  * self.block)), (pt0[0]                       , pt0[1] - int(-15 * self.block)), (192,192,192), thickness=1, lineType=cv2.LINE_AA)
        cv2.rectangle(image, (0                             , pt0[1] - int(14 * self.block)), (mapsize[0]                   , pt0[1] - int(7   * self.block)), (192,192,192), thickness=1, lineType=cv2.LINE_AA)
        cv2.imshow("demo", image)

        q = 0
        senser_points = list()

        for filename in maplist:
            with open(filename, "r") as f:
                mapdata = json.load(f)
                # センサー座標系の原点を地図座標系に変換
                pt1 = (int(mapdata["origin"]["x"] * self.block) + pt0[0], int(-mapdata["origin"]["y"] * self.block) + pt0[1])
                senser_points.append(pt1)
                print(pt1)

                data = mapdata["data"]
                max_idx = len(data) - 1

                # 各偏角とセンサー座標を頂点とする三角形を描画する
                if q == 0:
                    for idx in range(len(data)):
                        if idx == max_idx:
                            pt2 = [int((data[idx]["range"] / self.scale)*np.cos(data[idx]["radian"])) + pt1[0], -int((data[idx]["range"] / self.scale)*np.sin(data[idx]["radian"])) + pt1[1]]
                            pt3 = [int((data[0]["range"] / self.scale)*np.cos(data[0]["radian"])) + pt1[0], -int((data[0]["y"]   / self.scale)*np.sin(data[0]["radian"])) + pt1[1]]
                        else:
                            pt2 = [int((data[idx]["range"] / self.scale)*np.cos(data[idx]["radian"])) + pt1[0], -int((-data[idx]["range"] / self.scale)*np.sin(data[idx]["radian"])) + pt1[1]]
                            pt3 = [int((data[idx + 1]["range"] / self.scale)*np.cos(data[idx + 1]["radian"])) + pt1[0], -int((-data[idx + 1]["range"] / self.scale)*np.sin(data[idx + 1]["radian"])) + pt1[1]]

                        def convert_data(point):
                            # '''データを地図に合わせる'''
                            # if point[0] > mapsize[0]:
                            #     point[0] = mapsize[0]
                            # if point[1] > mapsize[1]:
                            #     point[1] = mapsize[1]
                            return tuple(point)

                        pt2 = convert_data(pt2)
                        pt3 = convert_data(pt3)

                        triangle_cnt = np.array([pt1, pt2, pt3], dtype=np.int32)

                        cv2.drawContours(image, [triangle_cnt], 0, self.color["WHITE"], -1)

                        if (pt1[0] == pt2[0] and pt1[1] == pt2[1]) or (pt1[0] == pt3[0] and pt1[1] == pt3[1]):
                            pass
                        else:
                            cv2.line(image, pt2, pt3, self.color["RED"], 2)
                    q = 1

        cv2.imshow("demonstration", image)
        while cv2.waitKey(0) != 27:
            pass
        cv2.destroyAllWindows()

    def draw_cv_map(self, mapsize=[1000, 1000]):
        cv2.namedWindow('demo', cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow('demo', 1500, 1100)

        image = np.full((mapsize[0], mapsize[1], 3),
                        self.color["GRAY"][0],
                        dtype=np.uint8)

        pt1 = (int(mapsize[0] / 2), int(mapsize[1] / 2))
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
            # if idx == len(self.cx):
            #     pt2  = (self.cx[0] + pt1[0], self.cy[0] + pt1[1])
            #     pt3  = (self.cx[1] + pt1[0], self.cy[1] + pt1[1])
            # elif idx + 1 == len(self.cx):
            #     pt2  = (self.cx[idx] + pt1[0], self.cy[idx] + pt1[1])
            #     pt3  = (self.cx[0]   + pt1[0], self.cy[0]   + pt1[1])
            # else:
            #     pt2  = (self.cx[idx]     + pt1[0], self.cy[idx]     + pt1[1])
            #     pt3  = (self.cx[idx + 1] + pt1[0], self.cy[idx + 1] + pt1[1])

            pt2 = (self.cx[idx % self.data_len] + pt1[0],
                   self.cy[idx % self.data_len] + pt1[1])
            pt3 = (self.cx[(idx + 1) % self.data_len] + pt1[0],
                   self.cy[(idx + 1) % self.data_len] + pt1[1])

            # if midx == len(self.mx):
            #     mpt2 = (self.mx[0] + pt1[0], self.my[0] + pt1[1])
            #     mpt3 = (self.mx[1] + pt1[0], self.my[1] + pt1[1])
            # elif midx + 1 == len(self.mx):
            #     mpt2 = (self.mx[midx] + pt1[0], self.my[midx] + pt1[1])
            #     mpt3 = (self.mx[0]   + pt1[0], self.my[0]   + pt1[1])
            # else:
            #     mpt2 = (self.mx[midx]     + pt1[0], self.my[midx]     + pt1[1])
            #     mpt3 = (self.mx[midx + 1] + pt1[0], self.my[midx + 1] + pt1[1])
            mpt2 = (self.mx[midx % len(self.mx)] + pt1[0],
                    self.my[midx % len(self.mx)] + pt1[1])
            mpt3 = (self.mx[(midx + 1) % len(self.mx)] + pt1[0],
                    self.my[(midx + 1) % len(self.mx)] + pt1[1])

            # cv2.circle(image, pt1, 10, (255,255,255), -1)
            # triangle_cnt = np.array( [pt1, mpt2, mpt3] , dtype=np.int32)

            # cv2.drawContours(image, [triangle_cnt], 0, self.color["WHITE"], -1)
            # cv2.line(image, mpt2, mpt3, self.color["BLACK"], 2)
            triangle_cnt = np.array([pt1, pt2, pt3], dtype=np.int32)

            cv2.drawContours(image, [triangle_cnt], 0, self.color["WHITE"], -1)
            cv2.line(image, pt1, pt2, (128, 255, 0), 1)
            if (pt1[0] == pt2[0]
                    and pt1[1] == pt2[1]) or (pt1[0] == pt3[0]
                                              and pt1[1] == pt3[1]):
                pass
            else:
                cv2.line(image, pt2, pt3, self.color["RED"], 2)
            # cv2.drawContours(image, [triangle_cnt], 0, self.color["BLACK"], thickness=1)

            cv2.waitKey(1)
            cv2.imshow('demo', image)

            idx += 1
            midx += 1

        cv2.destroyAllWindows()

    def draw_mat_map(self, mapsize=[5000, 5000]):
        '''draw surrounding area'''
        plt.close("all")
        fig = plt.switch_backend('qt5agg')  # バックエンドをPyQt5に変更
        fig = plt.figure()
        line, = plt.plot(
            self.cx,
            self.cy,
            label="now",
            marker=".",
            markersize=2,
            linestyle="None",
            color="#7777FF")
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
    args = sys.argv
    sp = {"x":0, "y":0}
    if len(args) == 3:
        sp = {"x":int(args[1]), "y":int(args[2])}

    cli = Client(origin=sp, mapping=True)
    cli.run()
