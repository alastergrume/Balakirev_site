import os
import time
import numpy as np
import pandas as pd
# from _data import deficit_file, internal_file, razuzlovka_file_path, internal_order_dir, prices_path
# from config.config import custom_deficit, new_collumns
# from database.database import DataBase
from datetime import date

import locale


def input_deficit(deficit_file):
    """
    Функция очищает полученный дефицит от ненужных значений в таблице
    :param deficit_file: файл с таблицей по форме дефицита
    :return: df - Преобразованный Data Frame.
             Опционально: pd4_str - Список словарей
    """
    # Загружаем лист Excel в Dataframe
    deficit_frame = pd.read_excel(deficit_file, sheet_name='TDSheet')

    # Метод удаляет строки, со значением NaN. Параметр how='all' - удаляет строки с всеми пустыми значениями
    pd_str = deficit_frame.dropna(how='all')

    # Заполняем значения NaN по столбцу "Код" нолями
    values = {"Код": 0}
    pd2_str = pd_str.fillna(value=values)
    pd3_str = pd2_str.to_dict(orient='records')

    group_item = ''  # Сохраняются номенклатурные группы
    deleted_group = []  # Сохраняются удаленные номенклатурные группы
    pd4_str = []  # Сохраняется новый список из строк

    # БЛОК: ------------ ФОРМИРОВАНИЕ СТРОК -------------------

    for i in range(len(pd3_str)):

        # Удаляем разделы (!Материалы ПКИ и !Металл)
        if pd3_str[i]['Код'] == 0 and pd3_str[i + 1]['Код'] == 0:
            deleted_group.append(pd3_str[i]['Номенклатура'])

        # Находим номенклатурные группы
        elif pd3_str[i]['Код'] == 0 and pd3_str[i + 1]['Код'] != 0:
            group_item = pd3_str[i]['Номенклатура']

        # Заносим номенклатурную группу в строку и добавляем эту строку в новый список
        elif pd3_str[i]['Номенклатура'] != group_item and pd3_str[i]['Номенклатура'] not in deleted_group:
            if group_item != '':
                pd3_str[i]['Номенклатурная группа'] = group_item
            else:
                pd3_str[i]['Номенклатурная группа'] = 'Группа не установлена'
            pd4_str.append(pd3_str[i])
    # --------------------------------------------------------

    df = pd.DataFrame(pd4_str)
    print('Преобразование дефицита произведено')
    # print(df.to_dict(orient='records'))

    return df.to_dict(orient='records')


'''
Класс для обработки дефицита и внутренних заказов
'''


# INFO: https://pandas.pydata.org/                          -->>> Официальная документация
# INFO: https://pandas.pydata.org/docs/user_guide/basics.html#iteration
# INFO: https://habr.com/ru/companies/ruvds/articles/494720/    -->>> Шпаргалка по Pandas
class Serialized_DF:

    # def __init__(self):
    #     try:
    #         self.unser_deficit = self.unserialized_df()
    #         print('Дефицит десерилизован')
    #     except Exception as e:
    #         print(f'Рабочий дефицит ещё не сохранен, сначала сформируйте дефицит {e}')
    def __init__(self):
        self.destination_path = 'E:/PycharmProjects/Balakirev_site/sitewomen/media/uploads_deficit_files/labor_deficit.txt'

    def serialized_df(self, deficit):
        deficit.to_pickle(self.destination_path)

    def unserialized_df(self):
        return pd.read_pickle(self.destination_path)


