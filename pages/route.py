from fastapi import APIRouter, Request, FastAPI
from fastapi.templating import Jinja2Templates
from fastapi_users import fastapi_users, schemas, exceptions
from starlette.responses import HTMLResponse, RedirectResponse

app = FastAPI()
router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/profile")
def get_base_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})


