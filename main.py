from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

from datebase import *

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

        user = get_user()
        if user:
            self.username = user
            self.show_screen(WeekScreen)
        else:
            self.show_screen(LoginScreen)

    def show_screen(self, screen_class, *args, **kwargs):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = screen_class(self, *args, **kwargs)
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
        add_profile(name)
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

        self.counts = get_week()
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
               activeforeground='white', font=('Arial', 10),
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

        for i in range(len(days)):
            day_box = Frame(center_container, bg=bg_color)
            day_box.pack(side='left')

            Label(day_box, text=days[i], bg=bg_color, font=('Arial', 10),  fg=font_color).pack()
            Label(day_box, text=f'{self.counts[i]} тр', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(pady=10)
            Button(day_box, text='Подробнее', font=('Arial', 10), bg=font2_color, fg=bg_color, command=lambda i = i: self.app.show_screen(DayScreen, i)).pack(padx=4)
        main.pack(fill='x')

    def _aboutProgramm(self):
        dialog = AboutDialog(self)
        self.wait_window(dialog)


class DayScreen(Frame):
    def __init__(self, app, week_day_id):
        super().__init__()
        self.app = app
        self.configure(bg=bg_color)

        self.data = get_day(week_day_id)
        self.days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        self.week_day_id = week_day_id
        self.week_day = self.days[week_day_id]

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
        Label(header, text=self.week_day, bg=bg_color, font=('Arial', 10),  fg=font_color).pack(anchor='e')

        main = Frame(self, bg=bg_color)
        main.pack(fill='x')

        trains = Frame(main, bg=bg_color)
        trains.pack(pady=(30,0), fill='x')

        for info in self.data:
            tr_card = Frame(trains, bg=bg_color)
            tr_card.pack(side='left', padx=30)
            Label(tr_card, text=f'#{info[0][1]}  {info[0][2]}  {'выполнена ☑' if info[0][3] == 'done' else 'не выполнена ☐,' }', bg=bg_color, font=('Arial', 10, 'bold'),  fg=font_color).pack(anchor='w')
            for ex in info[1][:5]:
                Label(tr_card, text=f'• {ex[0]} — {ex[1]}×{ex[2]}{f', {ex[3]}кг' if ex[3] > 0 else ''}', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(padx=10, anchor='w')

            if len(info[1]) > 5:
                Label(tr_card, text=f'...', bg=bg_color,
                    font=('Arial', 10), fg=font_color).pack(padx=10, anchor='w')
            btns = Frame(tr_card, bg=bg_color)
            btns.pack(anchor='w', pady=(10, 0))
            Button(btns, text='Подробнее', font=('Arial', 10), bg=font2_color, fg=bg_color,
                   command=lambda info=info: self.app.show_screen(WorkoutEditScreen, self.week_day_id, info)).pack(side='left')
            Button(btns, text='Удалить',
                   font=('Arial', 10),
                   bg=red_color,
                   activebackground=red_color,
                   fg=font_color,
                   activeforeground=font_color,
                   command=lambda tr_card=tr_card: self._delete_train(tr_card, info[0][0])).pack(side='left')



        Button(main, text='+ Добавить тренировку', font=('Arial', 10), bg=font2_color, fg=bg_color,
               command=lambda: self.app.show_screen(WorkoutEditScreen, self.week_day_id)).pack(anchor='w', pady=(40, 0))

        btns2 = Frame(main,  bg=bg_color)
        btns2.pack(anchor='w', pady=4)
        Button(btns2, text='Назад', bg=font2_color, font=('Arial', 10), command=lambda: self.app.show_screen(WeekScreen)).pack()


    def _delete_train(self, card, workout_id):
        if messagebox.askyesno('Удаление', 'Удалить тренировку?'):
            delete_workout(workout_id)
            card.destroy()

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
        Label(self, text='https://github.com/kamil2757/WorcoutAI', bg=bg_color, font=('Arial', 10),  fg=font_color).pack(pady=(0, 20), anchor='w')

        Button(self, text='Закрыть', font=('Arial', 10), bg=font2_color, fg=bg_color, command=self.destroy).pack()



class WorkoutEditScreen(Frame):
    def __init__(self, app, week_day_id, data=None):
        super().__init__(app)
        self.app = app
        self.configure(bg=bg_color)

        self.days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        self.week_day = self.days[week_day_id]
        self.week_day_id = week_day_id
        self.workout_id = data[0][0] if data else None
        self.exercise_data = []

        if data:
            self.type_var = StringVar(value=data[0][2])
            self.status_var = BooleanVar(value=data[0][3] == 'done')
            for name, sets, reps, weight, order_num in data[1]:
                self.exercise_data.append({'name': name, 'sets': sets, 'reps': reps, 'weight': weight})
        else:
            self.type_var = StringVar(value="Силовая")
            self.status_var = BooleanVar()

        self._build()

    def _build(self):
        header = Frame(self, bg=bg_color)
        header.pack(fill='x')

        Button(header, text='< Назад ко дню', relief='groove', borderwidth=0,
               highlightthickness=0, bg=bg_color, activebackground=bg_color,
               activeforeground='white', font=('Arial', 10), fg=font_color, anchor='w',
               command=lambda: self.app.show_screen(DayScreen, self.week_day_id)).pack(side='left')
        Label(header, text=self.week_day, bg=bg_color, font=('Arial', 10), fg=font_color).pack(anchor='e')

        miniForm = Frame(self, bg=bg_color)
        miniForm.pack()
        Label(miniForm, text='Тип: ', bg=bg_color, font=('Arial', 10), fg=font_color).grid(row=0, column=0)
        Combobox(miniForm, state="readonly", textvariable=self.type_var, values=[
            "Силовая", "Кардио", "Функциональная", "Растяжка"], width=16).grid(row=0, column=1)
        Label(miniForm, text='Статус: ', bg=bg_color, font=('Arial', 10), fg=font_color).grid(row=1, column=0)
        Checkbutton(miniForm, variable=self.status_var, text='Выполнена',
                    bg=bg_color, fg=font_color, selectcolor=dark_bg_color,
                    activebackground=bg_color, activeforeground=font_color,
                    highlightthickness=0, font=('Arial', 10)).grid(row=1, column=1, sticky='w', padx=5, pady=2)

        exercises = Frame(self, bg=bg_color)
        exercises.pack(pady=10)
        Label(exercises, text='Упражнения:', bg=bg_color, font=('Arial', 10), fg=font_color).pack(anchor='w')

        self.cards_frame = Frame(exercises, bg=bg_color)
        self.cards_frame.pack(fill='x')

        for ex in self.exercise_data:
            self._add_exercise_card(ex)

        btns = Frame(self.cards_frame, bg=bg_color)
        btns.pack(pady=(10), anchor='w')

        Button(btns, text='+ Добавить упражнение', bg=font2_color, font=('Arial', 10),
               command=self._add_exercise).pack(side="left", padx=2)
        Button(btns, text='Сохранить', bg='white', font=('Arial', 10),
               command=self._save).pack(side="left")

    def _add_exercise_card(self, ex):
        card = Frame(self.cards_frame, bg=dark_bg_color, padx=6, pady=2)
        card.pack(pady=1, anchor='w')

        weight_str = f' × {ex["weight"]}кг' if ex['weight'] > 0 else ''
        text = f'{ex["name"]}: {ex["sets"]} подхода × {ex["reps"]} повт.{weight_str}'

        e_header = Frame(card, bg=dark_bg_color)
        e_header.pack(fill='x')
        Label(e_header, text=text, bg=dark_bg_color, font=('Arial', 10),
              fg=font_color).pack(side='left', anchor='w')
        e_btns = Frame(e_header, bg=dark_bg_color)
        e_btns.pack(side='right', anchor='e', padx=(10, 0))
        Button(e_btns, text='✎', font=('Arial', 7), height=0, width=0, bg=font2_color, fg=dark_bg_color,
               command=lambda e=ex: self._edit_exercise(e)).pack(side='left')
        Button(e_btns, text='✕', font=('Arial', 7), height=0, width=0, bg=font2_color, fg=dark_bg_color,
               command=lambda c=card, e=ex: self._delete_exercise(c, e)).pack(side='left', padx=(4, 0))

    def _save(self):
        if not self.exercise_data:
            messagebox.showerror('Ошибка', 'Тренировка не может быть без упражнений')
            return

        kind = self.type_var.get()
        status = 'done' if self.status_var.get() else 'planned'

        if self.workout_id:
            update_workout(self.workout_id, kind, status)
            delete_workout_exercises(self.workout_id)
            wid = self.workout_id
        else:
            wid = create_workout(self.week_day_id, kind, status)
        if type(wid) == list:
            messagebox.showerror(wid[0], wid[1])
            return


        for i, ex in enumerate(self.exercise_data):
            add_exercise(wid, ex['name'], ex['sets'], ex['reps'], ex['weight'], i)

        self.app.show_screen(DayScreen, self.week_day_id)

    def _add_exercise(self):
        dialog = ExerciseDialog(self)
        self.wait_window(dialog)
        if dialog.result:
            self.exercise_data.append(dialog.result)
            self._add_exercise_card(dialog.result)

    def _edit_exercise(self, ex):
        dialog = ExerciseDialog(self, ex)
        self.wait_window(dialog)
        if dialog.result:
            self.exercise_data[self.exercise_data.index(ex)] = dialog.result
            for w in self.cards_frame.winfo_children():
                w.destroy()
            for e in self.exercise_data:
                self._add_exercise_card(e)

    def _delete_exercise(self, card, ex):
        if messagebox.askyesno('Удаление', 'Удалить упражнение?'):
            self.exercise_data.remove(ex)
            card.destroy()

class ExerciseDialog(Toplevel):
    def __init__(self, parent, exercise=None):
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
        if exercise:
            self.title_var.set(exercise['name'])
            self.sets_var.set(exercise['sets'])
            self.repetitions_var.set(exercise['reps'])
            self.weight_var.set(exercise['weight'])

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

        Button(self, text='Добавить', bg=font2_color, font=('Arial', 10), command=self._add,width=10).grid(row=6, column=0, sticky='w')
        Button(self, text='Отмена', bg=font2_color, font=('Arial', 10), command=self.destroy).grid(row=6, column=1, sticky='w')

    def _add(self):
        try:
            if self.title_var.get() == '':
                messagebox.showerror('Ошибка','Названия не должно быть пустым', parent=self)
                return
            self.result = {'name': self.title_var.get(), 'sets': self.sets_var.get(), 'reps': self.repetitions_var.get(), 'weight': self.weight_var.get()}
            self.destroy()
        except:
            messagebox.showerror('Ошибка', 'Заполните поля правильно', parent=self)



if __name__ == '__main__':
    app = App()
    app.mainloop()