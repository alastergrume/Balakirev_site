import pandas as pd



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

