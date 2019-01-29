/*
 * Last Change: Wed 17 Oct 2018 14:50:52.
 * Usage: ./myapp {[dp_on]|dp_off} [device=/dev/ttyUSB0] [baudrate=115200]
 */
#include <stdio.h>
#include <unistd.h>

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <pthread.h>

#include "rplidar.h"

#ifndef _countof
#define _countof(_Array) (int)(sizeof(_Array) / sizeof(_Array[0]))
#endif

#include <arpa/inet.h>
#include <ctype.h>

static inline void delay(_word_size_t ms){
    while(ms >= 1000){
        usleep(1000*1000);
        ms -= 1000;
    }
    if(ms != 0){
        usleep(ms * 1000);
    }
}

using namespace rp::standalone::rplidar;

u_result     op_result;
RPlidarDriver * drv;
rplidar_response_measurement_node_t nodes[8192];
size_t count = _countof(nodes);

bool checkRPLIDARHealth(void){
    rplidar_response_device_health_t healthinfo;

    op_result = drv->getHealth(healthinfo);
    if(IS_OK(op_result)) {
        printf("RPLidar health status : %d\n", healthinfo.status);
        if(healthinfo.status == RPLIDAR_STATUS_ERROR) {
            fprintf(stderr, "Error, rplidar internal error detected. Please reboot the device to retry.\n");
            return false;
        } else {
            return true;
        }
    } else {
        fprintf(stderr, "Error, cannot retrive the lidar healt code : %x\n", op_result);
        return false;
    }
}

#include <signal.h>
bool ctrl_c_pressed;
void ctrlc(int signum){
    ctrl_c_pressed = true;
    printf("%d catch SIGINT\n", signum);
    printf("ctrl_c_pressed = %s\n", ctrl_c_pressed ? "true": "false");
}

bool dp_on       = true;                        // ログ出力判定フラグ
bool wait_set_ip = true;

/*
 * 周辺環境を取得するスレッド
 */
void *scanDataThread(void *arg) {
    char client_addr[16];                                   // client IP address
    printf("====================================\n");
    printf(" Client IP address > ");
    scanf("%s", client_addr);
    printf("====================================\n");

    // wait_set_ip = false;

    int sock              = socket(AF_INET, SOCK_DGRAM, 0); // IPv4 UDP socket
    struct sockaddr_in sa = {0};
    sa.sin_family         = AF_INET;                        // IPv4
    sa.sin_port           = htons(8888);                    // Port:8888
    sa.sin_addr.s_addr    = inet_addr(client_addr);         // Address

    char buffer[1024];                                      // 送信データバッファ
    // RPLIDARのモーター駆動開始(stopしないとプログラム終了後も回転し続ける)
    drv->startMotor();
    // スキャンの開始
    drv->startScan(0,1);

    while(!ctrl_c_pressed){
        rplidar_response_measurement_node_t nodes[8192];
        size_t count = _countof(nodes);
        // スキャンしたデータを取得する
        op_result = drv->grabScanData(nodes, count);

        if(IS_OK(op_result)) {
            drv->ascendScanData(nodes, count);
            for(int idx = 0; idx < (int)count; idx++) {
                float angle = (nodes[idx].angle_q6_checkbit >> RPLIDAR_RESP_MEASUREMENT_ANGLE_SHIFT) / 64.0f;
                float range = nodes[idx].distance_q2 / 4.0f;
                float radian = (M_PI / 180.0) * angle;
                float x = range * cos(radian);
                float y = range * sin(radian);

                // JSONのフォーマット
                sprintf(buffer,"{\"idx\":%d,\"range\":%.4f,\"angle\":%.4f,\"radian\":%.4f,\"x\":%f,\"y\":%f}",
                        idx,
                        range,
                        angle,
                        radian,
                        x, y
                        );

                if(dp_on)
                    fprintf(stderr, "%d\n", idx);   // エラー出力
                // JSONを送信
                sendto(sock, buffer, strlen(buffer), 0, (struct sockaddr *)&sa, sizeof(sa));
                memset(buffer,'\0', sizeof(buffer));    // bufferをクリア
            }
        }
    }
    sendto(sock, "END", strlen("END"), 0, (struct sockaddr *)&sa, sizeof(sa));
    close(sock);
    return NULL;
}


