from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import json
from gigachat import GigaChat  # Подключаем библиотеку Сбера

from datebase import (get_user, add_profile, get_week, get_day,
                      save_workout, delete_workout, WorkoutLimitError, clean_week)

bg_color = '#1c1f2b'
dark_bg_color = '#101219'
font_color = 'white'
font2_color = '#a3b3d7'
red_color = '#640b0f'

DAYS_SHORT = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
DAYS_FULL = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

# ----------------- НАСТРОЙКА GIGACHAT -----------------
# Вставьте сюда ваш длинный ключ Base64 из личного кабинета developers.sber.ru
GIGA_CREDENTIALS = "MDFhMWYzZWItZjkwOS03OWZkLWJkNDUtZjZkMjFkYmM2ZmMxOjM1NzA2MTI0LTc1YzgtNDg4ZC1hM2Q0LTc4OWJmZDU5OWVlMA=="

giga = GigaChat(
    credentials=GIGA_CREDENTIALS,
    scope="GIGACHAT_API_PERS",  # Обязательно для физлиц (бесплатный тариф)
    verify_ssl_certs=False      # Чтобы не ругался на сертификаты Минцифры
)
# ------------------------------------------------------


class ScrollableFrame(Frame):
    def __init__(self, container, height=150, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self, bg=bg_color, highlightthickness=0, height=height)
        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = Frame(self.canvas, bg=bg_color)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.bind("<Enter>", self._bind_wheel)
        self.bind("<Leave>", self._unbind_wheel)

    def _bind_wheel(self, event=None):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_wheel(self, event=None):
        w = self.winfo_containing(*self.winfo_pointerxy())
        if w is not None and str(w).startswith(str(self)):
            return
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        if not self.canvas.winfo_exists():
            return
        if self.scrollable_frame.winfo_height() <= self.canvas.winfo_height():
            return

        if event.num == 4:
            step = -1
        elif event.num == 5:
            step = 1
        elif abs(event.delta) >= 120:
            step = int(-event.delta / 120)
        else:
            step = -event.delta
        self.canvas.yview_scroll(step, "units")


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('WorkoutИИ')
        self.geometry('700x450')
        self.resizable(False, False)
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
        Label(self, text='WorkoutИИ: Журнал тренировок', font=('Arial', 14, 'bold'),
              bg=bg_color, fg=font_color).pack(pady=20)
        Label(self, text='Как тебя зовут?', bg=bg_color, fg=font_color,
              font=('Arial', 10)).pack(pady=8)
        self.name_entry = Entry(self, textvariable=self.username_var)
        self.name_entry.pack(pady=10)
        self.name_entry.focus_set()
        self.name_entry.bind('<Return>', lambda e: self._login())
        Button(self, text='Продолжить', command=self._login, bg='white',
               font=('Arial', 10)).pack()

    def _login(self):
        name = self.username_var.get().strip()
        if not name:
            messagebox.showerror('Ошибка', 'Поле имени не может быть пустым')
            return
        add_profile(name)
        self.app.username = name
        self.app.show_screen(CreateWeekScreen)


