import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import sympy as sp
from sympy import symbols, Eq, integrate, diff, solve, sin, cos, tan, log, exp, sqrt
import re

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot tokenınızı buraya girin
TOKEN = "8087647718:AAHZndbMVmUqdxZ2ybET47c5BgPZxhUOBLA"

# Dil desteği - Çeviriler
translations = {
    'en': {
        'welcome': "Welcome to the Scientific Calculator Bot! Please choose a language:",
        'select_operation': "Please select an operation:",
        'basic_operations': "Basic Operations",
        'trigonometry': "Trigonometry",
        'logarithms': "Logarithms/Exponentials",
        'calculus': "Calculus",
        'graphing': "Graphing",
        'equation_solving': "Equation Solving",
        'symbolic_math': "Symbolic Math",
        'main_menu': "Main Menu",
        'back': "Back",
        'invalid_input': "Invalid input! Please enter numbers in the correct format.",
        'result': "Result: {}",
        'enter_numbers': "Please enter the numbers separated by spaces (example: 5 3 2)",
        'enter_angle': "Please enter the angle value in degrees:",
        'enter_value': "Please enter the value:",
        'enter_base_number': "Please enter the base and number separated by space (example: 2 8):",
        'enter_base_exponent': "Please enter the base and exponent separated by space (example: 3 4):",
        'enter_function_range': "Please enter the x range as start end step (example: -10 10 0.1):",
        'enter_custom_function': "Please enter the function in Python syntax (use x variable, example: np.sin(x) + x**2):",
        'enter_integral': "Please enter the function, lower bound, upper bound, variable (example: x**2,0,1,x):",
        'enter_indefinite_integral': "Please enter the function and variable (example: sin(x),x):",
        'enter_derivative': "Please enter the function and variable (example: x**2,x):",
        'enter_equation': "Please enter the equation and variable (example: x**2 - 4 = 0,x):",
        'enter_symbolic': "Please enter the symbolic expression to evaluate:",
        'enter_symbolic_equation': "Please enter the equation to solve (example: x**2 - 4 = 0):",
        'enter_symbolic_derivative': "Please enter the expression and variable (example: x**2 + sin(x), x):",
        'enter_symbolic_integral': "Please enter the expression and variable (example: x**2, x):",
        'enter_simplify': "Please enter the expression to simplify:",
        'no_solution': "No solution found for the equation.",
        'solutions': "Solutions:\n{}",
        'graph_title': "Graph: {}",
        'language_set': "Language has been set to: {}",
        'select_language': "Please select your language:"
    },
    'es': {
        'welcome': "¡Bienvenido al Bot Calculadora Científica! Por favor elige un idioma:",
        'select_operation': "Por favor selecciona una operación:",
        'basic_operations': "Operaciones Básicas",
        'trigonometry': "Trigonometría",
        'logarithms': "Logaritmos/Exponenciales",
        'calculus': "Cálculo",
        'graphing': "Graficación",
        'equation_solving': "Resolución de Ecuaciones",
        'symbolic_math': "Matemática Simbólica",
        'main_menu': "Menú Principal",
        'back': "Atrás",
        'invalid_input': "¡Entrada inválida! Por favor ingresa números en el formato correcto.",
        'result': "Resultado: {}",
        'enter_numbers': "Por favor ingresa los números separados por espacios (ejemplo: 5 3 2)",
        'enter_angle': "Por favor ingresa el valor del ángulo en grados:",
        'enter_value': "Por favor ingresa el valor:",
        'enter_base_number': "Por favor ingresa la base y el número separados por espacio (ejemplo: 2 8):",
        'enter_base_exponent': "Por favor ingresa la base y el exponente separados por espacio (ejemplo: 3 4):",
        'enter_function_range': "Por favor ingresa el rango de x como inicio fin paso (ejemplo: -10 10 0.1):",
        'enter_custom_function': "Por favor ingresa la función en sintaxis Python (usa la variable x, ejemplo: np.sin(x) + x**2):",
        'enter_integral': "Por favor ingresa la función, límite inferior, límite superior, variable (ejemplo: x**2,0,1,x):",
        'enter_indefinite_integral': "Por favor ingresa la función y variable (ejemplo: sin(x),x):",
        'enter_derivative': "Por favor ingresa la función y variable (ejemplo: x**2,x):",
        'enter_equation': "Por favor ingresa la ecuación y variable (ejemplo: x**2 - 4 = 0,x):",
        'enter_symbolic': "Por favor ingresa la expresión simbólica a evaluar:",
        'enter_symbolic_equation': "Por favor ingresa la ecuación a resolver (ejemplo: x**2 - 4 = 0):",
        'enter_symbolic_derivative': "Por favor ingresa la expresión y variable (ejemplo: x**2 + sin(x), x):",
        'enter_symbolic_integral': "Por favor ingresa la expresión y variable (ejemplo: x**2, x):",
        'enter_simplify': "Por favor ingresa la expresión a simplificar:",
        'no_solution': "No se encontró solución para la ecuación.",
        'solutions': "Soluciones:\n{}",
        'graph_title': "Gráfico: {}",
        'language_set': "El idioma ha sido establecido a: {}",
        'select_language': "Por favor selecciona tu idioma:"
    },
    'ar': {
        'welcome': "مرحبًا بكم في بوت الآلة الحاسبة العلمية! يرجى اختيار اللغة:",
        'select_operation': "الرجاء اختيار العملية:",
        'basic_operations': "العمليات الأساسية",
        'trigonometry': "علم المثلثات",
        'logarithms': "اللوغاريتمات/الأسس",
        'calculus': "حساب التفاضل والتكامل",
        'graphing': "الرسم البياني",
        'equation_solving': "حل المعادلات",
        'symbolic_math': "الرياضيات الرمزية",
        'main_menu': "القائمة الرئيسية",
        'back': "رجوع",
        'invalid_input': "إدخال غير صحيح! يرجى إدخال الأرقام بالتنسيق الصحيح.",
        'result': "النتيجة: {}",
        'enter_numbers': "الرجاء إدخال الأرقام مفصولة بمسافات (مثال: 5 3 2)",
        'enter_angle': "الرجاء إدخال قيمة الزاوية بالدرجات:",
        'enter_value': "الرجاء إدخال القيمة:",
        'enter_base_number': "الرجاء إدخال الأساس والرقم مفصولين بمسافة (مثال: 2 8):",
        'enter_base_exponent': "الرجاء إدخال الأساس والأس مفصولين بمسافة (مثال: 3 4):",
        'enter_function_range': "الرجاء إدخال نطاق x كبداية نهاية خطوة (مثال: -10 10 0.1):",
        'enter_custom_function': "الرجاء إدخال الدالة بصيغة بايثون (استخدم المتغير x، مثال: np.sin(x) + x**2):",
        'enter_integral': "الرجاء إدخال الدالة، الحد الأدنى، الحد الأعلى، المتغير (مثال: x**2,0,1,x):",
        'enter_indefinite_integral': "الرجاء إدخال الدالة والمتغير (مثال: sin(x),x):",
        'enter_derivative': "الرجاء إدخال الدالة والمتغير (مثال: x**2,x):",
        'enter_equation': "الرجاء إدخال المعادلة والمتغير (مثال: x**2 - 4 = 0,x):",
        'enter_symbolic': "الرجاء إدخال التعبير الرمزي لتقييمه:",
        'enter_symbolic_equation': "الرجاء إدخال المعادلة لحلها (مثال: x**2 - 4 = 0):",
        'enter_symbolic_derivative': "الرجاء إدخال التعبير والمتغير (مثال: x**2 + sin(x), x):",
        'enter_symbolic_integral': "الرجاء إدخال التعبير والمتغير (مثال: x**2, x):",
        'enter_simplify': "الرجاء إدخال التعبير لتبسيطه:",
        'no_solution': "لم يتم العثور على حل للمعادلة.",
        'solutions': "الحلول:\n{}",
        'graph_title': "الرسم البياني: {}",
        'language_set': "تم تعيين اللغة إلى: {}",
        'select_language': "الرجاء اختيار لغتك:"
    },
    'ru': {
        'welcome': "Добро пожаловать в бот научного калькулятора! Пожалуйста, выберите язык:",
        'select_operation': "Пожалуйста, выберите операцию:",
        'basic_operations': "Основные операции",
        'trigonometry': "Тригонометрия",
        'logarithms': "Логарифмы/Экспоненты",
        'calculus': "Математический анализ",
        'graphing': "Графики",
        'equation_solving': "Решение уравнений",
        'symbolic_math': "Символьная математика",
        'main_menu': "Главное меню",
        'back': "Назад",
        'invalid_input': "Неверный ввод! Пожалуйста, введите числа в правильном формате.",
        'result': "Результат: {}",
        'enter_numbers': "Пожалуйста, введите числа через пробел (пример: 5 3 2)",
        'enter_angle': "Пожалуйста, введите значение угла в градусах:",
        'enter_value': "Пожалуйста, введите значение:",
        'enter_base_number': "Пожалуйста, введите основание и число через пробел (пример: 2 8):",
        'enter_base_exponent': "Пожалуйста, введите основание и показатель степени через пробел (пример: 3 4):",
        'enter_function_range': "Пожалуйста, введите диапазон x как начало конец шаг (пример: -10 10 0.1):",
        'enter_custom_function': "Пожалуйста, введите функцию в синтаксисе Python (используйте переменную x, пример: np.sin(x) + x**2):",
        'enter_integral': "Пожалуйста, введите функцию, нижний предел, верхний предел, переменную (пример: x**2,0,1,x):",
        'enter_indefinite_integral': "Пожалуйста, введите функцию и переменную (пример: sin(x),x):",
        'enter_derivative': "Пожалуйста, введите функцию и переменную (пример: x**2,x):",
        'enter_equation': "Пожалуйста, введите уравнение и переменную (пример: x**2 - 4 = 0,x):",
        'enter_symbolic': "Пожалуйста, введите символьное выражение для вычисления:",
        'enter_symbolic_equation': "Пожалуйста, введите уравнение для решения (пример: x**2 - 4 = 0):",
        'enter_symbolic_derivative': "Пожалуйста, введите выражение и переменную (пример: x**2 + sin(x), x):",
        'enter_symbolic_integral': "Пожалуйста, введите выражение и переменную (пример: x**2, x):",
        'enter_simplify': "Пожалуйста, введите выражение для упрощения:",
        'no_solution': "Решение уравнения не найдено.",
        'solutions': "Решения:\n{}",
        'graph_title': "График: {}",
        'language_set': "Язык установлен: {}",
        'select_language': "Пожалуйста, выберите ваш язык:"
    },
    'zh': {
        'welcome': "欢迎使用科学计算器机器人！请选择语言：",
        'select_operation': "请选择操作：",
        'basic_operations': "基本运算",
        'trigonometry': "三角函数",
        'logarithms': "对数/指数",
        'calculus': "微积分",
        'graphing': "绘图",
        'equation_solving': "解方程",
        'symbolic_math': "符号数学",
        'main_menu': "主菜单",
        'back': "返回",
        'invalid_input': "输入无效！请以正确的格式输入数字。",
        'result': "结果：{}",
        'enter_numbers': "请输入以空格分隔的数字（示例：5 3 2）",
        'enter_angle': "请输入角度值（度）：",
        'enter_value': "请输入值：",
        'enter_base_number': "请输入基数和数字，以空格分隔（示例：2 8）：",
        'enter_base_exponent': "请输入基数和指数，以空格分隔（示例：3 4）：",
        'enter_function_range': "请输入x范围作为开始结束步骤（示例：-10 10 0.1）：",
        'enter_custom_function': "请输入Python语法中的函数（使用x变量，示例：np.sin(x) + x**2）：",
        'enter_integral': "请输入函数、下限、上限、变量（示例：x**2,0,1,x）：",
        'enter_indefinite_integral': "请输入函数和变量（示例：sin(x),x）：",
        'enter_derivative': "请输入函数和变量（示例：x**2,x）：",
        'enter_equation': "请输入方程和变量（示例：x**2 - 4 = 0,x）：",
        'enter_symbolic': "请输入要评估的符号表达式：",
        'enter_symbolic_equation': "请输入要解的方程（示例：x**2 - 4 = 0）：",
        'enter_symbolic_derivative': "请输入表达式和变量（示例：x**2 + sin(x), x）：",
        'enter_symbolic_integral': "请输入表达式和变量（示例：x**2, x）：",
        'enter_simplify': "请输入要简化的表达式：",
        'no_solution': "未找到方程的解。",
        'solutions': "解决方案：\n{}",
        'graph_title': "图表：{}",
        'language_set': "语言已设置为：{}",
        'select_language': "请选择您的语言："
    },
    'fr': {
        'welcome': "Bienvenue sur le bot Calculatrice Scientifique ! Veuillez choisir une langue :",
        'select_operation': "Veuillez sélectionner une opération :",
        'basic_operations': "Opérations de base",
        'trigonometry': "Trigonométrie",
        'logarithms': "Logarithmes/Exponentielles",
        'calculus': "Calcul infinitésimal",
        'graphing': "Graphiques",
        'equation_solving': "Résolution d'équations",
        'symbolic_math': "Mathématiques symboliques",
        'main_menu': "Menu principal",
        'back': "Retour",
        'invalid_input': "Entrée invalide ! Veuillez entrer des nombres dans le bon format.",
        'result': "Résultat : {}",
        'enter_numbers': "Veuillez entrer les nombres séparés par des espaces (exemple : 5 3 2)",
        'enter_angle': "Veuillez entrer la valeur de l'angle en degrés :",
        'enter_value': "Veuillez entrer la valeur :",
        'enter_base_number': "Veuillez entrer la base et le nombre séparés par un espace (exemple : 2 8) :",
        'enter_base_exponent': "Veuillez entrer la base et l'exposant séparés par un espace (exemple : 3 4) :",
        'enter_function_range': "Veuillez entrer la plage x comme début fin pas (exemple : -10 10 0.1) :",
        'enter_custom_function': "Veuillez entrer la fonction en syntaxe Python (utilisez la variable x, exemple : np.sin(x) + x**2) :",
        'enter_integral': "Veuillez entrer la fonction, borne inférieure, borne supérieure, variable (exemple : x**2,0,1,x) :",
        'enter_indefinite_integral': "Veuillez entrer la fonction et la variable (exemple : sin(x),x) :",
        'enter_derivative': "Veuillez entrer la fonction et la variable (exemple : x**2,x) :",
        'enter_equation': "Veuillez entrer l'équation et la variable (exemple : x**2 - 4 = 0,x) :",
        'enter_symbolic': "Veuillez entrer l'expression symbolique à évaluer :",
        'enter_symbolic_equation': "Veuillez entrer l'équation à résoudre (exemple : x**2 - 4 = 0) :",
        'enter_symbolic_derivative': "Veuillez entrer l'expression et la variable (exemple : x**2 + sin(x), x) :",
        'enter_symbolic_integral': "Veuillez entrer l'expression et la variable (exemple : x**2, x) :",
        'enter_simplify': "Veuillez entrer l'expression à simplifier :",
        'no_solution': "Aucune solution trouvée pour l'équation.",
        'solutions': "Solutions :\n{}",
        'graph_title': "Graphique : {}",
        'language_set': "La langue a été définie sur : {}",
        'select_language': "Veuillez sélectionner votre langue :"
    },
    'tr': {
        'welcome': "Bilimsel Hesap Makinesi Botuna Hoş Geldiniz! Lütfen bir dil seçin:",
        'select_operation': "Lütfen bir işlem seçin:",
        'basic_operations': "Temel İşlemler",
        'trigonometry': "Trigonometri",
        'logarithms': "Logaritma/Üstel",
        'calculus': "Kalkülüs",
        'graphing': "Grafik Çizme",
        'equation_solving': "Denklem Çözme",
        'symbolic_math': "Sembolik Matematik",
        'main_menu': "Ana Menü",
        'back': "Geri",
        'invalid_input': "Geçersiz giriş! Lütfen doğru formatta sayı girin.",
        'result': "Sonuç: {}",
        'enter_numbers': "Lütfen işlem yapmak istediğiniz sayıları boşlukla ayırarak yazın (örnek: 5 3 2)",
        'enter_angle': "Lütfen hesaplamak istediğiniz açı değerini derece cinsinden yazın:",
        'enter_value': "Lütfen hesaplamak istediğiniz değeri yazın:",
        'enter_base_number': "Lütfen taban ve sayıyı boşlukla ayırarak yazın (örnek: 2 8):",
        'enter_base_exponent': "Lütfen taban ve üssü boşlukla ayırarak yazın (örnek: 3 4):",
        'enter_function_range': "Lütfen x aralığını başlangıç bitiş adım olarak yazın (örnek: -10 10 0.1):",
        'enter_custom_function': "Lütfen çizmek istediğiniz fonksiyonu Python sözdizimiyle yazın (x değişkenini kullanın, örnek: np.sin(x) + x**2):",
        'enter_integral': "Lütfen integralini almak istediğiniz fonksiyonu ve sınırları şu formatta girin:\nfonksiyon,alt_sınır,üst_sınır,değişken\nÖrnek: x**2,0,1,x",
        'enter_indefinite_integral': "Lütfen integralini almak istediğiniz fonksiyonu ve değişkeni şu formatta girin:\nfonksiyon,değişken\nÖrnek: sin(x),x",
        'enter_derivative': "Lütfen türevini almak istediğiniz fonksiyonu ve değişkeni şu formatta girin:\nfonksiyon,değişken\nÖrnek: x**2,x",
        'enter_equation': "Lütfen çözmek istediğiniz denklemi şu formatta girin:\ndenklem,değişken\nÖrnek: x**2 - 4 = 0,x",
        'enter_symbolic': "Lütfen hesaplamak istediğiniz sembolik ifadeyi yazın (x gibi değişkenler kullanabilirsiniz):",
        'enter_symbolic_equation': "Lütfen çözmek istediğiniz denklemi yazın (örnek: x**2 - 4 = 0):",
        'enter_symbolic_derivative': "Lütfen türevini almak istediğiniz ifadeyi ve değişkeni yazın (örnek: x**2 + sin(x), x):",
        'enter_symbolic_integral': "Lütfen integralini almak istediğiniz ifadeyi ve değişkeni yazın (örnek: x**2, x):",
        'enter_simplify': "Lütfen sadeleştirmek istediğiniz ifadeyi yazın:",
        'no_solution': "Denklemin çözümü bulunamadı.",
        'solutions': "Çözümler:\n{}",
        'graph_title': "Grafik: {}",
        'language_set': "Dil şu şekilde ayarlandı: {}",
        'select_language': "Lütfen dilinizi seçin:"
    },
    'ku': {
        'welcome': "Bi xêr hatî Botê Hesabkera Zanistî! Ji kerema xwe zimanek hilbijêrin:",
        'select_operation': "Ji kerema xwe operasyonek hilbijêrin:",
        'basic_operations': "Operasyonên Bingehîn",
        'trigonometry': "Trîgonometrî",
        'logarithms': "Logarîtma/Exponential",
        'calculus': "Hesab",
        'graphing': "Xêzkirin",
        'equation_solving': "Çareserkirina Hevkêşeyan",
        'symbolic_math': "Matematîka Sembolîk",
        'main_menu': "Menuya Sereke",
        'back': "Paşve",
        'invalid_input': "Têketina nederbasdar! Ji kerema xwe bi formata rast jimareyan binivîse.",
        'result': "Encam: {}",
        'enter_numbers': "Ji kerema xwe jimareyan bi cihê vala veqetînin (mînak: 5 3 2)",
        'enter_angle': "Ji kerema xwe nirxa goşeyê bi dereceyê binivîse:",
        'enter_value': "Ji kerema xwe nirxê binivîse:",
        'enter_base_number': "Ji kerema xwe bingeh û jimareyê bi cihê vala veqetînin (mînak: 2 8):",
        'enter_base_exponent': "Ji kerema xwe bingeh û qasê bi cihê vala veqetînin (mînak: 3 4):",
        'enter_function_range': "Ji kerema xwe rêza x wekî destpêk qedem qedem binivîse (mînak: -10 10 0.1):",
        'enter_custom_function': "Ji kerema xwe fonksiyonê bi sintaksa Python binivîse (guherbara x bikar bînin, mînak: np.sin(x) + x**2):",
        'enter_integral': "Ji kerema xwe fonksiyonê, sînorên jêrîn û jorîn, guherbar binivîse (mînak: x**2,0,1,x):",
        'enter_indefinite_integral': "Ji kerema xwe fonksiyon û guherbar binivîse (mînak: sin(x),x):",
        'enter_derivative': "Ji kerema xwe fonksiyon û guherbar binivîse (mînak: x**2,x):",
        'enter_equation': "Ji kerema xwe hevkêşeyê û guherbar binivîse (mînak: x**2 - 4 = 0,x):",
        'enter_symbolic': "Ji kerema xwe vegotina sembolîk ji bo nirxandinê binivîse:",
        'enter_symbolic_equation': "Ji kerema xwe hevkêşeya çareserkirî binivîse (mînak: x**2 - 4 = 0):",
        'enter_symbolic_derivative': "Ji kerema xwe vegotin û guherbar binivîse (mînak: x**2 + sin(x), x):",
        'enter_symbolic_integral': "Ji kerema xwe vegotin û guherbar binivîse (mînak: x**2, x):",
        'enter_simplify': "Ji kerema xwe vegotina hêsankirî binivîse:",
        'no_solution': "Ji bo hevkêşeyê çareserî nehat dîtin.",
        'solutions': "Çareserî:\n{}",
        'graph_title': "Grafîk: {}",
        'language_set': "Ziman hate danîn: {}",
        'select_language': "Ji kerema xwe zimanê xwe hilbijêrin:"
    }
}

