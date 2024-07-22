# from fastapi import FastAPI
# from sthali_crud import AppSpecification, SthaliCRUD

# class SthaliAuth:
#     app: FastAPI

#     def __init__(self, app_spec: AppSpecification) -> None:
#         sthali_crud = SthaliCRUD(app_spec)
#         self.app = sthali_crud.app






import fastapi


app = fastapi.FastAPI()


@app.post("/token")
async def token(token: dict):
    return {"message": "Hello World"}
