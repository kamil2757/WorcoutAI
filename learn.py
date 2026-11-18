# from tkinter import *

# root = Tk()
# icon_image = PhotoImage(file ='icon.png')

# root.geometry('600x300')
# root.resizable(width=False, height=False)
# root.title('Learning tkinter...')
# root.config(bg='#C0C0C0')
# root.iconphoto(True, icon_image)

# def click():
#     print('Hello')

# textButtonColor = 'white'
# textColor = 'black'

# fontSizeBase = 12

# btn = Button(root,
#               text='Button', 
#               command=click, 
#               font = ('Arial', fontSizeBase, 'bold'), 
#               bg="#535353", 
#               activebackground="#474747",
#               fg=textButtonColor,
#               activeforeground=textButtonColor
#               )

# lab = Label(root,
#             text='some Text',
#             font = ('Arial', fontSizeBase),
#             fg=textColor,
#             bg='#C0C0C0'
#             )
# img = PhotoImage(file='icon.png')
# l_img = Label(root,
#               image=img,
#               height=100,
#               width=700,
#               )
# l_img.pack()
# btn.pack()
# lab.pack()

# root.mainloop()

# from tkinter import *
# from random import *
# root = Tk()
# root.title('Камень ножницы бумага')
# root.resizable(width=False, height=False)
# root.geometry('600x300')

# fontColor = 'white'
# bgColor = "#313138"
# fontBase = 'Sans MS'

# root['bg'] = bgColor
# def RandomKnb(player_choice):
#     knb = ['Камень', 'Ножницы', 'Бумага']
#     computer_choice = choice(knb)

#     if player_choice == computer_choice:
#         result = "Ничья! 🤝"
#     elif (player_choice == 'Камень' and computer_choice == 'Ножницы') or \
#          (player_choice == 'Ножницы' and computer_choice == 'Бумага') or \
#          (player_choice == 'Бумага' and computer_choice == 'Камень'):
#         result = "Вы победили! 🎉"
#     else:
#         result = "Вы проиграли! 😢"

#     labelText.configure(text=f'Противник: {computer_choice}')
#     writeResult.configure(text=result)

# labelTitle = Label(root, text='Камень ножницы бумага', fg=fontColor, font=(fontBase, 14), bg=bgColor)
# labelText = Label(root, text='Выбор противника', fg=fontColor, font=(fontBase, 12), bg=bgColor)

# labelText.pack()
# stone = Button(root, text='Камень', font=(fontBase, 12), bg='white', activebackground='white', command=lambda: RandomKnb('Камень'))
# stone.pack()

# scissors = Button(root, text='Ножницы', font=(fontBase, 12), bg='white', activebackground='white', command=lambda: RandomKnb('Ножницы'))
# scissors.pack()

# paper = Button(root, text='Бумага', font=(fontBase, 12), bg='white', activebackground='white', command=lambda: RandomKnb('Бумага'))
# paper.pack()

# writeResult = Label(root, text='Результат', fg=fontColor, font=(fontBase, 12), bg=bgColor)
# writeResult.pack()


# root.mainloop()


# from tkinter import *
#
# root = Tk()
# root.title('Learn')
# root.geometry('600x400')
# root.resizable(0,0)
#
# def open_dialog():
#     win = Toplevel(root)
#     win.geometry('400x300')
#     win.resizable(0,0)
#
#     win.title('dialog')
#     Label(win, text='Диалог поверх главного').pack()
#     Button(win, text='Закрыть окно', command=win.destroy).pack()
#
# Button(text='button', command=open_dialog).pack()
#
# root.mainloop()


# from tkinter import *
#
# root = Tk()
# root.geometry('400x300')
# root.resizable(0, 0)
# root.title = 'Learn'
#
# Label(root, text='Название упражнения').pack()
# entry = Entry(root, width=30)
# entry.pack()
#
# Label(root, text='заметки:').pack()
# text = Text(root, height=5, width=40)
# text.pack()
#
#
# def on_click():
#     name = entry.get()
#     note = text.get('1.0', 'end-1c')
#     Label(root, text=f'Упражнение: {name}; заметка: {note}').pack()
#
# Button(text='Add', command=on_click).pack()
#
# root.mainloop()