# Dil seçenekleri
language_options = [
    [InlineKeyboardButton("English", callback_data='lang_en')],
    [InlineKeyboardButton("Español", callback_data='lang_es')],
    [InlineKeyboardButton("العربية", callback_data='lang_ar')],
    [InlineKeyboardButton("Русский", callback_data='lang_ru')],
    [InlineKeyboardButton("中文", callback_data='lang_zh')],
    [InlineKeyboardButton("Français", callback_data='lang_fr')],
    [InlineKeyboardButton("Türkçe", callback_data='lang_tr')],
    [InlineKeyboardButton("Kurdî", callback_data='lang_ku')]
]

def get_user_language(user_data):
    return user_data.get('language', 'en')

def tr(user_data, key, *args):
    lang = get_user_language(user_data)
    return translations[lang][key].format(*args) if args else translations[lang][key]

# Ana menü butonları
def main_menu_keyboard(user_data):
    keyboard = [
        [InlineKeyboardButton(tr(user_data, 'basic_operations'), callback_data='temel')],
        [InlineKeyboardButton(tr(user_data, 'trigonometry'), callback_data='trigonometri')],
        [InlineKeyboardButton(tr(user_data, 'logarithms'), callback_data='logaritma')],
        [InlineKeyboardButton(tr(user_data, 'calculus'), callback_data='calculus')],
        [InlineKeyboardButton(tr(user_data, 'graphing'), callback_data='grafik')],
        [InlineKeyboardButton(tr(user_data, 'equation_solving'), callback_data='denklem')],
        [InlineKeyboardButton(tr(user_data, 'symbolic_math'), callback_data='sembolik')],
        [InlineKeyboardButton(tr(user_data, 'select_language'), callback_data='change_language')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Temel işlemler menüsü
def temel_islemler_keyboard(user_data):
    keyboard = [
        [InlineKeyboardButton("+ " + tr(user_data, 'basic_operations'), callback_data='toplama'),
         InlineKeyboardButton("- " + tr(user_data, 'basic_operations'), callback_data='cikarma')],
        [InlineKeyboardButton("× " + tr(user_data, 'basic_operations'), callback_data='carpma'),
         InlineKeyboardButton("÷ " + tr(user_data, 'basic_operations'), callback_data='bolme')],
        [InlineKeyboardButton("xʸ", callback_data='us'),
         InlineKeyboardButton("√x", callback_data='karekok')],
        [InlineKeyboardButton("x!", callback_data='faktoriyel'),
         InlineKeyboardButton("|x|", callback_data='mutlak')],
        [InlineKeyboardButton(tr(user_data, 'back'), callback_data='main')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Trigonometri menüsü
def trigonometri_keyboard(user_data):
    keyboard = [
        [InlineKeyboardButton("sin", callback_data='sin'),
         InlineKeyboardButton("cos", callback_data='cos')],
        [InlineKeyboardButton("tan", callback_data='tan'),
         InlineKeyboardButton("cot", callback_data='cot')],
        [InlineKeyboardButton("arcsin", callback_data='arcsin'),
         InlineKeyboardButton("arccos", callback_data='arccos')],
        [InlineKeyboardButton("arctan", callback_data='arctan'),
         InlineKeyboardButton("arccot", callback_data='arccot')],
        [InlineKeyboardButton("° → rad", callback_data='deg2rad'),
         InlineKeyboardButton("rad → °", callback_data='rad2deg')],
        [InlineKeyboardButton(tr(user_data, 'back'), callback_data='main')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Logaritma/Üstel menüsü
def logaritma_keyboard(user_data):
    keyboard = [
        [InlineKeyboardButton("log₁₀", callback_data='log10'),
         InlineKeyboardButton("ln", callback_data='ln')],
        [InlineKeyboardButton("logₐb", callback_data='logx')],
        [InlineKeyboardButton("eˣ", callback_data='exp'),
         InlineKeyboardButton("2ˣ", callback_data='exp2')],
        [InlineKeyboardButton("10ˣ", callback_data='exp10'),
         InlineKeyboardButton("aˣ", callback_data='expa')],
        [InlineKeyboardButton(tr(user_data, 'back'), callback_data='main')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Kalkülüs menüsü
def calculus_keyboard(user_data):
    keyboard = [
        [InlineKeyboardButton("∫ f(x)dx [a,b]", callback_data='belirli_integral')],
        [InlineKeyboardButton("∫ f(x)dx", callback_data='belirsiz_integral')],
        [InlineKeyboardButton("d/dx", callback_data='turev_alma')],
        [InlineKeyboardButton("f(x)=0", callback_data='denklem_cozme')],
        [InlineKeyboardButton(tr(user_data, 'back'), callback_data='main')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Grafik menüsü
def grafik_keyboard(user_data):
    keyboard = [
        [InlineKeyboardButton("y = x", callback_data='grafik_linear')],
        [InlineKeyboardButton("y = x²", callback_data='grafik_quadratic')],
        [InlineKeyboardButton("y = sin(x)", callback_data='grafik_trig')],
        [InlineKeyboardButton("y = eˣ", callback_data='grafik_exp')],
        [InlineKeyboardButton("y = ln(x)", callback_data='grafik_log')],
        [InlineKeyboardButton(tr(user_data, 'enter_custom_function'), callback_data='grafik_custom')],
        [InlineKeyboardButton(tr(user_data, 'back'), callback_data='main')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Sembolik matematik menüsü
def sembolik_keyboard(user_data):
    keyboard = [
        [InlineKeyboardButton(tr(user_data, 'enter_symbolic'), callback_data='sembolik_hesap')],
        [InlineKeyboardButton(tr(user_data, 'enter_symbolic_equation'), callback_data='sembolik_denklem')],
        [InlineKeyboardButton(tr(user_data, 'enter_symbolic_derivative'), callback_data='sembolik_turev')],
        [InlineKeyboardButton(tr(user_data, 'enter_symbolic_integral'), callback_data='sembolik_integral')],
        [InlineKeyboardButton(tr(user_data, 'enter_simplify'), callback_data='sembolik_sadelestir')],
        [InlineKeyboardButton(tr(user_data, 'back'), callback_data='main')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def send_plot(update: Update, user_data, x, y, title="", xlabel="x", ylabel="y"):
    plt.figure()
    plt.plot(x, y)
    plt.title(title if title else tr(user_data, 'graph_title', str(y)))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    buf.seek(0)
    
    await update.message.reply_photo(photo=buf, caption=title if title else tr(user_data, 'graph_title', str(y)))
    plt.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Kullanıcı verilerini başlat
    if 'language' not in context.user_data:
        context.user_data['language'] = 'en'
    
    # Dil seçim ekranını göster
    await update.message.reply_text(
        tr(context.user_data, 'welcome'),
        reply_markup=InlineKeyboardMarkup(language_options)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_data = context.user_data

    # Dil değiştirme işlemi
    if query.data.startswith('lang_'):
        lang = query.data.split('_')[1]
        user_data['language'] = lang
        await query.edit_message_text(
            text=tr(user_data, 'language_set', query.data.split('_')[1]),
            reply_markup=main_menu_keyboard(user_data)
        )
        return
    
    if query.data == 'main':
        await query.edit_message_text(
            text=tr(user_data, 'select_operation'),
            reply_markup=main_menu_keyboard(user_data)
        )
    elif query.data == 'change_language':
        await query.edit_message_text(
            text=tr(user_data, 'select_language'),
            reply_markup=InlineKeyboardMarkup(language_options)
        )
    elif query.data == 'temel':
        await query.edit_message_text(
            text=tr(user_data, 'select_operation'),
            reply_markup=temel_islemler_keyboard(user_data)
        )
    elif query.data == 'trigonometri':
        await query.edit_message_text(
            text=tr(user_data, 'select_operation'),
            reply_markup=trigonometri_keyboard(user_data)
        )
    elif query.data == 'logaritma':
        await query.edit_message_text(
            text=tr(user_data, 'select_operation'),
            reply_markup=logaritma_keyboard(user_data)
        )
    elif query.data == 'calculus':
        await query.edit_message_text(
            text=tr(user_data, 'select_operation'),
            reply_markup=calculus_keyboard(user_data)
        )
    elif query.data == 'grafik':
        await query.edit_message_text(
            text=tr(user_data, 'select_operation'),
            reply_markup=grafik_keyboard(user_data)
        )
    elif query.data == 'sembolik':
        await query.edit_message_text(
            text=tr(user_data, 'select_operation'),
            reply_markup=sembolik_keyboard(user_data)
        )
    elif query.data in ['toplama', 'cikarma', 'carpma', 'bolme']:
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_numbers'))
    elif query.data in ['us', 'karekok', 'faktoriyel', 'mutlak']:
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_value'))
    elif query.data in ['sin', 'cos', 'tan', 'cot', 'arcsin', 'arccos', 'arctan', 'arccot', 'deg2rad', 'rad2deg']:
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_angle'))
    elif query.data in ['log10', 'ln', 'exp', 'exp2', 'exp10']:
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_value'))
    elif query.data == 'logx':
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_base_number'))
    elif query.data == 'expa':
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_base_exponent'))
    elif query.data.startswith('grafik_'):
        user_data['operation'] = query.data
        if query.data == 'grafik_custom':
            await query.edit_message_text(text=tr(user_data, 'enter_custom_function'))
        else:
            await query.edit_message_text(text=tr(user_data, 'enter_function_range'))
    elif query.data == 'belirli_integral':
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_integral'))
    elif query.data == 'belirsiz_integral':
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_indefinite_integral'))
    elif query.data == 'turev_alma':
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_derivative'))
    elif query.data == 'denklem_cozme':
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_equation'))
    elif query.data == 'sembolik_hesap':
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_symbolic'))
    elif query.data == 'sembolik_denklem':
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_symbolic_equation'))
    elif query.data == 'sembolik_turev':
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_symbolic_derivative'))
    elif query.data == 'sembolik_integral':
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_symbolic_integral'))
    elif query.data == 'sembolik_sadelestir':
        user_data['operation'] = query.data
        await query.edit_message_text(text=tr(user_data, 'enter_simplify'))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_data = context.user_data
    if 'operation' not in user_data:
        await update.message.reply_text(tr(user_data, 'select_operation'), reply_markup=main_menu_keyboard(user_data))
        return

    operation = user_data['operation']
    text = update.message.text

    try:
        if operation in ['toplama', 'cikarma', 'carpma', 'bolme']:
            numbers = list(map(float, text.split()))
            if operation == 'toplama':
                result = sum(numbers)
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
            elif operation == 'cikarma':
                result = numbers[0] - sum(numbers[1:])
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
            elif operation == 'carpma':
                result = 1
                for num in numbers:
                    result *= num
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
            elif operation == 'bolme':
                result = numbers[0]
                for num in numbers[1:]:
                    result /= num
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
        
        elif operation == 'us':
            numbers = list(map(float, text.split()))
            result = numbers[0] ** numbers[1]
            await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
        
        elif operation == 'karekok':
            num = float(text)
            result = np.sqrt(num)
            await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
        
        elif operation == 'faktoriyel':
            num = int(float(text))
            result = np.math.factorial(num)
            await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
        
        elif operation == 'mutlak':
            num = float(text)
            result = abs(num)
            await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
        
        elif operation in ['sin', 'cos', 'tan', 'cot']:
            angle = float(text)
            rad = np.radians(angle)
            if operation == 'sin':
                result = np.sin(rad)
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
            elif operation == 'cos':
                result = np.cos(rad)
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
            elif operation == 'tan':
                result = np.tan(rad)
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
            elif operation == 'cot':
                result = 1 / np.tan(rad)
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
        
        elif operation in ['arcsin', 'arccos', 'arctan', 'arccot']:
            value = float(text)
            if operation == 'arcsin':
                result = np.degrees(np.arcsin(value))
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
            elif operation == 'arccos':
                result = np.degrees(np.arccos(value))
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
            elif operation == 'arctan':
                result = np.degrees(np.arctan(value))
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
            elif operation == 'arccot':
                result = np.degrees(np.arctan(1/value))
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
        
        elif operation == 'deg2rad':
            deg = float(text)
            rad = np.radians(deg)
            await update.message.reply_text(tr(user_data, 'result', rad), reply_markup=main_menu_keyboard(user_data))
        
        elif operation == 'rad2deg':
            rad = float(text)
            deg = np.degrees(rad)
            await update.message.reply_text(tr(user_data, 'result', deg), reply_markup=main_menu_keyboard(user_data))
        
        elif operation in ['log10', 'ln', 'exp', 'exp2', 'exp10']:
            num = float(text)
            if operation == 'log10':
                result = np.log10(num)
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
            elif operation == 'ln':
                result = np.log(num)
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
            elif operation == 'exp':
                result = np.exp(num)
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
            elif operation == 'exp2':
                result = 2 ** num
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
            elif operation == 'exp10':
                result = 10 ** num
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
        
        elif operation == 'logx':
            base, num = map(float, text.split())
            result = np.log(num) / np.log(base)
            await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
        
        elif operation == 'expa':
            base, exponent = map(float, text.split())
            result = base ** exponent
            await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
        
        elif operation.startswith('grafik_'):
            if operation == 'grafik_custom':
                func_str = text
                x_vals = np.linspace(-10, 10, 400)
                try:
                    y_vals = eval(func_str, {'np': np, 'x': x_vals})
                    await send_plot(update, user_data, x_vals, y_vals, f"y = {func_str}")
                except Exception as e:
                    await update.message.reply_text(f"{tr(user_data, 'invalid_input')} {str(e)}")
            else:
                start, end, step = map(float, text.split())
                x_vals = np.arange(start, end, step)
                if operation == 'grafik_linear':
                    y_vals = x_vals
                    await send_plot(update, user_data, x_vals, y_vals, "y = x")
                elif operation == 'grafik_quadratic':
                    y_vals = x_vals**2
                    await send_plot(update, user_data, x_vals, y_vals, "y = x²")
                elif operation == 'grafik_trig':
                    y_vals = np.sin(x_vals)
                    await send_plot(update, user_data, x_vals, y_vals, "y = sin(x)")
                elif operation == 'grafik_exp':
                    y_vals = np.exp(x_vals)
                    await send_plot(update, user_data, x_vals, y_vals, "y = eˣ")
                elif operation == 'grafik_log':
                    y_vals = np.log(np.abs(x_vals) + 1e-10)
                    await send_plot(update, user_data, x_vals, y_vals, "y = ln(x)")
        
        elif operation in ['belirli_integral', 'belirsiz_integral', 'turev_alma', 'denklem_cozme']:
            if operation == 'belirli_integral':
                parts = [p.strip() for p in text.split(',')]
                if len(parts) != 4:
                    await update.message.reply_text(tr(user_data, 'invalid_input'))
                    return
                
                expr_str, a_str, b_str, var_str = parts
                x = symbols(var_str)
                expr = sp.sympify(expr_str)
                integral = sp.integrate(expr, (x, float(a_str), float(b_str)))
                await update.message.reply_text(f"∫({expr_str})dx from {a_str} to {b_str} = {integral.evalf()}", reply_markup=main_menu_keyboard(user_data))
            
            elif operation == 'belirsiz_integral':
                parts = [p.strip() for p in text.split(',')]
                if len(parts) != 2:
                    await update.message.reply_text(tr(user_data, 'invalid_input'))
                    return
                
                expr_str, var_str = parts
                x = symbols(var_str)
                expr = sp.sympify(expr_str)
                integral = sp.integrate(expr, x)
                await update.message.reply_text(f"∫({expr_str})d{var_str} = {sp.pretty(integral)} + C", reply_markup=main_menu_keyboard(user_data))
            
            elif operation == 'turev_alma':
                parts = [p.strip() for p in text.split(',')]
                if len(parts) != 2:
                    await update.message.reply_text(tr(user_data, 'invalid_input'))
                    return
                
                expr_str, var_str = parts
                x = symbols(var_str)
                expr = sp.sympify(expr_str)
                derivative = sp.diff(expr, x)
                await update.message.reply_text(f"d/d{var_str}({expr_str}) = {sp.pretty(derivative)}", reply_markup=main_menu_keyboard(user_data))
            
            elif operation == 'denklem_cozme':
                parts = [p.strip() for p in text.split(',')]
                if len(parts) != 2:
                    await update.message.reply_text(tr(user_data, 'invalid_input'))
                    return
                
                eq_str, var_str = parts
                x = symbols(var_str)
                
                if '=' in eq_str:
                    lhs, rhs = eq_str.split('=')
                    eq = Eq(sp.sympify(lhs), sp.sympify(rhs))
                else:
                    eq = Eq(sp.sympify(eq_str), 0)
                
                solutions = solve(eq, x)
                
                if not solutions:
                    await update.message.reply_text(tr(user_data, 'no_solution'), reply_markup=main_menu_keyboard(user_data))
                else:
                    solutions_str = "\n".join([f"{var_str} = {sp.pretty(sol)}" for sol in solutions])
                    await update.message.reply_text(tr(user_data, 'solutions', solutions_str), reply_markup=main_menu_keyboard(user_data))
        
        elif operation.startswith('sembolik_'):
            if operation == 'sembolik_hesap':
                expr = sp.sympify(text)
                result = expr.evalf()
                await update.message.reply_text(tr(user_data, 'result', result), reply_markup=main_menu_keyboard(user_data))
            
            elif operation == 'sembolik_denklem':
                if '=' in text:
                    lhs, rhs = text.split('=')
                    eq = Eq(sp.sympify(lhs), sp.sympify(rhs))
                else:
                    eq = Eq(sp.sympify(text), 0)
                
                solutions = solve(eq)
                
                if not solutions:
                    await update.message.reply_text(tr(user_data, 'no_solution'), reply_markup=main_menu_keyboard(user_data))
                else:
                    solutions_str = "\n".join([f"x = {sp.pretty(sol)}" for sol in solutions])
                    await update.message.reply_text(tr(user_data, 'solutions', solutions_str), reply_markup=main_menu_keyboard(user_data))
            
            elif operation == 'sembolik_turev':
                expr_str, var_str = [s.strip() for s in text.split(',')]
                x = sp.symbols(var_str)
                expr = sp.sympify(expr_str)
                derivative = sp.diff(expr, x)
                await update.message.reply_text(f"Derivative:\n{sp.pretty(derivative)}\n\nSimplified: {sp.pretty(sp.simplify(derivative))}", reply_markup=main_menu_keyboard(user_data))
            
            elif operation == 'sembolik_integral':
                expr_str, var_str = [s.strip() for s in text.split(',')]
                x = sp.symbols(var_str)
                expr = sp.sympify(expr_str)
                integral = sp.integrate(expr, x)
                await update.message.reply_text(f"Integral:\n{sp.pretty(integral)}\n\nSimplified: {sp.pretty(sp.simplify(integral))}", reply_markup=main_menu_keyboard(user_data))
            
            elif operation == 'sembolik_sadelestir':
                expr = sp.sympify(text)
                simplified = sp.simplify(expr)
                await update.message.reply_text(f"Simplified expression:\n{sp.pretty(simplified)}", reply_markup=main_menu_keyboard(user_data))
        
        user_data.pop('operation', None)
    
    except ValueError as ve:
        await update.message.reply_text(f"{tr(user_data, 'invalid_input')} {str(ve)}")
    except sp.SympifyError:
        await update.message.reply_text(tr(user_data, 'invalid_input'))
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()