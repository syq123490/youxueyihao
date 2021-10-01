import threading
import time


def sing(a):
    print("线程为%s,接收到的参数为%s", threading.current_thread().name, a)
    for i in range(1, 6):
        print("I'm singing")
        time.sleep(1)


def dance(a):
    print("线程为%s,接收到的参数为%s", threading.current_thread().name, a)
    for i in range(1, 6):
        print("I'm dancing")
        time.sleep(1)


def main():
    a = '孙悟空'
    tsing = threading.Thread(target=sing, name='唱歌线程', args=(a, ))
    tdance = threading.Thread(target=dance, name='跳舞线程', args=(a, ))
    tsing.start()
    print("主线程正在运行1")
    tdance.start()
    print("主线程正在运行2")
    tsing.join()
    tdance.join()
    print("主线程结束")


if __name__ == '__main__':
    main()
