from ast import literal_eval

class Products:
    
    all_products = {}
    
    def __init__(self, data):
        self.__id = data[1]
        self.title = data[2]
        self.price = literal_eval(data[3])
        self.category = data[5]
        self.description = data[4]
        self.image = data[6]
        self.rating = literal_eval(data[7])
        
        Products.all_products[self.__id] = self
        
    @staticmethod
    def get_product_object(_id):
        return Products.all_products.get(_id, None)
    
    @staticmethod
    def display_all_product():
        
        print("Please select a product from below: \n")
        print("Id\t| " + "Title")
        print("-"*100)
        for _id in Products.all_products:
            ind = _id
            title = Products.all_products.get(_id).title
            print("{0})\t| {1}".format(ind, title))
        
    def get_id(self):
        return self.__id
        
    def display_detail(self):
        print("\nThe product you selected:")
        print("1.\tId: ", self.__id)
        print("2.\tProduct Name: ", self.title)
        print("3.\tPrice: Rs.", self.price)
        print("4.\tCategory: ", self.category)
        print("5.\tRating: ", str(self.rating.get('rate',0)) + " out of " + str(self.rating.get("count", 0)) + " customer")
        print("6.\tProduct Description: \n", self.description)
        print("7.\tImage: ", self.image)
    
    def get_total_price(self, qty):
        return qty * self.price