class XLSXReader:
    """
    Принимает xlsc файлы дефицита, внутренних заказов, разузловки
    методы удаляюь из них лишние строки
    Возвращает датафреймы каждого файла для дальнейше работы.
    """

    def __init__(self):

        self.deficit_file = deficit_file
        self.internal_file = internal_file
        self.razuzlovka_file_path = razuzlovka_file_path
        self.prices_path = prices_path
        self.df_prices = None
        self.df_unraveling = None

    def input_deficit(self):
        """
        Функция очищает полученный дефицит от ненужных значений в таблице
        :param deficit_file: файл с таблицей по форме дефицита
        :return: df - Преобразованный Data Frame.
                 Опционально: pd4_str - Список словарей
        """
        # Загружаем лист Excel в Dataframe
        deficit_frame = pd.read_excel(self.deficit_file, sheet_name='TDSheet')

        # Метод удаляет строки, со значением NaN. Параметр how='all' - удаляет строки с всеми пустыми значениями
        pd_str = deficit_frame.dropna(how='all')

        # Заполняем значения NaN по столбцу "Код" нолями
        values = {"Код": 0}
        pd2_str = pd_str.fillna(value=values)
        pd3_str = pd2_str.to_dict(orient='records')

        group_item = ''  # Сохраняются номенклатурные группы
        deleted_group = []  # Сохраняются удаленные номенклатурные группы
        pd4_str = []  # Сохраняется новый список из строк

        # БЛОК: ------------ ФОРМИРОВАНИЕ СТРОК -------------------

        for i in range(len(pd3_str)):

            # Удаляем разделы (!Материалы ПКИ и !Металл)
            if pd3_str[i]['Код'] == 0 and pd3_str[i + 1]['Код'] == 0:
                deleted_group.append(pd3_str[i]['Номенклатура'])

            # Находим номенклатурные группы
            elif pd3_str[i]['Код'] == 0 and pd3_str[i + 1]['Код'] != 0:
                group_item = pd3_str[i]['Номенклатура']

            # Заносим номенклатурную группу в строку и добавляем эту строку в новый список
            elif pd3_str[i]['Номенклатура'] != group_item and pd3_str[i]['Номенклатура'] not in deleted_group:
                if group_item != '':
                    pd3_str[i]['Номенклатурная группа'] = group_item
                else:
                    pd3_str[i]['Номенклатурная группа'] = 'Группа не установлена'
                pd4_str.append(pd3_str[i])
        # --------------------------------------------------------

        df = pd.DataFrame(pd4_str)
        print('Преобразование дефицита произведено')
        time.sleep(1)
        return df

    def razuzlovka_reader(self):
        """
        Принимает файл с разузловкой по всему дефициту
        :return: Список строк в упорядоченном виде.
        """
        df_razuzlovka = pd.read_excel(self.razuzlovka_file_path, sheet_name='TDSheet')

        # БЛОК: ------------------- ПРЕОБРАЗОВАНИЕ СТРОК --------------------------

        # Отбор строк по значениию: Вид обеспечения - Закупка
        df_razuzlovka = df_razuzlovka.loc[df_razuzlovka['ВО'] == 'З']
        # Создание нового датафрейма из подмножества столбцов
        df_razuzlovka = df_razuzlovka[['Код', 'Номенклатура', 'Заказчик', 'ЕИ', 'Кол-во', 'Срок', 'Продукция']]

        print('Перобразование Разузловки произведено')
        time.sleep(1)
        self.df_unraveling = df_razuzlovka

    # Форматирование даты в файле Цены
    def formate_prices(self):
        self.df_prices = pd.read_excel(self.prices_path, sheet_name='TDSheet')
        locale.setlocale(locale.LC_ALL, 'ru_RU')

        # df_prices = pd.read_excel(self.prices_path, sheet_name='TDSheet')

        def _itarate_date(n):
            """
            Функция преобразовывает дату в универсальнй формат даты, для последующего преобразования
            :param n: принимает строку с датой
            :return: возвращает строк с датой приведенная к виду: 00/00/0000
            """
            # убираем ненужные символы в конце строки с датой
            df_date = n[:-3].split(' ')

            new_date = ''
            month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
                          'октября', 'ноября', 'декабря']
            for i in range(len(df_date)):
                if df_date[i] not in month_list:
                    if len(df_date[i]) == 1:
                        new_date += f'0{df_date[i]}'
                        new_date += '/'
                    else:
                        new_date += df_date[i]
                        new_date += '/'
                else:
                    if len(str(month_list.index(df_date[i]) + 1)) == 1:
                        new_date += f'0{month_list.index(df_date[i]) + 1}'
                        new_date += '/'
                    else:
                        new_date += f'{month_list.index(df_date[i]) + 1}'
                        new_date += '/'

            return new_date[:-1]

        # Приводим строку с датой к виду: 00/00/0000, через встроенную функцию _itarate_date()
        self.df_prices['Период'] = self.df_prices['Период'].apply(_itarate_date)

        # Применяем формат даты
        self.df_prices['Период'] = pd.to_datetime(self.df_prices['Период'], dayfirst=True)  # format='"%d-%B-%y"',
        print("Список цен сформирован")

    def prices_reader(self, nom_item, param=None):

        """
        Функция считывает информацию о ценах, и выводит информацию о последней поставке
        :param nom_item: str -> наименование закупаемой продукции из дефицита или внутреннего заказа
        :param param: None - вывод всех поставщиков, и информацию об их последних поставках
                             формат DataFrame.to_markdown()

        :return: param -> 'list' -> выводит информацию о последнем поставщике и ценах в форме списка
                 param -> 'dict' -> выводит информацию о последнем поставщике и ценах в форме словаря
                 param ->  None -> выводит в консоль фрейм в режиме markdown()
                       ->  при отсутствии nom_item в файле prices -> None
        """

        # Вывод фрейма по определенной позиции
        data = self.df_prices[self.df_prices['Номенклатура'] == nom_item]  # 'Пластина токарная WNMG 080408-TF IC 907'

        try:
            # Выводит индекс строки с самым свежим приходов
            newest_data_index = data['Период'].idxmax()
        except ValueError:
            # если nom_item отсутствует, то возвращает None
            return None
        # Вывод последнего прихода с информацией о нем по индексу
        newest_data_value = data.loc[newest_data_index, ['Партнер', 'Период', 'Цена', 'Валюта', 'Вид цены']]

        if param:
            if param == 'dict':
                return newest_data_value.to_dict()
            if param == 'list':
                return newest_data_value.to_list()

        # БЛОК: ---------- Сборка нового фрейма из кросс-таблицы -------------
        else:
            # Группировка по полю 'Партнер' и выводит Поставщика и дату поставки
            partner_data = data.groupby(by=['Партнер'])[['Период', 'Цена', 'Вид цены', 'Валюта']].first()

            """
            `first()` берет первое значение из каждой группы, если в группе несколько строк с одинаковой `Номенклатура`.
            Важно:  Эта строка уже возвращает новый DataFrame, в котором для каждой `Номенклатура` будут первые значения из `Продукция`, `ЕИ`, `Кол-во`.
            """
            # Сохранение кросс-таблицы в словарь, для последующего преобразования в общий Датафрейм
            partner_data_json = partner_data.to_dict(orient='split')

            # Вывод кросс-таблицы при использовании параметра 'split':
            # {'index': ['Асраров Альберт Мухаматбаянович ИП', 'ДЕТАЛЬ-АВТО ООО', 'Шинторг'],
            #  'columns': ['Период', 'Цена', 'Вид цены', 'Валюта'],
            #  'data': [[Timestamp('2024-04-17 00:00:00'), 7430.0, 'Закупочная с НДС', 'руб.'],
            #           [Timestamp('2024-08-06 00:00:00'), 7800.0, 'Закупочная с НДС', 'руб.'],
            #           # [Timestamp('2024-08-24 00:00:00'), 40811.0, 'Закупочная с НДС', 'руб.']]}

            columns = (partner_data_json['columns'])
            data = (partner_data_json['data'])
            df_all = pd.DataFrame(data, columns=columns)
            df_all['Поставщик'] = partner_data_json['index']
            # --------------------------------------------------------------

            return df_all.to_markdown()

    def forming_list_product(self, nom_item):

        # ======== Формирование списка продукции =========
        mew_df_unraveling = self.df_unraveling[
            self.df_unraveling['Номенклатура'] == nom_item]  # 'Болт М16-6gх75.88.019 ГОСТ 7798-70'
        ser_one = mew_df_unraveling[['Продукция', 'ЕИ', 'Кол-во', 'Срок']].values.tolist()
        return ser_one

    def internal_order_reader(self, path_list=None):
        """
        Считывает информацию из внутреннего заказа
        :return: Преобразованный dataframe.
        """
        if path_list:
            self.internal_file = path_list

        # БЛОК: ------------- ПРЕОБРАЗОВАНИЯ СТРОК И СТОЛБЦОВ ------------------------

        internal_order_frame = pd.read_excel(self.internal_file, sheet_name='TDSheet', header=None)
        # Удаляются строки которые полностью в NaN
        internal_order_frame = internal_order_frame.dropna(axis='index', how='all')
        # Удаляются столбцы, которые полностью в NaN
        internal_order_frame = internal_order_frame.dropna(axis='columns', how='all')
        # Сохранение название внутреннего заказа в переменную
        order_label = internal_order_frame[1].iloc[0]
        # Сохранение в переменную Заказчика
        ordered = internal_order_frame[5].iloc[1]

        # Формирование нового Data Frame
        # Удаление столбцов со значением Nan,# и обрезка ненужных строк
        internal_order_frame = internal_order_frame[2:-2].dropna(axis='columns', how='all')
        # Преобразование первой строки в названия столбцов
        internal_order_frame.columns = internal_order_frame.iloc[0]
        # Удаление первой строки с наименованиями столбцов
        internal_order_frame = internal_order_frame[1:]
        # Добавление нового столбца со значением внутреннего заказа
        internal_order_frame['Заказ поставщику'] = order_label
        # Установка нового столбца со значением Заказчика
        internal_order_frame['Заказчик'] = ordered

        # -------------------------------------------------------------------------
        # print(internal_order_frame.columns.tolist())
        # print(internal_order_frame)

        # Преобразование в список словарей
        # internal_order_frame = internal_order_frame.to_dict(orient='records')

        # Вывод отсортированного списка в json формате
        # print("Sorted_list")
        # for i in range(len(internal_order_frame)):
        #     print(internal_order_frame[i])
        # -------------------------------------------------------------------------

        print('Перобразование внутреннего заказа произведено')
        # time.sleep(1)
        # database = DataBase()
        # database.pandas_to_sqlite(df=internal_order_frame, table_name='internal_orders')
        return internal_order_frame