# from tkinter import *
# root = Tk()
# root.geometry('600x400')
# root.resizable(0, 0)
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)
#
#
# form = LabelFrame(root, padx=10, pady=10, text='title', bg='black', fg='white')
# form.grid(row=0, column=0, sticky='n')
#
# Label(form, text='Упражнения:', bg='black', fg='white').grid(row=0, column=0, sticky='w', pady=0)
# exercises = Entry(form, width=50)
# exercises.grid(row=0, column=1, padx=5)
#
# Label(form, text='Подходы:', bg='black', fg='white').grid(row=1, column=0, sticky='w', pady=10)
# sets = Entry(form, width=50)
# sets.grid(row=1, column=1, padx=5)
#
#
# def printInfo():
#     print('Упражнения: ' + exercises.get() + '; подходы: ' + sets.get())
# Button(form, text='Добавить', command=printInfo).grid(row=2, column=1, pady=10)
#
#
# root.mainloop()

# from tkinter import *
#
# root = Tk()
# root.geometry('400x300')
# root.resizable(0, 0)
#
# name_var = StringVar()
# reps_var = IntVar(value=10)
#
# Label(root, text='title:').grid(row=0, column=0, padx=10, pady=10)
# Entry(root, textvariable=name_var).grid(row=0, column=1)
#
# Label(root, text='repetitions:').grid(row=1, column=0)
# Entry(root, textvariable=reps_var).grid(row=1, column=1)
#
#
# def show():
#     print('title:', name_var.get())
#     print('repetitions:', reps_var.get())
#
# Button(root, text='see', command=show).grid(row=2, column=0)
#
# root.mainloop()


# from tkinter import *
# from tkinter.ttk import *
#
# root = Tk()
# root.geometry('500x350')
# root.resizable(0, 0)
# done_var = IntVar()
# type_var = StringVar()
#
# Checkbutton(root, text='Done', variable=done_var).grid(row=0, column=0)
# combo = Combobox(root, textvariable=type_var, values=['Силовая', 'Кардио', 'Растяжка'], state='readonly')
# combo.grid(row=1, column=0, pady=10)
# combo.current(0)
#
#
# def show():
#     print('Done: ', bool(done_var.get()))
#     print('Type:', type_var.get())
#
# Button(text='Ok', command=show).grid(row=2, column=0)
#
# root.mainloop()


# from tkinter import *
# from tkinter import messagebox
#
# root = Tk()
# root.geometry('400x300')
# root.resizable(0, 0)
#
# messagebox.showinfo('Ready', 'The train is saved')
# messagebox.showerror('Error', 'Title cant be empty')
#
# if messagebox.askyesno('Delete?', 'Delete the exercise?'):
#     print('Delete')
# else:
#     print('Cancel')
#
# root.mainloop()


# from tkinter import *
# from tkinter.ttk import *
#
# root = Tk()
# root.geometry('700x400')
# root.resizable(0, 0)
# cols = ('exercise', 'sets', 'reps', 'done')
# tree = Treeview(root, columns=cols, show='headings', height=6)
#
# tree.heading('exercise', text='Упражнение')
# tree.heading('sets', text='Подходы')
# tree.heading('reps', text='Повторы')
# tree.heading('done', text='✓')
#
# tree.column('exercise', width=200)
# tree.column('sets', width=80)
# tree.column('reps', width=80)
# tree.column('done', width=40)
#
# tree.pack(padx=0, pady=10)
#
# tree.insert('', 'end', values=('Присед', 3, 10, '☐'))
# tree.insert('', 'end',values=("Жим лёжа", 4, 8, "☑"))
#
# def get_selected():
#     sel = tree.selection()
#     if sel:
#         item_id = sel[0]
#         values = tree.item(item_id, 'values')
#         print('Choose: ', values)
#
# Button(root, text='choose', command=get_selected).pack()
#
# root.mainloop()


