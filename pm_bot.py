from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ChatActions 
from aiogram.utils import executor
import mysql.connector
import asyncio
from mysql.connector import errorcode
import datetime
import pytz

TOKEN = '000000'

# настройки базы данных
DB_HOST = 'localhost'
DB_NAME = 'arknet_pm_bot'
DB_USER = 'kasperky_tg_bot'
DB_PASSWORD = 'D4tas27w@'

now = datetime.datetime.now() 

# Установить начальное и конечное время
start_time = now.replace(hour=9, minute=0, second=0)
end_time = now.replace(hour=18, minute=0, second=0)

try:
    db = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, autocommit=True)
    cursor = db.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Ошибка авторизации в БД.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("База данных не существует.")
    else:
        print(f"Ошибка подключения к базе данных: {err}")


def get_table_columns(table_name):
    columns = []
    cursor = db.cursor()
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    results = cursor.fetchall()
    for column in results:
        column_name = column[0]
        columns.append(column_name)
    return columns

# объект команды на хранение в базе данных
class Task:
    def __init__(self, task_id, user_id, task_text, deadline,done,color):
        self.task_id = task_id
        self.user_id = user_id
        self.task_text = task_text
        self.deadline = deadline
        self.done = done
        self.color = color

        # Добавляем недостающие поля в объект класса User

# объект команды на хранение в базе данных
class User:
    def __init__(self, user_id, is_admin, reassign_allowed,name):
        self.user_id = user_id
        self.is_admin = is_admin
        self.reassign_allowed = reassign_allowed
        self.name = name


loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage,loop=loop)

# настройки состояний пользователя
class UserStates(StatesGroup):
    waiting_for_task_text = State()    
    waiting_for_deadline = State()
    waiting_for_close_task_id = State()
    waiting_for_remove_task_id = State() 
    waiting_for_reassign_task_id = State()
    waiting_for_reassign_user_id = State()
    waiting_for_reassign_deadline = State()
    waiting_for_close_reason = State()
    waiting_for_close_comment = State() 
    waiting_for_task_description = State()
    waiting_for_task_color = State()


@dp.message_handler(commands=['show_users'])
async def show_users(message: types.Message):
    query = "SELECT * FROM users"
    cursor.execute(query)
    rows = cursor.fetchall()
    users = []
    for row in rows:
        user = User(user_id=row[0], is_admin=row[1], reassign_allowed=row[2],name = row[3])
        users.append(user)
    text = "Список пользователей:\n"
    for user in users:
        text += f"ID: {user.user_id} Username: {user.name} - {'администратор' if user.is_admin else 'пользователь'}\n"
    await message.answer(text)

@dp.message_handler(commands=['add_task'])
async def add_task(message: types.Message, state: FSMContext):
    # Запросить у пользователя описание задачи
    await UserStates.waiting_for_task_description.set()
    await message.answer("Введите описание задачи:")

@dp.message_handler(state=UserStates.waiting_for_task_description, content_types=types.ContentTypes.TEXT)
async def add_task_color(message: types.Message, state: FSMContext):
    task_description = message.text
    
    # Запросить цвет задачи с помощью клавиатуры с кнопками
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
       types.KeyboardButton("Красный"),
        types.KeyboardButton("Желтый"),
        types.KeyboardButton("Зеленый")
    )
    await UserStates.waiting_for_task_color.set()
    await state.update_data(task_description=task_description)
    await message.answer("Выберите цвет задачи:", reply_markup=keyboard)

@dp.message_handler(state=UserStates.waiting_for_task_color, content_types=types.ContentTypes.TEXT)
async def set_deadline(message: types.Message, state: FSMContext):
    await UserStates.waiting_for_deadline.set()
    task_color = message.text
    await message.answer("Укажите срок выполнения задачи в формате: YYYY-MM-DD",reply_markup=types.ReplyKeyboardRemove())

    # сохранение состояния пользователя
    await state.set_state(UserStates.waiting_for_deadline)
    await state.update_data(task_color=task_color)
    
@dp.message_handler(state=UserStates.waiting_for_deadline, content_types=types.ContentTypes.TEXT)
async def add_task_submit(message: types.Message, state: FSMContext):
    deadline = message.text
    
    # Получить данные из состояния пользователя
    data = await state.get_data()
    task_description = data["task_description"]
    task_color = data["task_color"]
    
    # Вставить новую задачу в базу данных
    try:
        query = "INSERT INTO tasks (user_id, task_text, color, deadline,done) VALUES (%s, %s, %s,%s,0)"
        data = (message.from_user.id, task_description, task_color, deadline)
        cursor.execute(query, data)

        await message.answer("Задача добавлена")
        await state.finish()
    except:
        await message.answer("Что-то пошло не так при добавлении задачи")
        await state.finish()
