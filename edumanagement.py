#学生类
from random import choice


class Student:
    def __init__(self,name,chinese,math,english):
        self.name=name
        self.chinese=chinese
        self.math=math
        self.english=english

    def __str__(self) :
        return f"姓名：{self.name}|语文：{self.chinese}|数学：{self.math}|英语：{self.english},总分：{self.chinese+self.math+self.english}"
#修改学生成绩
    def update_score(self,chinese=None,math=None,english=None):
        if chinese is not None:
            self.chinese=chinese
        if math is not None:
            self.math=math
        if english is not None:
            self.english=english

class edu:
    system_version="1.0"
    system_name="EDU"

    def __init__(self):

        #学生成绩信息
        self.student_list=[]

    #添加成绩
    def add(self):
        name=input("输入学生姓名：")

        #判断是否存在，不能重复
        for s in self.student_list:
            if s.name==name:
                print("已存在，失败")
                return
        chinese=int(input("输入学生语文成绩："))
        math=int(input("输入学生数学成绩："))
        english=int(input("输入学生英语成绩："))

        #判断分数是否再0-100
        if 0<=chinese<=100 and 0<=math<=100 and 0<=english<=100:
            stu=Student(name,chinese,math,english)
            self.student_list.append(stu)
            print("添加成功")
        else:
            print("分数需要在0-100")
    #修改
    def update(self):
        name = input("输入待修改学生姓名：")

        # 找到学生信息
        for s in self.student_list:
            if s.name == name:
                print(f"{s}")
                chinese = int(input("输入学生新语文成绩："))
                math = int(input("输入学生新数学成绩："))
                english = int(input("输入学生新英语成绩："))
                if 0<=chinese<=100 and 0<=math<=100 and 0<=english<=100:
                    s.update_score(chinese,math,english)
                    print("修改成功")
                    print(f"新成绩：{s}")
                    return
                else:
                    print("分数需要在0-100")
                    return
        print("未找到该学生")
    #删除
    def dele(self):
        name = input("输入待删除学生姓名：")
        for s in self.student_list:
            if s.name == name:
                self.student_list.remove(s)
                print("删除成功")
                return
        print("未找到")
    #查询
    def query(self):
        name = input("输入查询学生姓名：")
        for s in self.student_list:
            if s.name == name:
                print(f"学生信息为：{s}")
                return
        print("未找到")

    #展示全部学生信息
    def list(self):
        for s in self.student_list:
            print(s)

    #运行系统方法
    def run(self):
        print(f"欢迎\n V{edu.system_version}")

        while True:
            print()
            print("#"*50)
            print("1.添加  2.修改  3.删除  4.查询指定  5。查询所有  6.exit")
            print("#"*50)
            choice=input("\n输入1-6:\n")
            match choice:
                case "1":
                    self.add()
                case"2":
                    self.update()
                case"3":
                    self.dele()
                case"4":
                    self.query()
                case"5":
                    self.list()
                case"6":
                    print("bye!")
                    break
                case _:
                    print("输入1-6")




if __name__=='__main__':
    edu1=edu()
    edu1.run()