int main(int argc, const char * argv[]){
    const char * opt_com_path = NULL;                   // RPLIDARのデバイス
    _u32         baudrateArray[2] = {115200, 256000};   // デフォルトのボーレートリスト
    _u32         opt_com_baudrate = 0;                  // ボーレート

    bool useArgBaudrate  = false;

    // SIGINTシグナルをキャッチしたらctrlcハンドラを走らせる
    signal(SIGINT, ctrlc);

    printf("LIDAR data grabber for RPLIDAR.\nVersion : " RPLIDAR_SDK_VERSION "\n");

        /*
         * オプションのチェック
         * 1. debug print on/off
         * 2. device
         * 3. baudrate
         */
    for(int i = 1; i < argc; i++){
        if(strcmp(argv[i], "Usage") == 0){
            fprintf(stderr, "Usage: ./myapp {[dp_on]|dp_off} device=[/dev/ttyUSB0] baudrate=[115200]\n");
            exit(-2);
        }
        // debug print
        else if(strcmp(argv[i], "dp_on") == 0){
            dp_on = true;
            printf("dp_on = true\n");
        }
        else if(strcmp(argv[i], "dp_off") == 0){
            dp_on = false;
            printf("dp_on = false\n");
        }
        // device
        else if(strstr(argv[i], "/dev/") != NULL){
            opt_com_path = argv[i];
            printf("opt_com_path = argv[i]\n");
        }
        else if(isdigit(argv[i][0])){
            opt_com_baudrate = strtol(argv[i], NULL, 10);
            useArgBaudrate = true;
            printf("opt_com_baudrate = strtol(argv[i], NULL, 10)\n");
        }
        // 誤ったオプションが存在する場合
        else{
            fprintf(stderr, "Usage: ./myapp {[dp_on]|dp_off} device=[/dev/ttyUSB0] baudrate=[115200]\n");
            exit(-2);
        }
    }

    if(!opt_com_path)
        opt_com_path = "/dev/ttyUSB0";

    drv = RPlidarDriver::CreateDriver(DRIVER_TYPE_SERIALPORT);
    if(!drv) {
        fprintf(stderr, "insufficent memory, exit\n");
        exit(-2);
    }

    rplidar_response_device_info_t devinfo;
    bool connectSuccess = false;

    // コネクションの確立
    if(useArgBaudrate) {
        if(!drv)
            drv = RPlidarDriver::CreateDriver(DRIVER_TYPE_SERIALPORT);
        if(IS_OK(drv->connect(opt_com_path, opt_com_baudrate))) {
            op_result = drv->getDeviceInfo(devinfo);
            if(IS_OK(op_result)) {
                connectSuccess = true;
            }
            else {
                delete drv;
                drv = NULL;
            }
        }
    } else {
        size_t baudrateArraySize = (sizeof(baudrateArray)) / (sizeof(baudrateArray[0]));
        for(size_t i = 0; i < baudrateArraySize; ++i) {
            if(!drv)
                drv = RPlidarDriver::CreateDriver(DRIVER_TYPE_SERIALPORT);
            if(IS_OK(drv->connect(opt_com_path, baudrateArray[i]))) {
                op_result = drv->getDeviceInfo(devinfo);
                if(IS_OK(op_result)) {
                    connectSuccess = true;
                    break;
                } else {
                    delete drv;
                    drv = NULL;
                }
            }
        }
    }
    // コネクションができているかチェックする
    if(!connectSuccess) {
        fprintf(stderr, "Error, cannot bind to the specified serial port %s.\n",
                opt_com_path);
        goto on_finished;
    }

    // 接続されたRPLIDARのシリアル番号,ファームウェア,ハードウェアバージョン
    printf("RPLIDAR S/N: ");
    for(int pos = 0; pos < 16; ++pos) {
        printf("%02X", devinfo.serialnum[pos]);
    }
    printf("\n"
           "Firmware Ver : %d.%02d\n"
           "Hardware Ver : %d\n",
           devinfo.firmware_version >> 8,
           devinfo.firmware_version & 0xFF,
           (int)devinfo.hardware_version);

    // RPLIDARの状態を検査
    if(!checkRPLIDARHealth())
        goto on_finished;

    // scanDataThreadをスレッドとして実行
    pthread_t scanTh;
    pthread_create(&scanTh, NULL, scanDataThread, NULL);
    // pthread_detach(scanTh);

    // delay(8000);
    printf("restart\n");


    // Ctrl + cが入力されるまでスキャンする
    // while(!ctrl_c_pressed) {
    //     // op_result = drv->grabScanData(nodes, count);
    //
    //     // if(IS_OK(op_result)) {
    //         for(int pos = 0; pos < (int)count; ++pos) {
    //             // ログ出力
    //
    //             if(dp_on){
    //                 drv->ascendScanData(nodes, count);
    //                 fprintf(stderr,"%d : %s theta: %03.2f Dist: %08.2f Q: %d \n",
    //                     pos,
    //                    (nodes[pos].sync_quality & RPLIDAR_RESP_MEASUREMENT_SYNCBIT) ? "true ": "false",
    //                    (nodes[pos].angle_q6_checkbit >> RPLIDAR_RESP_MEASUREMENT_ANGLE_SHIFT) / 64.0f,
    //                    nodes[pos].distance_q2 / 4.0f,
    //                    nodes[pos].sync_quality >> RPLIDAR_RESP_MEASUREMENT_QUALITY_SHIFT);
    //             }
    //         }
    //     // }
    //     // if(ctrl_c_pressed)
    //     //     break;
    // }

    pthread_join(scanTh, NULL);

// on_stop:
    drv->stop();
    drv->stopMotor();

on_finished:
    RPlidarDriver::DisposeDriver(drv);
    drv = NULL;
    return 0;
}
