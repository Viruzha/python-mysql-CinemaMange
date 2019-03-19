import MySQLdb
import msvcrt
import os
import re
import threading
# class movie():
#     def __init__(self,serial_number,name,derict,main_actor,date,last_time,price):
#         self.serial_number=serial_number
#         self.name

class cinema():
    def __init__(self):
        self.CONN=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='1234',db='mysql',charset='UTF8')
        self.conn=self.CONN.cursor()
        try:
            self.conn.execute('USE ticket;')#如果ticket数据不存在则会抛出异常，然后就会初始化数据库
        except:
            self.__init()
    def __del__(self):
        self.conn.close()
        self.CONN.close()
    def __init(self):#重置系统
        self.conn.execute('''
        DROP DATABASE IF EXISTS ticket;
        CREATE DATABASE ticket;
        USE ticket;
        DROP TABLE IF EXISTS movie;
        CREATE TABLE 
        movie(serial_number char(10) NOT NULL PRIMARY KEY,
        name char(20) NOT NULL,
        derict char(10) DEFAULT 'unknown',
        main_actor char(10) DEFAULT 'unknown',
        last_time time NOT NULL,
        price double NOT NULL)CHARACTER SET utf8;

        DROP TABLE IF EXISTS infoRoom;
        CREATE TABLE 
        infoRoom(name char(10) NOT NULL,
        dbname int(10) PRIMARY KEY,
        size char(10))CHARACTER SET utf8;

        DROP TABLE IF EXISTS changci;
        CREATE TABLE
        changci(id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        serial_number char(10),
        ytname int(10),
        time datetime,
        left_seat int(10),
        choosen_seat text(1000));

        commit;
        ''')
    #    影厅座位的格式 4,5|3,4 以|分隔的是位置的坐标
    # CONSTRAINT FOREIGN KEY (serial_number) REFERENCES movie(serial_number),
    # CONSTRAINT FOREIGN KEY (ytname) REFERENCES infoROOM(dbname))CHARACTER SET utf8;

    def __exe(self,sql):
        #print(sql)
        self.conn.execute(sql)
        
        #self.conn.execute('commit;')
        return self.conn.fetchall()

    # def __make_string(self,a):
    #     s=''
    #     for i in range(a-1):
    #         s+=f'{i+1} char(2),'
    #     s+=f'{a} char(2)'
    #     return s

    def add_room(self):
        print('请选择影厅大小')
        size=self.xuanzhejiemian([('8*10',),('10*11',),('12*13',),('自定义',)],4,2,'请选择影厅大小')
        if size==None:
            return
        if self.__exe('SELECT COUNT(name) FROM infoRoom;')==():
            count=0
        else:
            count=int(self.__exe('SELECT COUNT(name) FROM infoRoom;')[0][0])
        if size=='自定义':
            size=f"{int(input('请输入排数'))}*{int(input('请输入列数'))}"
        self.__exe(f'''INSERT INTO infoRoom VALUES('影厅{count+1}','{count+1}','{size}');''')
        self.__exe('commit;')
        print('添加成功')
        print('按任意键返回主界面')
        msvcrt.getwch()
    
    def add_movie(self):
        while True:
            try:
                self.__exe(f'''INSERT INTO movie 
                VALUES('{input('请输入电影编号')}',
                '{input('电影名称：')}',
                '{input('导演：')}',
                '{input('主演：')}',
                '{input('持续时间：')}',
                '{input('票价:')}');''')
                self.__exe('commit;')
                print('添加成功')
                print('按任意键返回主界面')
                msvcrt.getwch()
                break
            except:
                print('输入错误或电影编号已存在请重新输入')
                print('按任意键继续。。。')
                msvcrt.getwch()
    
	
    def add_changci(self):
        while True:
            yt=self.__exe('SELECT name FROM infoRoom;')
            if yt==():
                print('影厅为空，请先添加影厅后再进行添加场次')
                print('按任意键继续。。。')
                msvcrt.getwch()
                break
            ytname=self.xuanzhejiemian(yt,len(yt),2,'请选择新增场次所在影厅')
            if ytname==None:
                return
            mv=self.__exe('SELECT serial_number FROM movie')
            if mv==():
                print('电影列表为空，请先添加电影后再进行添加场次')
                print('按任意键继续。。。')
                msvcrt.getwch()
                break
            mv_number=self.xuanzhejiemian(mv,len(mv),2,'请选择新增电影序列号')
            if mv_number==None:
                return
            rq=input('请输入增加该电影场次日期')
            cc=self.xuanzhejiemian([('9:00',),('13:00',),('17:00',),('21:00',),('0:00',)],5,2,'请选择增加该电影的时间段')
            if cc==None:
                return
            datetime=rq+' '+cc
            ii=self.__exe(f'''SELECT size FROM infoRoom WHERE name='{ytname}';''')
            left_seat=int(ii[0][0].split('*')[0])*int(ii[0][0].split('*')[1])
            if self.__exe(f'''SELECT * FROM changci WHERE  ytname='{ytname[2]}' AND time='{datetime}';''' )==():
                self.__exe(f'''INSERT INTO changci 
                (serial_number,ytname,time,left_seat,choosen_seat)
                VALUES('{mv_number}','{ytname[2]}','{datetime}','{left_seat}','-1,-1');''')
                self.__exe('commit;')
                print('添加场次成功')
                print('按任意键继续。。。')
                msvcrt.getwch()
                break
            else:
                print('该影厅当前时间段已存在播放电影,请重新选择')
                print('按任意键继续。。。')
                msvcrt.getwch()

        # yt=int(input('请输入新增场次所在的影厅号'))
        # rq=input('请输入增加该电影场次的日期')
        # cc=int(input('请输入增加该电影场次的时间 1.9:00场 2.13:00场 3.17:00场 4.21:00场 5.00:00场'))
        
    def del_room(self):
        while True:
            n=self.__exe('''SELECT name FROM infoRoom;''')
            if n==():
                print('不存在电影信息')
                print('按任意键继续。。。')
                msvcrt.getwch()
                return
            x=self.xuanzhejiemian(n,len(n),2,'请选择要删除的影厅名称')
            if x==None:
                return
            if self.__exe(f'''SELECT * FROM changci 
            INNER JOIN infoRoom ON changci.ytname=infoRoom.dbname 
            WHERE infoRoom.name='{x}';''')==():
                self.__exe(f'''DELETE FROM infoRoom WHERE name='{x}';''')
                self.__exe('commit;')
                print('删除成功')
                print('按任意键继续。。。')
                msvcrt.getwch()
                break
            else:
                print('该影厅还存在放映电影场次，请确认后重新输入')
                print('按任意键继续。。。')
                msvcrt.getwch()


    def del_movie(self):
        while True:
            n=self.__exe('''SELECT name FROM movie;''')
            if n==():
                print('不存在电影信息')
                print('按任意键继续。。。')
                msvcrt.getwch()
                return
            x=self.xuanzhejiemian(n,len(n),2,'请选择要删除的电影名称')
            if x==None:
                return
            
            if self.__exe(f'''SELECT * FROM changci 
            INNER JOIN movie 
            ON changci.serial_number=movie.serial_number 
            WHERE movie.name='{x}';''')==():
                self.__exe(f'''DELETE FROM movie WHERE name='{x}';''')
                self.__exe('commit;')
                print('删除成功')
                print('按任意键继续。。。')
                msvcrt.getwch()
                break
            else:
                print('该电影还存在放映电影场次，请确认后重新选择')
                print('按任意键继续。。。')
                msvcrt.getwch()

                