# удаление задачи
@dp.message_handler(commands=['remove_task'])
async def remove_task(message: types.Message, state: FSMContext):

    query = "SELECT * FROM users WHERE user_id = %s"
    data = (message.from_user.id,)
    cursor.execute(query, data)
    Rows = cursor.fetchone()

    if Rows[1] == True:
        await UserStates.waiting_for_remove_task_id.set()
        await message.answer("Введите ID удаляемой задачи:")
    

    # сохранение состояния пользователя
        await state.set_state(UserStates.waiting_for_remove_task_id)
    else:
        await bot.send_message(text = "Эта функция доступна только администраторам",chat_id= message.from_user.id)

@dp.message_handler(state=UserStates.waiting_for_remove_task_id, content_types=types.ContentTypes.TEXT)
async def set_deadline(message: types.Message, state: FSMContext):
    task_id = message.text
    query = "SELECT * FROM users WHERE user_id = %s"
    data = (message.from_user.id,)
    cursor.execute(query, data)
    Rows = cursor.fetchone()
    try:
        if Rows[1] == True:
            
            query = "DELETE FROM tasks WHERE task_id = %s"
            data = (task_id,)
            cursor.execute(query, data)
            await message.answer(f"Задача с ID {task_id} успешно удалена.")
        else:
            await bot.send_message(text = "Эта функция доступна только администраторам",chat_id= message.from_user.id)

        await state.finish()
    except:
        await message.answer("Что-то пошло не так при удалении задачи")
        await state.finish()        


# обработчик для /start
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    # добавление пользователя в базу данных
    user = User(user_id=message.from_user.id, is_admin=False,reassign_allowed=True,name = message.from_user.first_name)
    query = "INSERT IGNORE INTO users (user_id, is_admin,reassign_allowed,username) VALUES (%s, %s,%s,%s)"
    data = (user.user_id, user.is_admin,user.reassign_allowed,user.name)
    cursor.execute(query, data)
    await message.answer("Привет, я бот для хранения задач. Используй команду /help для подсказок и помощи.")


@dp.message_handler(commands=['help'])
async def help(message: types.Message, state: FSMContext):
    query = "SELECT * FROM users WHERE user_id = %s"
    data = (message.from_user.id,)
    cursor.execute(query, data)
    Rows = cursor.fetchone()

    if Rows[1] == True:
        await message.answer("Список команд:\n /add_task - добавить новую задачу \n /remove_task - Удалить задачу\n /done_task -  завершить задачу\n /show_tasks - посмотреть свои задачи \n /show_all_tasks - посмотреть все задачи \n /reassign_task - переназначить задачу\n /show_users - список всех пользователей\n")
    else:
        await message.answer("Список команд:\n /add_task - добавить новую задачу\n /done_task -  завершить задачу\n /show_tasks - посмотреть свои задачи \n /reassign_task - переназначить задачу другому пользователю \n /show_users - список всех пользователей\n")



@dp.message_handler(commands=['done_task'])
async def done_task(message: types.Message, state: FSMContext):
    # Запросить у пользователя ID завершаемой задачи
    await UserStates.waiting_for_remove_task_id.set()
    await message.answer("Введите ID завершаемой задачи:")

    # Сохранение состояния пользователя
    await state.set_state(UserStates.waiting_for_close_task_id)


@dp.message_handler(state=UserStates.waiting_for_close_task_id, content_types=types.ContentTypes.TEXT)
async def done_task_reason(message: types.Message, state: FSMContext):
    task_id = message.text
    # Проверить, принадлежит ли задача текущему пользователю
    query = "SELECT * FROM tasks WHERE task_id = %s"
    data = (task_id,)
    cursor.execute(query, data)
    Rows = cursor.fetchone()

    if Rows[0] == message.from_user.id:
        # Запросить причину закрытия задачи с помощью клавиатуры с кнопками
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Завершена Успешно", "Задача требует дополнительных ресурсов", "Задача не может быть выполнена", "Другая")
        await state.update_data(task_id=task_id)
        await UserStates.waiting_for_close_reason.set()
        await message.answer("Выберите причину закрытия:", reply_markup=keyboard)
    else:
        await message.answer("Эта задача принадлежит другому пользователю")
        await state.finish()


@dp.message_handler(state=UserStates.waiting_for_close_reason, content_types=types.ContentTypes.TEXT)
async def done_task_comment(message: types.Message, state: FSMContext):
    # Получить причину закрытия из сообщения пользователя
    reason = message.text

    # Запросить комментарий к закрытию с помощью обычного текстового сообщения
    await state.update_data(reason=reason)
    await UserStates.waiting_for_close_comment.set()
    await message.answer("Введите комментарий к закрытию:",reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=UserStates.waiting_for_close_comment, content_types=types.ContentTypes.TEXT)
