import os
import textwrap

from openpyxl import load_workbook, Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment

from parse import course_parse as course_parse_handler
from parse import authorization as authorization_handler

data1 = {
    "data": {
        "Б1.В.02 Теория и методика обучения математике": {
            "id": "32466",
            "Преподователь": "Нина Васильевна Аргунова"
        },
        "Б1.О.25 Дискретная математика и математическая логика": {
            "id": "32465",
            "Преподователь": "Татьяна Неустроева"
        },
        "Б1.О.22 Вариационное исчисление и оптимальное управление": {
            "id": "32464",
            "Преподователь": "Оксана Федотовна Иванова"
        },
        "Б1.В.08 Базы данных": {
            "id": "32463",
            "Преподователь": "Ирина Германовна Ларионова"
        },
        "Б1.В.03 Теория и методика обучения информатике": {
            "id": "32462",
            "Преподователь": "Екатерина Винокурова"
        },
        "Б1.О.19 Функциональный анализ": {
            "id": "32461",
            "Преподователь": "Валерий Брониславович Хохолов"
        },
        "Б1.О.26 Теория вероятностей и математическая статистика": {
            "id": "32460",
            "Преподователь": "Александра Ивановна Григорьева"
        },
        "Б1.В.ДВ.01.01 Элективные дисциплины по физической культуре и спорту": {
            "id": "32459"
        },
        "Б1.О.20 Теория функций комплексного переменного": {
            "id": "32458",
            "Преподователь": "Татьяна Семеновна Попова"
        },
        "Б1.О.21 Уравнения с частными производными": {
            "id": "32457",
            "Преподователь": "Оксана Федотовна Иванова"
        }
    }
}

data2 = {
    "data": {
        "Базовый модуль": {
            "БРС ИПТОМ 2023-2024": "Файл",
            "Объявления": "Форум"
        },
        "Нормативный модуль": {
            "Рабочая программа дисциплины": "Файл",
            "Текущий журнал БРС МО-20": "Файл",
            "IMI-B-M-20 экзамен": "Файл"
        },
        "Теоретический модуль": {
            "Предмет и задачи методики обучения математике": "Файл",
            "1. Предмет методики обучения математике": "Файл",
            "Изменения содержания школьного математического образования": "Файл",
            "2. Методы обучения математике и их классификации": "Файл",
            "3. Средства обучения и формы организации": "Файл",
            "4. Урок как основная форма организации учебного процесса": "Файл",
            "5. Математические понятия": "Файл",
            "6. Теоремы и методика их изучения в школьном курсе математики": "Файл",
            "7. Задачи в обучении математике": "Файл",
            "8. Преподавание математики в 5-6 классах": "Файл",
            "9. Тождественные преобразования выражений": "Файл",
            "10. Понятие функции в школьном курсе математики основной школы": "Файл",
            "11. Методика изучения треугольников": "Файл",
            "12. Методика изучения геометрических построений в курсе планиметрии": "Файл",
            "13. Методика изучения показательной, логарифмической и тригонометрических функций": "Файл",
            "14. Методика изучения параллельности прямых и плоскостей": "Файл",
            "15. Методические подходы к изучению объемов": "Файл",
            "Folder": {
                "Методы обучения математике": {
                    "Интерактивные методы.pdf": "Файл",
                    "Методы обучения математике.pdf": "Файл"
                },
                "Организация обучения математике": {
                    "Конструктор урока.pdf": "Файл",
                    "Организация обучения математике.pdf": "Файл",
                    "Памятка для самоанализа урока.pdf": "Файл",
                    "Типы и виды уроков. Современные требования к уроку..pdf": "Файл"
                }
            }
        },
        "Практический модуль": {
            "Folder": {
                "Практические задания": {
                    "Виды и методы решения текстовых задач.pdf": "Файл",
                    "Методика изучения квадратичной функции.pdf": "Файл",
                    "Методика изучения квадратных уравнений и систем уравнений в школьном курсе алгебры.pdf": "Файл",
                    "Методика изучения параллельности и перпендикулярности в пространстве.pdf": "Файл",
                    "Методика изучения показательной и логарифмической функций.pdf": "Файл",
                    "Методика изучения темы «Подобные треугольники».pdf": "Файл",
                    "Методика изучения темы Многогранники.pdf": "Файл",
                    "Методика изучения темы Четырехугольники.pdf": "Файл",
                    "Методика обучения методам решения логарифмических уравнений и неравенств.pdf": "Файл",
                    "Понятие площади. Площади плоских фигур..pdf": "Файл",
                    "Тела вращения.docx.pdf": "Файл",
                    "Формирование понятия первообразной и интеграла.pdf": "Файл",
                    "Формирование понятия производной. Применение производной к исследованию функций..pdf": "Файл"
                }
            },
            "Практическоезадание1.": "Задание",
            "Практическоезадание2": "Задание",
            "Практическоезадание3": "Задание",
            "Практическоезадание4": "Задание",
            "Практическоезадание5": "Задание",
            "Практическоезадание6": "Задание",
            "Практическоезадание7": "Задание",
            "Практическоезадание8": "Задание",
            "Практическоезадание9": "Задание",
            "Практическоезадание10": "Задание",
            "Практическоезадание11": "Задание",
            "Практическоезадание12": "Задание",
            "Глоссарий": "Задание"
        },
        "Диагностический модуль": {
            "Образцы типовых тестовых заданий": "Файл",
            "Вопросы экзамена МО-21": "Файл",
            "Folder": {
                "Контрольные работы": {
                    "Методика преподавания алгебры в 7-9 кл.pdf": "Файл",
                    "Методика преподавания тем математики 5-6 классов.docx.pdf": "Файл"
                }
            },
            "Тест": "Тест"
        },
        "Методический модуль": {
            "Методические рекомендации": "Файл",
            "ФГОС ООО": "Файл",
            "Примерная РП ООО базовый": "Файл",
            "Примерная РП ООО углубленный": "Файл",
            "ФРП Математика 5-9-классы база": "Файл",
            "ФРП Математика-7-9-классы угл": "Файл",
            "ФРП-Математика-10-11-классы база": "Файл",
            "ФРП Математика-10-11-классы угл": "Файл",
            "Логико-дидактический анализ": "Файл",
            "Пример логико-дидактического анализа Перпендикулярность прямых и плоскостей": "Файл",
            "Пример анализа геометрического материала учебника математики": "Файл",
            "Нормативныедокументы": "Ссылка"
        },
        "Литература": {
            "ТИМОМ в схемах и таблицах": "Файл",
            "Методика изучения функционально-содержательной линии": "Файл"
        },
        "Секция 7": {},
        "Секция 8": {},
        "Секция 9": {},
        "Секция 10": {}
    }
}


