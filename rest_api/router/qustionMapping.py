from fastapi import APIRouter
from rest_api.controllers.quetionMapping import upload_documnt,get_document,process_output,check_input

from rest_api.request.questionMapping import askquestion,askfromgpt
from rest_api.request.user import User
from fastapi import Depends
from rest_api.router.auth import get_current_active_user
router = APIRouter()


@router.get('/test')
def get_text(current_user: User = Depends(get_current_active_user)):
    print("gopal")
    return current_user
    
    

@router.get('/askfromgpt')
def get_text(quesiton,index,current_user: User = Depends(get_current_active_user)):
    flag= check_input(quesiton)
    if(flag==False):
        return {"status":0,'result':"query is Too Long"}

    try:
        result=upload_documnt(question=quesiton,index_name=index)
        return {"status":1,'result':result}
    except:
        return {"status":0,'result':"Error occure"}

@router.get('/askqustion')
def ask_quesiton(quesiton,index,topk,threshold,current_user: User = Depends(get_current_active_user)):

    flag= check_input(quesiton)
    print("input checked")
    if(flag==False):
        return {"status":0,'result':"query is Too Long"}
    
    try:
        result=get_document(question=quesiton,index_name=index,
                            topk=int(topk),threshhold=int(threshold))
        return {"status":1,'result':result}
    except:
        return {"status":0,'result':"Error occure"}