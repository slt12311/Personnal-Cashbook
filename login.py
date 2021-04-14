#用户信息处理

import Analyze
from tkinter import *
import tkinter.messagebox
import tkinter.font as tkFont
from PIL import ImageTk, Image
#用户登陆
class Login:
    #跳转
    #跳转注册界面
    def b_goRegi(self):
        self.root.destroy()
        tmp=Regi(self.con,self.goMain,self.Base)
    #跳转初始界面
    def b_return(self):
        self.root.destroy()
        self.Base()

    #功能函数：
    #登陆信息合法性检验/正确性检验
    def iflogin(self):
        flag=0
        self.id=self.e1.get()
        self.password=self.e2.get()
        #id
        if(len(self.id)==0):
            tkinter.messagebox.showwarning('警告', '未输入id')
            flag = 1
        elif(len(self.id)>20):
            tkinter.messagebox.showwarning('警告','id超过20个字符')
            flag=1
        elif(' ' in self.id):
            tkinter.messagebox.showwarning('警告','id中不可以含有空格')
            flag=1
        elif(self.id.isalnum()!=TRUE):
            tkinter.messagebox.showwarning('警告', 'id中不可以含有特殊字符')
            flag = 1
        elif (len(self.id)==0):
            tkinter.messagebox.showwarning('警告', '未输入密码')
            flag = 1
        #pw
        elif (len(self.password) > 20):
            tkinter.messagebox.showwarning('警告', '密码超过20个字符')
            flag=1
        elif (' ' in self.password):
            tkinter.messagebox.showwarning('警告', '密码中不可以含有空格')
            flag = 1
        if(flag==1):
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            return

        #数据库查询
        sql = self.con.execute("select * from name where id='%s'"%(self.id))
        result = self.con.fetchone()
        #用户存在性
        if(result==None):
            tkinter.messagebox.showwarning('警告', '用户不存在')
            flag=1
        else:#密码正确性
            for i in range(4):
                result[i] = "".join(result[i].split())
            if(self.password!=result[1]):
                tkinter.messagebox.showwarning('警告', '密码错误')
                flag = 1
        #清空
        if (flag == 1):
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            return
        tkinter.messagebox.showinfo('提示', '登陆成功')
        self.root.destroy()
        self.goMain(user=self.id)

    #忘记密码
    #新密码输入合法性/实施修改
    def forget3(self):
        passw=self.e4.get()
        flag = 0

        # 检查输入合法性
        if (len(passw)==0):
            tkinter.messagebox.showwarning('警告', '未输入新密码')
            flag = 1
        elif (len(passw) > 20):
            tkinter.messagebox.showwarning('警告', '密码超过20个字符')
            flag = 1
        elif (' ' in passw):
            tkinter.messagebox.showwarning('警告', '密码中不可以含有空格')
            flag = 1
        if (flag == 1):
            self.e4.delete(0, END)
            return

        #修改数据库
        sql="UPDATE name SET password = '%s' WHERE id = '%s' "%(passw,self.id)
        self.con.execute(sql)
        self.con.commit()
        tkinter.messagebox.showinfo('提示', '密码修改成功')
        self.newroot.destroy()
    #密保答案输入检验
    def forget2(self):
        answer=self.e3.get()
        flag = 0

        # 检查输入合法性
        if (len(answer)==0):
            tkinter.messagebox.showwarning('警告', '未输入回答')
            flag = 1
        elif (len(answer) > 20):
            tkinter.messagebox.showwarning('警告', '答案超过20个字符')
            flag = 1
        elif (' ' in answer):
            tkinter.messagebox.showwarning('警告', '答案中不可以含有空格')
            flag = 1
        if (flag == 1):
            self.e3.delete(0, END)
            return

        #验证答案正确性
        if(answer==self.result[3]):
            tkinter.messagebox.showinfo('提示', '验证成功')
            self.win.destroy()
            self.newroot = Tk()
            self.newroot.title("密码重置")
            self.newroot.geometry('250x70')
            Label(self.newroot, text="新密码").grid(row=0, column=0)
            self.e4 = Entry(self.newroot)
            self.e4.grid(row=0, column=1, columnspan=2)
            Button(self.newroot, text="确定", command=self.forget3).grid(row=1, column=1)
    #id输入/密保输入界面
    def forget1(self):
        self.id=self.e0.get()
        flag=0

        #id输入
        #检查输入合法性
        if (len(self.id)==0):
            tkinter.messagebox.showwarning('警告', '未输入id')
            flag = 1
        elif (len(self.id) > 20):
            tkinter.messagebox.showwarning('警告', 'id超过20个字符')
            flag = 1
        elif (' ' in self.id):
            tkinter.messagebox.showwarning('警告', 'id中不可以含有空格')
            flag = 1
        elif (self.id.isalnum() != TRUE):
            tkinter.messagebox.showwarning('警告', 'id中不可以含有特殊字符')
            flag = 1
        if (flag == 1):
            self.e0.delete(0, END)
            return
        #检查id存在性
        sql = self.con.execute("select * from name where id='%s'" % (self.id))
        result1 = self.con.fetchall()
        if (result1[0] == None):
            tkinter.messagebox.showwarning('警告', '用户不存在')
            self.e0.delete(0, END)
            return
        self.result=[]
        for i in range(4):
            self.result.append( "".join(result1[0][i].split()))

        #密保输入
        self.newroot.destroy()
        self.win=Tk()
        self.win.title("身份验证")
        self.win.resizable(0, 0)
        self.win.geometry('300x100')
        Label(self.win, text="密保问题").grid(row=0, column=0)
        Label(self.win,text='%s'%self.result[2]).grid(row=0,column=1)
        Label(self.win,text="密保答案").grid(row=1,column=0)
        self.e3=Entry(self.win)
        self.e3.grid(row=1, column=1, columnspan=2)
        Button(self.win, text="确定",command=self.forget2).grid(row=2, column=1)
    #忘记密码主界面
    def forget(self):
        self.newroot=Toplevel()
        self.newroot.title("身份验证")
        self.newroot.geometry('250x70')
        Label(self.newroot, text="id").grid(row=0, column=0)
        self.e0=Entry(self.newroot)
        self.e0.grid(row=0, column=1, columnspan=2)
        Button(self.newroot, text="确定",command=self.forget1).grid(row=1, column=1)

    #初始化
    def __init__(self,con,goMain,Base):
        self.Base=Base
        self.goMain=goMain
        self.con=con
        self.root=Tk()
        Analyze.goHelp(root=self.root)
        self.root.title("我的记账本")
        self.root.resizable(0, 0)
        self.root.geometry('500x300')

        image1 = Image.open('source/鸟底纹素材.png')
        image2 = Image.open(r'source/曲线2.png')
        image3 = Image.open(r'source/曲线3.png')
        image4 = Image.open(r'source/cat.png')
        background_image = ImageTk.PhotoImage(image2)
        back_image = ImageTk.PhotoImage(image1)
        back_image2 = ImageTk.PhotoImage(image3)
        back_image3 = ImageTk.PhotoImage(image4)

        Label(self.root, image=back_image).place(x=0, y=0)
        Label(self.root,image=back_image3,borderwidth=0).place(relx=0.4,rely=0)
        label = Label(self.root, text='用户登录',compound='center',image=background_image)
        label.place(relx=0.32,rely=0.15)

        Label(self.root, text="id").place(relx=0.18,rely=0.3)
        self.e1=Entry(self.root)
        self.e1.place(relx=0.25,rely=0.3,relwidth=0.5)
        ft1 = tkFont.Font(size=8)
        Label(self.root, text="字符长度小于20", font=ft1, fg='grey').place(relx=0.75, rely=0.3)
        Label(self.root, text="密码").place(relx=0.18,rely=0.4)
        Label(self.root, text="字符长度小于20", font=ft1, fg='grey').place(relx=0.75, rely=0.4)
        self.e2=Entry(self.root, show="*")
        self.e2.place(relx=0.25,rely=0.4,relwidth=0.5)
        Button(self.root, text="登陆",command=self.iflogin,compound='center',image=back_image2).place(relx=0.12,rely=0.5)
        Button(self.root, text="注册",command=self.b_goRegi,compound='center',image=back_image2).place(relx=0.32,rely=0.5)
        Button(self.root, text="忘记密码",command=self.forget,compound='center',image=back_image2).place(relx=0.52, rely=0.5)
        Button(self.root, text="退出",command=self.b_return,compound='center',image=back_image2).place(relx=0.72, rely=0.5)
        self.root.mainloop()

