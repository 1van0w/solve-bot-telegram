
import sympy
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import re
from sympy import symbols, sympify, sqrt, integrate, diff
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sympy as sp
from sympy import Sum, Symbol


tg_token = "6868429370:AAGtMnYIYl7NFUCE47qeZryI0eA_2E33UrU"
bot = Bot(tg_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_help = types.KeyboardButton('/help')
    keyboard.add(button_help)
    user = message.from_user
    await message.answer(f"Привет, {user.first_name}! Нажмите /help, чтобы получить дополнительную информацию о командах бота.", reply_markup=keyboard)

# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    help_text = (
        "Доступные команды:\n"
        "/menu - Меню со списком команд для решения задач.\n"
        "/help - Список общих команд.\n"
        "/info - Информация о боте.\n"
    )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_menu = types.KeyboardButton('/menu')
    button_info = types.KeyboardButton('/info')
    button_return = types.KeyboardButton("/help")
    keyboard.add(button_menu, button_info, button_return)
    await message.answer(help_text, reply_markup=keyboard)

# Обработчик команды /menu
@dp.message_handler(commands=['menu'])
async def send_additional_menu(message: types.Message):
    additional_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    additional_menu.add(
        types.KeyboardButton('/help'),
        types.KeyboardButton('/dydx'),
        types.KeyboardButton('/fx'),
        types.KeyboardButton('/int'),
        types.KeyboardButton('/lim'),
        types.KeyboardButton('/series'),
        types.KeyboardButton('/root'),
        types.KeyboardButton('/factor'),
        types.KeyboardButton('/comp'),
    )
    menu_text = (
        "Список команд для расчетов:\n"
        "/help - Вернуться к списку основных команд.\n"
        "/dydx - Найти производную.\n"
        "/fx - Найти первообразную.\n"
        "/int - Найти интеграл.\n"
        "/lim - Найти предел.\n"
        "/series - Посчитать ряд.\n"
        "/root - Найти корень.\n"
        "/factor - Разложить на множители.\n"
        "/comp - Посчитать сложный процент."
    )
    await message.answer(menu_text, reply_markup=additional_menu)

# Обработчик команды /info
@dp.message_handler(commands=['info'])
async def help_command(message: types.Message):
    info_text = (
        "Для списка общих команд вы можете нажать /help\n"
        "А для списка команд для решений вы можете нажать /menu\n"
        "Наши соц.сети:\n"
        "Twitch: https://www.twitch.tv/sinbrightly\n"
        "YouTube: https://www.youtube.com/@Sin_Brightly\n"
        "Instagram: https://www.instagram.com/sin_brightlyru/\n"
    )
    await message.answer(info_text, disable_web_page_preview=True)


# Классы для статики
class MathState(StatesGroup):
    DYDX = State()
    FX = State()
    INT = State()
    LIM = State()
    SERIES = State()
    SERIES_LENGHT = State()
    ROOT = State()
    FACTOR = State()
    COMP = State()



# Работа с производными

# Исполнитель команды /dydx, поддерживающий работу данного отрезка кода, только в том случае, если команда введена
@dp.message_handler(commands=["dydx"])
async def start_dydx(message: types.Message, state: FSMContext):
    await MathState.DYDX.set()
    menu_text = (
        f"Введите уравнение для нахождения производной.\n"
        f"Вы можете нажать /restartdydx для перезапуска операции.\n"
        f"Не забудьте нажать команду /stopdydx для остановки операции.\n\n"
        f"Вводите уравнение в формате x = ваше уравнение."
    )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('/menu'))
    keyboard.add(types.KeyboardButton('/stopdydx'))
    keyboard.add(types.KeyboardButton('/restartdydx'))
    await message.answer(text=menu_text, reply_markup=keyboard)

