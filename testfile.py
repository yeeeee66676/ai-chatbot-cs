# #读
# f=open("./resourse/新建 文本文档.txt","r",encoding="utf-8")
#
# # contxt=f.read()#读取所有内容
#
# # contxt2=f.readline()#读取一行
# # context4=f.readline()
# # print(contxt2)
# # print(context4)
#
# contxt3=f.readlines()#读取所有内容
# print(contxt3)
#
# # print(contxt)
# f.close()

#写（try...finally）
# f=open("./resourse/静夜思.txt","r",encoding="utf-8")
#
# try:
#     f.write("静夜思（唐 李白）\n")
#     f.write("床前明月光\n")
#     f.write("疑是地上霜\n")
#     f.write("举头望明月\n")
#     f.write("低头思故乡\n")
# finally:
#     f.close()
    #or(推荐 使用with open)
with open("./resourse/静夜思.txt","w",encoding="utf-8") as f:
    f.write("静夜思（唐 李白）\n")
    f.write("床前明月光\n")
    f.write("疑是地上霜\n")
    f.write("举头望明月\n")
    f.write("低头思故乡\n")
