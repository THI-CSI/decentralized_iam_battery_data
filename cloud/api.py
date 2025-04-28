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

@app.get("/batterypass/")
def read_items(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(authorize_user)
):
    return db.query(models.Item).all()

@app.put("/batterypass/")
# @decrypt_request_data
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
        db.refresh(new_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Item already exists.")
    return new_item

@app.post("/batterypass/{did}")
# @decrypt_request_data
async def update_item(
    did: int,
    item: ItemCreatePlain,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(authorize_user)
):
    db_item = db.query(models.Item).filter(models.Item.id == did).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found.")
    if not hasattr(item, "name") or not hasattr(item, "description"):
        raise HTTPException(status_code=400, detail="Decrypted fields missing.")
    
    db_item.name = item.name
    db_item.description = item.description
    try:
        db.commit()
        db.refresh(db_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Item already exists.")
    return db_item

@app.delete("/batterypass/")
def delete_item(
    did: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(authorize_user)
):
    item = db.query(models.Item).filter(models.Item.id == did).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    db.delete(item)
    db.commit()
    return {"ok": True}
