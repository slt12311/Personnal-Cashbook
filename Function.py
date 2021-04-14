#账单管理

import Analyze
from tkinter import *
import tkinter.messagebox
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import scrolledtext
from PIL import ImageTk, Image
import re
import decimal
from builtins import str
import numpy as np

#添加账单
class Add:
    #跳转主界面
    def d_return(self):
        self.root.destroy()
        self.goMain(user=self.user)

    #功能函数：
    #类型统计
    def typeWehave(self):
        #初始类型
        self.type=['食物','交通','服饰','日用品','娱乐','其他']
        #已存在类型（读取数据库）
        sql="select distinct type from [%s]"%self.table
        alltype=self.con.execute(sql)
        for i in alltype:
            i[0] = "".join(i[0].split())
            if(i[0] not in self.type):
                self.type.append(i[0])
    #清空输入
    def clearin(self):
        self.e1.delete(0, END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.e4.delete(0, END)
        self.e5.delete(0, END)
        # self.numberChosen2.current(0)
        # self.numberChosen.current(0)
    #日期输入合法性
    def timeallow(self):
        time=[self.e3.get(),self.e4.get(),self.e5.get()]
        #是否数字
        for i in range(3):
            if(time[i].isdecimal()!=1):
                return i+1
        year=int(time[0])
        month=int(time[1])
        date=int(time[2])
        #分别检验年月日输入的正确性
        if(year>2021 or year<1900):
            return 1
        if(month<1 or month>12):
            return 2
        if(date<1 or date>31):
            return 3
        rday = [ 31, 29,  31, 30,  31,  30,  31,  31,  30, 31, 30,
                 31]
        nrday = [ 31, 28,  31, 30,  31,  30,  31,  31,  30, 31, 30,
                 31]
        flag=0
        #闰年判断-判断具体月份、日期的正确性
        if (year % 4) == 0:
            if (year % 100) == 0:
                if (year % 400) == 0:
                    flag=1
            else:
                flag=1
        if(flag==1):
            if(date>rday[month-1]):
                return 3
        else:
            if(date>nrday[month-1]):
                return 3
        self.time=str(year)+'-'+str(month)+'-'+str(date)
        return 0
    #通常输入合法性（空/长度/空格）
    def inputcheck(self,str,name):
        if(len(str)==0):
            tkinter.messagebox.showwarning('警告', '未输入%s'%name)
            return 1
        if(len(str)>20):
            tkinter.messagebox.showwarning('警告', '%s长度大于20字符' % name)
            return 1
        if(' ' in str):
            tkinter.messagebox.showwarning('警告', '%s字符串中含有空格' % name)
            return 1
        return 0
    #能否添加
    def ifAdd(self):
        #输入合法性
        j=self.timeallow()
        reason=['年','月','日']
        #日期输入
        for i in range(3):
            if(j==i+1):
                tkinter.messagebox.showwarning('警告', '您日期中的“%s”未正确输入' %reason[i])
                self.clearin()
                return
        #金额输入
        test0=self.e2.get()
        test=test0.split('.')
        if(test[0].isdecimal()!= TRUE):
            tkinter.messagebox.showwarning('警告', '您的金额未正确输入' )
            self.clearin()
            return
        #其他输入
        tmp=[self.e1.get(),self.numberChosen.get(),float(test0),self.time,self.numberChosen2.get()]
        name=['名称','类型','金额','日期','属性']
        for i in [0,1,4]:
            a=self.inputcheck(tmp[i],name[i])
            if (a == 1):
                self.clearin()
                return
        if(tmp[2]<0):
            tkinter.messagebox.showwarning('警告', '请检查金额输入是否有误')
            self.clearin()
            return

        # 成功添加
        #数据库修改
        self.con.execute('''SELECT num FROM [%s] where num=(select max(num) from %s)'''%(self.table,self.table))
        search=self.con.fetchone()
        if(search==None):
            num=1
        else:
            num=int(search[0]+1)
        sql_insert = '''insert into [%s] values(%d,'%s','%s',%f,'%s','%s')''' % (self.table,num,tmp[0],tmp[1],tmp[2],tmp[3],tmp[4])
        #txt记录
        with open('./%s/%s.txt' % (self.table,self.table), mode='a') as filename:
            filename.write('add %s %s %.2f %s %s'%(tmp[0],tmp[1],tmp[2],tmp[3],tmp[4]))
            filename.write('\n')  # 换行
        self.con.execute(sql_insert)
        self.con.commit()
        tkinter.messagebox.showinfo('提示', '添加成功')
        #返回主面板
        self.root.destroy()
        tmp = self.goMain(user=self.user)

    #界面构建
    def __init__(self,con,user,goMain):
        self.con=con
        self.user=user
        self.table="user"+user
        self.goMain=goMain
        self.root=Tk()
        Analyze.goHelp(root=self.root)
        self.root.title("添加一条新记账")
        self.root.resizable(0, 0)
        self.root.geometry('500x300')

        image1 = Image.open('source/鸟底纹素材.png')
        back_image = ImageTk.PhotoImage(image1)
        image2 = Image.open('source/045-trumpet.png')
        back_image2 = ImageTk.PhotoImage(image2)
        Label(self.root, image=back_image).place(x=0, y=0)
        Label(self.root, image=back_image2, borderwidth=0).place(relx=0.4, rely=0)

        # 名称
        Label(self.root, text="名称").place(relx=0.22, rely=0.2)
        self.e1 = Entry(self.root)
        self.e1.place(relx=0.35, rely=0.2, relwidth=0.3)

        #类型
        self.typeWehave()
        Label(self.root, text="类型").place(relx=0.22, rely=0.3)
        number = StringVar()
        self.numberChosen = ttk.Combobox(self.root, width=12, textvariable=number)
        self.numberChosen['values'] = self.type
        self.numberChosen.place(relx=0.35,rely=0.3)
        self.numberChosen.current(0)

        #金额
        Label(self.root, text="金额").place(relx=0.22, rely=0.4)
        Label(self.root, text="￥").place(relx=0.3, rely=0.4)
        self.e2 = Entry(self.root)
        self.e2.place(relx=0.35, rely=0.4, relwidth=0.3)

        #日期
        Label(self.root, text="日期").place(relx=0.22, rely=0.5)
        Label(self.root, text="年").place(relx=0.46, rely=0.5)
        self.e3 = Entry(self.root)
        self.e3.place(relx=0.35, rely=0.5, relwidth=0.1)
        Label(self.root, text="月").place(relx=0.61, rely=0.5)
        self.e4 = Entry(self.root)
        self.e4.place(relx=0.5, rely=0.5, relwidth=0.1)
        Label(self.root, text="日").place(relx=0.76, rely=0.5)
        self.e5 = Entry(self.root)
        self.e5.place(relx=0.65, rely=0.5, relwidth=0.1)

        #属性
        Label(self.root, text="属性").place(relx=0.22, rely=0.6)
        number2 = StringVar()
        self.numberChosen2 = ttk.Combobox(self.root, width=12, textvariable=number2,state='readonly')
        self.numberChosen2['values'] = ('支出','收入')
        self.numberChosen2.place(relx=0.35, rely=0.6)
        self.numberChosen2.current(0)

        Button(self.root, text="确定", bg='snow',command=self.ifAdd).place(relx=0.4, rely=0.7)
        Button(self.root, text="取消",  bg='snow',command=self.d_return).place(relx=0.5, rely=0.7)
        self.root.mainloop()

#账目显示
#账目显示（主界面）
class Check:
    #按照月份记录账单日期
    def allRecord(self):
        sql = '''SELECT distinct time FROM [%s]'''%self.table
        self.con.execute(sql)
        tables = self.con.fetchall()
        if(len(tables)==0):
            return 0
        old_list=[]
        self.table_list=[]
        #获取日期中年-月
        for i in tables:
            i=str(i)[2:]
            a=re.match(r'(.*?)(?:-)(.*?)(?:-)', str(i))
            tmp = []
            tmp.append(int(a.group(1)))
            tmp.append(int(a.group(2)))
            old_list.append(tmp)
        #去重复
        for i in old_list:
            if i not in self.table_list:
                self.table_list.append(i)
        self.table_list= np.array(self.table_list)
        #排序
        idex = np.lexsort([-1 * self.table_list[:, 1], -1*self.table_list[:, 0]])
        sorted_data = self.table_list[idex, :]
        self.table_list=[]
        for i in sorted_data:
            str1=str(i[0])+'-'+str(i[1])
            self.table_list.append(str1)

        return 1

    #账目显示
    def __init__(self,root,con,user,goMain):
        self.con=con
        self.user=user
        self.table='user'+user
        self.goMain=goMain

        #界面搭建
        self.root = root
        scr = scrolledtext.ScrolledText(self.root, width=70, height=13)
        scr.place(relx=0, rely=0.07)
        a=self.allRecord()#获取日期

        if(a==0):#是否有记账数据
            scr.insert(END, "暂无记账数据")
            scr.config(state=DISABLED)
            return

        ft = tkFont.Font(weight=tkFont.BOLD)
        scr.tag_add('tag',END)
        scr.tag_config('tag', font=ft)
        scr.tag_add('tag1', END)
        scr.tag_config('tag1', foreground='MediumAquamarine',font=ft)
        scr.tag_add('tag2', END)
        scr.tag_config('tag2', foreground='LightCoral', font=ft)

        #插入记账记录
        endsum=0#总净支出/收入
        sum1=0#计数
        for i in self.table_list:
            scr.insert(END, i,'tag')
            scr.insert(END, '\n')
            sql="select * from [%s] where time like '%%%s-%%'"%(self.table,i)
            self.con.execute(sql)
            result=self.con.fetchall()
            sum=0
            for j in result:
                sum1+=1
                for k in [1,2,4,5]:
                    j[k] = "".join(j[k].split())
                record='属性:'+str(j[5])+"  名称:"+str(j[1])+'  类型:'+str(j[2])+'  金额:'+str(j[3])+'  日期:'+str(j[4])
                if(j[5]=='支出'):#统计月支出/收入
                    sum+=j[3]
                else:
                    sum-=j[3]
                scr.insert(END,record)
                scr.insert(END, '\n')
                if (sum1 >= 30):#已显示账目数量控制
                    break
            scr.insert(END, '\n')
            #月净支出/收入
            endsum+=sum
            if(sum>0):
                addup="                 净支出:￥"+str(sum)
                scr.insert(END,addup,'tag')
            else:
                sum=-sum
                addup="                 净收入:￥"+str(sum)
                scr.insert(END, addup, 'tag')
            scr.insert(END, '\n\n')

        #总净支出/收入
        if (endsum > 0):
            addup = "总净支出:￥" + str(endsum)
            scr.insert(END, addup, 'tag2')
        else:
            endsum = -endsum
            addup = "总净收入:￥" + str(endsum)
            scr.insert(END, addup, 'tag1')
        scr.insert(END, "\n\n只显示30条记账信息，以上可能非全部记录")
        scr.config(state=DISABLED)
#账目显示（查询/删除界面）
class Show:
    #tag:1-查询到记录/0-未查询到记录
    #aim:1-跳转删除/0-跳转修改
    def showCheck(self,tag,aim):
        #界面
        self.root = Tk()
        self.root.title("查询结果")
        Analyze.goHelp(root=self.root)
        self.root.resizable(0, 0)
        self.root.geometry('500x300')
        image1 = Image.open('source/鸟底纹素材.png')
        back_image = ImageTk.PhotoImage(image1)
        Label(self.root, image=back_image).place(x=0, y=0)
        record=[]
        #是否有记录
        if (tag == 1):
            #结果记录文本处理
            for j in self.result:
                for k in [1, 2, 4, 5]:
                    j[k] = "".join(j[k].split())
                record.append ( '属性:' + str(j[5]) + "  名称:" + str(j[1]) + '  类型:' + str(j[2]) + '  金额:' + str(
                    j[3]) + '  日期:' + str(j[4]))
        else:
            str1 = "没有查询到指定的记账记录！"

        #跳转删除
        if(aim==1):
            #界面
            scr = scrolledtext.ScrolledText(self.root, width=70, height=13)
            scr.place(relx=0, rely=0.07)
            if(tag==1):
                for i in record:
                    scr.insert(END, i)
                    scr.insert(END, '\n')
            else:
                scr.insert(END,str1)
            scr.config(state=DISABLED)
            Button(self.root, text="确定", bg='snow', command=self.b_return).place(relx=0.5, rely=0.8)
        else:#跳转修改
            sc = Scrollbar(self.root)
            sc.pack(side=RIGHT, fill=Y)

            self.lb = Listbox(self.root, yscrollcommand=sc.set)
            self.lb.pack(side=LEFT, fill=BOTH, expand=True)
            if (tag == 1):
                for i in record:
                    self.lb.insert(END, i)
                    sc.config(command=self.lb.yview)
                    if(aim==0):
                        Button(self.root, text="确定",  bg='snow',command=self.go_Change).place(relx=0.4, rely=0.8)
                    else:
                        Button(self.root, text="确定",  bg='snow',command=self.go_Dele).place(relx=0.4, rely=0.8)
                    Button(self.root, text="取消", bg='snow', command=self.b_return).place(relx=0.6, rely=0.8)
            else:
                self.lb.insert(END, str1)
                sc.config(command=self.lb.yview)
                Button(self.root, text="确定", bg='snow', command=self.b_return).place(relx=0.4, rely=0.8)
                Button(self.root, text="取消",  bg='snow',command=self.b_return).place(relx=0.6, rely=0.8)

            self.root.mainloop()

#账单查询
class Search:
    #跳转
    #跳转删除
    def go_Dele(self):
        choose=self.lb.curselection()
        if(len(choose)==0):
            tkinter.messagebox.showwarning("警告","没有选择任何记录！")
            self.b_return()
        tochange=self.result[choose[0]]
        self.root.destroy()
        Dele(goMain=self.goMain,user=self.user,con=self.con,todele=tochange)
    #跳转修改
    def go_Change(self):
        choose=self.lb.curselection()
        if(len(choose)==0):
            tkinter.messagebox.showwarning("警告","没有选择任何记录！")
            self.b_return()
        tochange=self.result[choose[0]]
        self.root.destroy()
        Change(goMain=self.goMain,user=self.user,con=self.con,tochange=tochange)
    #跳转主界面
    def b_return(self):
        self.root.destroy()
        self.goMain(user=self.user)

    #功能函数
    #查询输入合法性
    def RightSe(self):
        self.num=[]#记录非空输入
        name=['名称','类型','金额','年','月','日','属性']
        self.str0=[self.e1.get(),self.numberChosen.get(),self.e2.get(),self.e3.get(),self.e4.get(),self.e5.get(),self.numberChosen2.get()]
        for i in range(7):
            if(len(self.str0[i])!=0):
                self.num.append(i)
        #查询输入为空
        if(len(self.num)==0):
            return 1
        #检查通用输入合法性
        for i in [0,1,2,6]:
            if(i in self.num):
                if (len(self.str0[i]) > 20):
                    tkinter.messagebox.showwarning('警告', '%s长度大于20字符' % name[i])
                    Add.clearin(self=self)
                    return 0
                if (' ' in self.str0[i]):
                    tkinter.messagebox.showwarning('警告', '%s字符串中含有空格' % name[i])
                    Add.clearin(self=self)
                    return 0
        #检查日期合法性
        time=[[1900,2021],[1,12],[1,31]]
        for i in [3,4,5]:
            if(i in self.num):
                if(self.str0[i].isdecimal()!=1):
                    tkinter.messagebox.showwarning('警告', '日期中 %s 未正确输入' % name[i])
                    Add.clearin(self=self)
                    return 0
                self.str0[i]=int(self.str0[i])
                if(self.str0[i]<time[i-3][0] or self.str0[i]>time[i-3][1]):
                    tkinter.messagebox.showwarning('警告', '日期中 %s 未正确输入' % name[i])
                    Add.clearin(self=self)
                    return 0
        #检查金额合法性
        if(2 in self.num):
            test =self.str0[2].split('.')
            if (test[0].isdecimal() != TRUE):
                tkinter.messagebox.showwarning('警告', '您的金额未正确输入')
                Add.clearin(self=self)
                return 0
            self.str0[2]=float(self.str0[2])
        return 2
    #判断查询内容
    def ifse(self):
        #查找合法性
        res=self.RightSe()
        if(res==1):#输入合法/查询输入为空（显示所有记账记录）
            #数据库查询
            self.root.destroy()
            sql = "select * from [%s] ORDER BY time desc" % (self.table)
            self.con.execute(sql)
            self.result = self.con.fetchall()
            #数据显示
            if(len(self.result)==0):
                Show.showCheck(self=self,tag=0,aim=self.choice)
            else:
                Show.showCheck(self=self,tag=1,aim=self.choice)
        elif(res==2):#输入合法/查询非空
            self.Dosearch(resu=self.str0, num=self.num)
        else:#输入非法
            return
    #进行查询
    def Dosearch(self,resu,num):
        name=['name','type','money','年','月','日','prime']
        #输入日期文本处理
        time=''
        for i in [3,4,5]:
             if(i in num):
                if(i==3):
                    time+=str(resu[i])
                else:
                    time+='-'+str(resu[i])
        check=[]
        for i in num:
            if(i not in [3,4,5]):
                check.append(i)
        #首先从数据库通过日期查询
        if(time!=''):
            sql = "select * from [%s] where time like '%%%s%%'" % (self.table, time)
            self.con.execute(sql)
            self.result = self.con.fetchall()
        else:#若未输入日期，则从第一个输入查询
            sql= "select * from [%s] where %s = '%s'" % (self.table,name[check[0]],resu[check[0]])
            self.con.execute(sql)
            self.result = self.con.fetchall()
        #非日期查询输入：0项或1项（已完成条件查询）
        if(len(check)==0 or len(check)==1):
            self.root.destroy()
            if(len(self.result)==0):#查询结果为空
                Show.showCheck(self=self,tag=0,aim=self.choice)
            else:
                Show.showCheck(self=self,tag=1,aim=self.choice)
            return

        #仍有其他未查询条件
        for i in self.result:
            for k in [1, 2, 5]:
                i[k] = "".join(i[k].split())
            for j in check:
                if(j==check[0]):continue
                if(j in [1,2,0]):
                    if(i[j+1]!=resu[j]):
                        del self.result[i]
                        break
                else:
                    if(i[5]!=resu[j]):
                        del self.result[i]
                        break
        self.root.destroy()
        #查询结果显示
        if(len(self.result)==0):
            Show.showCheck(self=self,tag=0,aim=self.choice)
        else:
            Show.showCheck(self=self,tag=1,aim=self.choice)

    #查询主界面
    def __init__(self,con,user,goMain,choice):
        self.con = con
        self.user = user
        self.table = "user" + user
        self.choice=choice
        self.goMain = goMain
        self.root = Tk()
        Analyze.goHelp(root=self.root)
        self.root.title("查询记账")
        self.root.resizable(0, 0)
        self.root.geometry('500x300')
        # 界面美化
        image1 = Image.open('source/鸟底纹素材.png')
        back_image = ImageTk.PhotoImage(image1)
        image2 = Image.open('source/Drums.png')
        back_image2 = ImageTk.PhotoImage(image2)
        Label(self.root, image=back_image).place(x=0, y=0)
        Label(self.root, image=back_image2, borderwidth=0).place(relx=0.4, rely=0)

        # 界面控件
        # 名称
        Label(self.root, text="名称").place(relx=0.22, rely=0.2)
        self.e1 = Entry(self.root)
        self.e1.place(relx=0.35, rely=0.2, relwidth=0.3)

        # 类型
        Add.typeWehave(self=self)
        self.type.append('')
        Label(self.root, text="类型").place(relx=0.22, rely=0.3)
        number = StringVar()
        self.numberChosen = ttk.Combobox(self.root, width=12, textvariable=number)
        self.numberChosen['values'] = self.type
        self.numberChosen.place(relx=0.35, rely=0.3)
        self.numberChosen.current(len(self.type) - 1)

        # 金额
        Label(self.root, text="金额").place(relx=0.22, rely=0.4)
        Label(self.root, text="￥").place(relx=0.3, rely=0.4)
        self.e2 = Entry(self.root)
        self.e2.place(relx=0.35, rely=0.4, relwidth=0.3)

        # 日期
        Label(self.root, text="日期").place(relx=0.22, rely=0.5)
        Label(self.root, text="年").place(relx=0.46, rely=0.5)
        self.e3 = Entry(self.root)
        self.e3.place(relx=0.35, rely=0.5, relwidth=0.1)
        Label(self.root, text="月").place(relx=0.61, rely=0.5)
        self.e4 = Entry(self.root)
        self.e4.place(relx=0.5, rely=0.5, relwidth=0.1)
        Label(self.root, text="日").place(relx=0.76, rely=0.5)
        self.e5 = Entry(self.root)
        self.e5.place(relx=0.65, rely=0.5, relwidth=0.1)

        # 属性
        Label(self.root, text="属性").place(relx=0.22, rely=0.6)
        number2 = StringVar()
        self.numberChosen2 = ttk.Combobox(self.root, width=12, textvariable=number2, state='readonly')
        self.numberChosen2['values'] = ('', '支出', '收入')
        self.numberChosen2.place(relx=0.35, rely=0.6)
        self.numberChosen2.current(0)
        Button(self.root, text="确定", bg='snow',command=self.ifse).place(relx=0.4, rely=0.7)
        Button(self.root, text="取消", bg='snow',command=self.b_return).place(relx=0.5, rely=0.7)
        self.root.mainloop()

#账单修改
class Change:
    #返回主界面
    def b_return(self):
        self.root.destroy()
        self.goMain(user=self.user)
    #信息合法性与实施修改
    def ifchange(self):
        #修改信息合法性判断
        resu=Search.RightSe(self)
        if(resu==1):
            tkinter.messagebox.showwarning('警告', '未输入修改信息' )
            return
        elif(resu==2):
            #判断新日期组合后是否正确
            time=self.tochange[4]
            time=time.split(' ')[0]
            test=time.split('-',3)
            for i in [3,4,5]:
                if (i in self.num):
                    test[i-3]=self.str0[i]
                test[i-3]=int(test[i-3])
            rday = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30,
                    31]
            nrday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30,
                     31]
            flag = 0
            if (test[0] % 4) == 0:
                if (test[0] % 100) == 0:
                    if (test[0] % 400) == 0:
                        flag = 1
                else:
                    flag = 1
            if (flag == 1):
                if (test[2] > rday[test[1] - 1]):
                    tkinter.messagebox.showwarning('警告', '日期输入有误')
                    Add.clearin(self=self)
                    self.insertinfo()
                    return
            else:
                if (test[2] > nrday[test[1] - 1]):
                    tkinter.messagebox.showwarning('警告', '日期输入有误')
                    Add.clearin(self=self)
                    self.insertinfo()
                    return
            time=str(test[0])+'-'+str(test[1])+'-'+str(test[2])
        else:
            self.insertinfo()
            return
        #更新记账信息
        for i in [0,1,2]:
            if(i in self.num):
                self.tochange[i+1]=self.str0[i]
        if(6 in self.num):
            self.tochange[5]=self.str0[6]
        self.tochange[4]=time

        #数据库更新
        sql_insert = '''update [%s] set name='%s',type='%s',money=%f,time='%s',prime='%s' where num=%d'''% (
        self.table, self.tochange[1], self.tochange[2], self.tochange[3], self.tochange[4], self.tochange[5], self.tochange[0])
        #txt更新
        with open('./%s/%s.txt' % (self.table,self.table), mode='a') as filename:
            filename.write('BeforeChange %s %s %.2f %s %s' % (
            self.nochange[1], self.nochange[2], self.nochange[3], self.nochange[4], self.nochange[5]))
            filename.write('\n')
            filename.write('AfterChange %s %s %.2f %s %s' % (self.tochange[1], self.tochange[2], self.tochange[3], self.tochange[4],self.tochange[5]))
            filename.write('\n')  # 换行
        self.con.execute(sql_insert)
        self.con.commit()
        tkinter.messagebox.showinfo('提示', '修改成功')
        self.root.destroy()
        tmp = self.goMain(user=self.user)
    def insertinfo(self):
        self.e1.insert(0, self.tochange[1])
        self.numberChosen.current(self.type.index(self.tochange[2]))
        num = float(round(self.tochange[3],2))
        self.e2.insert(0, num)
        self.e3.insert(0, re.match(r'(.*?)(?:-)', self.tochange[4]).group(1))
        self.e4.insert(0, re.match(r'(?:.*?-)(.*?)(?:-)', self.tochange[4]).group(1))
        self.e5.insert(0, re.match(r'(?:.*?-.*?-)(.*)', self.tochange[4]).group(1))
        tag1=1
        if(self.tochange[5]=='支出'):
            tag1=0
        self.numberChosen2.current(tag1)
    #界面初始化
    def __init__(self,con,user,goMain,tochange):
        self.con = con
        self.user = user
        self.table = "user" + user
        self.tochange=tochange
        self.nochange=[]
        for i in tochange:
            self.nochange.append(i)
        self.goMain = goMain
        self.root = Tk()
        Analyze.goHelp(root=self.root)
        self.root.title("修改记账")
        self.root.resizable(0, 0)
        self.root.geometry('500x300')
       

        # 界面美化
        image1 = Image.open('source/鸟底纹素材.png')
        back_image = ImageTk.PhotoImage(image1)
        image2 = Image.open('source/123.png')
        back_image2 = ImageTk.PhotoImage(image2)
        Label(self.root, image=back_image).place(x=0, y=0)
        Label(self.root, image=back_image2, borderwidth=0).place(relx=0.4, rely=0)

        # 界面控件
        # 名称
        Label(self.root, text="名称").place(relx=0.22, rely=0.2)
        self.e1 = Entry(self.root)
        self.e1.place(relx=0.35, rely=0.2, relwidth=0.3)

        # 类型
        Add.typeWehave(self=self)
        self.type.append('')
        Label(self.root, text="类型").place(relx=0.22, rely=0.3)
        number = StringVar()
        self.numberChosen = ttk.Combobox(self.root, width=12, textvariable=number)
        self.numberChosen['values'] = self.type[:len(self.type)-1]
        self.numberChosen.place(relx=0.35, rely=0.3)

        # 金额
        Label(self.root, text="金额").place(relx=0.22, rely=0.4)
        Label(self.root, text="￥").place(relx=0.3, rely=0.4)
        self.e2 = Entry(self.root)
        self.e2.place(relx=0.35, rely=0.4, relwidth=0.3)

        # 日期
        Label(self.root, text="日期").place(relx=0.22, rely=0.5)
        Label(self.root, text="年").place(relx=0.46, rely=0.5)
        self.e3 = Entry(self.root)
        self.e3.place(relx=0.35, rely=0.5, relwidth=0.1)
        Label(self.root, text="月").place(relx=0.61, rely=0.5)
        self.e4 = Entry(self.root)
        self.e4.place(relx=0.5, rely=0.5, relwidth=0.1)
        Label(self.root, text="日").place(relx=0.76, rely=0.5)
        self.e5 = Entry(self.root)
        self.e5.place(relx=0.65, rely=0.5, relwidth=0.1)

        # 属性
        Label(self.root, text="属性").place(relx=0.22, rely=0.6)
        number2 = StringVar()
        self.numberChosen2 = ttk.Combobox(self.root, width=12, textvariable=number2, state='readonly')
        self.numberChosen2['values'] = ( '支出', '收入')
        self.numberChosen2.place(relx=0.35, rely=0.6)
        self.insertinfo()
        Button(self.root, text="确定", bg='snow',command=self.ifchange).place(relx=0.4, rely=0.7)
        Button(self.root, text="取消", bg='snow',command=self.b_return).place(relx=0.5, rely=0.7)
        self.root.mainloop()

