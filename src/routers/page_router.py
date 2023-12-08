from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.routers.router_bank import get_transactions, about_me

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")

a = ["О нас", "Клиенты", "Сервисы", "Услуги", "Тарифы", "Акции"]
avt = ["Иванов Виктор","Сергей Симонов", "Юрий Николаев"]
@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request, 'a': a,'avt': avt,})


@router.get("/home")
def get_base_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/login")
def get_log(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/logout")
def get_log(request: Request):
    return templates.TemplateResponse("logout.html", {"request": request})

@router.get("/transactions")
def get_search_page(request: Request, trs=Depends(get_transactions)):
    return templates.TemplateResponse("transactions.html", {"request": request, "transactions": trs})


@router.get("/me")
def get_search_page(request: Request, trs=Depends(about_me)):
    return templates.TemplateResponse("home.html", {"request": request, "me": trs})