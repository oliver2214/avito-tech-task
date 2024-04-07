from fastapi import FastAPI
from app.banners.router import router as router_banners


app = FastAPI()
app.title = "Сервис баннеров"
app.include_router(router=router_banners)
