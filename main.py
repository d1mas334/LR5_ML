import sys
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests
import pandas as pd


def parse_data():
    url = "http://www.pogodaiklimat.ru/history/27612.htm"  # url сайта
    headers = {  # задание заголовков для обхода защиты сайта
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,'
                  'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'uk,en-US;q=0.9,en;q=0.8,ru;q=0.7',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/89.0.4389.90 Safari/537.36'
    }
    response = requests.get(url, headers=headers)  # отправка запроса на сайт

    if not response.ok:  # проверка ответа сайта
        print("Нет доступа к сайту!")
        sys.exit(2)

    bs = BeautifulSoup(response.content, "lxml")  # преобразование кода сайта
    ind = bs.find('div', 'chronicle-table-left-column')  # выбор кода названий строк
    name_rows = []  # массив названий строк
    for elemInd in ind.find_all('td'):  # запись названий строк
        name_rows.append(elemInd.text)

    elements = bs.find('div', 'chronicle-table')  # выбор кода основной таблицы
    mas_table = []  # массив данных о температуре с названиями колонок
    for row in elements.find_all('tr'):  # поиск кодов строк
        mas_row = []  # массив элементов строки
        for atomElem in row.find_all('td'):  # поиск кодов столбцов
            mas_row.append(atomElem.text)  # запись значения элемента таблицы
        mas_table.append(mas_row)  # добавление строки в общий массив

    table_dict = dict()  # создание словаря из полученных данных
    for i in range(len(mas_table) - (2023 - 1821 + 1) - 1, len(mas_table) - 1):  # перебор строк
        for j in range(0, len(mas_table[i])):  # перебор столбцов
            if mas_table[i][j] == '999.9':  # проверка наличия данных
                mas_table[i][j] = str((float(mas_table[i - 1][j]) +
                                       float(mas_table[i + 1][j])) / 2.0)  # аппроксимация
        table_dict[name_rows[i]] = mas_table[i]  # запись строки в словарь

    # создание объекта с данными pandas.DataFrame из словаря:
    table_df = pd.DataFrame.from_dict(table_dict, orient='index', columns=mas_table[0])
    table_df.index.name = name_rows[0]  # задание названия колонки с индексами (годами)
    table_df = table_df.drop('за год', axis = 1)  # удаление ненужного столбца

    # запись объекта с данными DataFrame в таблицу Excel:
    table_df.to_excel("ML_LR5.xlsx", sheet_name='Погода в Москве по годам')
    return 0


def lr5():
    parse_data()  # парсинг данных с сайта
    read_file = pd.read_excel("ML_LR5.xlsx", index_col=0)  # чтение файла Excel
    read_file.to_csv("ML_LR5.csv", index=True, header=True)  # создание файла CSV на
    # основе данных из файла Excel
    read_csv = pd.DataFrame(pd.read_csv("ML_LR5.csv", index_col=0))  # чтение файла CSV
    print(read_csv)  # вывод объекта с данными DataFrame

    lineTypes = ['--', '-', '-.', ':']  # задание массива типов линий
    lineColours = ['b', 'g', 'r', 'm']  # задание массива цветов линий
    for i in range(0, 12, 3):  # построение графиков для средних месяцев каждого времени года
        plt.plot(read_csv.index, read_csv[read_csv.columns[i]],
                 lineTypes[i // 3], label=read_csv.columns[i], color=lineColours[i // 3])

    plt.title("График изменения средней температуры за месяц по годам")  # задание заголовка
    plt.xlabel("Год")  # название оси Ох
    plt.ylabel("Средняя температура")  # название оси Оу
    plt.legend()  # вывод легенды
    plt.show()  # показ графиков


def lr6():
    #parse_data()  # парсинг данных с сайта
    read_file = pd.read_excel("ML_LR5.xlsx", index_col=0)  # чтение файла Excel
    read_file.to_csv("ML_LR5.csv", index=True, header=True)  # создание файла CSV на
    # основе данных из файла Excel
    read_csv = pd.DataFrame(pd.read_csv("ML_LR5.csv", index_col=0))  # чтение файла CSV
    df1 = pd.DataFrame()
    df1.index = read_csv.columns
    print("Данные имеют вид:")
    print(read_csv)  # вывод объекта с данными DataFrame
    read_csv['Средняя за год'] = read_csv.mean(axis=1)  # добавление столбца со средними значениями температуры
    print("Данные со столбцом средней температуры по годам:")
    print(read_csv)  # вывод объекта

    counter = pd.DataFrame()  # создание объекта-счётчика вхождений месяцев

    read_csv2 = read_csv.drop('Средняя за год', axis=1)  # создание нового объекта без столбца
                                                                # усреднённых значений
    read_csv2['Макс'] = read_csv.idxmax(axis=1) # выбор месяца с максимальной температурой в каждой строке
    # подсчёт количества лет, когда каждый из месяцев был максимальным
    df1 = read_csv2['Макс'].groupby(by=read_csv2['Макс']).count()
    print("Количество лет, когда каждый из месяцев был максимальным")
    print(df1)
    plt.hist(read_csv2['Макс']) # построение графика
    plt.title("Количество лет, когда каждый из месяцев был максимальным")
    plt.show()  # показ графиков

    read_csv2['Мин'] = read_csv.idxmin(axis=1) # выбор месяца с минимальной температурой в каждой строке
    # подсчёт количества лет, когда каждый из месяцев был минимальным
    df1 = read_csv2['Мин'].groupby(by=read_csv2['Мин']).count()
    print("Количество лет, когда каждый из месяцев был минимальным")
    print(df1)
    plt.hist(read_csv2['Мин']) # построение графика
    plt.title("Количество лет, когда каждый из месяцев был минимальным")
    plt.show()  # показ графиков

    # задание параметров графика
    plt.plot(read_csv.index, read_csv['Средняя за год'], label='Средняя температура за год')
    plt.title("График изменения среднегодовой температуры по годам")  # задание заголовка
    plt.xlabel("Год")  # название оси Ох
    plt.ylabel("Средняя температура")  # название оси Оу
    plt.legend()  # вывод легенды
    plt.show()  # показ графиков


#lr5()
lr6()