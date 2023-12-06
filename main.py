import uvicorn
from fastapi import FastAPI, Request

from home import home as home_handler

app = FastAPI()


@app.get("/")
def home(request: Request):
    return home_handler(request)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
