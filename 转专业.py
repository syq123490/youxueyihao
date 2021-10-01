import xlrd
import pprint

number = 0
emptylist = ["智矿2001","智矿2002"]
emptylist1 = []
list_dalei = [
    '人工智能',
    '环境工程',
    '给排水科学与工程',
    '水利水电工程',
    '水文与水资源工程',
    '农业水利工程',
    '土木工程',
    '建筑环境与能源应用工程',
    '道路桥梁与渡河工程',
    '安全工程',
    '应急技术与管理',
    '地质工程',
    '测绘工程',
    '资源勘查工程',
    '采矿工程',
    '矿物加工工程',
    '城市地下空间工程',
    '工程管理']
data = xlrd.open_workbook("附件1：令德书院-采矿工程-姚冬洁.xls")
sheet = data.sheet_by_index(0)
banji = sheet.col_values(3)
print(banji)
for i in banji:
    if i in emptylist:
        number+=1
        emptylist1.append(i)
print(number)
print(emptylist1)
# for i in list_laizi:
#     if i in list_dalei:
#         print(i)
#         number +=1
# 统计基础学院总共转出人数


# list_zhuanru = list(enumerate(list_zhuanru))
# for i in list_zhuanru:
#     if i[1] == '计算机科学与技术':
#         emptylist.append(list_laizi[i[0]])
# for i in emptylist:
#     if i in list_dalei:
#         number +=1
#         print(i)
#         print("")
# print(number)