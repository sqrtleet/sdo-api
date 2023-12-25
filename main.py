import uvicorn
import urllib.parse

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from io import BytesIO

from home import home as home_handler
from parse import parse as parse_handler
from parse import semester_parse as semester_parse_handler
from parse import course_parse as course_parse_handler
from parse import authorization as auth_handler
from excel import create_excel as create_excel_handler
from excel import get_excel as get_excel_handler

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/')
def home(request: Request):
    return home_handler(request)


@app.post('/parse_data')
def parse_data():
    data = parse_handler()
    return data


@app.post('/semester_parse')
def semester_parse(semester_id: str):
    data = semester_parse_handler(semester_id)
    return {'data': data}


@app.post('/course_parse')
def course_parse(course_id: str):
    data = course_parse_handler(course_id)
    return {'data': data}


@app.post('/get_excel_count')
def get_excel_count(data: dict):
    print(data)
    specialty = data['specialty']
    res = get_excel_handler(specialty, data['data'])
    stream = BytesIO()
    res.save(stream)
    stream.seek(0)
    headers = {
        'Content-Disposition': f'attachment; filename={urllib.parse.quote(specialty)}.xlsx; filename*=UTF-8\'\'{urllib.parse.quote(specialty)}.xlsx',
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'charset': 'utf-8',
    }
    return StreamingResponse(iter([stream.getvalue()]), headers=headers)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
