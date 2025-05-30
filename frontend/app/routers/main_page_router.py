from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import httpx

router = APIRouter()

templates = Jinja2Templates(directory='templates')


async def get_current_user_with_tokens(request: Request) -> dict:
    access_token = request.cookies.get('access_token')
    if not access_token:
        return {}
    user = await get_user_info(access_token)
    user['access_token'] = access_token
    return user

@router.get('/')
async def index(request: Request, user: dict=Depends(get_current_user_with_tokens)):
    context = {'request': request}
    if user.get('name'):
        context['user'] = user
    response = templates.TemplateResponse('index.html', context=context)
    return response

async def login_user(user_email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url='http://backend_api:9999/api/auth/login',
            data={"username": user_email, 'password': password}

        )
        print(response.json())
        return response.json()


async def get_user_info(access_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url='http://backend_api:9999/api/auth/get-my-info',
            headers={"Authorization": f'Bearer {access_token}'}

        )
        print(response.json())
        return response.json()

@router.get('/login')
@router.post('/login')
async def login(request: Request, user: dict=Depends(get_current_user_with_tokens), user_email: str = Form(''), password: str = Form('')):
    context = {'request': request}
    print(user, 5555555555555555555555)
    if user.get('name'):
        redirect_url = request.url_for("index")
        response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        return response

    if request.method == "GET":
        response = templates.TemplateResponse('login.html', context=context)
        response.delete_cookie('access_token')
        return response

    user_tokens = await login_user(user_email, password)
    access_token = user_tokens.get('access_token')
    if not access_token:
        return templates.TemplateResponse('login.html', context=context)

    user = await get_user_info(access_token)
    context["user"] = user
    response = templates.TemplateResponse('login.html', context=context)
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=60*5)
    return response