def create_excel(course_data):
    fn = 'output.xlsx'
    wb = Workbook()
    ws = wb.active

    for col, module in enumerate(course_data['data'], start=1):
        row = 2
        ws.cell(row=1, column=col, value=module).fill = PatternFill('solid', fgColor='FF6AA84F')
        ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = len(module) + 2
        for value in course_data['data'][module]:
            if value == 'Folder':
                ws.cell(row=row, column=col, value=value).fill = PatternFill('solid', fgColor='FF0f55f7')
                for child in course_data['data'][module]['Folder']:
                    row += 1
                    ws.cell(row=row, column=col, value=child).fill = PatternFill('solid', fgColor='FF3C78D8')
                    for child_value in course_data['data'][module]['Folder'][child]:
                        row += 1
                        ws.cell(row=row, column=col,
                                value='{}: {}'.format(course_data['data'][module][value][child][child_value],
                                                      child_value)).fill = PatternFill('solid', fgColor='FFA4C2F4')
            else:
                cdmv = course_data['data'][module][value]
                if cdmv == 'Файл' or cdmv == 'Форум' or cdmv == 'Задание' or cdmv == 'Тест':
                    ws.cell(row=row, column=col, value='{}: {}'.format(cdmv, value)).fill = PatternFill('solid',
                                                                                                        fgColor='FFB6D7A8')
                elif cdmv == 'Ссылка':
                    ws.cell(row=row, column=col, value='{}: {}'.format(cdmv, value)).fill = PatternFill('solid',
                                                                                                        fgColor='FF7c07f5')
                else:
                    ws.cell(row=row, column=col, value='{}: {}'.format(cdmv, value)).fill = PatternFill('solid',
                                                                                                        fgColor='FFefe3bc')
            row += 1

    for col in range(1, len(course_data['data']) + 1):
        max_length = 0
        for cell in ws[ws.cell(row=1, column=col).column_letter]:
            wrapped_value = textwrap.fill(str(cell.value), width=50)
            if len(wrapped_value) > max_length:
                max_length = len(wrapped_value)
        adjusted_width = (max_length + 2)
        ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = adjusted_width
    # wb.save(fn)
    return wb


def create_excel_count(wb, name, course_data):
    ws = wb.active
    next_row = ws.max_row + 2
    module_elements = dict()
    resource_types = ['Файл', 'Задание', 'Тест', 'Ссылка', 'Страница']

    for module in course_data:
        module_elements[module] = {}
        for resource_type in resource_types:
            module_elements[module][resource_type] = 0

    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    ws.merge_cells(start_row=next_row, start_column=1, end_row=next_row, end_column=len(course_data))
    cell = ws.cell(row=next_row, column=1, value=name)
    cell.fill = PatternFill('solid', fgColor='FFb3ffe6')
    cell.border = thin_border

    for col, module in enumerate(course_data, start=1):
        row = next_row + 2
        ws.cell(row=next_row + 1, column=col, value=module).border = thin_border
        ws.column_dimensions[ws.cell(row=next_row + 1, column=col).column_letter].width = len(module) + 4 if len(module) < 23 else 26
        for value in course_data[module]:
            if value == 'Folder':
                for child in course_data[module]['Folder']:
                    for child_value in course_data[module]['Folder'][child]:
                        module_elements[module]['Файл'] += 1
            else:
                cdmv = course_data[module][value]
                if cdmv in resource_types:
                    module_elements[module][cdmv] += 1
        for key, value in module_elements[module].items():
            ws.cell(row=row, column=col, value=f'{key}: {value}').border = thin_border
            row += 1
    return wb


def get_excel(specialty, data):
    # authorization_handler()
    wb = Workbook()
    ws = wb.active
    ws.cell(row=1, column=1, value=specialty)
    for course in data['data']:
        course_name = course
        course_data = course_parse_handler(data['data'][course]['id'])
        create_excel_count(wb, course_name, course_data)
    return wb


if __name__ == '__main__':
    get_excel('01.03.01', data1)
