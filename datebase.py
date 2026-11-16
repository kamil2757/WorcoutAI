import sqlite3


conn = sqlite3.connect('workoutAI.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL
        day_of_week INTEGER NOT NULL,
        order_in_day INTEGER NOT NULL,
        kind TEXT NOT NULL,
        status TEXT DEFAULT 'planned'
        FOREIGN KEY (user_id) REFERENCES profile(id) ON DELETE CASCADE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workout_id INTEGER NOT NULL, 
        name TEXT NOT NULL,
        sets INTEGER NOT NULL,
        reps INTEGER NOT NULL,
        weight REAL DEFAULT 0,
        order_num INTEGER NOT NULL,
        FOREIGN KEY (workout_id) REFERENCES workouts(id) ON DELETE CASCADE)
''')
conn.commit()


def add_profile(username):
    cursor.execute('INSERT INTO profile (name) VALUES (?)', (username,))
    conn.commit()
    print('Пользователь добавлен')


def get_user():
    cursor.execute('SELECT name FROM profile')
    user = cursor.fetchone()[0]
    return user


def get_week(username):
    """Получаем неделю"""
    cursor.execute('SELECT day_of_week, order_in_day FROM workouts')
    rows = cursor.fetchall()
    return rows


def create_workout(day_of_week, kind, status='planned'):
    """Создаем новую тренировку"""
    cursor.execute('SELECT COUNT(*) as count FROM  workouts HERE day_of_week = ?', (day_of_week,))
    count = cursor.fetchone()['count']
    order_in_day = count + 1

    cursor.execute('''
        INSERT INTO workouts (day_of_week, order_in_day, kind, status)
        VALUES (?,?,?,?,?)
    '''), (day_of_week, order_in_day, kind, status)
    conn.commit()


def update_workout(workout_id, kind, status):
    """Обновляет данные существующей тренировки."""
    cursor.execute('''
        UPDATE workouts
        SET kind = ?, status = ?
        WHERE id = ?    
    ''', (kind, status, workout_id))
    conn.commit()


def delete_workout_exercises(workout_id):
    """Удаляет все упражнения конкретной тренировки (для перезаписи)."""
    cursor.execute('''
        DELETE FROM exercises WHERE workout_id = ?
    ''', (workout_id,))
    conn.commit()

def add_exercise(workout_id, name, sets, reps, weight, order_num):
    """Добавляет одно упражнение в тренировку."""
    cursor.execute('''
        INSERT INTO exercises (workout_id, name, sets, reps, weight, order_num)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (workout_id, name, sets, reps, weight, order_num))
    conn.commit()

add_profile('Kamil')
get_user()


conn.close()