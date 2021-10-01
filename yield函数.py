def demo():
    '''
    函数中出现yield后,代表函数为生成器.生成器并非一次生成所有数据,而是保存数据的生存方式,调用一次生成一个
    '''
    for item in range(1, 4):
        yield item
        print('嘿嘿嘿')
    yield '哈哈哈'
    # 函数中可以返回多个yield


def main():
    x = demo()
    # x为生成器
    print(next(x))
    # 使用next方法调用生成器,执行demo函数第一个循环,返回item=1.函数停在yield处
    print(next(x))
    # demo函数从yield开始执行下一行打印嘿嘿嘿,进入第二次循环,返回item=2,函数停在yield处
    print(next(x))
    # demo函数从yield开始执行下一行打印嘿嘿嘿,进入第三次循环,返回item=3,函数停在yield处
    print(next(x))
    # demo函数从yield开始执行下一行打印嘿嘿嘿,结束循环.下一步返回哈哈哈,函数停在yield处
    # print(next(x))


if __name__ == '__main__':
    main()