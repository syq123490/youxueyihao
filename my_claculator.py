import statistics
import math


def record():
    time = 1
    data = []
    while 1:
        number = float(input('请输入第%d次测量结果:' % time))
        if number == 00:
            break
        data.append(number)
        time = time + 1
    return data


class Calculator(object):
    def __init__(self, datalist):
        self.datalist = datalist

    def cal_average(self):
        '''
        该函数用以计算平均值,需传入一个实验数据列表
        '''
        raverage = statistics.mean(self.datalist)
        print('本组实验平均值为:{}'.format(raverage))
        average = float(input('修正平均值(通常为两位小数):'))
        if average == 00:
            average = raverage
        return average

    def cla_Bbzc(self, xbar):
        '''
        计算实验标准差,需传入实验数据列表,返回实验标准差
        '''
        rstdev = statistics.stdev(self.datalist, xbar=xbar)
        print('实验标准差为:{}'.format(rstdev))
        stdev = float(input('实验标准差修正:'))
        if stdev == 00:
            stdev = rstdev
        return stdev

    def cla_judge(self, Bbzc, average):
        wronglist = []
        for i in self.datalist:
            if average - i > Bbzc * 3 or i - average > Bbzc * 3:
                print('{}数据异常'.format(i))
                wronglist.append(i)
        print('异常数据为{}'.format(wronglist))
        return wronglist

    def cla_uncertainA(self, shiyanbzc):
        '''
        传入实验标准差(用以计算算术平均值标准差),与测量次数和置信概率有关的t因子
        '''
        rsuanshubzc = shiyanbzc / math.sqrt(len(self.datalist))
        print('算术平均值标准差差为:{}'.format(rsuanshubzc))
        suanshubzc = float(input('修正算术标准差(通常为三位小数):'))
        if suanshubzc == 00:
            suanshubzc = rsuanshubzc
        t = float(input('查表,t因子为:'))
        uncertainA = suanshubzc * t
        print('A类不确定度为:{}'.format(uncertainA))
        return uncertainA

    def cla_finaluncertain(self, uncertainA, uncertainB):
        finaluncertain = math.sqrt(
            math.pow(uncertainA, 2) + math.pow(uncertainB, 2))
        print('最终不确定度为:{}'.format(finaluncertain))
        return finaluncertain


def main():
    qidong = int(input('输入00默认启动'))
    if qidong == 00:
        firstdata = record(  )
    else:
        firstdata = [3.787, 3.782, 3.789, 3.784, 3.781, 3.785, 3.783, 3.781]
    cla = Calculator(firstdata)
    average = cla.cal_average()
    shiyanbzc = cla.cla_Bbzc(average)
    print('实验标准差为:{}'.format(shiyanbzc))
    wronglist = cla.cla_judge(shiyanbzc, average)
    uncertainA = cla.cla_uncertainA(shiyanbzc=shiyanbzc)
    uncertainB = float(input('请输入不确定度B:'))
    finaluncertain = cla.cla_finaluncertain(uncertainA, uncertainB)
    fp = open(
        file='物理实验数据.txt',
        mode='a',
    )
    fp.write(str(firstdata))
    fp.close()


if __name__ == '__main__':
    main()
