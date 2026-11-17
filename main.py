from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import showerror
from tkinter.ttk import Combobox

bg_color = '#1c1f2b'
dark_bg_color = '#101219'
font_color = 'white'
font2_color = '#a3b3d7'
red_color = '#640b0f'

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('WorkoutИИ')
        self.geometry('700x400')
        self.resizable(0, 0)
        self.configure(bg=bg_color)

        self.username = None

        self.current_screen = None
        self.show_screen(LoginScreen)

    def show_screen(self, screen_class):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = screen_class(self)
        self.current_screen.pack(fill='both', expand=True, padx=20, pady=20)


class LoginScreen(Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.username_var = StringVar()
        self.configure(bg=bg_color)
        self._build()

    def _build(self):
        Label(self, text='WorkoutИИ: Журнал тренировок', font=('Arial', 14, 'bold'), bg=bg_color, fg=font_color).pack(pady=20)

        Label(self, text='Как тебя зовут?',  bg=bg_color, fg=font_color, font=('Arial', 10)).pack(pady=8)
        self.name_entry = Entry(self, textvariable=self.username_var)
        self.name_entry.pack(pady=10)
        Button(self, text='Продолжить', command=self._login, bg='white', font=('Arial', 10)).pack()

    def _login(self):
        name = self.username_var.get()
        if not name:
            messagebox.showerror('Ошибка', 'Поле имени не может быть пустым')
            return
        self.app.username = name
        self.app.show_screen(CreateWeekScreen)


class CreateWeekScreen(Frame):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.configure(bg=bg_color)
        self._build()

    def _build(self):
        Label(self, text=f'Привет, {self.app.username}', font=('Arial', 10), bg=bg_color, fg=font_color).pack()
        Label(self, text='Как создашь свое расписание?', font=('Arial', 14), bg=bg_color, fg=font_color).pack( pady=20)

        Button(self, text='✍ Заполнить вручную', font=('Arial', 10, 'bold'),height=2, bg=font2_color, command=lambda: self.app.show_screen(WeekScreen), width=40).pack(pady=0)
        Label(self, text='Сам добавишь тренировки на каждый день', font=('Arial', 10), bg=bg_color, fg=font_color).pack()


        Button(self, text='🤖 Составить с помощью ИИ', font=('Arial', 10, 'bold'), height=2, bg=font2_color, command=lambda: self.app.show_screen(CreateAiScreen), width=40).pack(pady=(20, 0))
        Label(self, text='Заполняешь анкеты - ИИ расставит план', font=('Arial', 10), bg=bg_color, fg=font_color).pack()

        Label(self, text='План всегда можно будет пересоздать', font=('Arial', 8), bg=bg_color, fg=font2_color).pack(pady=26)


class CreateAiScreen(Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        self.height_var = IntVar()
        self.width_var = IntVar()
        self.age_var = IntVar()
        self.aim_var = StringVar()
        self.experience_var = StringVar()
        self.equipment_var = StringVar()
        self.per_week_var = IntVar()
        self.duration_var = IntVar()

        self.configure(bg=bg_color)

        self._build()

    def _build(self):
        header = Frame(self)
        header.pack()
        Label(header, text='Генерация плана с помощью ИИ', font=('Arial', 14), bg=bg_color, fg=font_color).pack(anchor='w')

        main = Frame(self, bg=bg_color)
        main.pack(anchor='w', fill='both', expand=True, pady=(20, 0))

        # --- ЛЕВАЯ КОЛОНКА (col=0 и col=1) ---
        Label(main, text='Рост, см: ', bg=bg_color,font=('Arial', 10),  fg=font_color).grid(row=1, column=0, sticky='w', pady=2)
        Entry(main, textvariable=self.height_var, width=8).grid(row=1, column=1, sticky='w', padx=5, pady=2)

        Label(main, text='Вес, кг: ', bg=bg_color,font=('Arial', 10),  fg=font_color).grid(row=2, column=0, sticky='w', pady=2)
        Entry(main, textvariable=self.width_var, width=8).grid(row=2, column=1, sticky='w', padx=5, pady=2)

        Label(main, text='Возраст: ', bg=bg_color,font=('Arial', 10),  fg=font_color).grid(row=3, column=0, sticky='w', pady=2)
        Entry(main, textvariable=self.age_var, width=8).grid(row=3, column=1, sticky='w', padx=5, pady=2)

        Label(main, text='Цель: ', bg=bg_color,font=('Arial', 10),  fg=font_color).grid(row=4, column=0, sticky='w', pady=2)
        Combobox(main, textvariable=self.aim_var, values=[
            'Похудение', 'Набор массы', 'Поддержание формы', 'Сила', 'Выносливость'
        ], state='readonly', width=18).grid(row=4, column=1, sticky='w', padx=5, pady=2)

        # --- ПРАВАЯ КОЛОНКА (col=2 и col=3) ---
        Label(main, text='Опыт: ', bg=bg_color,font=('Arial', 10),  fg=font_color).grid(row=1, column=2, sticky='w', pady=2, padx=(20, 0))
        Combobox(main, state="readonly", textvariable=self.experience_var, width=18, values=[
            'Новичок', 'Средний', 'Продвинутый'
        ]).grid(row=1, column=3, sticky='w', padx=5, pady=2)

        Label(main, text='Оборудование: ', bg=bg_color,font=('Arial', 10),  fg=font_color).grid(row=2, column=2, sticky='w', pady=2, padx=(20, 0))
        Combobox(main, state="readonly", textvariable=self.equipment_var,values=[
            'Зал (всё есть)','Дом (без инвентаря)', 'Улица'
        ], width=18).grid(row=2, column=3, sticky='w', padx=5, pady=2)

        Label(main, text='Тренировок в нед.: ', bg=bg_color,font=('Arial', 10),  fg=font_color).grid(row=3, column=2, sticky='w',
                                                                                 padx=(20, 0), pady=2)
        Entry(main, textvariable=self.per_week_var, width=8).grid(row=3, column=3, sticky='w', padx=5, pady=2)

        Label(main, text='Длительность, мин: ', bg=bg_color,font=('Arial', 10),  fg=font_color).grid(row=4, column=2, sticky='w',
                                                                                 padx=(20, 0), pady=2)
        Entry(main, textvariable=self.duration_var, width=8).grid(row=4, column=3, sticky='w', padx=5, pady=2)

        # --- БЛОК ПОЖЕЛАНИЙ (в самом низу, на всю ширину) ---
        # Ставим в row=7 (ниже всех остальных полей)
        Label(main, text="Пожелания, ограничения и тд:", bg=bg_color,font=('Arial', 10),  fg=font_color).grid(row=7, column=0, columnspan=4,
                                                                                          sticky='w', pady=(15, 2))

        # columnspan=4 растягивает на все 4 колонки. sticky='ew' растягивает сам виджет
        self.wishesText = Text(main, height=4, width=40)
        self.wishesText.grid(row=8, column=0, columnspan=3, sticky='ew', pady=5)

        btn_frame = Frame(main, bg=bg_color)
        btn_frame.grid(row=8, column=3, columnspan=2, sticky='w', padx=10)

        # А внутри фрейма просто пакуем кнопки в ряд
        Button(btn_frame, text='Создать', bg=font2_color,font=('Arial', 10),  command=self._generate).pack(side='left', padx=(36, 5))
        Button(btn_frame, text='Отмена', bg=font2_color,font=('Arial', 10),  command=lambda: self.app.show_screen(WeekScreen)).pack(side='left')

        # Label(main, text='План', font=('Arial', 8), bg=bg_color, fg=font2_color).grid(row=9, column=4, columnspan=3)


    def _generate(self):
        print('Тут будет генерация')


class WeekScreen(Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.configure(bg=bg_color)
        self._build()

    def _build(self):
        header = Frame(self, bg=bg_color)
        header.pack(fill='x', pady=(0,40))
        Label(header, text=f'Привет {self.app.username}!', bg=bg_color, font=('Arial', 12, 'bold'), fg=font_color).pack(side='left')
        btn_frame = Frame(header, bg=bg_color)
        btn_frame.pack(side='right')
        Button(btn_frame, text='Сгенерировать с ИИ',
               bg=bg_color,
               fg=font_color,
               relief='groove',
               borderwidth=2,
               highlightthickness=0,
               activebackground=bg_color,
               activeforeground='white',font=('Arial', 10),
               command=lambda: self.app.show_screen(CreateAiScreen)).pack(anchor='e')
        Button(btn_frame, text='О программе',
               bg=bg_color,
               fg=font_color,
               relief='groove',
               borderwidth=2,
               activebackground=bg_color,
               activeforeground='white', font=('Arial', 10),
               command=self._aboutProgramm).pack(anchor='e')


        main = Frame(self, bg=bg_color)
        center_container = Frame(main, bg=bg_color)
        center_container.pack(expand=True)
        days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
        counts = ["2 тр", "0", "1 тр", "2 тр", "0", "1 тр", "0"]

        for i in range(len(days)):
            day_box = Frame(center_container, bg=bg_color )
            day_box.pack(side='left')

            Label(day_box, text=days[i], bg=bg_color, font=('Arial', 10),  fg=font_color).pack()
            Label(day_box, text=counts[i], bg=bg_color, font=('Arial', 10),  fg=font_color).pack(pady=10)
            Button(day_box, text='Подробнее', font=('Arial', 10), bg=font2_color, fg=bg_color, command=lambda: self.app.show_screen(DayScreen)).pack(padx=4)
        main.pack(fill='x')

    def _aboutProgramm(self):
        dialog = AboutDialog(self)
        self.wait_window(dialog)


class AboutDialog(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('WorkoutИИ')
        self.geometry('400x280')
        self.resizable(0, 0)
        self.configure(padx=20, pady=20, bg=bg_color)

        self.transient(parent)
        self.grab_set()

        self._build()

    def _build(self):
        Label(self, text='О программе', bg=bg_color, font=('Arial', 11, 'bold'),  fg=font_color).pack(anchor='w')
        Label(self, text='🏋️ WorkoutИИ v0.1', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(pady=(20, 0), anchor='w')
        Label(self, text='Твой персональный фитнес-помощник', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(pady=(0, 20), anchor='w')
        Label(self, text='Разработал: Гумеров Камиль', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(anchor='w')
        Label(self, text='Исходный код на GitHub:', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(pady=(20, 0), anchor='w')
        Label(self, text='github.com/username/training-journal', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(pady=(0, 20), anchor='w')

        Button(self, text='Закрыть', font=('Arial', 10), bg=font2_color, fg=bg_color, command=self.destroy).pack()




class DayScreen(Frame):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.configure(bg=bg_color)
        self._build()

    def _build(self):
        header = Frame(self, bg=bg_color)
        header.pack(fill='x')

        Button(header, text='< Назад к неделе',
               relief='groove',
               borderwidth=0,
               highlightthickness=0,
               bg=bg_color,
               activebackground=bg_color,
               activeforeground='white',
               font=('Arial', 10),
               fg=font_color,
               anchor='w',
               command=lambda: self.app.show_screen(WeekScreen)).pack(side='left')
        Label(header, text='Понедельник', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(anchor='e')

        main = Frame(self, bg=bg_color)
        main.pack(fill='x')

        trains = Frame(main, bg=bg_color)
        trains.pack(pady=(30,0), fill='x')

        tr_card = Frame(trains, bg=bg_color)
        tr_card.pack(side='left', padx=30)
        Label(tr_card, text='#1  Силовая  [выполнена ☑]', bg=bg_color, font=('Arial', 10, 'bold'),  fg=font_color).pack(anchor='w')
        Label(tr_card, text='• Жим лёжа — 4×8, 60 кг', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(padx=10, anchor='w')
        Label(tr_card, text='• Приседания — 4×10, 80 кг', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(padx=10, anchor='w')
        btns = Frame(tr_card, bg=bg_color)
        btns.pack(anchor='w', pady=(10, 0))
        Button(btns, text='Подробнее', font=('Arial', 10), bg=font2_color, fg=bg_color,
               command=lambda: self.app.show_screen(WorkoutEditScreen)).pack(side='left')
        Button(btns, text='Удалить',
               font=('Arial', 10),
               bg=red_color,
               activebackground=red_color,
               fg=font_color,
               activeforeground=font_color,
               command=lambda: self._delete_train(tr_card), ).pack(side='left')

        tr_card2 = Frame(trains, bg=bg_color)
        tr_card2.pack(side='left', padx=30)
        Label(tr_card2, text='#2  Кардио  [выполнена ☑]', bg=bg_color, font=('Arial', 10, 'bold'),  fg=font_color).pack(anchor='w')
        Label(tr_card2, text='• Жим лёжа — 4×8, 60 кг', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(padx=10, anchor='w')
        Label(tr_card2, text='• Приседания — 4×10, 80 кг', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(padx=10, anchor='w')
        btns = Frame(tr_card2, bg=bg_color)
        btns.pack(anchor='w', pady=(10,0))
        Button(btns, text='Подробнее', font=('Arial', 10), bg=font2_color, fg=bg_color,
               command=lambda: self.app.show_screen(WorkoutEditScreen)).pack(side='left')
        Button(btns, text='Удалить',
               font=('Arial', 10),
               bg=red_color,
               activebackground=red_color,
               fg=font_color,
               activeforeground=font_color,
               command=lambda: self._delete_train(tr_card2),
               ).pack(side='left')

        Button(main, text='+ Добавить тренировку', font=('Arial', 10), bg=font2_color, fg=bg_color,
               command=lambda: self.app.show_screen(WorkoutEditScreen)).pack(anchor='w', pady=(40, 0))

        btns2 = Frame(main,  bg=bg_color)
        btns2.pack(anchor='w', pady=4)

        Button(btns2, text='Сохранить', bg=font2_color, font=('Arial', 10)).pack(side='left', padx=(0,4))
        Button(btns2, text='Отмена', bg=font2_color, font=('Arial', 10), command=lambda: self.app.show_screen(WeekScreen)).pack()


    def _delete_train(self, card):
        if messagebox.askyesno('Удаление', 'Удалить тренировку?'):
            card.destroy()


class WorkoutEditScreen(Frame):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.configure(bg=bg_color)

        self.type_var = StringVar()
        self.status_var = BooleanVar()

        self._build()


    def _build(self):
        header = Frame(self, bg=bg_color)
        header.pack(fill='x')

        Button(header, text='< Назад ко дню',
               relief='groove',
               borderwidth=0,
               highlightthickness=0,
               bg=bg_color,
               activebackground=bg_color,
               activeforeground='white',
               font=('Arial', 10),
               fg=font_color,
               anchor='w',
               command=lambda: self.app.show_screen(DayScreen)).pack(side='left')
        Label(header, text='Понедельник', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(anchor='e')

        miniForm = Frame(self, bg=bg_color)
        miniForm.pack()
        Label(miniForm, text='Тип: ', bg=bg_color, font=('Arial', 10),  fg=font_color).grid(row=0, column=0)
        Combobox(miniForm, state="readonly", textvariable=self.type_var,  values=[
            "Силовая", "Кардио", "Функциональная", "Растяжка"], width=16).grid(row=0, column=1)
        Label(miniForm, text='Статус: ', bg=bg_color, font=('Arial', 10),  fg=font_color).grid(row=1, column=0)
        Checkbutton(miniForm,
                    variable=self.status_var,
                    text='Выполнена',
                    bg=bg_color,  # Темный фон, как у всего экрана
                    fg=font_color,  # Белый текст
                    selectcolor=dark_bg_color,  # Цвет квадратика (темный)
                    activebackground=bg_color,  # Фон при клике
                    activeforeground=font_color,  # Текст при клике
                    highlightthickness=0,  # Убирает пунктирную рамку
                    font=('Arial', 10),
                    ).grid(row=1, column=1, sticky='w', padx=5, pady=2)

        exercises = Frame(self, bg=bg_color)
        exercises.pack(pady=20)
        Label(exercises, text='Упражнения:', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(anchor='w')

        exerc_card = Frame(exercises, bg=dark_bg_color, padx=10, pady=8)
        exerc_card.pack(pady=4)

        e_header = Frame(exerc_card, bg=dark_bg_color)
        e_header.pack(fill='x')
        Label(e_header, text='Жим лёжа: 4 подхода × 8 повт. × 60 кг', bg=dark_bg_color, font=('Arial', 10), fg=font_color).pack(side='left', anchor='w')
        e_btns = Frame(e_header, bg=dark_bg_color)
        e_btns.pack(side='right', anchor='e', padx=(10, 0))
        Button(e_btns, text='✎',  font=('Arial', 8), bg=font2_color, fg=dark_bg_color, command=self._edit_exercise ).pack(side='left')
        Button(e_btns, text='✕',  font=('Arial', 8), bg=font2_color, fg=dark_bg_color, command=lambda: self._delete_exercise(exerc_card)).pack(side='left', padx=(4, 0))

        Button(exercises, text='+ Добавить упражнение',  bg=font2_color, font=('Arial', 10),  command=self._add_exercise).pack(anchor='w', pady=(10, 4))
        Button(exercises, text='Сохранить', bg='white', font=('Arial', 10),
               command=self._add_exercise).pack(anchor='w')

    def _add_exercise(self):
        dialog = ExerciseDialog(self)
        self.wait_window(dialog)

    def _edit_exercise(self, index=None):
        dialog = ExerciseDialog(self)
        self.wait_window(dialog)

    def _delete_exercise(self, exercise):
        if messagebox.askyesno('Удаление', 'Удалить упражнение?'):
            exercise.destroy()



class ExerciseDialog(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Упражнение')
        self.geometry('400x300')
        self.configure(bg=bg_color)
        self.resizable(0, 0)
        self.configure(padx=20, pady=20)

        self.transient(parent)
        self.grab_set()

        self.result = None

        self.title_var = StringVar()
        self.sets_var = IntVar()
        self.repetitions_var = IntVar()
        self.weight_var = IntVar()

        self._build()

    def _build(self):
        Label(self, text='Упражнение', bg=bg_color, font=('Arial', 11, 'bold'), fg=font_color).grid(row=0,
                                                                                                          column=0,
                                                                                                          sticky='w', pady=(0, 20))

        Label(self, text='Название:', bg=bg_color, font=('Arial', 10), fg=font_color).grid(row=1, column=0, sticky='w')
        Entry(self, textvariable=self.title_var).grid(row=1, column=1, sticky='w')
        Label(self, text='Например: Подтягивания', bg=bg_color, font=('Arial', 8), fg=font2_color).grid(row=2,
                                                                                                             column=1,
                                                                                                             sticky='w')

        Label(self, text='Подходы: ', bg=bg_color, font=('Arial', 10), fg=font_color).grid(row=3, column=0, sticky='w', pady=10)
        Entry(self, textvariable=self.sets_var,  width=8).grid(row=3, column=1, sticky='w')

        Label(self, text='Повторения: ', bg=bg_color, font=('Arial', 10), fg=font_color).grid(row=4, column=0,
                                                                                              sticky='w')
        Entry(self, textvariable=self.repetitions_var,  width=8).grid(row=4, column=1, sticky='w')

        Label(self, text='Вес, кг: ', bg=bg_color, font=('Arial', 10), fg=font_color).grid(row=5, column=0, sticky='w', pady=10)
        Entry(self, textvariable=self.weight_var, width=8).grid(row=5, column=1, sticky='w')
        Label(self, text='(0 = без веса)', bg=bg_color, font=('Arial', 10), fg=font_color).grid(row=5, column=2,
                                                                                                sticky='w')

        Button(self, text='Добавить', bg=font2_color, font=('Arial', 10), width=10).grid(row=6, column=0, sticky='w')
        Button(self, text='Отмена', bg=font2_color, font=('Arial', 10), command=self.destroy).grid(row=6, column=1, sticky='w')





if __name__ == '__main__':
    app = App()
    app.mainloop()