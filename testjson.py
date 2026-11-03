import json

user={
    "name":"张三",
    "age":18,
    "sex":"男",
    "hobbies":["抽烟","喝酒","烫头"]
}
#写入
#indent:缩进，ensure_ascii:是否将非ascii字符(中文)转换为ascii字符
# with open("./resourse/user.json","w",encoding="utf-8") as f:
#     json.dump(user,f,ensure_ascii=False,indent=4)
#读取
with open("./resourse/user.json","r",encoding="utf-8") as f:
    user=json.load(f)
    print(user)
    print(type(user))