#    def show_movie(self):
    #     a=self.__exe('SELECT * FROM movie')
    #     return a
        
    # def show_changci(self,name):
    #     a=self.__exe(f'SELECT movie.name,changci.time,changci.ytname,changci.left_seat,movie.price FROM changci INNER JOIN movie ON changci.serial_number=movie.serial_number WHERE movie.name={name}')
    #     return a 

    # def show_leftTicket(self,name,id_changci):
    #     a=self.__exe(f'SELECT choosen_seat FROM changci INNER JOIN movie ON changci.serial_number=movie.serial_number WHERE changci.id={id_changci}')
    #     return a

    

    def xuanzhejiemian(self,a,size1,m,remind):#a为显示数据，size为显示数据的大小 为列表【宽，长】(从1开始) m=1时为选座位 m=2时为菜单选择界面
        if m==1:#a,size1此时仅为文本数据 需要将其转化为数组形式
            size1=[int(size1[0].split('*')[0]),int(size1[0].split('*')[1])]
            a=a[0][0].split('|')
            b=[]#储存临时数据
            if a!=['']:
                for i in a:
                    #print(type(a))
                    #print(a)
                    b.append((int(i.split(',')[0]),int(i.split(',')[1])))#a的储存形式为：'4,3|2,5'
            a=b
            b=set() #选择结果
            c=0 #指针的横坐标
            d=0 #指针的竖坐标
            while (c,d) in a:
                if c==size1[0]:
                    c=0
                    d+=1
                else:
                    c+=1   #将指针遍历到空座位
            
            while True:
                print(remind)
                #print('guangbiao:',[c,d])
                for i in range(size1[0]):
                    for n in range(size1[1]):
                        if (i,n) in a:
                            print('+    ',end='')
                        elif (i,n) in b:
                            print('%    ',end='')#如果该坐标已经被自己选择就会打印%
                        else:
                            print('@    ',end='')
                    print('')
                    for n in range(size1[1]):
                        if (i,n)==(d,c):
                            print('↑    ',end='')
                        else:
                            print('     ',end='')
                    print('')
                print('w 上，a 左，s 下，d 右来移动光标，j选择位置，k确定位置并提交')
                if b==set():
                    print('你现在还没有选择座位')
                else:
                    print('你现在选择的座位有',b)
                i=ord(msvcrt.getwch())
                if i==119 or i==87:
                    if d!=0:
                        for n in reversed(range(d)):#遍历到座位没有被选过的坐标上，下同
                            if (n,c) not in a:
                                d=n
                                break
                                
                elif i==65 or i==97:
                    if c!=0:
                        for n in reversed(range(c)):
                            if (d,n) not in a:
                                c=n
                                break
                                
                elif i==115 or i==83:
                    if d!=size1[0]:
                        for n in range(d+1,size1[0]):
                            if (n,c) not in a:
                                d=n
                                break
                                
                elif i==68 or i==100:
                    if c!=size1[1]:
                        for n in range(c+1,size1[1]):
                            if (d,n) not in a:
                                c=n
                                break
                elif i==106:
                    b.add((d,c))
                elif i==107 or i==75:
                    os.system('cls')
                    return b
                os.system('cls')
        elif m==2:
            c=0
            while True:
                os.system('cls')
                print('\t',remind)
                for i in range(size1):
                    if i==c:
                        print('→ \t',end='')
                    else:
                        print(' \t',end='')
                    print(a[i][0])
                    
                print('')
                print('w，s分别向上下移动光标，k确定,q返回上一界面(主界面即退出)')
                i=ord(msvcrt.getwch())
                #print(i)
                if i==119 or i==87 :
                    if c!=0:
                        c-=1
                elif i==115 or i==83:
                    if c!=size1-1:
                        c+=1
                elif i==107 or i==75:
                    #print(i)s
                    return a[c][0]
                elif i==113:
                    return
                os.system('cls')
    def choose_seat(self):
        i=self.__exe('''SELECT DISTINCT movie.name 
        FROM changci 
        INNER JOIN movie 
        ON changci.serial_number=movie.serial_number;''')
        if i==():
            print('本电影院还没有电影要放映，请联系管理员添加电影放映')
            print('按任意键继续。。。')
            msvcrt.getwch()
            return
        os.system('cls')
        name=self.xuanzhejiemian(i,len(i),2,'请选择需要观看的电影')
        if name==None:
            return
        i=self.__exe(f'''SELECT DISTINCT infoRoom.name 
        FROM changci 
        INNER JOIN infoRoom 
        ON changci.ytname=infoRoom.dbname 
        INNER JOIN movie 
        ON changci.serial_number=movie.serial_number 
        WHERE movie.name='{name}';''')
        ytname=self.xuanzhejiemian(i,len(i),2,f'请选择要在哪个影厅观看{name}')
        if ytname==None:
            return
        i=self.__exe(f'''SELECT DISTINCT changci.time 
        FROM changci 
        INNER JOIN infoRoom 
        ON changci.ytname=infoRoom.dbname 
        INNER JOIN movie 
        ON changci.serial_number=movie.serial_number 
        WHERE movie.name='{name}' AND infoRoom.name='{ytname}';''')
        time=self.xuanzhejiemian(i,len(i),2,f'请选择要在哪个时间在{ytname}观看{name}')
        if time==None:
            return
        i=self.__exe(f'''SELECT changci.id FROM changci 
        INNER JOIN infoRoom 
        ON changci.ytname=infoRoom.dbname 
        INNER JOIN movie 
        ON changci.serial_number=movie.serial_number 
        WHERE movie.name='{name}' AND infoRoom.name='{ytname}' AND time='{time}';''')[0]
        #i为选择的场次的ID信息
        n=self.__exe(f'SELECT choosen_seat FROM changci where id ={i[0]}')#已选择的座位信息
        size=self.__exe(f'''SELECT infoRoom.size FROM changci 
        INNER JOIN infoRoom 
        ON changci.ytname=infoRoom.dbname 
        INNER JOIN movie 
        ON changci.serial_number=movie.serial_number 
        WHERE movie.name='{name}' AND infoRoom.name='{ytname}' AND time='{time}';''')[0]
        os.system('cls')
        left_seat=int(self.__exe(f'SELECT left_seat FROM changci WHERE id={i[0]};')[0][0])
        if left_seat ==0:
            print('该场次已满')
            print('按任意键返回。。。')
            msvcrt.getwch()
            return
        seat=self.xuanzhejiemian(n,size,1,'请选择座位')
        if seat!=set():
            s=''#要更新的场次座位信息
            for m in seat:
                s+=('|'+str(m[0])+','+str(m[1]))
            #print('s:',type(s))
            #print('n:',type(n))
            s=n[0][0]+s
            self.__exe(f'''UPDATE changci SET choosen_seat='{s}' WHERE id={i[0]};''')
            self.__exe(f'''UPDATE changci 
            SET left_seat=
            '{self.__exe(f'SELECT left_seat FROM changci WHERE id={i[0]};')[0][0]-len(seat)}' 
            WHERE id={i[0]};''')
            self.__exe('commit;')
            print('选票成功')
            print(f'你选择的是在{time}的{ytname}中观看{name}')
            print(f'你的座位号为{seat}')
            print('按任意键返回主界面')
            msvcrt.getwch()
        else:
            print('选择票为空，按任意键返回主界面')
            msvcrt.getwch()

                    


def main():
    def start():
        global a
        a=cinema()
    t=threading.Thread(target=start)
    t.start()
    os.system('cls')
    print('\n'*2)
    print('\t\t启动中。')
    print('\n'*3)
    t.join()
    while True:
        os.system('cls')
        ch=a.xuanzhejiemian([('1.管理界面',),('2.选票界面',)],2,2,'影院主界面')
        if ch==None:
            return

        if ch=='1.管理界面':
            while True:
                ch1=a.xuanzhejiemian([('1.增加新电影',),('2.删除电影',),('3.添加影厅',),('4.删除影厅',),('5.添加场次',)],5,2,'管理界面')
                if ch1==None:
                    break
                if ch1=='1.增加新电影':
                    a.add_movie()
                elif ch1=='2.删除电影':
                    a.del_movie()
                elif ch1=='3.添加影厅':
                    a.add_room()
                elif ch1=='4.删除影厅':
                    a.del_room()
                elif ch1=='5.添加场次':
                    a.add_changci()
        elif ch=='2.选票界面':
            a.choose_seat()

main()



        # a=self.__exe('SELECT * FROM changci INNER JOIN movie ON changci.serial_number = movie.serial_number;')
        # for i in a:
        #     print(f'{i[6]}\t{}')
                
       
