from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.exc import IntegrityError

# Creates a new owner and handles DB integrity errors.
def create_owner(db: Session, owner_in: schemas.OwnerCreate):
    owner = models.Owner(**owner_in.dict())
    db.add(owner)
    try:
        db.commit()
        db.refresh(owner)  # Load generated fields (e.g., ID)
    except IntegrityError:
        db.rollback()
        raise
    return owner

# Retrieves an owner by ID.
def get_owner(db: Session, owner_id: int):
    return db.query(models.Owner).filter(models.Owner.id == owner_id).first()

# Creates a new car after validating owner existence.
def create_car(db: Session, car_in: schemas.CarCreate):
    owner = get_owner(db, car_in.owner_id)
    if not owner:
        return None
    car = models.Car(
        color=car_in.color,
        make=car_in.make,
        year=car_in.year,
        picture=car_in.picture,
        owner_id=car_in.owner_id
    )
    db.add(car)
    db.commit()
    db.refresh(car)
    return car

# Retrieves a car by ID.
def get_car(db: Session, car_id: int):
    return db.query(models.Car).filter(models.Car.id == car_id).first()

# Returns a list of cars.
def list_cars(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Car).offset(skip).limit(limit).all()

# Partially updates a car record.
def update_car(db: Session, car_id: int, car_update: schemas.CarUpdate):
    car = get_car(db, car_id)
    if not car:
        return None
    data = car_update.dict(exclude_unset=True)

    # Validate new owner ID if provided.
    if 'owner_id' in data and data['owner_id'] is not None:
        if not get_owner(db, data['owner_id']):
            return None

    for field, value in data.items():
        setattr(car, field, value)

    db.add(car)
    db.commit()
    db.refresh(car)
    return car

# Deletes a car; returns False if not found.
def delete_car(db: Session, car_id: int):
    car = get_car(db, car_id)
    if not car:
        return False
    db.delete(car)
    db.commit()
    return True
