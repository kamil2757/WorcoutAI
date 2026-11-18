from datebase import *


def seed():
    # очистка старых данных (порядок важен: сначала упражнения, потом тренировки)
    cursor.execute('DELETE FROM exercises')
    cursor.execute('DELETE FROM workouts')
    conn.commit()

    # --- Понедельник (0): Силовая ---
    wid = create_workout(0, 'Силовая', 'done')
    add_exercise(wid, 'Жим лёжа', 4, 8, 60, 0)
    add_exercise(wid, 'Приседания', 4, 10, 80, 1)
    add_exercise(wid, 'Подтягивания', 3, 8, 0, 2)

    # --- Вторник (1): Кардио ---
    wid = create_workout(1, 'Кардио', 'planned')
    add_exercise(wid, 'Бег на дорожке', 1, 30, 0, 0)
    add_exercise(wid, 'Скакалка', 3, 60, 0, 1)

    # --- Вторник (1): вторая тренировка ---
    wid = create_workout(1, 'Растяжка', 'planned')
    add_exercise(wid, 'Растяжка спины', 2, 30, 0, 0)
    add_exercise(wid, 'Шпагат (работа над ним)', 3, 40, 0, 1)

    # --- Среда (2): пусто, чтобы проверить пустой день ---

    # --- Четверг (3): Функциональная ---
    wid = create_workout(3, 'Функциональная', 'planned')
    add_exercise(wid, 'Берпи', 4, 12, 0, 0)
    add_exercise(wid, 'Отжимания', 4, 15, 0, 1)
    add_exercise(wid, 'Планка', 3, 60, 0, 2)

    # --- Суббота (5): Силовая ---
    wid = create_workout(5, 'Силовая', 'done')
    add_exercise(wid, 'Становая тяга', 4, 6, 100, 0)
    add_exercise(wid, 'Тяга штанги в наклоне', 3, 10, 40, 1)

    # --- Воскресенье (6): пусто ---
    print('Тестовые данные загружены')


if __name__ == '__main__':
    seed()