async def done_task_submit(message: types.Message, state: FSMContext):
     # Получить и сохранить комментарий к закрытию
    comment = message.text

    # Получить данные из состояния пользователя
    data = await state.get_data()
    task_id = data["task_id"]
    reason = data["reason"]

    # Обновить задачу в базе данных
    query = "UPDATE tasks SET done = 1, close_time = TIME(NOW()), close_type = %s, close_comment = %s WHERE task_id = %s"
    data = (reason, comment, task_id)
    cursor.execute(query, data)

    await message.answer(f"Задача с ID {task_id} выполнена с причиной {reason} и комментарием: {comment}")
    await state.finish()

# показ всех задач для текущего пользователя
@dp.message_handler(commands=['show_tasks'])
async def show_tasks(message: types.Message):
    user_id = message.from_user.id
    query = "SELECT * FROM tasks WHERE user_id = %s"
    data = (user_id,)
    cursor.execute(query, data)
    rows = cursor.fetchall()
    tasks = []
    for row in rows:
        task = Task(task_id=row[1], user_id=row[0], task_text=row[2], deadline=row[3], done=row[4],color =row[6])
        tasks.append(task)
    text = "Список задач:\n"
    for task in tasks:
        done = "True" if task.done == 1 else "False"
        text += f"Задача \n Статус завершения: {done}  Цвет {task.color} \n Номер задачи {task.task_id}. Текст задачи {task.task_text}\n " + (f" Срок выполнения ({task.deadline})" if task.deadline is not None else "") + "\n"
    await message.answer(text)

# показ всех задач для администратора
@dp.message_handler(commands=['show_all_tasks'])
async def show_all_tasks(message: types.Message):
    # Запрос для получения списка задач
    query = "SELECT * FROM tasks"
    cursor.execute(query)
    rows = cursor.fetchall()

    tasks = []
    for row in rows:
        task = Task(task_id=row[1], user_id=row[0], task_text=row[2], deadline=row[3], done=row[4],color = row[6])
        tasks.append(task)

    
    for task in tasks:
        text = "Список задач:\n"
        # Запрос для получения имени пользователя по user_id
        query = "SELECT username FROM users WHERE user_id = %s"
        data = (task.user_id,)
        cursor.execute(query, data)
        user = cursor.fetchone()

        if user is not None:
            username = user[0]
        else:
            username = "Unknown"  # Если имя пользователя не найдено, установим значение по умолчанию

        text += f"Номер задачи: {task.task_id}  Цвет задачи {task.color}.\n Задача: {task.task_text}\n"
        text += f"Исполнитель: {username}\n"
        text += f"Срок: {task.deadline}\n"
        text += f"Выполнен: {task.done}\n"
        text += "\n"

        await bot.send_message(text=text, chat_id=message.from_user.id)

async def remind_about_task():
    now = datetime.datetime.now() + datetime.timedelta(hours=5)

