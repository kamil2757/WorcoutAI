"""Модуль для работы с базой данных SQLite приложения WorkoutИИ."""

import os
import sqlite3
import sys

# Абсолютный путь к БД: файл всегда лежит рядом со скриптом
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "workoutAI.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.execute("PRAGMA foreign_keys = ON")
conn.row_factory = sqlite3.Row  # доступ к колонкам по именам
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_of_week INTEGER NOT NULL CHECK(day_of_week BETWEEN 0 AND 6),
        order_in_day INTEGER NOT NULL,
        kind TEXT NOT NULL,
        status TEXT DEFAULT 'planned' CHECK(status IN ('planned', 'done')),
        UNIQUE(day_of_week, order_in_day)
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workout_id INTEGER NOT NULL,
        name TEXT NOT NULL CHECK(length(trim(name)) > 0),
        sets INTEGER NOT NULL CHECK(sets > 0),
        reps INTEGER NOT NULL CHECK(reps > 0),
        weight REAL DEFAULT 0 CHECK(weight >= 0),
        order_num INTEGER NOT NULL,
        FOREIGN KEY (workout_id) REFERENCES workouts(id) ON DELETE CASCADE
    )
"""
)
conn.commit()


class WorkoutLimitError(Exception):
    """Исключение при попытке добавить больше 2 тренировок в один день."""

    pass


def add_profile(username):
    """Создает профиль пользователя с указанным именем в БД."""
    cursor.execute("INSERT INTO profile (name) VALUES (?)", (username,))
    conn.commit()


def get_user():
    """Возвращает имя пользователя из БД или None, если профиль не создан."""
    cursor.execute("SELECT name FROM profile ORDER BY id LIMIT 1")
    row = cursor.fetchone()
    return row["name"] if row else None


def get_week():
    """Возвращает количество тренировок на каждый день недели (список из 7 чисел)."""
    cursor.execute(
        "SELECT day_of_week, COUNT(*) AS count FROM workouts GROUP BY day_of_week"
    )
    counts = [0] * 7
    for row in cursor.fetchall():
        counts[row["day_of_week"]] = row["count"]
    return counts


def get_day(day_of_week):
    """
    Возвращает тренировки выбранного дня в виде списка словарей:
    {'id', 'order_in_day', 'kind', 'status', 'exercises': [{'name','sets','reps','weight','order_num'}, ...]}
    """
    cursor.execute(
        "SELECT id, order_in_day, kind, status FROM workouts "
        "WHERE day_of_week = ? ORDER BY order_in_day",
        (day_of_week,),
    )
    workouts = cursor.fetchall()

    data = []
    for w in workouts:
        cursor.execute(
            "SELECT name, sets, reps, weight, order_num FROM exercises "
            "WHERE workout_id = ? ORDER BY order_num",
            (w["id"],),
        )
        workout = dict(w)
        workout["exercises"] = [dict(ex) for ex in cursor.fetchall()]
        data.append(workout)
    return data


def save_workout(workout_id, day_of_week, kind, status, exercises):
    """
    Атомарно сохраняет или обновляет тренировку вместе со списком упражнений.
    При возникновении ошибки откатывает транзакцию.
    """
    try:
        if workout_id:
            cursor.execute(
                "UPDATE workouts SET kind = ?, status = ? WHERE id = ?",
                (kind, status, workout_id),
            )
            cursor.execute(
                "DELETE FROM exercises WHERE workout_id = ?", (workout_id,)
            )
        else:
            cursor.execute(
                "SELECT COUNT(*) AS count FROM workouts WHERE day_of_week = ?",
                (day_of_week,),
            )
            if cursor.fetchone()["count"] >= 2:
                raise WorkoutLimitError("Больше 2 тренировок в день нельзя")

            cursor.execute(
                "INSERT INTO workouts (day_of_week, order_in_day, kind, status) "
                "VALUES (?, (SELECT COALESCE(MAX(order_in_day), 0) + 1 FROM workouts WHERE day_of_week = ?), ?, ?)",
                (day_of_week, day_of_week, kind, status),
            )
            workout_id = cursor.lastrowid

        for i, ex in enumerate(exercises):
            cursor.execute(
                "INSERT INTO exercises (workout_id, name, sets, reps, weight, order_num) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    workout_id,
                    ex["name"],
                    ex["sets"],
                    ex["reps"],
                    ex["weight"],
                    i,
                ),
            )

        conn.commit()
        return workout_id
    except Exception:
        conn.rollback()
        raise


def clean_week():
    """Полностью очищает расписание тренировок на неделю."""
    cursor.execute("DELETE FROM workouts")
    conn.commit()


def delete_workout(workout_id):
    """Удаляет тренировку по её ID (упражнения удаляются каскадно)."""
    cursor.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))
    conn.commit()