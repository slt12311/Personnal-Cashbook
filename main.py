# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ShaoLuting
# @File    : Project.py

#主界面
import webbrowser
import re
import database
import login
import Function
import Analyze
import Down
import pyodbc
import datetime
import os
from tkinter import *
import tkinter.messagebox
from PIL import ImageTk, Image
import calendar

#系统模块
class BaseDesk:
    #退出系统
    def quit(self):
        self.newroot.destroy()

    #登录界面消息提示（记账提醒）
    def message(self):
        #时间
        localtime=datetime.date.today()
        local=str(localtime.year)+'年'+str(localtime.month)+'月'+str(localtime.day)+'日'
        self.time=self.local()

        #布局
        self.newroot = Toplevel()
        self.newroot.geometry('300x150')
        self.newroot.resizable(0, 0)
        image1 = Image.open('source/鸟底纹素材.png')
        back_image = ImageTk.PhotoImage(image1)
        image2 = Image.open('source/太阳.png')
        back_image2 = ImageTk.PhotoImage(image2)
        image3 = Image.open('source/牛奶.png')
        back_image3 = ImageTk.PhotoImage(image3)
        image4 = Image.open('source/咖啡.png')
        back_image4 = ImageTk.PhotoImage(image4)
        Label(self.newroot, image=back_image).place(x=-0.1, y=0)

        #判断并显示记账提醒
        if(self.time==0):
            txt='''今天是%s\n快来开启第一条记账吧！'''%local
            Label(self.newroot, text=txt,compound='center',image=back_image4, borderwidth=0).place(relx=0, rely=0.2)
        else:
            time=self.test[0]+'年'+self.test[1]+'月'+self.test[2]+'日'
            if(time!=local):
                txt='''今天是%s\n今天还没有记账呢，快来记录本日的开支吧！'''%local
                Label(self.newroot, text=txt,compound='center',image=back_image3, borderwidth=0).place(relx=0, rely=0.2)
            else:
                txt='''今天是%s\n新的账目要及时记录呀！'''%local
                Label(self.newroot, text=txt,compound='center',image=back_image2, borderwidth=0).place(relx=0, rely=0.2)
        Button(self.newroot,text='确定',bg='snow',command=self.quit).place(relx=0.3,rely=0.7)
        Button(self.newroot, text='记账日历',bg='snow', command=self.calendar).place(relx=0.45, rely=0.7)
        self.newroot.mainloop()
    #记账日历
    def calendar(self):
        user = 'user' + self.id

        #布局
        self.newroot.destroy()
        self.newroot = Toplevel()
        self.newroot.geometry('240x220')
        self.newroot.resizable(0, 0)
        image1 = Image.open('source/tody.png')
        back_image = ImageTk.PhotoImage(image1)
        image2 = Image.open('source/have.png')
        back_image2 = ImageTk.PhotoImage(image2)
        Label(self.newroot,text='', bg='snow', width=300, height=200).place(relx=0,rely=0)

        #当前日期
        localtime = datetime.date.today()
        local = str(localtime.year) + '年' + str(localtime.month) + '月'
        local_b = str(localtime.year) + '-' + str(localtime.month) + '-'
        self.newroot.title(local)

        MonthCal = calendar.monthcalendar(localtime.year, localtime.month)#月份数据
        labels = [['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']]#数据标签
        for i in range(len(MonthCal)):
            labels.append(MonthCal[i])

        #获取当前月份记账数据
        sql = "select distinct time from [%s] where time like '%%%s%%'" % (user, local_b)
        self.con.execute(sql)
        result = self.con.fetchall()
        tag = 1#记录当前月份是否有记账数据
        time_have = []#记录日期
        if (len(result) == 0):
            tag = 0
        else:
            for i in result:
                i = str(i)[2:]
                i = "".join(i.split())
                a = re.match(r"(?:.*?-.*?-)(.*?)(?:',)", str(i))
                time_have.append(int(a.group(1))
                                 )

        #日历显示
        for r in range(len(MonthCal) + 1):
            for c in range(7):
                flag = 0#记录是否加标识
                if labels[r][c] == 0:#空缺
                    labels[r][c] = ' '
                if (labels[r][c] == localtime.day):#当前日期
                    label = Label(self.newroot, compound='center', image=back_image, borderwidth=0,
                                  text=str(labels[r][c]))
                    label.grid(row=r + 1, column=c)
                    flag = 1
                elif (tag == 1):#不等于当前日期时，考虑是否已经记账
                    if (labels[r][c] in time_have):
                        label = Label(self.newroot, compound='center', image=back_image2, borderwidth=0,
                                      text=str(labels[r][c]))
                        label.grid(row=r + 1, column=c)
                        flag = 1
                if (flag == 0):#没有标识
                    label = Label(self.newroot, padx=5, pady=5, bg='snow', text=str(labels[r][c]))
                    label.grid(row=r + 1, column=c)

        self.newroot.mainloop()
    #获取当前最新记账时间
    def local(self):
        user='user'+self.id
        self.con.execute('''SELECT MAX(time) FROM [%s]'''%user)
        result= self.con.fetchone()
        if(result[0]==None):
            return 0
        time=result[0]
        time = time.split(' ')[0]
        self.test = time.split('-', 3)
        time=self.test[0]+'年'+self.test[1]+'月'
        return time



    #一系列跳转函数
    #退出系统
    def goQuit(self):
        self.root.destroy()
        self.con.close()
        self.conn.close()
    #退出登录
    def goBack(self):
        self.root.destroy()
        self.__init__()
    #返回主界面
    def b_return(self):
        self.root.destroy()
        self.goMain(user=self.id)

    #个人信息
    #登陆
    def goLogin(self):
        self.root.destroy()
        tmp=login.Login(con=self.con,goMain=self.goMain,Base=self.__init__)
    #注册
    def goRegi(self):
        self.root.destroy()
        tmp=login.Regi(con=self.con,goMain=self.goMain,Base=self.__init__)
    #修改信息
    def goInfor(self):
        self.root.destroy()
        tmp = login.Change(con=self.con,user=self.id,goMain=self.goMain)

    #账单管理
    #添加
    def goAdd(self):
        self.root.destroy()
        tmp=Function.Add(con=self.con,goMain=self.goMain,user=self.id)
    #查询
    def goSearch(self):
        self.root.destroy()
        Function.Search(con=self.con,user=self.id,goMain=self.goMain,choice=1)
    #删除
    def goDele(self):
        self.root.destroy()
        Function.Search(con=self.con, user=self.id, goMain=self.goMain, choice=2)#以查询为基础
    #修改
    def goChange(self):
        self.root.destroy()
        Function.Search(con=self.con, user=self.id, goMain=self.goMain, choice=0)#以查询为基础

    #账务分析
    #预算
    def goBudget(self):
        self.root.destroy()
        Analyze.Budget(con=self.con,user=self.id,goMain=self.goMain,time1=self.test)
    #统计
    def goStatistics(self):
        self.root.destroy()
        Analyze.Statistics(con=self.con,user=self.id,goMain=self.goMain,time1=self.test)
    #对比
    def goCompare(self):
        self.root.destroy()
        Analyze.Compare(con=self.con,user=self.id,goMain=self.goMain,time1=self.test)
    #下载
    def goDown(self):
        time = self.local()
        if(time==0):
            tkinter.messagebox.showwarning("警告","您当前还没有记账信息！")
        else:
            self.root.destroy()
            Down.DownLoad(con=self.con,user=self.id,goMain=self.goMain,time1=self.test)
    #帮助文档
    def goHelp(self):
            tkinter.messagebox.showinfo('提示','已经打开帮助文档')
            webbrowser.open('帮助文档.docx')

    #界面
    #界面初始化
    def menu(self):
        menubar = Menu(self.root)
        menubar.add_command(label='帮助',
                            command=self.goHelp)
        self.root.config(menu=menubar)
    def menubegin(self):
        menubar = Menu(self.root)
        menubar.add_command(label='帮助',
                            command=self.goHelp)
        menubar.add_command(label='退出系统',
                            command=self.goQuit)
        self.root.config(menu=menubar)
    def __init__(self):
        #数据库/表/文件存在性检查
        #检查数据库是否存在
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=LAPTOP-BBDHO34Q\SQLEXPRESS;DATABASE=master;UID=sa;PWD=bookkeep123')
        conn.autocommit = True
        con = conn.cursor()
        sql = '''IF not EXISTS(SELECT *
        FROM sysdatabases
        WHERE name = 'book')
        CREATE DATABASE [test] ON PRIMARY
        ( NAME = N'book', FILENAME = N'D:\\作业\\20.9\\学习素材\\数据库\\MSSQL10.SQLEXPRESS\\MSSQL\\DATA\\book.mdf' , SIZE = 3072KB , MAXSIZE = UNLIMITED, FILEGROWTH = 1024KB )
        LOG ON
        ( NAME = N'book_log', FILENAME = N'D:\\作业\\20.9\\学习素材\\数据库\\MSSQL10.SQLEXPRESS\\MSSQL\\DATA\\book_log.ldf' , SIZE = 1024KB , MAXSIZE = 2048GB , FILEGROWTH = 10%)
        COLLATE Chinese_PRC_CI_AS'''
        con.execute(sql)
        con.commit()
        con.close()
        conn.close()

        self.conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=LAPTOP-BBDHO34Q\SQLEXPRESS;DATABASE=book;UID=sa;PWD=bookkeep123')
        self.con = self.conn.cursor()

        # 检测是否存在用户信息表
        result = database.table_exists(self.con, 'name')
        if (result == 0):
            self.con.execute(
                "create table name(id char(20) primary key not null,password char(20) not null,question char(20) not null,answer char(20) not null)")
        self.con.commit()
        #检查是否存在用户预算表
        result = database.table_exists(self.con, 'Budget')
        if (result == 0):
            self.con.execute(
                "create table Budget(id char(20) primary key not null,budget decimal(18,2))")
        self.con.commit()

        #登陆/注册主界面
        self.root = Tk()
        self.root.title("我的记账本")
        self.root.resizable(0, 0)
        self.root.geometry('500x300')
        self.menubegin()
        image1=Image.open('source/鸟底纹素材.png')
        image2 = Image.open(r'source/鸟底纹素材2.png')
        image3=Image.open(r'source/鸟底纹素材2.jpg')
        back_image=ImageTk.PhotoImage(image1)
        back_image2 = ImageTk.PhotoImage(image3)
        background_image = ImageTk.PhotoImage(image2)

        Label(self.root,image=back_image).place(x=0,y=0)
        label = Label(self.root, text='欢迎进入您的个人记账本',compound='center',image=background_image)
        label.place(relx=0.15,rely=0.05)
        button1 = Button(self.root, text='用户登陆',command=self.goLogin,compound='center',image=back_image2)
        button1.place(relx=0.18, y=100)
        button2 = Button(self.root, text='用户注册',command=self.goRegi,compound='center',image=back_image2)
        button2.place(relx=0.50, y=100)
        #Button(self.root, text='退出系统', command=self.goQuit, width=43,height=1,justify='center',bg='snow').place(relx=0.18,rely=0.7)
        self.num=0
        self.root.mainloop()

    #分析主界面
    def goAnalyze(self):
        self.root.destroy()
        time=self.local()
        self.root = Tk()
        self.root.title("财务分析")
        self.menu()
        image1 = Image.open('source/鸟底纹素材.png')
        image2 = Image.open(r'source/鸟底纹素材2.png')
        image3 = Image.open(r'source/鸟底纹素材2.jpg')
        back_image = ImageTk.PhotoImage(image1)
        back_image2 = ImageTk.PhotoImage(image3)
        background_image = ImageTk.PhotoImage(image2)
        Label(self.root, image=back_image).place(x=0, y=0)
        if(time==0):
            self.root.resizable(0, 0)
            self.root.geometry('300x100')
            Label(self.root, text='您当前没有记账信息', compound='center', image=background_image).place(relx=-0.05, rely=0)
            Button(self.root,text='返回',command=self.b_return,bg='snow').place(relx=0.45,rely=0.5)
            self.root.mainloop()
            return
        self.root.resizable(0, 0)
        self.root.geometry('500x300')
        label = Label(self.root, text='当前分析月份：%s'%time, compound='center', image=background_image)
        label.place(relx=0.15, rely=0.05)
        button1 = Button(self.root, text='预算分析',  compound='center',command=self.goBudget, image=back_image2)
        button1.place(relx=0.05, y=100)
        button2 = Button(self.root, text='分类统计', compound='center', command=self.goStatistics,image=back_image2)
        button2.place(relx=0.35, y=100)
        button3 = Button(self.root, text='财务比对', compound='center',command=self.goCompare, image=back_image2)
        button3.place(relx=0.65, y=100)
        Button(self.root, text='确定',bg='snow',command=self.b_return).place(relx=0.46,rely=0.8)

        self.root.mainloop()

    #功能主界面
    def goMain(self,user):
        self.num+=1
        #用户表查询
        self.id=user
        user="user"+user
        result = database.table_exists(self.con,user)
        if (result == 0):
            self.con.execute("create table [%s](num int primary key not null,name char(20) not null,type char(20) not null,money decimal(18,2) not null,time char(10) not null,prime char(4) not null)"%user)
        self.con.commit()

        #用户txt查询
        #生成文件夹
        folder = os.path.exists(user)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(user)
        try:
            f = open("./%s/%s.txt"%(user,user), 'r')
            f.close()
        except IOError:
            f = open("./%s/%s.txt"%(user,user), 'w')

        #布局
        self.root = Tk()
        self.root.title("%s的记账本主页"%user)
        self.root.resizable(0, 0)
        self.root.geometry('600x290')
        self.menu()
        image1 = Image.open('source/鸟底纹素材3.png')
        back_image = ImageTk.PhotoImage(image1)
        image2 = Image.open('source/鸟底纹素材4.png')
        back_image2 = ImageTk.PhotoImage(image2)
        image3 = Image.open('source/1.png')
        back_image3 = ImageTk.PhotoImage(image3)
        image4 = Image.open('source/2.png')
        back_image4 = ImageTk.PhotoImage(image4)

        button1 = Button(self.root, text='用户信息修改',command=self.goInfor,justify='center',bg='snow',width=35,height=1)
        Button(self.root, text='退出登陆', command=self.goBack, justify='center', bg='snow', width=25, height=1).place(
            relx=0.4, rely=0)
        button1.place(relx=0,rely=0)
        Button(self.root, text='退出系统',command=self.goQuit,justify='center',bg='snow',width=25,height=1).place(relx=0.7,rely=0)
        Function.Check(con=self.con,user=self.id,root=self.root,goMain=self.goMain)
        button2 = Button(self.root, text='添加新记账',command=self.goAdd,compound='center',image=back_image,borderwidth=0)
        button2.place(relx=0,rely=0.65)
        button3=Button(self.root, text='查询记账',compound='center',image=back_image2,borderwidth=0,command=self.goSearch)
        button3.place(relx=0.21,rely=0.65)
        Button(self.root, text='修改记账', compound='center',image=back_image,borderwidth=0,command=self.goChange).place(relx=0.42, rely=0.65)
        Button(self.root, text='删除记账',compound='center',image=back_image2,borderwidth=0,command=self.goDele).place(relx=0.63, rely=0.65)
        Button(self.root, text='财务分析', compound='center',image=back_image3,borderwidth=0,command=self.goAnalyze).place(relx=0.85, rely=0.07)
        Button(self.root, text='报告下载', compound='center',image=back_image4,borderwidth=0,command=self.goDown).place(relx=0.85, rely=0.65)
        if(self.num==1):
            self.message()
        self.root.mainloop()




if __name__ == "__main__":
    BaseDesk()
