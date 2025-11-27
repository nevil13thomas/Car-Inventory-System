from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Owner model representing car owners
class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    name = Column(String, nullable=False)              # Owner's name, required
    license_number = Column(String, nullable=False, unique=True, index=True)  # Unique license number
    cars = relationship(
        "Car",
        back_populates="owner",
        cascade="all, delete-orphan"  # Delete related cars if owner is deleted
    )

# Car model representing vehicles
class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    color = Column(String, nullable=False)             # Car color, required
    make = Column(String, nullable=False)              # Car make/manufacturer, required
    year = Column(Integer, nullable=False)             # Manufacturing year, required
    picture = Column(String, nullable=True)            # Optional picture URL or path
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)  # Foreign key linking to Owner
    owner = relationship("Owner", back_populates="cars")  # Relationship to access the car's owner