class TotalFile(Serialized_DF):
    """
    Таблица со следующими полями:
    Основной раздел:
        Номенклатура - Дефицит, Внутренний заказ.
        Дата дефицита - Дата добавления позиции в дефицит, если строка была без изменений, то
                            остается дата добавления первой строки.
        Дополнительная информация - Из внутреннего заказа.
        Единица измерения - Дефицит, Внутренний заказ.

    Обработка заказа:
        К заказу - Столбец выводит информацию о количестве продукции к заказу
                #TODO должен быть расширенный режим просмотра изменений заказа

        Изменения заказа - Столбец выводит информацию о том, на сколько изменилось значение "к заказу"

    Сервисная информация:
        Длительность закупки - Дефицит, для внутреннего заказа необходимо реализовать логику по
                            подтягиванию длительности заказа к указанной позиции
        Основной Поставщик - Дефицит,
                             Внутренний заказ - необходимо реализовать логику, которая
                                                подтягивает Основного поставщика к указанной позиции.
        Менеджер закупки - Дефицит
                           Внутренний заказ - необходимо реализовать логику, которая
                                              подтягивает длительность заказа к указанной позиции.
        Изделие - Для дефицита: выводится информация об изделиях с указанием количества на каждое изделие
                  Для внутреннего заказа: выводится номер внутреннего заказа

                #TODO должен быть расширенный режим просмотра изделий, который включает:
                #TODO изделие, номер заказа, кол-во, серия позиции к заказу, обеспечение заказа складским запасом, или заказом поставщику

        Номенклатурная группа - Дефицит
                                Внутренний заказ - необходимо реализовать логику, которая
                                                   подтягивает номенклатурную группу к указанной позиции.
        Направление - Информация о том, от куда появилась потребность:
                      Дефицит - выводится слово дефицит
                      Внутренний заказ - Указывается номер заказа
        Потребитель - Указывается подразделение заказчик

    Движение заказа:
        Этап сделки
        Стадия этапа

    Информация об исполнении:
        Поставщик
        Счет на оплату
        Договор
        Спецификация

        Заказ поставщику


    """

    def __init__(self):
        Serialized_DF.__init__(self)
        # Инициализация класса Дефицит
        self.xls = XLSXReader()
        self.new_columns = new_collumns
        self.df = None
        self.custom_df = None
        self.custom_deficit_param = custom_deficit

    def _add_current_date(self):

        # Добавляем столбец со временем
        self.df['Дата дефицита'] = date.today()
        print('Текущая дата добавлена')

    def add_partner(self):
        # Чтение файла с ценами
        self.xls.formate_prices()
        # Добавление списка с партнерами и ценами в фрейм.
        self.custom_df['Предыдущая поставка'] = self.custom_df['Номенклатура'].apply(
            lambda nom_item: self.xls.prices_reader(nom_item, 'list'))

    def add_list_of_product(self):
        # Чтение файла Разузловка
        self.xls.razuzlovka_reader()
        # Добавление списка изделий в итоговый фрейм
        self.custom_df['Изделие'] = self.custom_df['Номенклатура'].apply(
            lambda nom_item: self.xls.forming_list_product(nom_item))

    def build_custom_deficit(self, param=None):
        """
        Метод формирует дефицит с полями по заданному шаблону, который
        хранится в файле config.py в папке config переменная custom_deficit
        :param param:   По умолчанию - /config/config.py/custom_deficit
                        Опционально - принимает список полей, необходимых для вывода
        :return: обновляет фрейм в свойстве класса self.custom_df
        """
        self.df = self.xls.input_deficit()
        self._add_current_date()

        if not param:
            param = self.custom_deficit_param
        try:
            self.custom_df = self.df[param]
            print("\nСоздание Custom_Frame произведено\n")
        except KeyError as e:
            print('Неверные значения полей', e, sep='\n')
        except TypeError as e:
            print(e)
            self.build_custom_deficit()

    def build_labor_deficit(self):
        """
        :return: Формирует рабочий дефицит, по уже заданному шаблону
        """
        self.build_custom_deficit()
        self.add_partner()
        self.add_list_of_product()
        self.serialized_df(self.custom_df)
        self.save_to_excel(param="custom")

    def save_to_excel(self, param=None):
        """
        При наличии параметра, печатается self.custom_df, который был отобран по полям
        :param param: str
        :return: Сохранение фрейма в Excel
        """
        try:
            if param:
                self.custom_df.to_excel('resources/output_custom.xlsx', index=False)
                print("Custom Fraime сохранен в Excel")
            else:
                self.df.to_excel('resources/output.xlsx', index=False)
                print(f'Общий фрейм сохранен в Excel')
        except PermissionError as e:
            print("\nОткрыт файл дефицита\n", e, '\n')
        except AttributeError as e:
            print("\nДанные для сохранения отсутствуют\n", e, '\n')

    # =============== Сервисные функции Пока нигде не задействованы ================
    def add_new_coll(self):
        # Добавляем новые столбцы из списка столбцов
        self.df = self.df.reindex(columns=self.df.columns.to_list() + self.new_columns)

    def view_columns(self):
        columns_list = self.df.columns.to_list()
        for i in range(len(columns_list)):
            print(f'{i + 1} - {columns_list[i]}')

    def view_df_of_columns(self, param=None):
        """
        Если param, то работает с пользовательским меню
        param должен быть list с int

        Example: param=[1, 2, 3, 4]

        Метод позволяет вывести датафрейм с опредеденными полями.
        Сначала выводит список полей в датафрейме импользуя метод view_columns
        Затем спрашивает у пользователя, какие поля вывести
        Затем выводит получившийся датафрейм

        Полезно будет использовать этот метод для вывода различных конфигураций
        датафрейма
        """
        list_of_columns = []
        try:
            if not param:

                print(list_of_columns)
                self.view_columns()
                try:
                    user_choice = input('Введите номер столбцов из списка - ').split()
                    print(user_choice)
                    for i in user_choice:
                        list_of_columns.append(self.df.columns.to_list()[int(i) - 1])
                except ValueError as e:
                    print(e, "Введено неверное значение")
                print(list_of_columns)
                if len(list_of_columns) == 0:
                    print("Не выбраны столбцы")
                elif len(list_of_columns) == 1:
                    # Если выбор 1, то выводим serial. Отправляем в df название столбца
                    self.custom_df = self.df[list_of_columns[0]]
                elif len(list_of_columns) > 1:
                    self.custom_df = self.df[list_of_columns]
            else:
                if type(param) == list:
                    for i in param:
                        list_of_columns.append(self.df.columns.to_list()[int(i) - 1])
                if len(list_of_columns) == 1:
                    # Если выбор 1, то выводим serial. Отправляем в df название столбца
                    self.custom_df = self.df[list_of_columns[0]]
                elif len(list_of_columns) > 1:
                    self.custom_df = self.df[list_of_columns]
                else:
                    return None
        except TypeError as e:
            print("Дефицит не загружен", e)


