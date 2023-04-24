from fastapi import APIRouter
from rest_api.router import qustionMapping,auth

api_router = APIRouter()


api_router.include_router(qustionMapping.router, tags=["Question-Mapping-Routes"])
api_router.include_router(auth.router, tags=["Auth-Testing"])


