from fastapi import FastAPI, Depends, HTTPException
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from pydantic import BaseModel

#
class ItemCreate(BaseModel):
    name: str
    description: str

#
models.Base.metadata.create_all(bind=engine)

#
app = FastAPI()

#
security = HTTPBearer()

#
API_TOKEN = "secret"

#
def authorize_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials.credentials

#
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#
@app.get("/batterypass/")
def read_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

#
@app.put("/batterypass/")
def create_item(
        item: ItemCreate,
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Security(authorize_user)
):
    new_item = models.Item(name=item.name, description=item.description)
    db.add(new_item)
    try:
        db.commit()
        db.refresh(new_item)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Item already exists.")
    return new_item

#
@app.post("/batterypass/")
def update_item(did: str, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == did).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found.")
    db_item.name = item.name
    db_item.description = item.description

#
@app.delete("/batterypass/")
def delete_item(did: str, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == did).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    db.delete(item)
    db.commit()
    return {"ok": True}
