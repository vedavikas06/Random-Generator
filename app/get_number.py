from fastapi import APIRouter, Request
from flask_login import login_required, current_user
import random, requests

#FastApi routes - [API-A]
router = APIRouter()

@router.get("/get_number")
async def read_random():
    rand_num = random.randint(0, 1000) 
    return {"Random_Number": rand_num}
    # return templates.TemplateResponse("random.html", {"request": request, "number": rand_num})