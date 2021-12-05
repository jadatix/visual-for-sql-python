from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import pymysql
from sql_config import user,host,db_name,port,password
from option_list_try import OptionList

def execute(query):
    try:
        connection=pymysql.connect(host=host,port=port,user=user,database=db_name,password=password)
        try:
            with connection.cursor() as cur:
                cur.execute(query)
            # connection.commit()
            re=cur.fetchall()
        except Exception as exe:
            print("Щось пішло не так "+str(exe))
        finally:
            connection.close()
            return re
    except Exception as ex:
        print("connection failed ")
        print(ex)

def go_query():
    query=input_.get()
    try:
        connection=pymysql.connect(
        host=host,
        port=port,
        user=user,
        database=db_name,
        password=password
        )
        try:
            with connection.cursor() as cursor:
                # insert_query="INSERT INTO `employers` VALUES ('Python','Python',222,NULL);"
                cursor.execute(query)
            connection.commit()
            result.config(text='Успішний запит')
        except Exception as exe:
            result.config(text='Запит зафейлився ', fg="#ff0000")
            messagebox.showerror(title='Помилка запиту', message=str(exe))
        finally:
            connection.close()
            # input_.delete(0,'end')
    except Exception as ex:
        print("connection failed ")
        print(ex)

def clear():
    result.config(text='Статус запиту', fg='#000000')
    input_.delete(0,'end')


def callback(*args):
    tv.delete()
    label_opt.configure(text="The selected item is {}".format(variable.get()))
    query="SELECT * FROM `"+str(variable.get())+"`;"
    try:
        connection=pymysql.connect(host=host,port=port,user=user,database=db_name,password=password)
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
            connection.commit()
            rows=cursor.fetchall()
            total=cursor.rowcount
            # with connection.cursor as cur:
            #     cur.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='"+db_name+"' AND `TABLE_NAME`='"+str(variable.get())+"';")
            headers=execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='"+db_name+"' AND `TABLE_NAME`='"+str(variable.get())+"';")
            # headers=cur.fetchall()
            col_num=len(headers)
        except Exception as exe:
            print("Щoсь пішло не так")
        finally:
            connection.close()
    except Exception as ex:
        print("connection failed ")
        print(ex)
    
    column = []
    for i in range(1,col_num+1):
        column.append(i)
    tv.config(columns=column)
    tv.place(y=30)
    hsb = Scrollbar(tab2, orient="horizontal", command=tv.xview)
    hsb.place(relx=0.014, rely=0.875, relheight=0.020, relwidth=0.965)

    tv.configure(xscrollcommand=hsb.set)

    for i in range(col_num):
        tv.heading(i+1,text=headers[i])
    for i in rows:
        tv.insert('','end',values=i)
    

root=Tk()


root['bg'] = '#1E5128'
root.title('Ваш СКюЛ запитник')
root.wm_attributes('-alpha',0.99)
root.geometry('720x400')
root.resizable(width=FALSE, height=False)

tabControl=ttk.Notebook(root)
tab1=ttk.Frame(tabControl)
tab2=ttk.Frame(tabControl)

tabControl.add(tab1,text='Запити')
tabControl.add(tab2,text='Переглянути таблиці')
tabControl.pack(expand=1, fill="both")

title=Label(tab1,text='Залиште ваш запит тут', font=20)
title.pack()

input_=Entry(tab1,bg='white',width=50)
input_.pack()

btn=Button(tab1,text='Виконати',command=go_query)
btn.place(relx=0.25,rely=0.25)

result=Label(tab1,text='Статус запиту', fg="#000000", font=20)
result.pack()

clear_btn=Button(tab1,text='Очистити',command=clear)
clear_btn.place(relx=0.62,rely=0.25)

variable = tk.StringVar(tab2)
variable.set(OptionList[0])

opt = tk.OptionMenu(tab2, variable, *OptionList)
opt.config(width=90, font=('Helvetica', 12))
opt.place(x=10,y=1, width=150)


label_opt = tk.Label(tab2,text="", font=('Helvetica', 12), fg='red')
label_opt.place()


variable.trace('w',callback)

tv=ttk.Treeview(tab2,column=0,show="headings",height=5)

# hsb = Scrollbar(tab2, orient="horizontal", command=tv.xview)
# hsb.place(relx=0.014, rely=0.875, relheight=0.020, relwidth=0.965)

# tv.configure(xscrollcommand=hsb.set)

# tv.config(selectmode='browse')
# vsb = ttk.Scrollbar(root,orient="vertical",command=tv.yview)
# tv.config(yscrollcommand=vsb.set)

root.mainloop()