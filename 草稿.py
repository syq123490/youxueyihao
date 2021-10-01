def demo():
    for item in range(1, 11):
        yield item


def main():
    x = demo()
    print(next(x))
    print(next(x))
    print(next(x))
    print(next(x))
    print(next(x))


if __name__ == '__main__':
    main()