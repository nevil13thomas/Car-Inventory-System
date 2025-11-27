from pydantic import BaseModel, conint
from typing import Optional

# Base schema for Owner, shared fields between create and read operations
class OwnerBase(BaseModel):
    name: str
    license_number: str

# Schema for creating an Owner
class OwnerCreate(OwnerBase):
    pass

# Schema for reading an Owner, includes ID
class OwnerRead(OwnerBase):
    id: int

    class Config:
        orm_mode = True  # Enable ORM mode for compatibility with SQLAlchemy models

# Base schema for Car, shared fields between create and read operations
class CarBase(BaseModel):
    color: str
    make: str
    year: conint(ge=1925, le=2025)  # Year must be between 1925 and 2025
    picture: Optional[str] = None   # Optional picture URL/path

# Schema for creating a Car, includes owner reference
class CarCreate(CarBase):
    owner_id: int

# Schema for updating a Car, all fields optional
class CarUpdate(BaseModel):
    color: Optional[str]
    make: Optional[str]
    year: Optional[conint(ge=1925, le=2025)]
    picture: Optional[str]
    owner_id: Optional[int]

# Schema for reading a Car, includes ID and nested Owner info
class CarRead(CarBase):
    id: int
    owner: OwnerRead

    class Config:
        orm_mode = True  # Enable ORM mode for compatibility with SQLAlchemy models
