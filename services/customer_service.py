from sqlalchemy import func
from models.customer import Customer as CustomerModel
from schemas.customer import Customer
from datetime import datetime

class CustomerService():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_records(self):
        result = self.db.query(CustomerModel).filter(CustomerModel.deleted_at == None).all()
        return result
    
    def get_record(self, id:int):
        result = self.db.query(CustomerModel).filter(
            CustomerModel.deleted_at == None,
            CustomerModel.customer_id == id
        ).first()
        return result

    def create_record(self, data: Customer, user_id: int):
        new_record = CustomerModel(**data.dict())
        new_record.created_by = user_id
        self.db.add(new_record)
        self.db.commit()
        self.db.refresh(new_record)
        return new_record
    
    def update_record(self, id:int, data: Customer, user_id: int):
        customer: CustomerModel = self.db.query(CustomerModel).filter(
            CustomerModel.deleted_at == None,
            CustomerModel.customer_id == id
        ).first()
        customer.address = data.address
        customer.city = data.city
        customer.internal_id = data.internal_id
        customer.name = data.name
        customer.phone = data.phone
        customer.updated_by = user_id
        customer.updated_at = func.now()

        self.db.commit()
        self.db.refresh(customer)
        return customer

    def delete_record(self, id:int, user_id: int):
        customer: CustomerModel = self.db.query(CustomerModel).filter(
            CustomerModel.deleted_at == None,
            CustomerModel.customer_id == id
        ).first()
        customer.deleted_at = func.now()
        customer.deleted_by = user_id
        self.db.commit()
        return
    