class CreateWeekScreen(Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.configure(bg=bg_color)
        self._build()

    def _build(self):
        Label(self, text=f'Привет, {self.app.username}', font=('Arial', 10),
              bg=bg_color, fg=font_color).pack()
        Label(self, text='Как создашь свое расписание?', font=('Arial', 14),
              bg=bg_color, fg=font_color).pack(pady=20)

        Button(self, text='✍ Заполнить вручную', font=('Arial', 10, 'bold'), height=2,
               bg=font2_color, width=40,
               command=lambda: self.app.show_screen(WeekScreen)).pack(pady=0)
        Label(self, text='Сам добавишь тренировки на каждый день', font=('Arial', 10),
              bg=bg_color, fg=font_color).pack()

        Button(self, text='🤖 Составить с помощью ИИ', font=('Arial', 10, 'bold'), height=2,
               bg=font2_color, width=40,
               command=lambda: self.app.show_screen(CreateAiScreen)).pack(pady=(20, 0))
        Label(self, text='Заполняешь анкеты - ИИ расставит план', font=('Arial', 10),
              bg=bg_color, fg=font_color).pack()

        Label(self, text='План всегда можно будет пересоздать', font=('Arial', 8),
              bg=bg_color, fg=font2_color).pack(pady=26)


class CreateAiScreen(Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        self.height_var = IntVar()
        self.weight_var = IntVar()
        self.age_var = IntVar()
        self.aim_var = StringVar(value='Поддержание формы')
        self.experience_var = StringVar(value='Новичок')
        self.equipment_var = StringVar(value='Зал (всё есть)')
        self.per_week_var = IntVar(value=3)
        self.duration_var = IntVar(value=60)

        self.configure(bg=bg_color)
        self._build()

    def _label(self, parent, text, row, column, padx=0):
        Label(parent, text=text, bg=bg_color, font=('Arial', 10), fg=font_color).grid(
            row=row, column=column, sticky='w', pady=2, padx=padx)

    def _build(self):
        header = Frame(self, bg=bg_color)
        header.pack()
        Label(header, text='Генерация плана с помощью ИИ', font=('Arial', 14),
              bg=bg_color, fg=font_color).pack(anchor='w')

        main = Frame(self, bg=bg_color)
        main.pack(anchor='w', fill='both', expand=True, pady=(20, 0))

        # --- ЛЕВАЯ КОЛОНКА ---
        self._label(main, 'Рост, см: ', 1, 0)
        Entry(main, textvariable=self.height_var, width=8).grid(
            row=1, column=1, sticky='w', padx=5, pady=2)

        self._label(main, 'Вес, кг: ', 2, 0)
        Entry(main, textvariable=self.weight_var, width=8).grid(
            row=2, column=1, sticky='w', padx=5, pady=2)

        self._label(main, 'Возраст: ', 3, 0)
        Entry(main, textvariable=self.age_var, width=8).grid(
            row=3, column=1, sticky='w', padx=5, pady=2)

        self._label(main, 'Цель: ', 4, 0)
        Combobox(main, textvariable=self.aim_var, values=[
            'Похудение', 'Набор массы', 'Поддержание формы', 'Сила', 'Выносливость'
        ], state='readonly', width=18).grid(row=4, column=1, sticky='w', padx=5, pady=2)

        # --- ПРАВАЯ КОЛОНКА ---
        self._label(main, 'Опыт: ', 1, 2, padx=(20, 0))
        Combobox(main, state='readonly', textvariable=self.experience_var, width=18, values=[
            'Новичок', 'Средний', 'Продвинутый'
        ]).grid(row=1, column=3, sticky='w', padx=5, pady=2)

        self._label(main, 'Оборудование: ', 2, 2, padx=(20, 0))
        Combobox(main, state='readonly', textvariable=self.equipment_var, values=[
            'Зал (всё есть)', 'Дом (без инвентаря)', 'Улица'
        ], width=18).grid(row=2, column=3, sticky='w', padx=5, pady=2)

        self._label(main, 'Тренировок в нед.: ', 3, 2, padx=(20, 0))
        Entry(main, textvariable=self.per_week_var, width=8).grid(
            row=3, column=3, sticky='w', padx=5, pady=2)

        self._label(main, 'Длительность, мин: ', 4, 2, padx=(20, 0))
        Entry(main, textvariable=self.duration_var, width=8).grid(
            row=4, column=3, sticky='w', padx=5, pady=2)

        Label(main, text='Пожелания, ограничения и тд:', bg=bg_color, font=('Arial', 10),
              fg=font_color).grid(row=7, column=0, columnspan=4, sticky='w', pady=(15, 2))

        self.wishesText = Text(main, height=4, width=40)
        self.wishesText.grid(row=8, column=0, columnspan=3, sticky='ew', pady=5)

        btn_frame = Frame(main, bg=bg_color)
        btn_frame.grid(row=8, column=3, columnspan=2, sticky='w', padx=10)

        Button(btn_frame, text='Создать', bg=font2_color, font=('Arial', 10),
               command=self._generate).pack(side='left', padx=(36, 5))
        Button(btn_frame, text='Отмена', bg=font2_color, font=('Arial', 10),
               command=lambda: self.app.show_screen(WeekScreen)).pack(side='left')

    def _generate(self):
        try:
            height = self.height_var.get()
            weight = self.weight_var.get()
            age = self.age_var.get()
            per_week = self.per_week_var.get()
            duration = self.duration_var.get()
        except:
            messagebox.showerror('Ошибка', 'Во все числовые поля нужно вводить целые числа')
            return

        if height <= 0 or weight <= 0 or age <= 0 or duration <= 0:
            messagebox.showerror('Ошибка', 'Рост, вес, возраст и длительность должны быть больше нуля')
            return

        if not 1 <= per_week <= 7:
            messagebox.showerror('Ошибка', 'Тренировок в неделю может быть от 1 до 7')
            return

        aim = self.aim_var.get()
        experience = self.experience_var.get()
        equipment = self.equipment_var.get()

        if not aim or not experience or not equipment:
            messagebox.showerror('Ошибка', 'Выберите цель, опыт и оборудование из списков')
            return

        wishes = self.wishesText.get('1.0', END).strip()

        data_to_AI = f"""
        Параметры пользователя:
        - Рост: {height} см, Вес: {weight} кг, Возраст: {age} лет
        - Цель: {aim}, Опыт: {experience}, Инвентарь: {equipment}
        - Тренировок: {per_week} в неделю, Длительность: {duration} мин.
        - Пожелания: {wishes if wishes else 'нет'}
        """

        system_prompt = f"""Ты опытный персональный фитнес-тренер. 
                Составь грамотный и разнообразный тренировочный план строго на {per_week} дня(ей) в неделю.
                Ответь ТОЛЬКО чистым JSON без лишних слов, без пояснений и без markdown-разметки (не пиши ```json).
                
                Схема ответа:
                {{
                    "workouts": [
                        {{
                            "day_index": 0, 
                            "kind": "Силовая",
                            "exercises": [
                                {{"name": "Подтягивания", "sets": 3, "reps": 8, "weight": 0}}
                            ]
                        }}
                    ]
                }}
                
                ПРАВИЛА:
                1. ИНВЕНТАРЬ И ПОЖЕЛАНИЯ (НАИВЫСШИЙ ПРИОРИТЕТ):
                   - Внимательно изучи пожелания! Если указан турник, гриф, гантели, груша — ОБЯЗАТЕЛЬНО включи упражнения с ними.
                2. РАЗНООБРАЗИЕ ТРЕНИРОВОК:
                   - ЗАПРЕЩЕНО делать все дни недели одинаковыми. Разделяй нагрузку по дням (например: день спины/тяги, день ног, день груди/рук).
                3. НАЗВАНИЯ:
                   - Только короткие названия (1-3 слова). Например: «Подтягивания», «Отжимания», «Жим грифа».
                   - Строго ОДНО упражнение (никаких вариантов через «или» и скобок).
                   - Не пиши «(с собственным весом)». Если вес не нужен — ставь "weight": 0.
                4. СТРУКТУРА:
                   - "day_index" — число от 0 до 6 (0-ПН, 1-ВТ, 2-СР, 3-ЧТ, 4-ПТ, 5-СБ, 6-ВС).
                   - Ровно {per_week} тренировки(ок) в массиве "workouts". От 3 до 4 упражнений на тренировку.
                """

        try:
            # Запрос к GigaChat
            response = giga.chat({
                "model": "GigaChat-3-Pro",
                "temperature": 0.2,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": data_to_AI}
                ]
            })

            raw_text = response.choices[0].message.content

            # Очищаем от возможных бэктиков ```json
            clean_json = raw_text.replace("```json", "").replace("```", "").strip()
            result = json.loads(clean_json)

            print("УСПЕХ! GigaChat составил план:")
            print(json.dumps(result, indent=4, ensure_ascii=False))
            clean_week()

            # Сохраняем в базу данных
            for w in result['workouts']:
                save_workout(None, w['day_index'], w['kind'], 'planned', w['exercises'])

            messagebox.showinfo("Успех", f"План успешно составлен на {per_week} дня(ей)!")
            self.app.show_screen(WeekScreen)

        except Exception as e:
            messagebox.showerror("Ошибка ИИ", f"Не удалось сгенерировать план: {e}")


class WeekScreen(Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.configure(bg=bg_color)
        self.counts = get_week()
        self._build()

    def _build(self):
        header = Frame(self, bg=bg_color)
        header.pack(fill='x', pady=(0, 40))
        Label(header, text=f'Привет {self.app.username}!', bg=bg_color,
              font=('Arial', 12, 'bold'), fg=font_color).pack(side='left')

        btn_frame = Frame(header, bg=bg_color)
        btn_frame.pack(side='right')
        Button(btn_frame, text='Сгенерировать с ИИ', bg=bg_color, fg=font_color, relief='groove',
               borderwidth=2, highlightthickness=0, activebackground=bg_color,
               activeforeground='white', font=('Arial', 10),
               command=lambda: self.app.show_screen(CreateAiScreen)).pack(anchor='e')
        Button(btn_frame, text='О программе', bg=bg_color, fg=font_color, relief='groove',
               borderwidth=2, activebackground=bg_color, activeforeground='white',
               font=('Arial', 10), command=self._aboutProgramm).pack(anchor='e')

        main = Frame(self, bg=bg_color)
        center_container = Frame(main, bg=bg_color)
        center_container.pack(expand=True)

        for i in range(len(DAYS_SHORT)):
            day_box = Frame(center_container, bg=bg_color)
            day_box.pack(side='left')
            Label(day_box, text=DAYS_SHORT[i], bg=bg_color, font=('Arial', 10),
                  fg=font_color).pack()
            Label(day_box, text=f'{self.counts[i]} тр', bg=bg_color, font=('Arial', 10),
                  fg=font_color).pack(pady=10)
            Button(day_box, text='Подробнее', font=('Arial', 10), bg=font2_color, fg=bg_color,
                   command=lambda i=i: self.app.show_screen(DayScreen, i)).pack(padx=4)
        main.pack(fill='x')

    def _aboutProgramm(self):
        dialog = AboutDialog(self)
        self.wait_window(dialog)


# ---------------------------------------------------------------- День
class DayScreen(Frame):
    def __init__(self, app, week_day_id):
        super().__init__(app)
        self.app = app
        self.configure(bg=bg_color)

        self.data = get_day(week_day_id)
        self.week_day_id = week_day_id
        self.week_day = DAYS_FULL[week_day_id]
        self._build()

    def _build(self):
        header = Frame(self, bg=bg_color)
        header.pack(fill='x')

        Button(header, text='< Назад к неделе', relief='groove', borderwidth=0,
               highlightthickness=0, bg=bg_color, activebackground=bg_color,
               activeforeground='white', font=('Arial', 10), fg=font_color, anchor='w',
               command=lambda: self.app.show_screen(WeekScreen)).pack(side='left')
        Label(header, text=self.week_day, bg=bg_color, font=('Arial', 10),
              fg=font_color).pack(anchor='e')

        main = Frame(self, bg=bg_color)
        main.pack(fill='x')

        trains = Frame(main, bg=bg_color)
        trains.pack(pady=(30, 0), fill='x')

        for index, info in enumerate(self.data, start=1):
            tr_card = Frame(trains, bg=bg_color)
            tr_card.pack(side='left', padx=30, anchor='n')
            status_text = 'выполнена ☑' if info['status'] == 'done' else 'не выполнена ☐'

            Label(tr_card, text=f"#{index}  {info['kind']}  {status_text}",
                  bg=bg_color, font=('Arial', 10, 'bold'), fg=font_color).pack(anchor='w')

            exercises = info['exercises']
            for ex in exercises[:5]:
                weight_str = f", {ex['weight']:g}кг" if ex['weight'] > 0 else ''
                Label(tr_card, text=f"• {ex['name']} — {ex['sets']}×{ex['reps']}{weight_str}",
                      bg=bg_color, font=('Arial', 10), fg=font_color).pack(padx=10, anchor='w')

            if len(exercises) > 5:
                Label(tr_card, text='...', bg=bg_color, font=('Arial', 10),
                      fg=font_color).pack(padx=10, anchor='w')

            btns = Frame(tr_card, bg=bg_color)
            btns.pack(anchor='w', pady=(10, 0))

            Button(btns, text='Подробнее', font=('Arial', 10), bg=font2_color, fg=bg_color,
                   command=lambda info=info: self.app.show_screen(
                       WorkoutEditScreen, self.week_day_id, info)).pack(side='left')

            Button(btns, text='Удалить', font=('Arial', 10), bg=red_color,
                   activebackground=red_color, fg=font_color, activeforeground=font_color,
                   command=lambda wid=info['id']: self._delete_train(wid)).pack(side='left')

        if len(self.data) < 2:
            Button(main, text='+ Добавить тренировку', font=('Arial', 10), bg=font2_color,
                   fg=bg_color,
                   command=lambda: self.app.show_screen(
                       WorkoutEditScreen, self.week_day_id)).pack(anchor='w', pady=(40, 0))
        else:
            Label(main, text='Максимум 2 тренировки в день', font=('Arial', 10),
                  bg=bg_color, fg=font2_color).pack(anchor='w', pady=(40, 0))

        btns2 = Frame(main, bg=bg_color)
        btns2.pack(anchor='w', pady=4)
        Button(btns2, text='Назад', bg=font2_color, font=('Arial', 10),
               command=lambda: self.app.show_screen(WeekScreen)).pack()

    def _delete_train(self, workout_id):
        if messagebox.askyesno('Удаление', 'Удалить тренировку?'):
            delete_workout(workout_id)
            self.app.show_screen(DayScreen, self.week_day_id)


# ---------------------------------------------------------------- О программе
class AboutDialog(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('WorkoutИИ')
        self.geometry('400x280')
        self.resizable(False, False)
        self.configure(padx=20, pady=20, bg=bg_color)

        self.transient(parent)
        self.grab_set()
        self._build()

    def _build(self):
        Label(self, text='О программе', bg=bg_color, font=('Arial', 11, 'bold'),
              fg=font_color).pack(anchor='w')
        Label(self, text='🏋️ WorkoutИИ v0.1', bg=bg_color, font=('Arial', 10),
              fg=font_color).pack(pady=(20, 0), anchor='w')
        Label(self, text='Твой персональный фитнес-помощник', bg=bg_color, font=('Arial', 10),
              fg=font_color).pack(pady=(0, 20), anchor='w')
        Label(self, text='Разработал: Гумеров Камиль', bg=bg_color, font=('Arial', 10),
              fg=font_color).pack(anchor='w')
        Label(self, text='Исходный код на GitHub:', bg=bg_color, font=('Arial', 10),
              fg=font_color).pack(pady=(20, 0), anchor='w')
        Label(self, text='https://github.com/kamil2757/WorcoutAI', bg=bg_color,
              font=('Arial', 10), fg=font_color).pack(pady=(0, 20), anchor='w')

        Button(self, text='Закрыть', font=('Arial', 10), bg=font2_color, fg=bg_color,
               command=self.destroy).pack()


# ---------------------------------------------------------------- Редактирование тренировки
class WorkoutEditScreen(Frame):
    def __init__(self, app, week_day_id, data=None):
        super().__init__(app)
        self.app = app
        self.configure(bg=bg_color)

        self.week_day = DAYS_FULL[week_day_id]
        self.week_day_id = week_day_id
        self.workout_id = data['id'] if data else None
        self.exercise_data = []

        if data:
            self.type_var = StringVar(value=data['kind'])
            self.status_var = BooleanVar(value=data['status'] == 'done')
            for ex in data['exercises']:
                self.exercise_data.append({'name': ex['name'], 'sets': ex['sets'],
                                           'reps': ex['reps'], 'weight': ex['weight']})
        else:
            self.type_var = StringVar(value='Силовая')
            self.status_var = BooleanVar()

        self._build()

    def _build(self):
        header = Frame(self, bg=bg_color)
        header.pack(fill='x')

        Button(header, text='< Назад ко дню', relief='groove', borderwidth=0,
               highlightthickness=0, bg=bg_color, activebackground=bg_color,
               activeforeground='white', font=('Arial', 10), fg=font_color, anchor='w',
               command=lambda: self.app.show_screen(DayScreen, self.week_day_id)).pack(side='left')
        Label(header, text=self.week_day, bg=bg_color, font=('Arial', 10),
              fg=font_color).pack(anchor='e')

        miniForm = Frame(self, bg=bg_color)
        miniForm.pack()
        Label(miniForm, text='Тип: ', bg=bg_color, font=('Arial', 10),
              fg=font_color).grid(row=0, column=0)
        Combobox(miniForm, state='readonly', textvariable=self.type_var, values=[
            'Силовая', 'Кардио', 'Функциональная', 'Растяжка'], width=16).grid(row=0, column=1)
        Label(miniForm, text='Статус: ', bg=bg_color, font=('Arial', 10),
              fg=font_color).grid(row=1, column=0)
        Checkbutton(miniForm, variable=self.status_var, text='Выполнена', bg=bg_color,
                    fg=font_color, selectcolor=dark_bg_color, activebackground=bg_color,
                    activeforeground=font_color, highlightthickness=0,
                    font=('Arial', 10)).grid(row=1, column=1, sticky='w', padx=5, pady=2)

        exercises = Frame(self, bg=bg_color)
        exercises.pack(fill='both', expand=True, pady=10)
        Label(exercises, text='Упражнения:', bg=bg_color, font=('Arial', 10),
              fg=font_color).pack(anchor='w')

        btns = Frame(exercises, bg=bg_color)
        btns.pack(side='bottom', anchor='w', pady=(10, 0))

        Button(btns, text='+ Добавить упражнение', bg=font2_color, font=('Arial', 10),
               command=self._add_exercise).pack(side='left', padx=2)
        Button(btns, text='Сохранить', bg='white', font=('Arial', 10),
               command=self._save).pack(side='left')

        self.cards_frame = ScrollableFrame(exercises, height=150, bg=bg_color)
        self.cards_frame.pack(fill='both', expand=True, pady=5)
        for ex in self.exercise_data:
            self._add_exercise_card(ex)

    def _add_exercise_card(self, ex):
        card = Frame(self.cards_frame.scrollable_frame, bg=dark_bg_color, padx=6, pady=2)
        card.pack(pady=1, anchor='w')

        weight_str = f' × {ex["weight"]:g}кг' if ex['weight'] > 0 else ''
        text = f'{ex["name"]}: {ex["sets"]} подх. × {ex["reps"]} повт.{weight_str}'

        e_header = Frame(card, bg=dark_bg_color)
        e_header.pack(fill='x')
        Label(e_header, text=text, bg=dark_bg_color, font=('Arial', 10),
              fg=font_color).pack(side='left', anchor='w')

        e_btns = Frame(e_header, bg=dark_bg_color)
        e_btns.pack(side='right', anchor='e', padx=(10, 0))
        Button(e_btns, text='✎', font=('Arial', 7), height=0, width=0, bg=font2_color,
               fg=dark_bg_color, command=lambda e=ex: self._edit_exercise(e)).pack(side='left')
        Button(e_btns, text='✕', font=('Arial', 7), height=0, width=0, bg=font2_color,
               fg=dark_bg_color,
               command=lambda c=card, e=ex: self._delete_exercise(c, e)).pack(side='left',
                                                                              padx=(4, 0))

    def _save(self):
        if not self.exercise_data:
            messagebox.showerror('Ошибка', 'Тренировка не может быть без упражнений')
            return

        kind = self.type_var.get()
        status = 'done' if self.status_var.get() else 'planned'

        try:
            save_workout(self.workout_id, self.week_day_id, kind, status, self.exercise_data)
        except WorkoutLimitError as e:
            messagebox.showerror('Ошибка', str(e))
            return
        except Exception as e:
            messagebox.showerror('Ошибка БД', f'Не удалось сохранить: {e}')
            return

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
            idx = [i for i, e in enumerate(self.exercise_data) if e is ex][0]
            self.exercise_data[idx] = dialog.result
            for w in self.cards_frame.scrollable_frame.winfo_children():
                w.destroy()
            for e in self.exercise_data:
                self._add_exercise_card(e)

    def _delete_exercise(self, card, ex):
        if messagebox.askyesno('Удаление', 'Удалить упражнение?'):
            self.exercise_data = [e for e in self.exercise_data if e is not ex]
            card.destroy()


class ExerciseDialog(Toplevel):
    def __init__(self, parent, exercise=None):
        super().__init__(parent)
        self.title('Упражнение')
        self.geometry('400x300')
        self.configure(bg=bg_color, padx=20, pady=20)
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()
        self.result = None
        self.is_edit = exercise is not None

        self.title_var = StringVar()
        self.sets_var = IntVar(value=3)
        self.repetitions_var = IntVar(value=10)
        self.weight_var = DoubleVar(value=0)

        if exercise:
            self.title_var.set(exercise['name'])
            self.sets_var.set(exercise['sets'])
            self.repetitions_var.set(exercise['reps'])
            self.weight_var.set(exercise['weight'])

        self._build()

    def _build(self):
        Label(self, text='Упражнение', bg=bg_color, font=('Arial', 11, 'bold'),
              fg=font_color).grid(row=0, column=0, sticky='w', pady=(0, 20))

        Label(self, text='Название:', bg=bg_color, font=('Arial', 10),
              fg=font_color).grid(row=1, column=0, sticky='w')
        name_entry = Entry(self, textvariable=self.title_var)
        name_entry.grid(row=1, column=1, sticky='w')
        name_entry.focus_set()
        Label(self, text='Например: Подтягивания', bg=bg_color, font=('Arial', 8),
              fg=font2_color).grid(row=2, column=1, sticky='w')

        Label(self, text='Подходы: ', bg=bg_color, font=('Arial', 10),
              fg=font_color).grid(row=3, column=0, sticky='w', pady=10)
        Entry(self, textvariable=self.sets_var, width=8).grid(row=3, column=1, sticky='w')

        Label(self, text='Повторения: ', bg=bg_color, font=('Arial', 10),
              fg=font_color).grid(row=4, column=0, sticky='w')
        Entry(self, textvariable=self.repetitions_var, width=8).grid(row=4, column=1, sticky='w')

        Label(self, text='Вес, кг: ', bg=bg_color, font=('Arial', 10),
              fg=font_color).grid(row=5, column=0, sticky='w', pady=10)
        Entry(self, textvariable=self.weight_var, width=8).grid(row=5, column=1, sticky='w')
        Label(self, text='(0 = без веса)', bg=bg_color, font=('Arial', 10),
              fg=font_color).grid(row=5, column=2, sticky='w')

        Button(self, text='Сохранить' if self.is_edit else 'Добавить', bg=font2_color,
               font=('Arial', 10), command=self._add, width=10).grid(row=6, column=0, sticky='w')
        Button(self, text='Отмена', bg=font2_color, font=('Arial', 10),
               command=self.destroy).grid(row=6, column=1, sticky='w')

    def _add(self):
        try:
            name = self.title_var.get().strip()
            sets = self.sets_var.get()
            reps = self.repetitions_var.get()
            weight = self.weight_var.get()
        except (ValueError, TclError):
            messagebox.showerror('Ошибка',
                                 'В числовые поля нужно вводить числа (без букв и символов)!',
                                 parent=self)
            return

        if not name:
            messagebox.showerror('Ошибка', 'Название не должно быть пустым', parent=self)
            return

        if sets <= 0 or reps <= 0:
            messagebox.showerror('Ошибка', 'Подходы и повторения должны быть больше нуля',
                                 parent=self)
            return

        if weight < 0:
            messagebox.showerror('Ошибка', 'Вес не может быть отрицательным', parent=self)
            return

        self.result = {'name': name, 'sets': sets, 'reps': reps, 'weight': weight}
        self.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()