# Обработчик команды /stopdydx для остановки операции
@dp.message_handler(commands=["stopdydx"], state=MathState.DYDX)
async def stop_dydx(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Операция по вычислению производной окончена.")

# Обработчик команды /restartdydx для перезапуска операции
@dp.message_handler(commands=["restartdydx"])
async def restart_dydx(message: types.Message, state: FSMContext):
    await start_dydx(message, state)

# Обработчик команды /dydx, вычисления.
async def calculate_derivative(message, variable, equation):
    try:
        var = symbols(variable)
        x = symbols('x')
        equation = re.sub(r'(\d+)([a-z])', r'\1*\2', equation)  # Преобразуем 3x в 3*x
        expr = sympify(equation)
        derivative = diff(expr, x)
        await message.reply(f"Производная вашей функции по переменной {variable}: {derivative}")
    except Exception as e:
        await message.reply(f"Произошла ошибка при вычислении производной. Попробуйте еще раз.")

# Обработчик сообщений для вычисления производной
@dp.message_handler(state=MathState.DYDX)
async def solve_math_tasks(message: types.Message, state: FSMContext):
    try:
        user_input = message.text.lower().replace(" ", "")

        # Ищем уравнение в сообщении
        equation_match = re.search(r'([a-z])\s*=\s*([^\n]*)', user_input)
        if equation_match:
            variable, equation = equation_match.group(1).strip(), equation_match.group(2).strip()
            await calculate_derivative(message, variable, equation)
        else:
            await message.reply("Не удалось извлечь уравнение для производной.")
    except Exception as e:
        await message.reply(f"Произошла ошибка при обработке задачи. Попробуйте еще раз.")



# Работа с первообразными

# Исполнитель команды /fx, поддерживающий работу данного отрезка кода, только в том случае, если команда введена
@dp.message_handler(commands=["fx"])
async def start_fx(message: types.Message, state: FSMContext):
    await MathState.FX.set()
    menu_text = (
        f"Введите уравнение для нахождения первообразной.\n"
        f"Вы можете нажать /restartfx для перезапуска операции.\n"
        f"Не забудьте нажать команду /stopfx для остановки операции.\n\n"
        f"Вводите уравнение в формате x = ваше уравнение."
    )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('/menu'))
    keyboard.add(types.KeyboardButton('/stopfx'))
    keyboard.add(types.KeyboardButton('/restartfx'))

    await message.answer(text=menu_text, reply_markup=keyboard)

# Обработчик команды /stopfx для остановки операции
@dp.message_handler(commands=['stopfx'], state='*')
async def stop_fx(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Операция по вычислению первообразной остановлена.")

# Обработчик команды /restartfx для перезапуска операции
@dp.message_handler(commands=["restartfx"])
async def restart_fx(message: types.Message, state: FSMContext):
    await start_fx(message, state)


# Обработчик команды /fx, вычисление первообразной
async def calculate_primitive(message, equation):
    try:
        x = symbols('x')
        # Заменяем обозначения умножения на верные
        equation = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', equation)  # Пример: замена 3x на 3*x
        expr = sympify(equation)
        primitive = integrate(expr, x)
        await message.reply(f"Первообразная вашего выражения: {primitive}")
    except Exception as e:
        await message.reply(f"Произошла ошибка при вычислении первообразной. Попробуйте еще раз.")


# Обработчик сообщений для вычисления первообразной в состоянии MathState.FX
@dp.message_handler(state=MathState.FX)
async def solve_primitive(message: types.Message, state: FSMContext):
    try:
        # Получаем текст сообщения и удаляем пробелы
        equation = message.text.replace(" ", "")

        # Проверяем, начинается ли сообщение с буквы и знака равенства
        if re.match(r'^[a-zA-Z]\s?=\s?', equation):
            equation = re.sub(r'^[a-zA-Z]\s?=\s?', "", equation)  # Убираем переменную перед вычислением
            await calculate_primitive(message, equation)
        else:
            await message.reply("Введите уравнение в формате 'x = ваше уравнение'.")

    except Exception as e:
        await message.reply(f"Произошла ошибка при обработке задачи. Попробуйте еще раз.")





# Работа с пределами

# Исполнитель команды /lim, поддерживающий работу данного отрезка кода, только в том случае, если команда введена
@dp.message_handler(commands=["lim"])
async def start_lim(message: types.Message, state: FSMContext):
    await MathState.LIM.set()
    menu_text = (
        f"Введите уравнение для нахождения предела.\n"
        f"Вы можете нажать /restartlim для перезапуска операции.\n"
        f"Не забудьте нажать команду /stoplim для остановки операции.\n\n"
        f"Вводите уравнение в формате lim_x-> ваше уравнение.\n"
        f"Используйте inf для обозначения бесконечности."
    )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('/menu'))
    keyboard.add(types.KeyboardButton('/stoplim'))
    keyboard.add(types.KeyboardButton('/restartlim'))

    await message.answer(text=menu_text, reply_markup=keyboard)

