from fastapi import FastAPI

from routers.song.router import song_router
from routers.service.router import router_service

app = FastAPI()

app.include_router(
    router=song_router,
    )

app.include_router(
    router=router_service,
    tags=['service'],
    prefix='/service'
)


@app.get('/')
def main():
    return 'Success'
