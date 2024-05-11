from fastapi import FastAPI, Request, Form, Query, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic
from urllib.parse import urlencode
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector
from mysql.connector import Error

website_db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="leeminho",
  database="website"
)

cursor = website_db.cursor()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()
app.add_middleware(SessionMiddleware, secret_key="secret")

def set_login_status(request: Request, value: bool):
    request.session["SIGNED-IN"] = value

@app.get("/")
def login_form(request: Request):
    return templates.TemplateResponse("home.html",{"request":request})
   
@app.post("/signup")
def register_user(name:str = Form(""), username: str = Form(""), password: str = Form("")):  
    
    try:   
        cursor.execute("SELECT COUNT(*) FROM member WHERE username = %s", (username,))
        (count,) = cursor.fetchone()
        if  count > 0: 
            error_message = "帳號已有人使用"
            query_params = urlencode({"message": error_message})
            error_url = f"/error?{query_params}"
            return RedirectResponse(url=error_url, status_code=303)
        
        
        cursor.execute("INSERT INTO member (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
        website_db.commit()
        return RedirectResponse(url="/", status_code=303)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise HTTPException(status_code=500, detail="something wrong")
  
    finally:
        cursor.close
        website_db.close
   
        rows = cursor.rowcount
        if  rows == 1:
            print("資料新增成功")
        else:
            print("資料新增失敗")


@app.post("/signin")
def login(request: Request, member_username:str=Form(""),member_password:str=Form("")):
    
    try:  
        cursor = website_db.cursor()
        cursor.execute("SELECT id, name FROM member WHERE username = %s AND password = %s", (member_username, member_password))
        
        member = cursor.fetchone()
        if  member:
            request.session['member_id'] = member[0]
            request.session['member_name'] = member[1]
            request.session["SIGNED-IN"] = True
            print("有找到會員資料")
            print(request.session["SIGNED-IN"])
            return RedirectResponse(url="/member", status_code=303)
        else:
            error_message = "帳號、或密碼輸入錯誤"
            query_params = urlencode({"message": error_message})
            error_url = f"/error?{query_params}"
            print("沒找到會員資料")  
            return RedirectResponse(url=error_url, status_code=303)
        
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")
    
    finally:
        cursor.close
        website_db.close

        
@app.get('/member')
def member(request: Request, member_name: str = Query("")):
    
    signed_in = request.session.get("SIGNED-IN")
    member_name = request.session.get("member_name")
    member_id = request.session.get("member_id")

    cursor.execute("SELECT message.id, member.name, message.content, (message.member_id=%s) AS is_own FROM message JOIN member ON message.member_id = member.id ORDER BY message.time DESC" ,(member_id, ))
    message_original= cursor.fetchall() 
    message_record = [(msg_id, sender, message, bool(is_own)) for msg_id, sender, message, is_own in message_original]
    
    if signed_in and member_name:  
        return templates.TemplateResponse("member.html", {"request": request,"member_name": member_name, "message_record":message_record})
    else:
        return RedirectResponse(url="/", status_code=302)
    
@app.get('/error')
def error(request: Request, message: str = Query("")):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

@app.get('/signout')
def error(request: Request):
    request.session["SIGNED-IN"] = False
    print(request.session["SIGNED-IN"])
    return RedirectResponse(url="/", status_code=303)


@app.post('/createMessage')
def createMessage(request: Request, content:str=Form("")):
    member_id = request.session.get("member_id")
    if  member_id:
        cursor.execute("INSERT INTO message (member_id, content) VALUES (%s,%s)",(member_id,content))
        website_db.commit()
        print("留言已存入資料庫啦")
        return RedirectResponse(url="/member", status_code=303)
    else: 
        print("留言無法存入資料庫欸")


@app.post('/deleteMessage')
def deleteMessage(request:Request, message_id: int=Form("")):
    print(message_id)
    cursor = website_db.cursor()
    cursor.execute("DELETE FROM message WHERE message.id = %s ",(message_id,))
    website_db.commit()
    if cursor.rowcount == 1:
            print("資料已經刪除囉")
    else:
            print("好像有問題喔")
   

    return RedirectResponse(url="/member", status_code=303)
    