# Обработчик команды /stoplim для остановки операции
@dp.message_handler(commands=["stoplim"], state=MathState.LIM)
async def stop_lim(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Операция по вычислению предела остановлена.")

# Обработчик команды /restartlim для перезапуска операции
@dp.message_handler(commands=["restartlim"])
async def restart_lim(message: types.Message, state: FSMContext):
    await start_lim(message, state)

# Функция для вычисления предела
async def calculate_limit(message, variable, value, equation):
    try:
        x = sp.symbols(variable)
        equation = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', equation)
        expr = sp.sympify(equation)
        if value == 'inf':
            limit_value = sp.limit(expr, x, sp.oo)
            await message.reply(f"Предел вашего выражения по переменной {variable} при {variable} -> ∞: {limit_value}")
        else:
            limit_value = sp.limit(expr, x, value)
            await message.reply(f"Предел вашего выражения по переменной {variable} при {variable} -> {value}: {limit_value}")
    except Exception as e:
        await message.reply(f"Произошла ошибка при вычислении предела. Попробуйте еще раз.")

# Обработчик сообщений для вычисления предела в состоянии MathState.LIM
@dp.message_handler(state=MathState.LIM)
async def solve_limit(message: types.Message, state: FSMContext):
    try:
        user_input = message.text.lower().replace(" ", "")
        equation_match = re.search(r'lim_([^=]+)->([^=]+)', user_input)
        if equation_match:
            variable = equation_match.group(1)
            value, equation = equation_match.group(2).split('(')
            value = value if value != 'inf' else value  # Проверяем на бесконечность
            value = float(value)
            equation = equation.rstrip(')')
            await calculate_limit(message, variable, value, equation)
        else:
            await message.reply("Не удалось извлечь выражение для предела.")
    except Exception as e:
        await message.reply(f"Произошла ошибка при обработке задачи. Попробуйте еще раз.")




# Работа с рядами

# Исполнитель команды /series, поддерживающий работу данного отрезка кода, только в том случае, если команда введена
@dp.message_handler(commands=["series"])
async def start_series(message: types.Message, state: FSMContext):
    await MathState.SERIES.set()
    menu_text = (
        f"Введите уравнение для подсчета ряда.\n"
        f"Вы можете нажать /restartseries для перезапуска операции.\n"
        f"Не забудьте нажать команду /stopseries для остановки операции.\n\n"
        f"Вводите в формате длина_ряда: уравнение\n"
        f"Не используйте переменная ="
    )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('/menu'))
    keyboard.add(types.KeyboardButton('/stopseries'))
    keyboard.add(types.KeyboardButton('/restartseries'))

    await message.answer(text=menu_text, reply_markup=keyboard)