#用户注册
class Regi:
    #跳转初始界面
    def b_return(self):
        self.root.destroy()
        self.Base()
    #注册信息合法性/进行注册
    def ifRegi(self):
        informa=[]
        name1=['id','密码','密保问题','密保答案']
        informa.extend([self.e1.get(),self.e2.get(),self.e3.get(),self.e4.get()])
        flag=0

        #检查输入是否合法
        for i in range(4):
            if (len(informa[i]) == 0):
                tkinter.messagebox.showwarning('警告', '未输入%s'%name1[i])
                self.e1.delete(0, END)
                self.e2.delete(0, END)
                self.e3.delete(0, END)
                self.e4.delete(0, END)
                return
            if(len(informa[i])>20):
                tkinter.messagebox.showwarning('警告', '%s超过20个字符'%name1[i])
                self.e1.delete(0, END)
                self.e2.delete(0, END)
                self.e3.delete(0, END)
                self.e4.delete(0, END)
                return
            if(' 'in informa[i]):
                tkinter.messagebox.showwarning('警告', '%s中含有空格'% name1[i])
                self.e1.delete(0, END)
                self.e2.delete(0, END)
                self.e3.delete(0, END)
                self.e4.delete(0, END)
                return
            if (informa[0].isalnum() != TRUE):
                tkinter.messagebox.showwarning('警告', 'id中不可以含有特殊字符')
                self.e1.delete(0, END)
                self.e2.delete(0, END)
                self.e3.delete(0, END)
                self.e4.delete(0, END)
                return

        #检查用户是否已经存在
        sql = self.con.execute("select * from name where id='%s'" % (informa[0]))
        result = self.con.fetchone()
        if(result!=None):
            tkinter.messagebox.showwarning('警告', '用户已经存在，请更改id')
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            self.e3.delete(0, END)
            self.e4.delete(0, END)
            return

        #成功注册
        for i in range(4):
            informa[i]="'"+str(informa[i])+"'"
        sql_insert = '''insert into name values(%s)''' % (",".join(str(n) for n in informa))
        self.con.execute(sql_insert)
        self.con.commit()
        tkinter.messagebox.showinfo('提示', '注册成功')
        id = self.e1.get()
        self.root.destroy()
        tmp = self.goMain(user=id)
    #初始化
    def __init__(self,con,goMain,Base):
        self.Base=Base
        self.goMain=goMain
        self.con = con
        self.root = Tk()
        Analyze.goHelp(root=self.root)
        self.root.title("我的记账本")
        self.root.resizable(0, 0)
        self.root.geometry('500x300')
        #界面
        image1 = Image.open('source/鸟底纹素材.png')
        image2 = Image.open(r'source/曲线2.png')
        image3 = Image.open(r'source/曲线3.png')
        image4 = Image.open(r'source/cat2.png')
        background_image = ImageTk.PhotoImage(image2)
        back_image = ImageTk.PhotoImage(image1)
        back_image2 = ImageTk.PhotoImage(image3)
        back_image3 = ImageTk.PhotoImage(image4)

        Label(self.root, image=back_image).place(x=0, y=0)
        Label(self.root, image=back_image3, borderwidth=0).place(relx=0.4, rely=0)
        label = Label(self.root, text='新用户注册',compound='center',image=background_image)
        label.place(relx=0.32, rely=0.15)
        #id
        Label(self.root, text="id").place(relx=0.13, rely=0.3)
        self.e1 = Entry(self.root)
        self.e1.place(relx=0.25, rely=0.3, relwidth=0.5)
        ft1=tkFont.Font(size=8)
        Label(self.root, text="字符长度小于20",font=ft1,fg='grey').place(relx=0.75, rely=0.3)

        #密码
        Label(self.root, text="密码").place(relx=0.13, rely=0.4)
        Label(self.root, text="字符长度小于20", font=ft1, fg='grey').place(relx=0.75, rely=0.4)
        self.e2 = Entry(self.root, show="*")
        self.e2.place(relx=0.25, rely=0.4, relwidth=0.5)

        #密保
        Label(self.root, text="密保问题").place(relx=0.13, rely=0.5)
        self.e3 = Entry(self.root)
        self.e3.place(relx=0.25, rely=0.5, relwidth=0.5)
        Label(self.root, text="字符长度小于20", font=ft1, fg='grey').place(relx=0.75, rely=0.5)

        Label(self.root, text="密保答案").place(relx=0.13, rely=0.6)
        self.e4 = Entry(self.root)
        self.e4.place(relx=0.25, rely=0.6, relwidth=0.5)
        Label(self.root, text="字符长度小于20", font=ft1, fg='grey').place(relx=0.75, rely=0.6)

        Button(self.root, text="确定",command=self.ifRegi,compound='center',image=back_image2).place(relx=0.32, rely=0.7)
        Button(self.root, text="退出", command=self.b_return,compound='center',image=back_image2).place(relx=0.5, rely=0.7)
        self.root.mainloop()

