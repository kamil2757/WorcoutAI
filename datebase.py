import sqlite3


conn = sqlite3.connect('workoutAI.db')
conn.execute("PRAGMA foreign_keys = ON")
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
        day_of_week INTEGER NOT NULL,
        order_in_day INTEGER NOT NULL,
        kind TEXT NOT NULL,
        status TEXT DEFAULT 'planned'
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
    print(1)
    cursor.execute('INSERT INTO profile (name) VALUES (?)', (username,))
    conn.commit()
    print('Пользователь добавлен')


def get_user():
    cursor.execute('SELECT name FROM profile LIMIT 1')
    row = cursor.fetchone()
    if row:
        return row[0]
    return None


def get_week():
    """Возвращает количество тренировок на каждый день недели"""
    cursor.execute('SELECT day_of_week, COUNT(*) FROM workouts GROUP BY day_of_week')
    rows = cursor.fetchall()

    counts = [0] * 7
    for day_indx, count in rows:
        counts[day_indx] = count
    return counts


def get_day(day_of_week):
    """Возвращает тренировки и упражнения для конкретного дня"""
    cursor.execute('SELECT id, order_in_day, kind, status FROM workouts WHERE day_of_week = ?', (day_of_week,))
    rows = cursor.fetchall()
    data = []
    for r in rows:
        cursor.execute('SELECT name, sets, reps, weight, order_num FROM exercises WHERE workout_id=? ORDER BY order_num', (r[0],))
        d_exercises = cursor.fetchall()
        data.append([r, d_exercises])
    return data


# def get_exercises(workout_id):
#     cursor.execute('SELECT name, sets, reps, weight, order_num FROM exercises WHERE workout_id = ? ORDER BY order_num', (workout_id,))
#     rows = cursor.fetchall()
#     return rows



def create_workout(day_of_week, kind, status='planned'):
    """Создаем новую тренировку"""
    cursor.execute('SELECT COUNT(*) FROM  workouts WHERE day_of_week = ?', (day_of_week,))
    count = cursor.fetchone()[0]
    if count == 2:
        return ['Ошибка', 'Больше 2 тренировок в день нельзя']
    order_in_day = count + 1

    cursor.execute('''
        INSERT INTO workouts (day_of_week, order_in_day, kind, status)
        VALUES (?,?,?,?)
    ''', (day_of_week, order_in_day, kind, status))
    conn.commit()
    return cursor.lastrowid


def update_workout(workout_id, kind, status):
    """Обновляет данные существующей тренировки."""
    cursor.execute('''
        UPDATE workouts
        SET kind = ?, status = ?
        WHERE id = ?    
    ''', (kind, status, workout_id))
    conn.commit()


def delete_workout(workout_id):
    cursor.execute('DELETE FROM workouts WHERE id = ?', (workout_id,))
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
