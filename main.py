from fastapi import Depends,FastAPI,HTTPException,status
# from mangum import Mangum
from rest_api.router.router import api_router
from starlette.middleware.cors import CORSMiddleware
import uvicorn

def get_application() -> FastAPI:
    application = FastAPI(title="Data-Knobs-Apis", debug=True, version="1.0")

    application.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
    )
    # @application.get("/")
    # def home():
    #     return {"messege":"jello"}
    # @application.get("/search")
    # def home():
    #     return {"messege":"search"}
    application.include_router(api_router)
    
    return application


app = get_application()
# handler=Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




