import lxml
import requests

from fastapi import FastAPI
from bs4 import BeautifulSoup

session = None


def authorization():
    global session
    url = 'https://sdo.s-vfu.ru/login/index.php'
    username = 'nikiforovsv'
    password = 'sergo1005'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'

    session = requests.Session()
    r = session.get(url, headers={'User-Agent': user_agent})
    session.headers.update({'Referer': url})
    session.headers.update({'User-Agent': user_agent})
    soup_r = BeautifulSoup(r.text, 'lxml')
    login_token = soup_r.find('input', {'name': 'logintoken'}).get('value')
    post_request = session.post(url, {
        'backUrl': url,
        'username': username,
        'password': password,
        'logintoken': login_token,
        'remember': 'yes',
    })
    return post_request


def get_ajax_params(category):
    ajax_params = {
        'categoryid': category['data-categoryid'],
        'depth': category['data-depth'],
        'showcourses': category['data-showcourses'],
        'type': category['data-type']
    }
    return ajax_params


def parse_categories(category):
    ajax_link = 'https://sdo.s-vfu.ru/course/category.ajax.php'

    try:
        ajax_response = requests.get(ajax_link, params=get_ajax_params(category)).json()
        soup = BeautifulSoup(ajax_response, 'lxml')
        level = {'Бакалавриат': {}, 'Магистратура': {}, 'Аспирантура': {}}

        categories_depth2 = soup.find_all('div', class_='category')
        for category_depth2 in categories_depth2:
            print(category_depth2.text)
            ajax_response_depth2 = requests.get(ajax_link, params=get_ajax_params(category_depth2)).json()
            soup_depth2 = BeautifulSoup(ajax_response_depth2, 'lxml')

            categories_depth3 = soup_depth2.find_all('div', class_='category')
            for category_depth3 in categories_depth3:
                if category_depth3.text not in level[category_depth2.text]:
                    level[category_depth2.text][category_depth3.text] = {}
                # print(category_depth3.text)
                ajax_response_depth3 = requests.get(ajax_link, params=get_ajax_params(category_depth3)).json()
                soup_depth3 = BeautifulSoup(ajax_response_depth3, 'lxml')

                specialties = soup_depth3.find_all('div', class_='category')
                for specialty in specialties:
                    if specialty.text not in level[category_depth2.text][category_depth3.text]:
                        level[category_depth2.text][category_depth3.text][specialty.text] = {}
                    ajax_response_semesters = requests.get(ajax_link, params=get_ajax_params(specialty)).json()
                    soup_semester = BeautifulSoup(ajax_response_semesters, 'lxml')

                    semesters = soup_semester.find_all('div', class_='category')
                    if len(semesters) == 0:
                        level[category_depth2.text][category_depth3.text][specialty.text]['общий'] = specialty.get(
                            'data-categoryid')

                    for semester in semesters:
                        if specialty.text not in level[category_depth2.text][category_depth3.text][specialty.text]:
                            semester_id = semester.get('data-categoryid')
                            level[category_depth2.text][category_depth3.text][specialty.text][
                                semester.text] = semester_id
                    # print('{} id={}'.format(specialty.text, specialty.get('data-categoryid')))
        return level
    except requests.exceptions.RequestException as e:
        print('Error during request: {}'.format(e))
        return 0


def set_modules_dict(resource_type, modules_dict, module_name, elements, is_folder=False, is_assign=False):
    type_dict = {'resource': 'Файл', 'forum': 'Форум', 'assign': 'Задание', 'quiz': 'Тест', 'url': 'Ссылка',
                 'page': 'Страница'}
    if is_folder:
        modules_dict[module_name]['Folder'] = {}
        for elem in elements:
            if not elem.find('div', class_='foldertree'):
                global session
                name = elem.find('span', class_='instancename').text
                modules_dict[module_name]['Folder'][name] = {}
                link = elem.find('a', class_='aalink').get('href')
                response = session.get(link)
                soup = BeautifulSoup(response.text, 'lxml')
                files = soup.find_all('span', class_='fp-filename-icon')
                for file in files:
                    modules_dict[module_name]['Folder'][name][file.text] = 'Файл'
            else:
                name = elem.find('div', class_='fp-filename-icon').find('span', class_='fp-filename').text
                values = elem.select('div.filemanager ul li span.fp-filename-icon')
                modules_dict[module_name]['Folder'][name] = {}
                for value in values:
                    modules_dict[module_name]['Folder'][name][value.text] = 'Файл'
    else:
        for elem in elements:
            names = elem.find_all('span', class_='instancename')
            for name in names:
                span = name.find('span', class_='accesshide')
                arr = name.text.split()
                if span:
                    modules_dict[module_name][' '.join(arr[:len(arr) - 1])] = type_dict[resource_type]
                else:
                    modules_dict[module_name][''.join(arr[:])] = type_dict[resource_type]
    return modules_dict


def semester_parse(semester_id):
    global session
    link = 'https://sdo.s-vfu.ru/course/index.php?categoryid=' + semester_id
    response = session.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.find('div', class_='courses')
    courses = content.find_all('div', class_='coursebox')
    courses_dict = {}
    for course in courses:
        course_text = course.find('a', class_='aalink').text
        course_teacher = course.find('ul', class_='teachers')

        courses_dict[course_text] = {}
        courses_dict[course_text]['id'] = course.get('data-courseid')
        if course_teacher:
            courses_dict[course_text]['Преподователь'] = course_teacher.find('a').text

    return courses_dict


def course_parse(course_id):
    global session
    modules_dict = {}
    link = 'https://sdo.s-vfu.ru/course/view.php?id=' + course_id
    response = session.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.find('div', class_='course-content')
    sections = content.find_all('li', class_='section')

    for section in sections:
        section_elements = section.find('ul', class_='section')
        module_name = section.find('div', class_='sectionhead')
        module_name = module_name.find('span', class_='the_header').text if module_name else 'Базовый модуль'
        modules_dict[module_name] = {}

        resource_types = ['resource', 'folder', 'forum', 'assign', 'quiz', 'url', 'page']

        for resource_type in resource_types:
            resources = section_elements.find_all('li', class_=resource_type)
            if resources:
                modules_dict = set_modules_dict(resource_type, modules_dict, module_name, resources,
                                                is_folder=(resource_type == 'folder'))
    return modules_dict


def parse():
    post_request = authorization()
    soup = BeautifulSoup(post_request.text, 'lxml')
    subcategories = soup.find('div', class_='subcategories')
    if subcategories:
        category_elements = subcategories.find_all('div', class_='category')
        if category_elements:
            result = parse_categories(category_elements[6])
            print(result)
            return result
        else:
            print('No \'category\' elements found.')
    else:
        print('No \'subcategories\' element found.')
    return 1


# if __name__ == '__main__':
#     # parse()
#
#     authorization()
#     print(course_parse('32457'))
#     # print(semester_parse('1671'))
