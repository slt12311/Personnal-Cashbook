#财务分析
import webbrowser
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import tkinter.messagebox
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time
#帮助
class goHelp:
    def __init__(self,root):
        self.root=root
        menubar = Menu(self.root)
        menubar.add_command(label='帮助',
                            command=self.goHelp)
        self.root.config(menu=menubar)
    def goHelp(self):
            tkinter.messagebox.showinfo('提示','已经打开帮助文档')
            webbrowser.open('帮助文档.docx')
#预算
class Budget:
    #页面切换
    def b_return(self):
        self.newroot.destroy()
        self.goMain(user=self.user)
    def d_return(self):
        self.root.destroy()
        self.goMain(user=self.user)
    def change(self):
        self.tag=1
        self.SetBudget()

    #功能函数
    #支出/收入合计
    def getSum(self):
        time=self.time[0]+'-'+self.time[1]+'-'#编辑日期
        sql = "select * from [%s] where time like '%%%s%%'" % (self.table, time)#数据库查询
        self.con.execute(sql)
        result = self.con.fetchall()
        #sum1,sum2计数收入/支出/绝对值差
        sum1 = 0
        sum2=0
        for j in result:
            if (j[5] == '支出'):
                sum1 += j[3]
            else:
                sum2 += j[3]
        endsum=sum1-sum2
        return sum1,sum2,endsum
    # 判断输入合法性/更新数据库
    def ifset(self):
        input = self.e.get()

        # 非法输入
        if (len(input) == 0):
            tkinter.messagebox.showwarning("警告", "请输入预算")
            self.e.delete(0, END)
            return
        test = input.split('.')
        if (test[0].isdecimal() != TRUE):
            tkinter.messagebox.showwarning('警告', '您的金额未正确输入')
            self.e.delete(0, END)
            return
        if(float(input)<=0):
            tkinter.messagebox.showwarning('警告', '预算不能为负或零')
            self.e.delete(0, END)
            return

        # 更新数据库
        if (self.tag == 0):
            sql = '''insert into Budget values('%s',%f)''' % (self.user, float(input))
        else:
            sql = "UPDATE Budget SET budget=%f where id='%s'" % (float(input), self.user)
        self.con.execute(sql)
        self.con.commit()

        #信息提示/界面跳转
        tkinter.messagebox.showinfo("提示", "设置预算成功")
        self.newroot.destroy()
        self.__init__(con=self.con, user=self.user, goMain=self.goMain, time1=self.time)

    #显示函数
    #设置预算主界面
    def SetBudget(self):
        self.root.destroy()
        self.newroot=Tk()
        self.newroot.title("设置预算")
        self.newroot.resizable(0, 0)
        self.newroot.geometry('200x100')
        Label(self.newroot,text="设置预算:￥").grid(row=0,column=0)
        self.e=Entry(self.newroot)
        self.e.place(relx=0.32,relwidth=0.5)
        Button(self.newroot,text="确定",command=self.ifset,bg='snow').grid(row=2,column=2)
        Button(self.newroot, text="取消", command=self.b_return,bg='snow').grid(row=2, column=3)
    #界面初始化/预算展示
    def __init__(self,con,user,goMain,time1):
        self.con=con
        self.user=user
        self.table='user'+user
        self.goMain=goMain
        self.time=time1
        time0 = time1[0] + '年' + time1[1] + '月'

        #界面初始
        self.root=Tk()
        goHelp(root=self.root)
        self.root.title("预算分析")
        self.root.resizable(0, 0)
        self.root.geometry('500x300')

        image1 = Image.open('source/鸟底纹素材.png')
        image2 = Image.open(r'source/鸟底纹素材2.png')
        image3 = Image.open(r'source/鸟底纹素材2.jpg')
        back_image2 = ImageTk.PhotoImage(image3)
        background_image = ImageTk.PhotoImage(image2)
        back_image = ImageTk.PhotoImage(image1)
        Label(self.root, image=back_image).place(x=0, y=0)

        #判断预算存在性
        sql="select budget from Budget where id='%s'"%self.user
        self.con.execute(sql)
        self.budget=self.con.fetchall()
        if(len(self.budget)==0):
            label = Label(self.root, text='当前还没有设置预算', compound='center', image=background_image)
            label.place(relx=0.15, rely=0.05)
            self.tag=0
            Button(self.root,text="设置预算", compound='center',command=self.SetBudget, image=back_image2).place(relx=0.34,rely=0.3)
            Button(self.root, text="取消",bg='snow',command=self.d_return).place(
                relx=0.45, rely=0.7)
            self.root.mainloop()
            return

        #若预算存在则以进度条格式显示预算
        #显示预算
        label = Label(self.root, text='%s预算: ￥%.2f' % (time0,self.budget[0][0]), compound='center', image=background_image)
        label.place(relx=0.15, rely=0.05)
        # 进度条
        canvas = Canvas(self.root, width=350, height=22, bg="white")
        canvas.place(relx=0.15, rely=0.33)

        #获取本月总支出
        budget = self.budget[0][0]
        sum=self.getSum()
        t = sum[0] / budget
        t = round(t, 2)
        t = int(100 * t)
        if(sum[0]<budget):
            fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
            for i in range(t):
                n =3.5*(i+2)
                canvas.coords(fill_line, (0, 0, n, 50))
                self.root.update()
                time.sleep(0.015)  # 控制进度条流动的速度
            Label(self.root, text='当前月预算剩余:￥%.2f' % (budget-sum[0]),fg='LimeGreen', compound='center',width=30,height=1,justify='center',bg='snow').place(relx=0.27, rely=0.7)
        else:
            fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="#d32a63")
            for i in range(100):
                n = 3.5 * (i + 2)
                canvas.coords(fill_line, (0, 0, n, 50))
                self.root.update()
                time.sleep(0.015)  # 控制进度条流动的速度
            Label(self.root, text='当前月预算超支:￥%.2f' % (sum[0]-budget), fg='#d32a63',compound='center', width=30, height=1,justify='center', bg='snow').place(relx=0.27, rely=0.7)
        Label(self.root,text='%d%%'%t).place(relx=0.9,rely=0.33)
        Label(self.root, text='总支出:￥%.2f' % sum[0], width=30,height=1,justify='center',bg='snow').place(relx=0.27, rely=0.5)
        Label(self.root, text='总收入:￥%.2f' % sum[1], width=30,height=1,justify='center',bg='snow').place(relx=0.27, rely=0.6)
        Button(self.root,text='  确定  ',bg='snow',command=self.d_return).place(relx=0.35,rely=0.8)
        Button(self.root, text='修改预算',bg='snow', command=self.change).place(relx=0.5, rely=0.8)
        self.root.mainloop()

