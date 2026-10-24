
# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
from schemas import *
from database import engine, get_db
from user_creation_validation import FamilyDetailsValidator
import bcrypt
import getpass


# Create the database tables (In production, use Alembic migrations instead)
models.Base.metadata.create_all(bind=engine)

app1 = FastAPI()

@app1.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    # print(__dict__(schemas))
    # email_valiation = validation(db, user.name, user.email, user.aadhar_number).validate_email()
    validation_message = FamilyDetailsValidator(db, user.name, user.email, user.aadhar_number)
    if validation_message.check_any_validation_issue():
        print(f"value is {validation_message}")
        errors = validation_message.get_errors()
        if errors:
            raise HTTPException(detail=','.join(errors))
        # errors.append("injected error")
        # errors.clear()
        print(validation_message.get_errors())
        return errors
    return None
    # password = getpass.getpass("Enter a secure password: ")
    # Generate a salt and hash the password
    # bcrypt automatically handles salt generation and embedding
    password = user.password
    salt = bcrypt.gensalt()
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    print(hashed_password)
    
    # Map Pydantic payload to SQLAlchemy ORM object
    new_user = models.FamilyDetails(name=user.name, email=user.email, password=hashed_password, aadhar_number=user.aadhar_number)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refreshes new_user to obtain its generated ID
    return new_user

@app1.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.FamilyDetails).offset(skip).limit(limit).all()
    return users

@app1.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.FamilyDetails).filter(models.FamilyDetails.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
