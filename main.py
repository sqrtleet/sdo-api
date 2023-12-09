import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from home import home as home_handler
from parse import parse as parse_handler
from parse import semester_parse as semester_parse_handler
from parse import course_parse as course_parse_handler
from parse import authorization as auth_handler

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/')
def home(request: Request):
    data = parse_handler()
    return home_handler(request, data)


@app.post('/semester_parse')
def semester_parse(semester_id: str):
    auth_handler()
    data = semester_parse_handler(semester_id)
    return {'data': data}


@app.post('/course_parse')
def course_parse(course_id: str):
    auth_handler()
    data = course_parse_handler(course_id)
    return {'data': data}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
