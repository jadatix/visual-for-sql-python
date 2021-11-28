from tkinter import *
from tkinter import font
from tkinter import messagebox
import pymysql
from sql_config import user,host,db_name,port

root=Tk()


def go_query():
    query=input_.get()
    try:
        connection=pymysql.connect(
        host=host,
        port=port,
        user=user,
        database=db_name,
        password=""
        )
        # messagebox.showinfo(title='Результат',message='success ')
        try:
            with connection.cursor() as cursor:
                # insert_query="INSERT INTO `employers` VALUES ('Python','Python',222,NULL);"
                cursor.execute(query)
                # print("Inserted! ")
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
    result.config(text='Статус запиту', fg='#4E9F3D')
    input_.delete(0,'end')



root['bg'] = '#1E5128'
root.title('Ваш СКюЛ запитник')
root.wm_attributes('-alpha',0.99)
root.geometry('720x400')
root.resizable(width=FALSE, height=False)

canvas=Canvas(root,height=400,width=720,bg='#1E5128')
canvas.pack()

frame=Frame(root,bg='#191A19')
frame.place(relx=0.15,rely=0.15,relheight=0.7,relwidth=0.7)
title=Label(frame,fg='#4E9F3D',bg='#191A19',text='Залиште ваш запит тут', font=20)
title.pack()
btn=Button(frame,bg='#D8E9A8',fg='#4E9F3D',text='Виконати',command=go_query)
btn.place(relx=0.25,rely=0.25)
input_=Entry(frame,bg='white',width=50)
input_.pack()
result=Label(frame,fg='#4E9F3D',bg='#191A19',text='Статус запиту', font=20)
result.pack()
clear_btn=Button(frame,bg='#D8E9A8',fg='#4E9F3D',text='Очистити',command=clear)
clear_btn.place(relx=0.62,rely=0.25)
root.mainloop()