# Установить начальное и конечное время
    start_time = now.replace(hour=9, minute=0, second=0)
    end_time = now.replace(hour=18, minute=0, second=0)
    # Получить текущую дату и время в местной временной зоне UTC+5
    while start_time <= now <= end_time:
        query = " select * from tasks where color = 'Красный' AND DATEDIFF(deadline, CURDATE())<=3 AND deadline > DATE(NOW()) AND done = 0"
        cursor.execute(query)
        tasks_red = cursor.fetchall()
        red_tasks = []
        for row in tasks_red:
            task = Task(task_id=row[1], user_id=row[0], task_text=row[2], deadline=row[3], done=row[4],color = row[6])
            red_tasks.append(task)
    # Проверить каждую красную задачу и отправить напоминание за 3 дня до дедлайна
        for task in red_tasks:
            task_description = task.task_text
            user_id = task.user_id
            await bot.send_message(user_id, f"Напоминание о задаче {task_description}: У вас есть менее 3 дней до дедлайна.")

    # Выбрать все задачи из базы данных с желтым цветом и дедлайном на следующий день

        query = "SELECT * FROM tasks WHERE color = 'Желтый' AND DATEDIFF(deadline, CURDATE())=1 AND done = 0"
        cursor.execute(query)
        tasks_yellow = cursor.fetchall()
        yellow_tasks = []
        for row in tasks_yellow:
            task = Task(task_id=row[1], user_id=row[0], task_text=row[2], deadline=row[3], done=row[4],color = row[6])
            yellow_tasks.append(task)
    # Проверить каждую желтую задачу и отправить напоминание за 1 день до дедлайна
        for task in yellow_tasks:
            task_description = task.task_text
            user_id = task.user_id
            await bot.send_message(user_id, f"Напоминание о задаче {task_description}: У вас завтра дедлайн.")

    # Выбрать все задачи из базы данных с зеленым цветом и дедлайном сегодня
        query = "SELECT * FROM tasks WHERE  deadline = DATE(NOW()) AND done = 0"
        cursor.execute(query)
        tasks_green = cursor.fetchall()
        green_tasks = []
        for row in tasks_green:
            task = Task(task_id=row[1], user_id=row[0], task_text=row[2], deadline=row[3], done=row[4],color = row[6])
            green_tasks.append(task)
    # Проверить каждую зеленую задачу и отправить напоминание в день дедлайна
        for task in green_tasks:
            task_description = task.task_text
            user_id = task.user_id
            await bot.send_message(user_id, f"Напоминание о задаче {task_description}: У вас дедлайн сегодня.")

        query = "SELECT * FROM tasks WHERE  deadline < DATE(NOW()) AND done = 0" 
        cursor.execute(query)
        tasks_green = cursor.fetchall()
        green_tasks = []
        for row in tasks_green:
            task = Task(task_id=row[1], user_id=row[0], task_text=row[2], deadline=row[3], done=row[4],color = row[6])
            green_tasks.append(task)
    # Проверить каждую зеленую задачу и отправить напоминание в день дедлайна
        for task in green_tasks:
            task_description = task.task_text
            user_id = task.user_id
            await bot.send_message(user_id, f"Напоминание о задаче {task_description}: Дедлайн просрочен. Задача должна была быть выполнена {task.deadline}")
        now = datetime.datetime.now() + datetime.timedelta(hours=5)
        await asyncio.sleep(3600)

# переназначение задачи
@dp.message_handler(commands=['reassign_task'])
async def reassign_task_handler(message: types.Message):
    await message.answer("Введите ID задачи, которую вы хотите переназначить")
    await UserStates.waiting_for_reassign_task_id.set()

@dp.message_handler(state=UserStates.waiting_for_reassign_task_id)
async def reassign_task_id_handler(message: types.Message, state: FSMContext):
    task_id = message.text
    if task_id.isdigit():
        await state.update_data(task_id=task_id)
        await message.answer("Введите ID пользователя, кому вы хотите переназначить задачу")
        await UserStates.waiting_for_reassign_user_id.set()
    else:
        await message.answer("Введите число.")
@dp.message_handler(state=UserStates.waiting_for_reassign_user_id)
async def reassign_task_id_handler(message: types.Message, state: FSMContext):
    user_id = message.text
    if user_id.isdigit():
        await state.update_data(user_id=user_id)
        await message.answer("Введите дедлайн задачи")
        await UserStates.waiting_for_reassign_deadline.set()
    else:
        await message.answer("Введите число.")

        
@dp.message_handler(state=UserStates.waiting_for_reassign_deadline)
async def reassign_user_id_handler(message: types.Message, state: FSMContext):
    task_id = (await state.get_data())['task_id']
    user_id = (await state.get_data())['user_id']
    deadline = message.text
        # проверяем, что новый пользователь существует и имеет право на переназначение задач
    query = "SELECT reassign_allowed FROM users WHERE user_id = %s"
    data = (message.from_user.id,)
    cursor.execute(query, data)
    rows = cursor.fetchall()

    reassign_allowed = bool(rows[0][0])
    if not reassign_allowed:
        await message.answer("Указанный пользователь не имеет прав на переназначение задач.")
        return
        # переназначаем задачу в базе данных
    try:
        query = "UPDATE tasks SET user_id = %s WHERE task_id = %s"
        
        data = (user_id, task_id)
        cursor.execute(query, data)
        query = "UPDATE tasks SET deadline = %s WHERE task_id = %s"
        data = (deadline, task_id)
        cursor.execute(query, data)

        query = "SELECT color,task_text FROM tasks WHERE task_id = %s"
        data = (task_id,)
        cursor.execute(query, data)
        color,task_text = cursor.fetchone()
        await message.answer(f"Задача с ID {task_id} успешно переназначена пользователю {user_id}.")
        await bot.send_message(chat_id=user_id, text = f"На вас переназначена задача {task_id}, ee цвет {color} \n Задача: {task_text}")
        await state.finish()
    except:
        await message.answer("Что-то пошло не так при перераспределении задачи")
        await state.finish() 






if __name__ == '__main__':
    # запуск напоминания о задаче в отдельном потоке
    
    dp.loop.create_task(remind_about_task())
    # запуск бота
	
    executor.start_polling(dp, skip_updates=True)