# Обработчик команды /stopseries для остановки операции
@dp.message_handler(commands=["stopseries"], state=MathState.SERIES)
async def stop_series(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Операция по подсчету ряда остановлена.")

# Обработчик команды /restartseries для перезапуска операции
@dp.message_handler(commands=["restartseries"])
async def restart_series(message: types.Message, state: FSMContext):
    await start_series(message, state)


# Функция вычисления суммы ряда
async def calculate_series_sum(message, length, equation):
    try:
        # Извлекаем переменную из уравнения
        variable = re.search(r'\b([a-zA-Z])\b', equation).group(1)

        # Создаем символ для переменной
        var = Symbol(variable)

        # Преобразуем уравнение, заменяя 3x на 3*x
        equation = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', equation)

        # Преобразуем уравнение в выражение SymPy
        expr = sympify(equation)

        # Вычисляем сумму ряда
        series_sum = Sum(expr, (var, 1, length)).doit()

        # Отправляем ответ пользователю
        await message.reply(f"Сумма ряда длиной {length} для вашего уравнения: {series_sum}")
    except Exception as e:
        await message.reply(f"Произошла ошибка при вычислении суммы ряда. Попробуйте еще раз.")


# Обработчик сообщений для вычисления суммы ряда
@dp.message_handler(state=MathState.SERIES)
async def solve_series_sum(message: types.Message, state: FSMContext):
    try:
        user_input = message.text.lower().replace(" ", "")

        # Ищем длину ряда и уравнение в сообщении
        series_match = re.search(r'(\d+)\s*:\s*(.+)', user_input)
        if series_match:
            length, equation = int(series_match.group(1).strip()), series_match.group(2).strip()

            # Заменяем выражения типа 3x на 3*x
            equation = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', equation)

            await calculate_series_sum(message, length, equation)
        else:
            await message.reply("Не удалось извлечь длину ряда или уравнение.")
    except Exception as e:
        await message.reply(f"Произошла ошибка при обработке задачи. Попробуйте еще раз.")



# Работа с степенными корнями

# Исполнитель команды /root, поддерживающий работу данного отрезка кода, только в том случае, если команда введена
@dp.message_handler(commands=["root"])
async def start_root(message: types.Message, state: FSMContext):
    await MathState.ROOT.set()
    menu_text = (
        f"Введите уравнение для нахождения корня.\n"
        f"Вы можете нажать /restartroot для перезапуска операции.\n"
        f"Не забудьте нажать команду /stoproot для остановки операции.\n\n"
        f"Вводите уравнение в формате:\n"
        f"Корень x степени из y.\n"

    )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('/menu'))
    keyboard.add(types.KeyboardButton('/stoproot'))
    keyboard.add(types.KeyboardButton('/restartroot'))

    await message.answer(text=menu_text, reply_markup=keyboard)

# Обработчик команды /stoproot для остановки операции
@dp.message_handler(commands=["stoproot"], state=MathState.ROOT)
async def stop_root(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Операция по нахождению корня остановлена.")

# Обработчик команды /restartroot для перезапуска операции
@dp.message_handler(commands=["restartroot"])
async def restart_root(message: types.Message, state: FSMContext):
    await start_root(message, state)

# Обработчик сообщений для вычисления степенного корня
@dp.message_handler(state=MathState.ROOT)
async def solve_math_tasks_general_root(message: types.Message, state: FSMContext):
    try:
        user_input = message.text.lower().replace(" ", "")
        equation_match = re.search(r'корень\s*(\d+)\s*степени\s*из\s*([^\n]*)', user_input)
        if equation_match:
            power = int(equation_match.group(1).strip())
            equation = equation_match.group(2).strip()
            equation = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', equation)
            equation = equation.replace('^', '**')
            var = sympy.symbols('x')
            expr = sympy.sympify(equation)
            root = expr ** (1 / power)  # Вычисление корня определенной степени
            await message.reply(f"Корень {power} степени из вашего выражения: {root}")
        else:
            await message.reply("Не удалось извлечь выражение для корня.")
    except Exception as e:
        await message.reply(f"Произошла ошибка при обработке задачи. Попробуйте еще раз.")




# Работа с разложением на множители

# Исполнитель команды /factor, поддерживающий работу данного отрезка кода, только в том случае, если команда введена
@dp.message_handler(commands=["factor"])
async def start_factor(message: types.Message, state: FSMContext):
    await MathState.FACTOR.set()
    menu_text = (
        f"Введите уравнение для разложения на множители.\n"
        f"Вы можете нажать /restartfactor для перезапуска операции.\n"
        f"Не забудьте нажать команду /stopfactor для остановки операции.\n\n"
        f"Вводите уравнение в формате:\n"
        f"x^2 - 4\n"
        f"Не используйте x ="

    )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('/menu'))
    keyboard.add(types.KeyboardButton('/stopfactor'))
    keyboard.add(types.KeyboardButton('/restartfactor'))

    await message.answer(text=menu_text, reply_markup=keyboard)

