from fastapi import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

from auth import schemas
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager, UserManager
from auth.schemas import UserRead, UserCreate
from pages.route import router as router_pages, templates
from fastapi import FastAPI, Depends, HTTPException
from fastapi_users import FastAPIUsers, BaseUserManager, schemas

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# Define a route for handling the registration form submission
@app.post("/auth/register")
async def register_user(request: Request, user_create: schemas.BaseUserCreate,
                        user_manager: UserManager = Depends(get_user_manager)):
    try:
        created_user = await user_manager.create(user_create, request=request)
        return RedirectResponse(url="/login", status_code=302)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()
app.include_router(router_pages)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"
