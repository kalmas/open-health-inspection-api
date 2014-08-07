from inspection import Inspection

class Business:

    def __init__(self, business_id, name, address):
        self.business_id = business_id
        self.name = name
        self.address = address
        self.inspections = []

    def add_inspection(self, date):
        i = Inspection(date)
        self.inspections.append(i)
