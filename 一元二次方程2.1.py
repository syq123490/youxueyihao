from fractions import Fraction 		#调用Fraction函数
a = int(input('请输入a的值：'))
b = int(input('请输入b的值：'))
c = int(input('请输入c的值：'))
delta = b*b-4*a*c
# 存储变量a,b,c,delta
if delta < 0:				#判断方程是否有实数根
	print('\n'*3+'方程无实数根')
else:
	if delta**0.5 == int(delta**0.5):		#判断根号下delta是否为整数
		result1 = Fraction(int((-b)-delta**0.5),int(a*2))		#使用Fraction函数输出分数结果
		result2 = Fraction(int((-b)+delta**0.5),int(a*2))		
		print("方程的第一个根为：{}\n方程的第二个根为：{}".format(result1,result2))
	else:		#无法直接得结果，输出直观表达))		
		for i in range(2000):		##添加开方程序
			for j in range(2000):
				if delta==i*j*j and j!=1:		#判断是否能开出整数
					print('X1分子：{}-{}根号（{}）'.format(-b,j,i))
					print('X1分母：{}'.format(a*2))
					print('\n'*2)
					print('X2分子：{}+{}根号（{}）'.format(-b,j,i))
					print('X2分母：{}'.format(a*2))
					break		#能开出，结束里层循环
				else:
					pass
			if delta==j*j or delta==i*j*j:		##能开出，结束外层循环
				break
			else:
				if i>=1999:
					print('X1分子：{}-根号({})'.format(-b,delta))
					print('X1分母：{}'.format(a*2))
					print('\n'*2)
					print('X2分子：{}+根号({})'.format(-b,delta))
					print('X2分母：{}'.format(a*2))
					break		##不能开出，结束外层循环

