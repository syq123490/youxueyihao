a = int(input("请输入待开方数："))
for i in range(1,200):
	for j in range(200):
		if i==1 and a==j*j:
			print("开方结果为：",j)
			break
		else:
			if a==i*j*j and j!=1:
				print("开方结果为：{}X根号下（{}）".format(j,i))
				break
	if a==j*j or a==i*j*j:
		break
	else:
		if i>=199:
			print("开方结果为:根号下（{}）".format(a))
			break