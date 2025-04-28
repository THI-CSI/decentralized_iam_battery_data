from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from util.models import ItemCreatePlain  # ItemCreate,
from util.middleware import decrypt_request_data
from util import models
from util.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

security = HTTPBearer()
API_TOKEN = "secret"

def authorize_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials.credentials

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Neuer Root-Endpunkt hinzugefügt:
@app.get("/")
def read_root():
    return {"message": "API is working"}

@app.get("/batterypass/")
def read_items(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(authorize_user)
):
    return db.query(models.Item).all()

@app.put("/batterypass/")
async def create_item(
    item: ItemCreatePlain,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(authorize_user)
):
    if not hasattr(item, "name") or not hasattr(item, "description"):
        raise HTTPException(status_code=400, detail="Decrypted fields missing.")
    
    new_item = models.Item(name=item.name, description=item.description)
    db.add(new_item)
    try:
        db.commit()