class InternalTotal:
    def __init__(self):
        self.internal_df = None

    def listed_files(self):
        """
        Функция считывает наименования файлов в папке
        :return: Список путей к файлам
        """
        directory = internal_order_dir
        pathList = []
        try:
            for filename in os.listdir(directory):
                f = os.path.join(directory, filename)
                if os.path.isfile(f):
                    pathList.append(f)
                # print(f)
        except Exception as e:
            print(e, "Файлы отсутствуют")
        return pathList

    def internal_order_formated(self):
        """
        Сборка фреймов из нескольких файлов.
        :return:
        """
        xls = XLSXReader()
        internal_order_frame = []
        for p in self.listed_files():
            internal_order_frame.append(xls.internal_order_reader(p))
        self.internal_df = pd.concat(internal_order_frame, ignore_index=True)

    def save_to_excel(self):
        self.internal_df.to_excel('resources/output_internal.xlsx', index=False)
        print("Внутренние заказы сохранены")

    def console_print_internal_df(self):
        print(self.internal_df.to_markdown())

    def add_partner(self):
        # Добавить столбец Партнер
        # Добавить в столбец данные из функции с выводом партнера
        total = TotalFile()
        total.add_partner()


class MaterialRequirements(TotalFile, Serialized_DF):
    """
    Функциональность класса:
    1. Загрузка нового и старого дефицита - Реализовано
    2. Сравнение старого и нового дефицита
        2.1 - Новая строка идентична старой -> Оставляем позицию в дефиците
        2.2 - Потребность увеличилась, К обеспечению увеличилось, Заказ и Запас неизменны
              ->
              Удаляем старую и вставляем новую позицию в Потребность
        2.3 - Потребность, Дефицит, к Обеспечению уменьшилось
              ->
              Удаляем старую, вставляем новую позицию в Потребность
        2.4 - Потребность не изменилась, К Обеспечению изменилось:
            2.4.1 - К Обеспеч == 0, and (Зак(new) - Зак(Old)) == К обспеч(New) - К обеспеч(OLD)
                    ->
                    Удаляем позицию из дефицита, Помещаем в статус Поставка или Оплата,
                    в зависимости от параметров заказа.
            2.4.2 - К Обеспеч уменьшилось, но != 0
                    ->
                    Удаляем старую вставляем новую позицию в Потребность. Выделяем измененения.
    3. Вывод актуального дефицита
    4. Сохранение в файл Excel - Здесь необходимо подумать про вынос сохранения
    в Excel актуального дефицита, можно либо переопределить метод в TotalFile,
    но видимо лучше создать класс сохранения для переопределения в других классах
    """

    def __init__(self):
        """
        Наследуем класс TotalFile и Serialized_DF для использования его методов
        """
        Serialized_DF.__init__(self)
        TotalFile.__init__(self)

        # Старый и новый дефициты
        self.old_deficit = self.unserialized_df()  # Так-то None, но для тестов поставил пока что, чтобы не запускать постоянно метод load_for_update_df
        self.new_deficit = self.unser_df()  # None Добавил для тестов, чтобы по сто раз не загружать из Эксель

        # Переменная для нового дефицита
        self.actual_deficit = None

    def build_labor_deficit(self):

        """
        :return: Переопределение метода TotalFile, для того, чтобы он не обновлял
                файл сериализазации при формировании рабочих Фреймов нового дефицита
        """
        self.build_custom_deficit()
        self.add_partner()
        self.add_list_of_product()

    def load_df_for_update(self):
        """
        Метод должен загружать новый дефицит, и старый десериализованный дефицит
        для их последующего сравнения

        TODO Тут все таки нужно сделать так чтобы новый фрейм сохранялся в новый файл

        :return:
        """
        self.build_labor_deficit()
        self.new_deficit = self.custom_df
        self.serialized_df(self.custom_df)
        print("Новый дефицит", self.new_deficit)
        print("Старый дефицит", self.old_deficit)

    # Сохранение нового дефицита под новым именем
    def serialized_df(self, deficit):
        deficit.to_pickle('resources/new_deficit.txt')

    # Пока что для тестов сюда добавил, чтобы быстрее загружался новый дефицит
    def unser_df(self):
        return pd.read_pickle('resources/new_deficit.txt')

    def identical(self):
        """Метод сравнивает строки на идентичность"""

        '''Метод equals() в Pandas позволяет проверить, 
        являются ли два DataFrames одинаковыми в плане формы 
        (то есть одинаковое количество строк и столбцов) и элементов.'''

        print(self.old_deficit.equals(self.new_deficit))

        print("Новый дефицит", self.new_deficit)
        print("Старый дефицит", self.old_deficit)

        """
        Сравнивает два датафрейма по наполнению.
        """
        try:
            df = self.old_deficit.compare(self.new_deficit)
            print(df)
        except ValueError as e:
            print(e)

    def compare_deficit(self):

        """
        Сравнение старого и нового дефицита с помощью pandas
        """
        # new_row = []

        print(len(self.old_deficit), '-', len(self.new_deficit), ' = ', len(self.old_deficit) - len(self.new_deficit))

        # dict_def = self.new_deficit.to_dict()['Номенклатура']
        # for i in range(len(self.old_deficit)):
        #     print(self.old_deficit['Номенклатура'].iloc[i])

        # print(ser_old_nom.to_dict())
        # print(ser_new_nom)

        '''1. Выявление позиций, которых не было ранее в дефиците и исключены из него'''
        # INFO позиции, которые были добавлены:
        all_rows = self.old_deficit.merge(self.new_deficit, on=['Код'])
        rows_not_in_old_deficit = self.new_deficit[(~self.new_deficit['Код'].isin(all_rows['Код']))]
        print("\nДобавленные позиции")
        print(rows_not_in_old_deficit.to_markdown())  # Выводятся позиции, которые были добавлены
        print(rows_not_in_old_deficit.index)
        for i in rows_not_in_old_deficit.index:
            print(self.old_deficit['Номенклатура'].iloc[i])

        # INFO позиции, которые исключили:
        all_rows = self.old_deficit.merge(self.new_deficit, on=['Код'])
        rows_not_in_new_deficit = self.old_deficit[(~self.old_deficit['Код'].isin(all_rows['Код']))]
        print("\nИсключенные позиции")
        print(rows_not_in_new_deficit.to_markdown())  # Выводятся позиции, которые исключили
        print(rows_not_in_new_deficit.index)
        for i in rows_not_in_new_deficit.index:
            print(self.new_deficit['Номенклатура'].iloc[i])

        '''2. Выявление позиций, которые не изменились'''
        # FIX IT Очень долго и не правильно

    def same_positions(self):
        """
        Нахождение позиций, которые не изменились
        """

        s1 = pd.merge(self.new_deficit, self.old_deficit, how='inner', on=['Номенклатура'])
        print(s1)

        # unchange_rows = []
        #
        # for index, row in self.new_deficit.iterrows():
        #     # new_row_nom = self.new_deficit['Номенклатура'].loc[index]
        #     for old_index, old_row in self.old_deficit.iterrows():
        #         if (row == old_row).all():
        #             unchange_rows.append(index)
        #
        # unchange_df = self.new_deficit.loc[unchange_rows]
        # print(unchange_df)
        #
        # print(unchange_rows)

        # for i in range(len(self.old_deficit)):
        #     # print(self.old_deficit['Номенклатура'].loc[i])
        #     for y in range(len(self.new_deficit)):
        #         if self.new_deficit['Номенклатура'].loc[y] != self.old_deficit['Номенклатура'].loc[i]:
        #             new_row.append(self.new_deficit.loc[y])
        #             print(self.new_deficit.loc[y])
