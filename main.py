from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from nodes_edges import workflow


origins = [
    "http://localhost:8000/*",
    "*"
]





class Base(BaseModel):
    user_query: str

app_agent = workflow.compile()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/user_query")
def query_handler(base: Base):
    response = app_agent.invoke({"messages":[("user",base.user_query)]})
    # print(response["messages"][-1])
    return PlainTextResponse(content=response["messages"][-1].content,status_code=200)


@app.get("/")
async def root():
    return {"message": "Hello World"}

