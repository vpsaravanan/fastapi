
# user-creation validation class
from fastapi import HTTPException
from models import FamilyDetails

class FamilyDetailsValidator:
    def __init__(self, db, name, email, aadhar_number):
        self.name = name
        self.email = email
        self.db = db
        self.aadhar_number = aadhar_number
        self.error_messages = []
    def email_exists_db(self):
        # email = self.email
        # db = self.db
        if self.email:
            # print("email is {}".format(self.email))
            db_user = self.db.query(FamilyDetails).filter(FamilyDetails.email == self.email).first()
            if db_user:
                # Check if user already exists
                self.error_messages.append('Email already registered')
                # raise HTTPException(status_code=400, detail="Email already registered")
    def aadhar_number_exists(self):
        aadhar_number_query = self.db.query(FamilyDetails).filter(FamilyDetails.aadhar_number == self.aadhar_number).first()
        if aadhar_number_query:
            # print('aadhar number exists')
            self.error_messages.append('Aadhar number already exists')
            # raise HTTPException(detail="Aadhar number already exists")
    def check_any_validation_issue(self):
        # self.error_messages.clear()
        self.email_exists_db()
        self.aadhar_number_exists()
        # print(self.error_messages)
        return self.has_errors()
        pass
    def has_errors(self):
        return bool(self.error_messages)
    def get_errors(self):
        return self.error_messages.copy()