#账单删除
class Dele:
    #跳转主界面
    def b_return(self):
        self.root.destroy()
        self.goMain(user=self.user)
    #进行删除
    def dele(self):
        #修改数据库
        sql='''delete from [%s] where num=%d'''%(self.table,self.todele[0])
        self.con.execute(sql)
        self.con.commit()
        #修改txt
        with open('./%s/%s.txt' % (self.table,self.table), mode='a') as filename:
            filename.write('Delete %s %s %.2f %s %s' % (
            self.todele[1], self.todele[2], self.todele[3], self.todele[4], self.todele[5]))
            filename.write('\n')
        tkinter.messagebox.showinfo('提示', '删除成功')
        #跳转返回
        self.b_return()
    #初始化
    def __init__(self,con,user,goMain,todele):
        self.con = con
        self.user = user
        self.table = "user" + user
        self.todele=todele
        self.goMain = goMain
        self.root = Tk()
        Analyze.goHelp(root=self.root)
        self.root.title("删除记账")
        #显示选择记录
        for i in [1,2,4,5]:
            self.todele[i] = "".join( self.todele[i].split())
        record='属性:' + str(self.todele[5]) + "  名称:" + str(self.todele[1]) + '  类型:' + str(self.todele[2]) + '  金额:' + str(
            self.todele[3]) + '  日期:' + str(self.todele[4])
        Label(self.root,text="您想要删除的记账信息：").grid(row=0,column=0)
        Label(self.root,text=record).grid(row=1, column=0)
        Button(self.root, text="确定", bg='snow',command=self.dele).grid(row=2,column=1)
        Button(self.root, text="取消", bg='snow', command=self.b_return).grid(row=2,column=2)