# from tkinter import *
# from tkinter import messagebox
# from tkinter.ttk import Combobox, Treeview
#
# root = Tk()
# root.title('fitness Tracker')
# root.geometry('500x300')
# root.resizable(0,0)
# root.columnconfigure(0, weight=1)
#
#
# name_var = StringVar()
# type_var = StringVar(value='Силовая')
# sets_var = IntVar(value=3)
# reps_var = IntVar(value=10)
#
# form = Frame(root, bg='#9ea2e5')
# form.grid(row=0, column=0,  sticky='ew')
# inner = Frame(form, bg='#9ea2e5')
# inner.pack(expand=True, pady=10)
#
#
# Label(inner, text='Упражнение:', bg='#9ea2e5').grid(row=0, column=0, sticky='w')
# Entry(inner, textvariable=name_var).grid(row=0, column=1, padx=10, pady=10, sticky='ew')
#
# Label(inner, text='Тип:', bg='#9ea2e5').grid(row=1, column=0)
# Combobox(inner,  textvariable=type_var, state='readonly', values=["Силовая", "Кардио", "Растяжка"]).grid(row=1, column=1, padx=10, sticky='ew')
#
# Label(inner, text='Подходы:', bg='#9ea2e5').grid(row=0, column=2)
# Entry(inner, textvariable=sets_var).grid(row=0, column=3, padx=10, sticky='ew')
#
# Label(inner, text='Повторы:', bg='#9ea2e5').grid(row=1, column=2)
# Entry(inner, textvariable=reps_var).grid(row=1, column=3, padx=10, pady=10, sticky='ew')
#
#
# cols = ('exercises', 'type', 'sets', 'reps', 'done')
# tree = Treeview(root, columns=cols, show='headings', height=10)
# for c, t, w in zip(cols, ["Упражнение", "Тип", "Подходы", "Повторы", "✓"],
#                    [200, 100, 70, 70, 40]):
#     tree.heading(c, text=t)
#     tree.column(c, width=w, anchor='center' if c != 'exercise' else 'w')
# tree.grid(row=1, column=0, sticky='nsew', padx=10)
# root.rowconfigure(1, weight=1)
#
# btns = Frame(root)
# btns.grid(row=2, column=0)
#
#
# def add_exercises():
#     name = name_var.get()
#     if not name:
#         messagebox.showerror('Ошибка', 'Введи название упражнения')
#         return
#     try:
#         sets = sets_var.get()
#         reps = reps_var.get()
#     except TclError:
#         messagebox.showerror("Ошибка", "Подходы и повторы должны быть числами")
#         return
#     tree.insert('', 'end', values=(name, type_var.get(), sets, reps, "☐"))
#     name_var.set('')
#
#
# def toggle_done():
#     sel = tree.selection()
#     if not sel:
#         return
#
#     item = sel[0]
#     vals = list(tree.item(item, 'values'))
#     vals[4] = '☑' if vals[4] == '☐' else '☐'
#     tree.item(item, values=vals)
#
#
# def delete_exercises():
#     sel = tree.selection()
#     if not sel:
#         return
#     if messagebox.askyesno('Удалить?', "Удалить выбранное упражнение?"):
#         tree.delete(sel[0])
#
# Button(btns, text='Add', command=add_exercises).pack(side='left', padx=2)
# Button(btns, text='Done', command=toggle_done).pack(side='left', padx=2)
# Button(btns, text='Delete', command=delete_exercises).pack(side='left', padx=2)
#
# root.mainloop()

# import sqlite3
#
# connection = sqlite3.connect('test.db')
# cursor = connection.cursor()
# cursor.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, age INT);')
#
# cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('frank', 18))
# connection.commit()


