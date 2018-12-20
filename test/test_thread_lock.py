import threading

cnt = 0
def count():
    global cnt
    lim = 100

    while True:
        cnt += 1
        print(cnt)
        if cnt > lim:
            cnt = 0
            lim -= 1

def flush():
    global cnt
    while True:
        print(cnt)
        if cnt % 7 == 0:
            print("div 7 = 0")

th1 = threading.Thread(target=count)
th2 = threading.Thread(target=flush)
th1.start()
th2.start()
th1.join()
th2.join()

