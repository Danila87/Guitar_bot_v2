from fastapi import FastAPI
from routers.song.router import song_router

app = FastAPI()

app.include_router(router=song_router)


@app.get('/')
def main():
    return 'Success'
