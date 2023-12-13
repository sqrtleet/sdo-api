import textwrap

from openpyxl import load_workbook, Workbook
from openpyxl.styles import PatternFill


def create_excel(course_data):
    fn = 'output.xlsx'
    wb = Workbook()
    ws = wb.active

    for col, module in enumerate(course_data['data']['data'], start=1):
        row = 2
        ws.cell(row=1, column=col, value=module).fill = PatternFill('solid', fgColor='FF6AA84F')
        ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = len(module) + 2
        for value in course_data['data']['data'][module]:
            if value == 'Folder':
                ws.cell(row=row, column=col, value=value).fill = PatternFill('solid', fgColor='FF0f55f7')
                for child in course_data['data']['data'][module]['Folder']:
                    row += 1
                    ws.cell(row=row, column=col, value=child).fill = PatternFill('solid', fgColor='FF3C78D8')
                    for child_value in course_data['data']['data'][module]['Folder'][child]:
                        row += 1
                        ws.cell(row=row, column=col,
                                value='{}: {}'.format(course_data['data']['data'][module][value][child][child_value],
                                                      child_value)).fill = PatternFill('solid', fgColor='FFA4C2F4')
            else:
                cdmv = course_data['data']['data'][module][value]
                if cdmv == 'Файл' or cdmv == 'Форум' or cdmv == 'Задание' or cdmv == 'тест':
                    ws.cell(row=row, column=col, value='{}: {}'.format(cdmv, value)).fill = PatternFill('solid', fgColor='FFB6D7A8')
                elif cdmv == 'Ссылка':
                    ws.cell(row=row, column=col, value='{}: {}'.format(cdmv, value)).fill = PatternFill( 'solid', fgColor='FF7c07f5')
                else:
                    ws.cell(row=row, column=col, value='{}: {}'.format(cdmv, value)).fill = PatternFill( 'solid', fgColor='FFefe3bc')
            row += 1

    for col in range(1, len(course_data['data']['data']) + 1):
        max_length = 0
        for cell in ws[ws.cell(row=1, column=col).column_letter]:
            wrapped_value = textwrap.fill(str(cell.value), width=50)
            if len(wrapped_value) > max_length:
                max_length = len(wrapped_value)
        adjusted_width = (max_length + 2)
        ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = adjusted_width
    # wb.save(fn)
    return wb