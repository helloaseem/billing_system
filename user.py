class User:
    
    def __init__(self, name):
        self.name = name
        self.item_bought = {}
        
    def set_item_bought(self, _id, qty):
        self.item_bought[_id] = qty
    
    