# Обработчик команды /stopfactor для остановки операции
@dp.message_handler(commands=["stopfactor"], state=MathState.FACTOR)
async def stop_factor(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Операция по разложению на множители остановлена.")

# Обработчик команды /restartfactor для перезапуска операции
@dp.message_handler(commands=["restartfactor"])
async def restart_factor(message: types.Message, state: FSMContext):
    await start_factor(message, state)

# Разложение на множители, расчет
@dp.message_handler(state=MathState.FACTOR)
async def factorize_expression(message: types.Message, state: FSMContext):
    try:
        user_input = message.text.lower().replace(" ", "")
        equation_match = re.search(r'([^\n]*)', user_input)
        if equation_match:
            equation = equation_match.group(1).strip()
            equation = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', equation)  # Преобразуем 2x в 2*x
            var = sympy.symbols('x')
            expr = sympy.sympify(equation)
            factored_expr = sympy.factor(expr)
            await message.reply(f"Разложение вашего выражения на множители: {factored_expr}")
        else:
            await message.reply("Не удалось извлечь выражение для разложения на множители.")
    except Exception as e:
        await message.reply(f"Произошла ошибка при обработке задачи. Попробуйте еще раз.")








# Работа с интегралами

# Исполнитель команды /int, поддерживающий работу данного отрезка кода, только в том случае, если команда введена
@dp.message_handler(commands=["int"])
async def start_int(message: types.Message, state: FSMContext):
    await MathState.INT.set()
    menu_text = (
        f"Введите уравнение для нахождения интеграла.\n"
        f"Вы можете нажать /restartint для перезапуска операции.\n"
        f"Не забудьте нажать команду /stopint для остановки операции.\n\n"
        f"Вводите уравнение в формате:\n"
        f"нижний предел and верхний предел: уравнение\n"
        f"Не используйте x ="

    )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('/menu'))
    keyboard.add(types.KeyboardButton('/stopint'))
    keyboard.add(types.KeyboardButton('/restartint'))

    await message.answer(text=menu_text, reply_markup=keyboard)

