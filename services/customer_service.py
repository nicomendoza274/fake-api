from models.customer import Customer as CustomerModel
from schemas.customer import Customer

class CustomerService():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_records(self):
        result = self.db.query(CustomerModel).all()
        return result
    
    def get_record(self, id:int):
        result = self.db.query(CustomerModel).filter(CustomerModel.customer_id == id).first()
        return result

    def create_record(self, data: Customer):
        new_record = CustomerModel(**data.dict())
        self.db.add(new_record)
        self.db.commit()
        return new_record
    
    def update_record(self, id:int, data: Customer):
        customer: CustomerModel = self.db.query(CustomerModel).filter(CustomerModel.customer_id == id).first()
        customer.address = data.address
        customer.city = data.city
        customer.internal_id = data.internal_id
        customer.name = data.name
        customer.phone = data.phone

        self.db.commit()
        return customer

    def delete_record(self, id:int):
        result = self.db.query(CustomerModel).filter(CustomerModel.customer_id == id).first()
        self.db.delete(result)
        self.db.commit()
        return
    