#用户信息修改
class Change:
    #返回主界面
    def b_return(self):
        self.root.destroy()
        self.goMain(user=self.user)
    #修改信息合法性/进行修改
    def ifchange(self):
        new=[self.e0.get(),self.e1.get(),self.e2.get()]
        index=[]
        name1=['新密码','新密保问题','新密保答案']
        name2=['password','question','answer']
        #修改合法性
        sum=0
        for i in range(3):
            if(len(new[i])>0):
                index.append(i)
                sum+=1
        if(sum==0):
            tkinter.messagebox.showwarning('警告', '未输入修改信息')
            self.e0.delete(0, END)
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            return
        for i in index:
            if (len(new[i]) > 20):
                tkinter.messagebox.showwarning('警告', '%s超过20个字符'% name1[i])
                self.e0.delete(0, END)
                self.e1.delete(0, END)
                self.e2.delete(0, END)
                return
            if (' ' in new[i]):
                tkinter.messagebox.showwarning('警告', '%s中含有空格' % name1[i])
                self.e1.delete(0, END)
                self.e2.delete(0, END)
                self.e0.delete(0, END)
                return
        #数据库修改
        for i in index:
            sql = "UPDATE name SET %s = '%s' WHERE id = '%s' " % (name2[i],new[i], self.user)
            self.con.execute(sql)
            self.con.commit()
        tkinter.messagebox.showinfo('提示', '信息修改成功')
        self.root.destroy()
        self.goMain(user=self.user)
    #初始化
    def __init__(self,con,user,goMain):
        self.con=con
        self.goMain=goMain
        self.user=user
        #获取用户信息
        sql = self.con.execute("select * from name where id='%s'" % (user))
        result = self.con.fetchall()
        self.result=result[0]
        for i in range(4):
            self.result[i]="".join(self.result[i].split())
        #界面架构
        self.root = Tk()
        Analyze.goHelp(root=self.root)
        self.root.title("用户信息修改")
        self.root.resizable(0, 0)
        self.root.geometry('500x300')
        image1 = Image.open('source/鸟底纹素材.png')
        back_image = ImageTk.PhotoImage(image1)

        Label(self.root, image=back_image).place(x=0, y=0)
        label = Label(self.root, text='个人信息')
        label.place(relx=0.45, rely=0)
        Label(self.root, text="id").place(relx=0.13, rely=0.1)
        Label(self.root,text=user).place(relx=0.25, rely=0.1, relwidth=0.5)

        ft1=tkFont.Font(size=8)
        Label(self.root, text="旧密码").place(relx=0.13, rely=0.2)
        Label(self.root,text=self.result[1]).place(relx=0.25, rely=0.2, relwidth=0.5)
        Label(self.root, text="新密码").place(relx=0.13, rely=0.3)
        self.e0 = Entry(self.root, show="*")
        self.e0.place(relx=0.25, rely=0.3, relwidth=0.5)
        Label(self.root, text="字符长度小于20", font=ft1, fg='grey').place(relx=0.75, rely=0.3)

        Label(self.root, text="旧密保").place(relx=0.13, rely=0.4)
        Label(self.root, text=self.result[2]).place(relx=0.25, rely=0.4, relwidth=0.5)
        Label(self.root, text="新密保").place(relx=0.13, rely=0.5)
        self.e1 = Entry(self.root)
        self.e1.place(relx=0.25, rely=0.5, relwidth=0.5)
        Label(self.root, text="字符长度小于20", font=ft1, fg='grey').place(relx=0.75, rely=0.5)

        Label(self.root, text="旧答案").place(relx=0.13, rely=0.6)
        Label(self.root, text=self.result[3]).place(relx=0.25, rely=0.6, relwidth=0.5)
        Label(self.root, text="新答案").place(relx=0.13, rely=0.7)
        self.e2 = Entry(self.root)
        self.e2.place(relx=0.25, rely=0.7, relwidth=0.5)
        Label(self.root, text="字符长度小于20", font=ft1, fg='grey').place(relx=0.75, rely=0.7)

        Button(self.root, text="确定",command=self.ifchange).place(relx=0.4, rely=0.8)
        Button(self.root, text="退出", command=self.b_return).place(relx=0.5, rely=0.8)
        self.root.mainloop()











