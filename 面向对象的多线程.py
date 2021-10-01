import threading
import time
from queue import Queue


# 写一个类,继承自threading.Thead
# 线程之间共享全局变量,操作同一对象时防止数据紊乱,此时用线程锁.谁先抢到锁谁先操作,其他线程只能等线程锁释放了之后再抢锁操作
# 需要写入数据的线程每个都要一把锁,只有加锁的线程会有先后顺序,未加锁线程不受影响.谁先上锁谁先操作,其他的等着释放了再抢谁先上锁
# 队列,用来存放和取出数据.下载和解析线程通过队列进行交互


class Singthread(threading.Thread):
    def __init__(self, name, fp, suo, q):
        # 此处继承了第三方的类,要注意手动调用父类的构造方法(__init__)
        super().__init__()
        self.name = name
        self.fp = fp
        self.suo = suo
        self.q = q

    # 实例化后start方法执行的函数就是run函数
    def run(self):
        time.sleep(5)
        # 停5秒,跳舞线程先上锁,跳舞线程锁释放后,唱歌线程上锁
        self.suo.acquire()
        for item in range(1, 4):
            sentence = "I am singing %d\n" % item
            # self.fp.write(sentence)
            self.q.put(sentence)
            time.sleep(1)
        self.fp.write('唱歌线程结束\n')
        self.suo.release()


class Dancethread(threading.Thread):
    def __init__(self, name, fp, suo, q):
        super().__init__()
        self.name = name
        self.fp = fp
        self.suo = suo
        self.q = q

    def run(self):
        self.suo.acquire()
        for item in range(1, 4):
            sentence = "I am dancing %d\n" % item
            # self.fp.write(sentence)
            self.q.put(sentence)
            time.sleep(1)
        self.fp.write('跳舞线程结束\n')
        self.suo.release()


def main():
    fp = open('test.py', 'a', encoding='utf8')
    suo = threading.Lock()
    q = Queue(10)
    tsing = Singthread('孙悟空', fp, suo, q)
    tdance = Dancethread('猪八戒', fp, suo, q)
    tsing.start()
    tdance.start()
    tsing.join()
    tdance.join()
    fp.close()
    print(q.get())
    print("主线程已结束")


if __name__ == '__main__':
    main()