# Обработчик команды /int для остановки операции
@dp.message_handler(commands=["stopint"], state=MathState.INT)
async def stop_int(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Операция по нахождению интеграла остановлена.")

# Обработчик команды /int для перезапуска операции
@dp.message_handler(commands=["restartint"])
async def restart_int(message: types.Message, state: FSMContext):
    await start_int(message, state)

# Функция вычисления интеграла
async def calculate_integral(message, lower_limit, upper_limit, equation):
    try:
        # Преобразуем уравнение в выражение SymPy
        expr = sympify(equation)

        # Вычисляем интеграл
        integral = integrate(expr, (Symbol('x'), lower_limit, upper_limit))

        # Отправляем ответ пользователю
        await message.reply(f"Результат интегрирования от {lower_limit} до {upper_limit} для вашего уравнения: {integral}")
    except Exception as e:
        await message.reply(f"Произошла ошибка при вычислении интеграла. Попробуйте еще раз.")

# Обработчик сообщений для вычисления интеграла
@dp.message_handler(state=MathState.INT)
async def solve_integral(message: types.Message, state: FSMContext):
    try:
        user_input = message.text.lower().replace(" ", "")

        # Ищем верхний и нижний пределы интегрирования и уравнение в сообщении
        integral_match = re.search(r'(\d+)\s*and\s*(\d+):\s*(.+)', user_input)
        if integral_match:
            lower_limit, upper_limit, equation = int(integral_match.group(1).strip()), int(integral_match.group(2).strip()), integral_match.group(3).strip()

            # Заменяем выражения типа 3x на 3*x
            equation = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', equation)

            await calculate_integral(message, lower_limit, upper_limit, equation)
        else:
            await message.reply("Не удалось извлечь пределы интегрирования или уравнение.")
    except Exception as e:
        await message.reply(f"Произошла ошибка при обработке задачи. Попробуйте еще раз.")







# Работа со сложным процентом

# Исполнитель команды /comp, поддерживающий работу данного отрезка кода, только в том случае, если команда введена
@dp.message_handler(commands=["comp"])
async def start_comp(message: types.Message, state: FSMContext):
    await MathState.COMP.set()
    menu_text = (
        f"Введите уравнение для нахождения сложного процента.\n"
        f"Вы можете нажать /restartcomp для перезапуска операции.\n"
        f"Не забудьте нажать команду /stopcomp для остановки операции.\n\n"
        f"Вводите уравнение в формате:\n"
        f"начальный капитал and процентная ставка and количество начислений процентов за год and количество лет\n"


    )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('/menu'))
    keyboard.add(types.KeyboardButton('/stopcomp'))
    keyboard.add(types.KeyboardButton('/restartcomp'))

    await message.answer(text=menu_text, reply_markup=keyboard)

# Обработчик команды /comp для остановки операции
@dp.message_handler(commands=["stopcomp"], state=MathState.COMP)
async def stop_comp(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Операция по нахождению сложного процента остановлена.")

# Обработчик команды /comp для перезапуска операции
@dp.message_handler(commands=["restartcomp"])
async def restart_comp(message: types.Message, state: FSMContext):
    await start_comp(message, state)

# Функция вычисления сложного процента
async def calculate_compound_interest(message, principal, rate, time, periods):
    try:
        # Преобразование процентной ставки в десятичную форму
        rate_decimal = rate

        # Вычисление сложного процента
        amount = principal * (1 + rate_decimal / 100) ** (periods * time)

        # Отправка ответа пользователю
        await message.reply(f"Сложный процент за {time} периодов составит: {amount:.2f}")
    except Exception as e:
        await message.reply(f"Произошла ошибка при расчете сложного процента. Попробуйте еще раз.")

# Обработчик сообщений для вычисления сложного процента
@dp.message_handler(state=MathState.COMP)
async def solve_compound_interest(message: types.Message, state: FSMContext):
    try:
        user_input = message.text.lower().replace(" ", "")

        # Извлекаем начальный капитал, процентную ставку, количество периодов и количество раз начисления процентов за год
        compound_interest_match = re.search(r'(\d+)\s*and\s*(\d+)\s*and\s*(\d+)\s*and\s*(\d+)', user_input)
        if compound_interest_match:
            principal, rate, time, periods = (
                int(compound_interest_match.group(1).strip()),
                int(compound_interest_match.group(2).strip()),
                int(compound_interest_match.group(3).strip()),
                int(compound_interest_match.group(4).strip())
            )

            await calculate_compound_interest(message, principal, rate, time, periods)
        else:
            await message.reply("Не удалось извлечь данные для расчета сложного процента.")
    except Exception as e:
        await message.reply(f"Произошла ошибка при обработке задачи. Попробуйте еще раз.")










executor.start_polling(dp)


