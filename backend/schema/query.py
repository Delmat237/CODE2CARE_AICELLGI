from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    language: str

class QueryResponse(BaseModel):
    response: str
    status: str