#分类统计
class Statistics:
    #界面跳转
    def d_return(self):
        self.root.destroy()
        self.goMain(user=self.user)

    #功能函数
    #判断收入/支出存在性（1：没有收入/支出，2：只有收入，3：只有支出，4：均有）
    def getSta(self,time):
        sql = "select * from [%s] where time like '%%%s%%' and prime='支出'" % (self.table, time)
        self.con.execute(sql)
        result = self.con.fetchall()
        self.con.execute("select * from [%s] where time like '%%%s%%' and prime='收入'" % (self.table, time))
        result2=self.con.fetchall()
        if(len(result)==0 and len(result2)==0):
            return 1
        elif(len(result)==0):
            return 2
        elif(len(result2)==0):
            return 3
        else:
            return 4
    # 数据汇总：获得月收入/支出汇总（参数：result2(金额）返回值(类型),tag(1:收入/0:支出选择))
    def getIncome(self, tag, result2, time_b):
        # 判断汇总值
        if (tag == 1):
            str1 = '收入'
        else:
            str1 = '支出'
        time = time_b[0] + '-' + time_b[1] + '-'
        # 数据库查询
        self.con.execute(
            "select distinct type from [%s] where time like '%%%s%%' and prime='%s'" % (self.table, time, str1))
        result0 = self.con.fetchall()
        result3 = []
        num = 0
        # 数值汇总
        for i in result0:
            self.con.execute(
                "select money from [%s] where time like '%%%s%%' and prime='%s' and type='%s'" % (
                self.table, time, str1, i[0]))
            result1 = self.con.fetchall()
            i[0] = i[0].split(' ')[0]
            result3.append(i[0])
            result2.append(0)
            for k in result1:
                result2[num] += k[0]
            num += 1
        return result3
    #绘图函数，result0(类型）/result2(金额)/a(颜色控制)
    def Show(self,result0,result2,size,a):
        #图表基础
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        pie = plt.figure(figsize=(size, size), facecolor="snow")
        pie.labels = result0
        pie.sizes = result2
        colors1=['#95e1d3','#eaffd0','#fce38a','#f38181','#ffe2e2','#ffffd2','#aa96da','#a8d8ea','#edb1f1','#d59bf6','#9896f1','#8ef6e4']
        #颜色多样化设置
        if(a==1):
            while(12<len(result0)):
                colors1.extend(colors1)
            colors=[]
            for i in range(len(result0)):
                colors.append(colors1[i])
            pie.colors = colors  # 自定义颜色
        else:
            colors=[]
            for i in range(12):
                colors.append(colors1[11-i])
            while(12<len(result0)):
                colors.extend(colors)
            pie.colors = colors
        size = []

        #将最大值色块脱离显示
        if(len(result0)==1):
            for i in range(len(result0)):
                size.append(0.03)
        else:
            a = result2.index(max(result2))
            for i in range(len(result0)):
                if(i==a):
                    size.append(0.07)
                else:
                    size.append(0.03)
        #绘图设置
        pie.explode = size
        pie.text1,pie.text2,pie.patches  = plt.pie(pie.sizes,
                                                    explode=pie.explode,
                                                    labels=pie.labels,
                                                    colors=pie.colors,
                                                    autopct='%.2f%%',
                                                    shadow=True,
                                                    pctdistance=0.5,
                                                    textprops={'fontsize': 7, 'color': '#000080'}
                                                    )
        plt.legend(fontsize=7,loc=[-0.15,0.9])
        plt.axis('equal')  # 正圆
        for t in pie.text2:  # 设置饼图标签的字体大小
            t.setsize = 7
        #图片保存，留待生成报告
        plt.savefig('./%s/Cat.jpg'%self.table)
        plt.close()
        return pie

    #初始化/结果显示
    def __init__(self, con, user, goMain, time1):
        self.con = con
        self.user = user
        self.table = 'user' + user
        self.goMain = goMain
        self.time = time1
        time0 = time1[0] + '年' + time1[1] + '月'

        #界面布局
        self.root = Tk()
        self.root.title("分类统计")
        self.root.resizable(0, 0)
        self.root.geometry('500x500')
        goHelp(root=self.root)
        image1 = Image.open('source/鸟底纹素材.png')
        image2 = Image.open(r'source/鸟底纹素材2.png')
        background_image = ImageTk.PhotoImage(image2)
        back_image = ImageTk.PhotoImage(image1)
        Label(self.root, image=back_image).place(x=0, y=0)
        label = Label(self.root, text='%s 开支分类统计' % time0, compound='center',
                      image=background_image)
        label.place(relx=0.15, rely=0.05)

        #判断是否有支出/收入
        time2 = self.time[0] + '-' + self.time[1] + '-'
        a=self.getSta(time=time2)
        matplotlib.use('TkAgg')
        result2 = []
        if(a==2):#只有收入
            result0=self.getIncome(tag=1,result2=result2,time_b=self.time)#获取数值
            pie=self.Show(result0=result0,result2=result2,size=3,a=0)#绘图
            canvas_statis = FigureCanvasTkAgg(pie, self.root)
            canvas_statis.get_tk_widget().place(relx=0.2, rely=0.19)
            #总结数据汇总并显示
            sum=0
            for i in result2:
                sum+=i
            Label(self.root,text="总收入：￥%.2f"%sum,width=30,height=1,justify='center',bg='snow',fg='LimeGreen').place(relx=0.3,rely=0.75)
            Label(self.root,text='最高收入来自%s'%(result0[result2.index(max(result2))]), width=30,height=1,justify='center',bg='snow').place(relx=0.3,rely=0.81)
        elif(a==3):#只有支出
            result0 = self.getIncome(tag=0, result2=result2,time_b=self.time)#获取数值
            pie = self.Show(result0=result0, result2=result2,size=3,a=1)#绘图
            canvas_statis = FigureCanvasTkAgg(pie, self.root)
            canvas_statis.get_tk_widget().place(relx=0.2, rely=0.19)
            sum = 0
            for i in result2:
                sum += i
            Label(self.root, text="总支出：￥%.2f" % sum, width=30, height=1, justify='center', bg='snow',fg='red').place(relx=0.3,
                                                                                                            rely=0.75)
            Label(self.root, text='最高支出来自%s' % (result0[result2.index(max(result2))]), width=30, height=1,
                  justify='center', bg='snow').place(relx=0.3, rely=0.81)
        else:
            #支出
            result0 = self.getIncome(tag=0, result2=result2,time_b=self.time)
            pie = self.Show(result0=result0, result2=result2, size=2.5,a=1)
            canvas_statis = FigureCanvasTkAgg(pie, self.root)
            canvas_statis.get_tk_widget().place(relx=0, rely=0.19)
            sum = 0
            for i in result2:
                sum += i
            Label(self.root, text="总支出：￥%.2f" % sum, width=20, height=1, justify='center', bg='snow',fg='red').place(relx=0.1,
                                                                                                            rely=0.75)
            Label(self.root, text='最高支出来自%s' % (result0[result2.index(max(result2))]), width=20, height=1,
                  justify='center', bg='snow').place(relx=0.1, rely=0.81)
            #收入
            result2=[]
            result0 = self.getIncome(tag=1, result2=result2,time_b=self.time)
            pie = self.Show(result0=result0, result2=result2, size=2.5,a=0)
            canvas_statis = FigureCanvasTkAgg(pie, self.root)
            canvas_statis.get_tk_widget().place(relx=0.5, rely=0.19)
            sum = 0
            for i in result2:
                sum += i
            Label(self.root, text="总收入：￥%.2f" % sum, width=20, height=1, justify='center', bg='snow',fg='LimeGreen').place(relx=0.6,
                                                                                                            rely=0.75)
            Label(self.root, text='最高收入来自%s' % (result0[result2.index(max(result2))]), width=20, height=1,
                  justify='center', bg='snow').place(relx=0.6, rely=0.81)
        Button(self.root, text='确定',bg='snow', command=self.d_return).place(relx=0.45, rely=0.86)
        self.root.mainloop()

