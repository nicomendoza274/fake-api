class BaseService():
    def __init__(self, db, Model) -> None:
        self.db = db
        self.Model = Model
    
    def get_records(self):
        result = self.db.query(self.Model).all()
        return result
    
    def get_record(self, id:int):
        result = self.db.query(self.Model).filter(self.Model.id == id).first()
        return result

    def create_record(self, data):
        new_record = self.Model(**data.dict())
        self.db.add(new_record)
        self.db.commit()
        return
    
    def update_record(self, id:int, data):
        # record = self.db.query(self.Model).filter(self.Model.id == id).first()
        self.db.update(id, data)
        self.db.commit()
        return 

    def delete_record(self, id:int):
        result = self.db.query(self.Model).filter(self.Model.id == id).first()
        self.db.delete(result)
        self.db.commit()
        return
    