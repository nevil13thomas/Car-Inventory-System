from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, Base
from .deps import get_db

# Create database tables based on models if they do not exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(title="Car Inventory API", version="1.0")

# Endpoint to create a new owner
@app.post("/owners", response_model=schemas.OwnerRead, status_code=status.HTTP_201_CREATED)
def create_owner(owner_in: schemas.OwnerCreate, db: Session = Depends(get_db)):
    try:
        owner = crud.create_owner(db, owner_in)
    except Exception:
        raise HTTPException(status_code=400, detail="Owner could not be created (maybe duplicate license)")
    return owner

# Endpoint to get an owner by ID
@app.get("/owners/{owner_id}", response_model=schemas.OwnerRead)
def get_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = crud.get_owner(db, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner

# Endpoint to create a new car
@app.post("/cars", response_model=schemas.CarRead, status_code=status.HTTP_201_CREATED)
def create_car(car_in: schemas.CarCreate, db: Session = Depends(get_db)):
    car = crud.create_car(db, car_in)
    if car is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return car

# Endpoint to list all cars with pagination
@app.get("/cars", response_model=list[schemas.CarRead])
def list_cars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_cars(db, skip=skip, limit=limit)

# Endpoint to get a car by ID
@app.get("/cars/{car_id}", response_model=schemas.CarRead)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = crud.get_car(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

# Endpoint to update a car by ID
@app.put("/cars/{car_id}", response_model=schemas.CarRead)
def update_car(car_id: int, car_in: schemas.CarUpdate, db: Session = Depends(get_db)):
    updated = crud.update_car(db, car_id, car_in)
    if updated is None:
        if not crud.get_car(db, car_id):
            raise HTTPException(status_code=404, detail="Car not found")
        else:
            raise HTTPException(status_code=404, detail="Owner not found")
    return updated

# Endpoint to delete a car by ID
@app.delete("/cars/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_car(db, car_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Car not found")
    return
