import lxml
import requests

from fastapi import FastAPI
from bs4 import BeautifulSoup


def parse():
    post_request = authorization()
    soup = BeautifulSoup(post_request.text, 'lxml')
    subcategories = soup.find('div', class_='subcategories')
    if subcategories:
        category_elements = subcategories.find_all('div', class_='category')
        if category_elements:
            for i in range(6, 7):
                print(category_elements[i].text)
                parse_categories(category_elements[i])
        else:
            print('No \'category\' elements found.')
    else:
        print('No \'subcategories\' element found.')


def authorization():
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
    # with open('kek.html', mode='w', encoding='utf-8') as f:
    #     f.write(post_request.text)
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

        categories_depth2 = soup.find_all('div', class_='category')
        for category_depth2 in categories_depth2:
            print(category_depth2.text)
            ajax_response_depth2 = requests.get(ajax_link, params=get_ajax_params(category_depth2)).json()
            soup_depth2 = BeautifulSoup(ajax_response_depth2, 'lxml')

            categories_depth3 = soup_depth2.find_all('div', class_='category')
            for category_depth3 in categories_depth3:
                print(category_depth3.text)
                ajax_response_depth3 = requests.get(ajax_link, params=get_ajax_params(category_depth3)).json()
                soup_depth3 = BeautifulSoup(ajax_response_depth3, 'lxml')
                specialties = soup_depth3.find_all('div', class_='category')
                for i in specialties:
                    print('{} id={}'.format(i.text, i.get('data-categoryid')))
    except requests.exceptions.RequestException as e:
        print('Error during request: {}'.format(e))
        return 0