# import sqlite3
#
# db = sqlite3.connect('mydb.db')
# cursor = db.cursor()
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS articles (
#     title TEXT,
#     full_text TEXT,
#     views INT,
#     author TEXT
# );""")
# db.commit()
#
# cursor.execute("""
#     INSERT INTO articles (title, full_text, views, author)
#     VALUES (?, ?, ?, ?);
# """, ('Гномы разбушевались', 'Гномы в Техасе захотели кушать, но не было денег, они разгромили по этой причине пол'
#                              'города', 5, 'Kamil'))
#
# cursor.execute('SELECT rowid, full_text FROM articles WHERE title=?', ('Гномы разбушевались',))
# cursor.execute('DELETE FROM articles WHERE rowid=5')
#     cursor.execute("""UPDATE articles SET author = 'Admin' where  title = 'l'""")
# # print(cursor.fetchall())
# print(cursor.fetchone())
# db.commit()
# db.close()


# from tkinter import *
# from tkinter import messagebox
#
#
# class App(Tk):
#     def __init__(self):
#         super().__init__()
#         self.title('Todo')
#         self.geometry('400x500')
#
#         self.username = ''
#         self.tasks = []
#
#         self.current_screen = None
#         self.show_screen(LoginScreen)
#
#     def show_screen(self, screen_class):
#         if self.current_screen:
#             self.current_screen.destroy()
#         self.current_screen = screen_class(self)
#         self.current_screen.pack(fill='both', expand=True)
#
#
# class LoginScreen(Frame):
#     def __init__(self, app):
#         super().__init__(app)
#         self.app = app
#         self._build()
#
#     def _build(self):
#         Label(self, text='Welcome!').pack(pady=40)
#         Label(self, text='Enter your name:').pack()
#         self.name_entry = Entry(self)
#         self.name_entry.pack(pady=10)
#         Button(self, text='Login', command=self._login).pack(pady=20)
#
#     def _login(self):
#         name = self.name_entry.get().strip()
#         if not name:
#             messagebox.showerror('Error', 'Name cant be empty')
#             return
#
#         self.app.username = name
#         self.app.show_screen(TodoScreen)
#
#
# class TodoScreen(Frame):
#     def __init__(self, app):
#         super().__init__(app)
#         self.app = app
#         self._build()
#
#     def _build(self):
#         header = Frame(self)
#         header.pack(fill='x', pady=10, padx=10)
#         Label(header, text=f'Hello, {self.app.username}!').pack(side='left')
#         Button(header, text='Exit', command=self._logout).pack(side='right')
#
#         input_frame = Frame(self)
#         input_frame.pack(fill="x", padx=10, pady=10)
#
#         self.task_entry = Entry(input_frame)
#         self.task_entry.pack(side='left', fill='x', expand=True)
#
#         self.task_entry.bind("<Return>", lambda event: self._add_task())
#         Button(input_frame, text='Добавить', command=self._add_task).pack()
#
#         self.listbox = Listbox(self)
#         self.listbox.pack()
#
#         for task in self.app.tasks:
#             self.listbox.insert(END, task)
#
#         Button(self, text='Очистить все', command=self._clear_tasks).pack()
#
#     def _add_task(self):
#         task_text = self.task_entry.get().strip()
#
#         if task_text:
#             self.app.tasks.append(task_text)
#             self.listbox.insert(END, task_text)
#             self.task_entry.delete(0, END)
#
#     def _clear_tasks(self):
#         self.app.tasks.clear()
#         self.listbox.delete(0, END)
#
#     def _logout(self):
#         self.app.show_screen(LoginScreen)
#
#
# if __name__ == '__main__':
#     app = App()
#     app.mainloop()




# import sqlite3
#
# conn = sqlite3.connect('todo.db')
# cursor = conn.cursor()
#
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS tasks (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         title TEXT NOT NULL,
#         is_done INTEGER DEFAULT 0,
#         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
# ''')
# conn.commit()
#
#
# def add_task(title):
#     cursor.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
#     conn.commit()
#     print(f'Задача {title} добавлена!')
#
#
# def get_all_tasks():
#     cursor.execute('SELECT id, title, is_done FROM tasks')
#     rows = cursor.fetchall()
#     for row in rows:
#         status = '✓' if rows[2] == 1 else '✗'
#         print(f'[{row[0]}] {row[1]} - {status}')
#
#
# def mark_as_done(task_id):
#     cursor.execute('UPDATE tasks SET is_done = 1 WHERE id = ?', (task_id,))
#     conn.commit()
#     print(f"Задача с ID {task_id} выполнена!")
#
#
# def delete_task(task_id):
#     cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
#     conn.commit()
#     print(f"Задача с ID {task_id} удалена!")
#
#
#
# add_task('buy bread')
# mark_as_done(1)
# delete_task(1)
# conn.close()


