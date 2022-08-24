import requests
import pandas as pd
import sqlite3
from products import Products
from user import User

def create_product_objects():
        
    valid_response = requests.get('https://fakestoreapi.com/products', verify = False)

    data2 = valid_response.json()

    df = pd.DataFrame(data2)

    with sqlite3.connect("StoreProducts.db") as connection:
        
        cursor = connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS Products;")
        df = df.applymap(str)
        df.to_sql('Products', connection)
        
        temp = cursor.execute("SELECT * FROM PRODUCTS")
        
        for i in temp.fetchall():
            Products(i)

def create_bill(user):
    item_bought = user.item_bought
    total_indent = 120

    data = ""
    data += ("Welcome To Friends Store".center(total_indent,' '))
    data += "\n"
    data += (("-"*total_indent))
    data += "\n"
    data += ("Customer's Name: {0}".format(user.name).ljust(total_indent))
    data += "\n"
    data += "\n"
    data += (("-"*total_indent))
    data += "\n"
    data += ("\n\n")
    data += "\n"
    data += ("Purchase Details:".ljust(total_indent))
    data += "\n"
    data += (("-"*total_indent))
    data += "\n"
    data += ("\n\n\n")
    data += "\n"
    data += (("S.N.".ljust(5," ") + " | Product ID".ljust(15, " ") + " | Product Name".ljust(50) + " | Price".ljust(10) + " | Qty".ljust(10) + " | Sub Total".ljust(10)))
    data += "\n"
    tot = 0
    count = 0
    for _id in item_bought:
        count+=1
        data += (("".ljust(5," ") + " | ".ljust(15, " ") + " | ".ljust(50) + " | ".ljust(10) + " | ".ljust(10) + " | "))
        obj = Products.get_product_object(_id)
        qty = item_bought.get(_id)
        tot += obj.get_total_price(qty)
        data += "\n"
        data += ((str(count).ljust(5," ") + (" | " + str(obj.get_id())).ljust(15, " ") + (" | "+obj.title[:45]).ljust(50) + (" | " + str(obj.price)).ljust(10) + (" | " + str(qty)).ljust(10) + (" | " + str(obj.get_total_price(qty)))))
        data += "\n"
    data += "\n"
    data += (("-"*total_indent))
    data += "\n\n"
    data += ("Total\t|{:.2f}\t".format(tot).rjust(total_indent-14))
    data += "\n"
    tax = tot * 0.13
    data += ("Tax\t|{:.2f}\t".format(tax).rjust(total_indent-17))
    data += "\n"
    disc = tot * 0.05
    data += ("Discount\t|{:.2f}\t".format(disc).rjust(total_indent-12))
    data += "\n"
    data += ("Net Total\t|{:.2f}\t".format(tot+tax-disc).rjust(total_indent-10))
    data += "\n"
    data += "\n"
    data += (("-"*total_indent))
    data += "\n"
    data += "\n"
    data += ("Thank you for Shopping. Visit Us again !!!".center(total_indent))
    data += "\n"
    data += "\n"
    data += (("-"*total_indent))

    return data


if __name__=="__main__":
    name = input("Enter your name: ")
    user = User(name)

    checkout = "N"

    create_product_objects()

    while(checkout in ["NO", "N"]):
        Products.display_all_product()
        ids = input("Select any product: ")
        print("\n")
        print("=="*50)
        try:
            Products.get_product_object(ids).display_detail()
        except AttributeError:
            print("ERROR! ERROR!! ERROR!!!".center(50, " "),"\n\nNot a valid Produc Id selected. Please select a valid option.")
            print("=="*50)
            print("\n")
            continue
        print("=="*50)
        print("\n")
        cart = input("Do you want to add in the cart?\n").upper()

        if (cart in ["YES", "Y"]):
            qty = int(input("How many item do you want to add?\n"))
            while(not(qty>0)):
                qty = int(input("Quantity must be Greater than 0\nEnter Again:\n"))
            user.set_item_bought(ids, qty)
            
        checkout = input("Do you want to checkout? \n").upper()

    with open("bill.txt", "w+") as file:
        file.write(create_bill(user))