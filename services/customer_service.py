from sqlalchemy import desc, func
from sqlalchemy.orm.session import Session
from models.customer import Customer as CustomerModel
from schemas.customer import Customer
from utils.base64_manager import base64_decode
from utils.json_manager import json_parse

class CustomerService():
    def __init__(self, db:Session) -> None:
        self.db = db
    
    def get_records(self, start: int | None, length: int | None, query: str | None):
        model = self.db.query(CustomerModel).filter(CustomerModel.deleted_at == None)
        if query:
            json_query = base64_decode(query)
            json = json_parse(json_query)
            json = {key.lower(): value for key, value in json.items()}

            if 'sorts' in json and len(json['sorts']) > 0:
                for sort in json['sorts']:
                    property_name = sort['propertyName']
                    descending = sort['descending']

                    if descending == False:
                        model = model.order_by(property_name)
                    else: 
                        model = model.order_by(desc(property_name))

            if 'filters' in json and len(json['filters']) > 0:
                for filter in json['filters']:
                    property_name = filter['propertyName']
                    type_filer = filter['type']
                    value_filter = filter['value']

                    if type_filer == 'eq':
                        model = model.filter(getattr(CustomerModel, property_name) == value_filter)
                    elif type_filer == 'neq':
                        model = model.filter(getattr(CustomerModel, property_name) != value_filter)
                    elif type_filer == 'gt':
                        model = model.filter(getattr(CustomerModel, property_name) > value_filter)
                    elif type_filer == 'lt':
                        model = model.filter(getattr(CustomerModel, property_name) < value_filter)
                    elif type_filer == 'gte':
                        model = model.filter(getattr(CustomerModel, property_name) >= value_filter)
                    elif type_filer == 'lte':
                        model = model.filter(getattr(CustomerModel, property_name) <= value_filter)
                    elif type_filer == 'like':
                        search = "%{}%".format(value_filter)
                        model = model.filter(getattr(CustomerModel, property_name).like(search))
                    elif type_filer == 'contains':
                        search = "%{}%".format(value_filter)
                        model = model.filter(getattr(CustomerModel, property_name).like(search))

            if 'search' in json:
                search = json['search']
                search = "%{}%".format(search)
                model = model.filter(getattr(CustomerModel, 'name').ilike(search))

        if length:
            model = model.limit(length)

        if start: 
            model = model.offset(start)
        
        result = model.all()
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
    