#月份账单对比
class Compare:
    #跳转返回
    def b_return(self):
        self.root.destroy()
        self.goMain(user=self.user)
    #功能函数
    #输入对比日期合法性
    def ifuse(self):
        str0=[]
        str0.append(self.e1.get())
        str0.append(self.e2.get())
        #输入格式合法性
        #是否有输入
        if(len(str0[0])==0 or len(str0[1])==0):
            tkinter.messagebox.showwarning("警告","信息输入不全！")
            self.e1.delete(0,END)
            self.e2.delete(0,END)
            return 0
        #日期合法性
        time = [[1900, 2021], [1, 12]]
        for i in range(2):
            #是否全是数字
            if (str0[i].isdecimal() != 1):
                tkinter.messagebox.showwarning('警告', '日期未正确输入')
                self.e1.delete(0, END)
                self.e2.delete(0, END)
                return 0
            str0[i] = int(str0[i])
            #是否符合日期特点
            if (str0[i] < time[i][0] or str0[i] > time[i][1]):
                tkinter.messagebox.showwarning('警告', '日期中未正确输入')
                self.e1.delete(0, END)
                self.e2.delete(0, END)
                return 0
        #日期是否当前日期
        if(str0[0]==int(self.time[0]) and str0[1]==int(self.time[1])):
            tkinter.messagebox.showwarning('警告', '输入日期为当前日期')
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            return 0
        return str0
    # 选择日期与当前日期收入/支出存在性提示
    def goUse(self):
        self.choose = self.numberChosen2.get()
        time1 = self.time[0] + '-' + self.time[1] + '-'
        time2 = str(self.test[0]) + '-' + str(self.test[1]) + '-'
        time3 = str(self.test[0]) + '年' + str(self.test[1]) + '月'
        a = Statistics.getSta(self=self, time=time1)
        b = Statistics.getSta(self=self, time=time2)

        # 是否存在收入/支出
        if (self.choose == '支出'):
            if (a == 2):
                tkinter.messagebox.showwarning("警告", "%s没有记录支出" % self.time0)
                return
            if (b == 2 or b == 1):
                tkinter.messagebox.showwarning("警告", "%s没有记录支出" % time3)
                return
        else:
            if (a == 3):
                tkinter.messagebox.showwarning("警告", "%s没有记录收入" % self.time0)
                return
            if (b == 3 or b == 1):
                tkinter.messagebox.showwarning("警告", "%s没有记录收入" % time3)
                return
        self.show(time3=time3)

    #界面函数
    #对比日期输入界面
    def __init__(self,con, user, goMain, time1):
        self.con = con
        self.user = user
        self.table = 'user' + user
        self.goMain = goMain
        self.time = time1
        self.time0 = time1[0] + '年' + time1[1] + '月'

        self.root=Tk()
        # goHelp(root=self.root)
        self.root.title('账单对比')
        self.root.resizable(0, 0)
        self.root.geometry('200x100')
        Label(self.root,text='分析月份:%s'%self.time0).place(relx=0,rely=0)
        Label(self.root,text='对比月份:').place(relx=0,rely=0.2)
        Label(self.root, text="年").place(relx=0.5, rely=0.2)
        self.e1 = Entry(self.root)
        self.e1.place(relx=0.3, rely=0.2, relwidth=0.2)
        Label(self.root, text="月").place(relx=0.7, rely=0.2)
        self.e2 = Entry(self.root)
        self.e2.place(relx=0.6, rely=0.2, relwidth=0.1)
        Button(self.root,text='确定',bg='snow',command=self.toCompare).place(relx=0.3,rely=0.5)
        Button(self.root, text='取消',bg='snow',command=self.b_return).place(relx=0.6, rely=0.5)
        self.root.mainloop()
    #对比界面框架绘制
    def toCompare(self):
        #判断输入合法性
        self.test=self.ifuse()
        if(self.test==0):
            return
        else:
            #框架搭建
            self.root.destroy()
            self.root=Tk()
            goHelp(root=self.root)
            time1 = str(self.test[0]) + '年' + str(self.test[1]) + '月'
            self.root.title('%s 与 %s 账单对比' %(self.time0,time1))
            self.root.resizable(0, 0)
            self.root.geometry('500x500')
            image1 = Image.open('source/鸟底纹素材.png')
            self.image2 = Image.open(r'source/鸟底纹素材2.png')
            back_image = ImageTk.PhotoImage(image1)
            self.background_image = ImageTk.PhotoImage(self.image2)
            Label(self.root, image=back_image).place(x=0, y=0)
            label = Label(self.root, text='%s 与 %s 账单对比' % (self.time0,time1), compound='center',
                          image=self.background_image)
            label.place(relx=0.18, rely=0)
            Label(self.root, text="查看",bg='snow').place(relx=0.55, rely=0.15)
            number2 = StringVar()
            self.numberChosen2 = ttk.Combobox(self.root, width=12, textvariable=number2, state='readonly')
            self.numberChosen2['values'] = ('支出', '收入')
            self.numberChosen2.place(relx=0.62, rely=0.15)
            self.numberChosen2.current(0)
            Button(self.root, text='确定', command=self.goUse,bg='snow').place(relx=0.86, rely=0.14)
            Button(self.root, text='返回', command=self.b_return,bg='snow').place(relx=0.47, rely=0.9)

            #图/文字绘制
            self.goUse()

            self.root.mainloop()
    # 对比显示界面绘图（参数：time3 对比月份/ self.choose: 支出/收入绘制选择）
    def show(self, time3):
        # 绘制种类选择
        tag = 1
        time1 = str(self.test[0]) + '年' + str(self.test[1])+ '月'
        if (self.choose == '支出'):
            tag = 0

        # 界面
        if (tag == 1):
            Label(self.root, text='%s 与 %s 收入对比' % (self.time0, time1), compound='center', fg='LimeGreen',
                  image=self.background_image).place(relx=0.18, rely=0)
        else:
            Label(self.root, text='%s 与 %s 支出对比' % (self.time0, time1), compound='center', fg='red',
                  image=self.background_image).place(relx=0.18, rely=0)

        # 当前日期
        # 饼图数据获取与绘制
        result2 = []
        result1 = Statistics.getIncome(self=self, tag=tag, result2=result2, time_b=self.time)
        pie = Statistics.Show(self=self, result0=result1, result2=result2, size=2.5, a=1 - tag)
        canvas_statis = FigureCanvasTkAgg(pie, self.root)
        canvas_statis.get_tk_widget().place(relx=0, rely=0.21)
        sum1 = 0
        # 最大值统计
        for i in result2:
            sum1 += i
        a = []
        a.append(result2[result2.index(max(result2))])
        a.append(result1[result2.index(max(result2))])

        # 对比日期
        # 饼图数据获取与绘制
        result2 = []
        self.test[0] = str(self.test[0])
        self.test[1] = str(self.test[1])
        result1 = Statistics.getIncome(self=self, tag=tag, result2=result2, time_b=self.test)
        pie = Statistics.Show(self=self, result0=result1, result2=result2, size=2.5, a=tag)
        canvas_statis = FigureCanvasTkAgg(pie, self.root)
        canvas_statis.get_tk_widget().place(relx=0.5, rely=0.21)
        sum2 = 0
        for i in result2:
            sum2 += i
        b = []
        b.append(result2[result2.index(max(result2))])
        b.append(result1[result2.index(max(result2))])

        # 数据统计并显示
        # 总支出/收入统计
        self.num(time1=self.time0, time2=time3, sum1=sum1, sum2=sum2, input="总%s" % self.choose)
        Label(self.root, text='%s总%s：￥%.2f' % (self.time0, self.choose, sum1), width=30, height=1,
              justify='center', bg='snow').place(relx=0.05, rely=0.7)
        Label(self.root, text='%s总%s：￥%.2f' % (time3, self.choose, sum2), width=30, height=1,
              justify='center', bg='snow').place(relx=0.55, rely=0.7)
        # 分别最高收入/支出统计
        if (b[1] == a[1]):
            Label(self.root, text='%s与%s最高%s均为：%s' % (self.time0, time3, self.choose, b[1]), width=70, height=1,
                  justify='center', bg='snow'). \
                place(relx=0, rely=0.76)
            self.num(time1=self.time0, time2=time3, sum1=a[0], sum2=b[0], input="%s" % self.choose)
        else:
            Label(self.root, text='%s最高%s：%s ￥%.2f' % (self.time0, self.choose, a[1], a[0]), width=30, height=1,
                  justify='center', bg='snow').place(relx=0.05, rely=0.76)
            Label(self.root, text='%s最高%s：%s ￥%.2f' % (time3, self.choose, b[1], b[0]), width=30, height=1,
                  justify='center', bg='snow').place(relx=0.55, rely=0.76)

        self.root.mainloop()
    # 对比结果输出显示（input:收入/支出等显示文字）
    def num(self, time1, time2, sum1, sum2, input):
        if (sum1 > sum2):
            a = round(sum1 / sum2, 2)
            a = int(a * 100)
            Label(self.root, text='%s比%s%s高：￥%.2f 百分比：%d%%' % (time1, time2, input, sum1 - sum2, a), width=70, height=1,
                  justify='center', bg='snow').place(relx=0, rely=0.85)
        elif (sum1 < sum2):
            a = round(sum2 / sum1, 2)
            a = int(a * 100)
            Label(self.root, text='%s比%s%s高：￥%.2f 百分比：%d%%' % (time2, time1, input, sum2 - sum1, a), width=70, height=1,
                  justify='center', bg='snow').place(relx=0, rely=0.85)
        else:
            Label(self.root, text='%s与%s有相同%s：￥%.2f' % (time1, time2, input, sum1), width=70, height=1,
                  justify='center', bg='snow').place(relx=0, rely=0.85)





