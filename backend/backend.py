from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config.settings import settings
from database.database import get_db
from schemas.query import QueryRequest, QueryResponse
from utils.langchain_client import get_llm_response
from models.query_log import QueryLog
from sqlalchemy.orm import Session

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dépendance pour vérifier le token JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Endpoint pour recevoir les requêtes du frontend
@app.post("/receive_query", response_model=QueryResponse)
async def receive_query(request: QueryRequest, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    # Stocker la requête
    db_query = QueryLog(query=request.query, language=request.language)
    db.add(db_query)
    db.commit()
    db.refresh(db_query)

    # Obtenir la réponse du LLM via LangChain
    response_text = get_llm_response(request.query, request.language)

    # Mettre à jour la réponse dans la base
    db_query.response = response_text
    db.commit()

    return {"response": response_text, "status": "success"}

# Endpoint pour envoyer une réponse au frontend
@app.get("/send_response/{query_id}", response_model=QueryResponse)
async def send_response(query_id: int, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    db_query = db.query(QueryLog).filter(QueryLog.id == query_id).first()
    if not db_query or not db_query.response:
        raise HTTPException(status_code=404, detail="Query not found or no response yet")
    return {"response": db_query.response, "status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)