# ------------- # 
# Documentation
#-------------- #
# Student name       : Jason Yong Hsien Jiat
# Student number     : S3555422
# Highest level      : ALL levels (100% of HD)
# Errors/Problems    : None that I am aware of  


# ------------------------ #
#        Reflection        #
# ------------------------ #
#  What could be improved
# ------------------------ #
# 1. Some of the methods in the front end do more than just obtain user inputs and print/display messages. This is due to the reliance of the str_input() method in the 
#    front end. If possible, I would like keep methods where they belong i.e. front end solely handles obtaining inputs/displays and back end solely handle list manipulations.

# 2. Some of the methods (e.g. enter_order_details() method) are quite lengthy and do a lot of things within the function. If I had more time, I would've loved to 
#    re-structure the method and break it up into smaller methods that solely specialise in doing one thing.

# 3. The program only displays the change in a products stock (when selected in the menu - Main menu option [1] followed by Enter new order menu option [3]) when an order
#    has been MANUALLY entered by the user. It does not do this when the same option is selected after orders are loaded in from an order file. If possible, I would want
#    to implement code that would allow the user to see the change in stock for ALL products ordered through an order file.


# ------------------------ #
#  What was challenging
# ------------------------ #
# 1. Initally, it was hard to figure out how the methods in each of the classes would interact with each other. But once I figured out to create classes such as the OrderManger
#    and Menu classes and also figuring out how to properly utilise the Records class, it became much clearer and everything became more intuitive.

# 2. Trying to figure out what should stored in the attributes of the Order class. Initially I went with storing the unique product and customer ID but then I realised
#    that I was constantly calling the findProducts/findCustomer methods to access the product/customer information. In the end I felt it was more efficient to just store
#    both customer and product objects in the Order object to save time and use fewer lines of code.

# 3. Trying to figure out what other methods I needed to make the overall structure of my code less clutered and more readable/organised. For example the int_input() method
#    took a lot of time to figure out due to all the different conditions that I had to check for. Making that its own method helped me eliminate a lot of repeated lines
#    of code which helped me make the overall structure a bit tidier.

# 4. Figuring out a way to determine if an input is an integer or not. The idea of it is simple but it took at 30 mins to get the logic right and another 30 mins to get 
#    the order of the if/else and try/except statements correct to get the method to work properly.


# ----------------- #
# Importing modules
#------------------ #
import sys
from datetime import date


# ------ #
# Errors
#------- #
# The description of what each of these execeptions capture can be found in the raise_exception() method in the back end of the program (i.e. in the Menu class)
class LoadError(Exception):
    pass

class QuantityError(Exception):
    pass

class IDError(Exception):
    pass

class PriceError(Exception):
    pass

class CustomerError(Exception):
    pass

class StockError(Exception):
    pass

class OutofStockError(Exception):
    pass

class ZeroQuantityError(Exception):
    pass

class ChoiceError(Exception):
    pass

class ValueError(Exception):
    pass

class LimitError(Exception):
    pass

class NonIntegerError(Exception):
    pass


# ----------------------- #
# Code and Implementation 
# ----------------------- #

# this class stores the basic information of the customer such as their unique ID, name, and the total value they have generated
class Customer:
    __ID = None # this is a unique value (stored as string) 
    __name = None # the customers name
    __total = None # the total value that the customer has generated (past + present orders)
    
    def __init__(self, ID, name, total = 0):
        self.__ID = ID
        self.__name = name
        self.__total = total
        
    @property
    def ID(self):
        return self.__ID
    
    @property
    def name(self):
        return self.__name
    
    @property
    def total(self):
        return self.__total
    
    # this method allows the user to set the discount for the customer (an empty super method)
    def get_discount(self,price):
        pass
    
    # allows the user to update the total value the customer has generated based on the orders made by the user
    @total.setter
    def update_total(self, amount):
        self.__total += amount


# this class is a subclass of the the Customer class and specifies that a customer is a Retail customer
class RetailCustomer(Customer):    
    def __init__(self, ID, name, total = 0, rate = 10):
        super().__init__(ID, name, total)
        self.__rate = rate # the discount rate is set to 10% by default unless given a value 
        
    @property
    def rate(self):
        return self.__rate
    
    def get_discount(self, price): # calculates the discount for a given item based on the discount rate the customer is given
        return price*(1-self.rate/100)
    
    def displayCustomer(self):
        sys.stdout.write("Customer ID: " + str(self.ID) + "\n")
        sys.stdout.write("Customer Name: " + self.name + "\n")
        sys.stdout.write("Discount Rate: " + str(self.rate) + "% \n")

    # this method allows the user to set the discount rate for a given retail customer.
    # I did not make this a static method because that makes no sense. The task in the spec sheet clearly states to state the discount for a PARTICULAR customer.
    @rate.setter
    def setRate(self, rate):
        self.__rate = rate


# this class is subclass of the Customer class and specifies that the customer is a Wholesale customer
class WholesaleCustomer(Customer):
    __threshold = None
    __rate = None
    __second_rate = None
    
    def __init__(self, ID, name, total = 0, rate = 10, threshold = 1000):
        super().__init__(ID, name, total)
        self.__threshold = threshold # the threshold is set to 1000 by default unless specified 
        self.__rate = rate # sets the regular discount rate to be 10% by default

        # the code below sets the threshold discount rate to be 5% more than the regular rate
        # if first checks that the regular rate is not greater than 95%. Does not make sense to have greater than 100% discount
        if rate <= 95:
            self.__second_rate = rate + 5
        else:
            self.__second_rate = 100

    # this method calculates the discount that a wholesale customer is eligible to get. the discount is based on the TOTAL value of the customers order
    # different discounts will apply depending on whether the total value is less than or equal to the threhold OR above the threshold.
    def get_discount(self, total):
        if total > self.threshold:
            return total*(1-self.second_rate/100)
        else:
            return total*(1-self.rate/100)

    @property
    def rate(self):
        return self.__rate
    
    @property 
    def second_rate(self):
        return self.__second_rate

    @property
    def threshold(self):
        return self.__threshold

    def displayCustomer(self):
        sys.stdout.write("Customer ID: " + self.ID + "\n")
        sys.stdout.write("Customer Name: " + self.name + "\n")
        sys.stdout.write("Threshold Discount Rate: " + str(self.rate) + "% \n")
        sys.stdout.write("Second Discount Rate: " + str(self.second_rate) + "% \n")
        sys.stdout.write("Threshold Amount: " + str(self.threshold))

    # this method allows the user to set the threshold for the wholesale customer
    @threshold.setter
    def setThreshold(self, threshold):
        self.__threshold = threshold

    # this method allows the user to set the regular discount rate for the customer
    @rate.setter
    def setRate(self, rate):
        self.__rate = rate

        # checks to see if the regular rate is not greater than 95% and sets the second rate to be 5% more than this.
        if self.__rate <= 95: 
            self.__second_rate = rate + 5
        else:
            self.__second_rate = 100


class Product:
    def __init__(self, ID, name, price, stock):
        self.__ID = ID
        self.__name = name
        self.__price = float(price) # the price is always a float to account for cents
        self.__stock = int(stock) # stock of a product can only be an integer (cannot have 0.5 a product)
        
    @property
    def ID(self):
        return self.__ID
    
    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    # allows the user to set the price of the product
    @price.setter
    def setPrice(self, price):
        self.__price = price

    # allows the user to set the amount of stock the product has
    @stock.setter
    def setStock(self, stock):
        self.__stock = stock

# the Combo class is a subclass of the Product class. It has an extra attribute that stores the products in the combo as a list
class Combo(Product):
    __products = [] 

    def __init__(self, ID, name, price, stock, products):
        super().__init__(ID, name, price, stock)
        self.__products = products
        
    @property
    def products(self):
        return self.__products        


class Order:
    def __init__(self, customer, product, quantity, date = date.today()):
        self.__customer = customer # this should take in the customer object
        self.__product = product # takes the product object
        self.__quantity = quantity # quantity of product orderd (this is an integer)
        self.__date = date # the date that the order was entered into the system. uses the exising python module "date"

    # below are the methods that allow the user to access the information stored in the order object
    @property
    def customer(self):
        return self.__customer

    @property
    def product(self):
        return self.__product

    @property
    def quantity(self):
        return self.__quantity
    
    @property
    def date(self):
        return self.__date


# this class keeps track of all orders that were made 
class OrderManager:
    __orders = [] # stores the order objects in a private list

    @property
    def orders(self):
        return self.__orders

    # this method allows the user to add orders (successful ones) to the list of orders stored in this class
    def add_order(self, customer, product, quantity):
        order = Order(customer, product, quantity)
        self.orders.append(order)


# this class keeps a record of all products and customers (both from the files read and the customers added by the user)
class Records:
    # stores all customer and product objects as a private list 
    __customers = [] 
    __products = []
    
    @property
    def customers(self):
        return self.__customers
    
    @property
    def products(self):
        return self.__products

    # this method reads the customer file and adds the customer object to the list of customers according to what type of customer they are (as indicated in the file)
    def readCustomers(self, filename):
        input_file = open(filename,"r")
        file_line = input_file.readline()
        i = 0 # keeps track of the number of lines read
        
        while file_line != "":
            field = file_line.split(",")
            field = [item.strip() for item in field] # strips all the whitespaces of the elements in the line in the customer file
            # the code below checks if the customer is a retail or wholesale customer
            if field[2] == "R": 
                self.customers.append(RetailCustomer(field[0], field[1], float(field[-1]), float(field[-2])))
            elif field[2] == "W":
                self.customers.append(WholesaleCustomer(field[0], field[1], float(field[-1]), float(field[-2])))
            file_line = input_file.readline() # moves on the the next line in the file
            i += 1

        input_file.close() # closes the customer file once all the lines have been read
            
        return i

    # this method reads the product file and adds the product to the list of products as an object containing the products information
    def readProducts(self, filename):
        input_file = open(filename,"r")
        file_line = input_file.readline()
        i = 0 # keeps track of the number of lines that have been successfully read

        while file_line != "":
            field = file_line.split(",")
            field = [item.strip() for item in field]
            if field[0][0].upper() == "C": # checks if the product is a combo product
                list_of_combo_products = [] 
                total_price = 0
                combo_products = field[2:len(field)-1] # index the products that are part of the combo
                for product_id in combo_products:
                    product = self.findProducts(product_id) # obtain the product object from the list of products in the records
                    list_of_combo_products.append(product) # adds the product object to the list of combo products
                for product in list_of_combo_products:
                    total_price += product.price*0.9 # determine the total price of the combo based on 90% of the invidual products in the combo
                self.products.append(Combo(field[0], field[1], round(total_price,2), field[-1], list_of_combo_products)) # adds the combo to the list of products in the records
            else:
                self.products.append(Product(field[0], field[1], float(field[2]), int(field[3])))
            file_line = input_file.readline() # moves on to the next line in the file
            i += 1

        input_file.close() # closes the file once all the lines have been read
            
        return i

    # this method searches the list of customers to see if any customers match the ID or name given by the user
    def findCustomers(self, customer_detail):
        search_result = None
        for customer in self.customers: # checks if the customer information provided by the user matches anything that is in the product list
            if customer_detail == customer.ID or customer_detail == customer.name:
                search_result = customer
        return search_result # returns the customer if the customer matches the name or ID given, if not returns None
    
    # this method searches the list of products to see if any products match the ID or name given by the user
    def findProducts(self, product_detail):
        search_result = None
        for product in self.products: # checks if the product information provided by the user matches anything that is the product list
            if (product_detail == product.ID) or (product_detail == product.name):
                search_result = product
        return search_result # returns the product if the product matches the name or ID given, if not returns None
    
    # this method prints out all the customers in the customer in a format that is similar to the customer file
    def listCustomers(self):
        message = "\n====================================================\n"
        message += "            Dispalying Existing Customers \n"
        message += "----------------------------------------------------\n"
        message += "ID |    Name    |    Type    | Rate (%) |  Value ($)\n"
        message += "====================================================\n"
        sys.stdout.write(message)
        
        display_format = "{:<3}"+"| "+"{:^11}"+"| "+"{:^11}"+"| "+"{:^9}"+"| "+"{:^10}"+"\n"
        for customer in self.customers:
            if isinstance(customer, RetailCustomer): # checks what type of customer (retail or wholesale) the customer is
                row = display_format.format(customer.ID, customer.name, "Retail", customer.rate, round(customer.total,2))
            else:
                row = display_format.format(customer.ID, customer.name, "Wholesale", customer.rate, round(customer.total,2))
            sys.stdout.write(row)
    
    # this method prints out all the products in the product list in a fomart that is similar to the product file
    def listProducts(self):
        message = "\n=========================================\n"
        message += "       Displaying Existing Products \n"
        message += "-----------------------------------------\n"
        message += "ID |      Name      |  Price ($) | Stock\n"
        message += "=========================================\n"
        sys.stdout.write(message)

        display_format = "{:<3}"+"| "+"{:^15}"+"| "+"{:^11}"+"| "+"{:^6}"+"\n"
        for product in self.products:
            row = display_format.format(product.ID, product.name, product.price, product.stock)
            #sys.stdout.write(product.ID + ", " + product.name + ", " + str(product.price) + ", " + str(product.stock) + "\n")
            sys.stdout.write(row)
    
    # this method allows the user to remove/delete a customer from the list of customers
    def remove_customer(self, customer):
        self.customers.remove(customer)
#--------------------------------------------------------------------------------------------------------


# -------- #
# Back End
# -------- #

# This class will handle managing records and orders and all manipulations
class Menu:
    record = Records()
    order_manager = OrderManager()

    # this method will be used to check if a certain file exists in the working directory
    def load_file(self, filename):
        try:
            file = open(filename, 'r')
            file.close()
        except: 
            return False # returns false if the file does not exit or if the file cannot be read (i.e. corrupted)
        else:
            return True # returns true if the file can be successfully opened
    
    # this method loops through all the customer in the list of customers and updates all customers + information in the customer file based on any changes made by the user
    # i.e. add any new customers and adjust the total value/discount rates if they were changed.
    def save_customer_file(self, file_name):

        file_object = open(file_name, "w") # the filename of the customer file that was read at the beginning of the program (default or given)

        for customer in self.record.customers: # loops through all the customers in the list of customers
            if isinstance(customer, WholesaleCustomer): # checks if the customer is a retail or wholesale customer and writes the customer type as needed.
                file_object.write(customer.ID + ", " + customer.name + ", W, " + str(customer.rate) + ", " + str(customer.total) + "\n")
            else:
                file_object.write(customer.ID + ", " + customer.name + ", R, " + str(customer.rate) + ", " + str(customer.total) + "\n") 
        file_object.close() # closes the file when all customers have been added to the file

    # this method loops through all the products in the product list and updates all the products + information in the product file based on any orders that were made
    # i.e. update the stock based on any orders that were manually entered or made through an order file
    def save_product_file(self, file_name):

        file_object = open(file_name, "w")

        for product in self.record.products:
            if isinstance(product, Combo): # checks if the product in the product list is a combo item
                list_of_combo_products = product.products # obtains the list of products (objects) that are part of the combo
                combo_string = "" # initialise the string that will be written into the file (contains all the product IDs of the products in the combo)
                i = 0
                while i < len(list_of_combo_products):
                    combo_product = list_of_combo_products[i] # takes the list of products (objects) that are part of the combo
                    # the code below adds the ID of the product that is part of the combo and adds the product ID to a string
                    if i == len(list_of_combo_products) - 1: 
                        combo_string += combo_product.ID 
                    else:
                        combo_string += combo_product.ID + ", " # adds comas if the product is not the last product in the list
                    i += 1
                file_object.write(product.ID + ", " + product.name + ", " + combo_string + ", " + str(product.stock) + "\n")
            else: # write the product information to the file for any products that arent combos
                file_object.write(product.ID + ", " + product.name + ", " + str(product.price) + ", " + str(product.stock) + "\n")

        file_object.close() # closes the product file once all products are written into the file

    # this method takes an order file and reads all the orders and displays the number of orders that were successfully made (based on whether there was enough stock)
    def readOrders(self, filename):
        input_file = open(filename,"r")
        file_line = input_file.readline()
        successful_orders = 0 # counts the number of successful orders
        failed_orders = 0 # counts the number of failed orders

        while file_line != "":
            field = file_line.split(",")
            field = [item.strip() for item in field]
            # extracting the order details
            customer_detail = field[0]
            product_detail = field[1]
            quantity = int(field[2])

            # looks for the products and customer according to either the name or ID
            customer = self.record.findCustomers(customer_detail)
            product = self.record.findProducts(product_detail)

            quantity = self.check_quantity(quantity, product) # checks if there is enough quantity in stock to fulfil the order
            if not quantity:
                failed_orders += 1
                file_line = input_file.readline() # moves on to the next line in the file
                continue # skips all the remaining code in the loop and moves on to check the next order
            else:
            # creating the object for the order and adds it to the list of orders
                self.order_manager.add_order(customer, product, quantity)
                successful_orders += 1
            file_line = input_file.readline()

        input_file.close() # closing the file after all the lines have been read

        # the block below prints out a message to display the number of successful and failed orders for the user.
        message = "\n======================\n"
        message += "   Load file report \n"
        message += "======================\n"
        sys.stdout.write(message)
        
        display_format = "{:>20}"+"{:<5}"+"\n" # setting the format of the messages that will be printed to the user
        row = display_format.format("Successful orders: ", str(successful_orders))
        sys.stdout.write(row)
        row = display_format.format("Failed orders: ", str(failed_orders))
        sys.stdout.write(row)  

        return successful_orders # returns the number of orders that have been successfully read

    # this method will create a dictionary of with all customers as the keys and the values will contain a dictionary with 
    # all the products as keys and the ordered quantities as values.
    def customer_orders(self):
        order_record = {} # initialising the dictionary
        for customer in self.record.customers:
            order_record[customer] = {}
            for product in self.record.products:
                order_record[customer][product] = 0
            order_record[customer]['Total'] = 0

        # updating the order ordered quantities based on the orders.txt file
        for order in self.order_manager.orders:
            customer = order.customer
            product = order.product
            order_record[order.customer][order.product] += order.quantity
            if isinstance(customer, WholesaleCustomer):
                total = customer.get_discount(order.quantity*product.price)
            else:
                price = customer.get_discount(product.price)
                total = order.quantity*price
            order_record[order.customer]["Total"] += round(total,2)

        return order_record

    # this method determines the most valuable customer (mvc) based on the total value of all orders made (past and present)
    def determine_mvc(self):
        mvc = None
        highest_total = 0 # keeps track of the highest total value

        for customer in self.record.customers: # loops through all the customers in the customer list
            # it will set the current customer to be the MVC if the total value is greater that the current highest total
            if customer.total > highest_total:
                mvc = customer 
                highest_total = customer.total
        
        return mvc

    # this method determines the most popular product (mpp) based on the number of orders that contain the product
    def determine_mpp(self, orderNum):
        mpp = None
        most_orders = 0

        for product in orderNum:
            if product == 'Total': # ignores the "Total" key/value pairing in the dictionary
                pass
            else:
                # checks to see which product has the highest number of orders that contain the product
                if orderNum[product] > most_orders:
                    mpp = product
                    most_orders = orderNum[product]
        
        return mpp, most_orders # returns the product with the most orders and the number of orders that contain the product

    # this functioon determines the number of orders that contain a particular product. (used when displaying all order information)
    def orderNum(self):
        orderNum = {}
        for product in self.record.products:
            orderNum[product] = 0 # initialises the dictionary to have the number of orders containing a particular product to be 0 for every product in the product list

        for order in self.order_manager.orders:
            orderNum[order.product] += 1 # increases the count (value) for a product (key) if the order contains that product
        
        orderNum["Total"] = sum(orderNum.values()) # adds a key "Total" to the dictionary whose value is the total number of orders made
        
        return orderNum

    # this function determines the total quantity of a particular product that has been ordered. (used when displaying all order information)
    def orderQty(self):
        orderQty = {}
        for product in self.record.products: # initialises the dictionary to have the ordered quantites for all products in the product list to be zero
            orderQty[product] = 0 

        for order in self.order_manager.orders: # checks the orders and updates the quantity of each product according to the quantity in the order
            orderQty[order.product] += order.quantity

        orderQty["Total"] = sum(orderQty.values()) # adds a new key in the dictionary which the value will correspond to the total quantity of ALL products ordered

        return orderQty

    # creates a new customer and adds it to the list of existing customers
    def create_customer(self, customer_id, name, category):
        if category == 'W': # creates a customer using the WholesaleCustomer class
            self.record.customers.append(WholesaleCustomer(customer_id, name))
            sys.stdout.write("\nMessage: Wholesale customer, " + name + ", (Customer ID: " + customer_id + ") has been created.\n")
        elif category == 'R': # creates a customer using teh RetailCustomer class
            self.record.customers.append(RetailCustomer(customer_id, name))
            sys.stdout.write("\nMessage: Retail customer, " + name + ", (Customer ID: " + customer_id + ") has been created.\n")
            
        return self.record.findCustomers(customer_id)
    
    # removes a new customer from the list of customers if the order was not successfully 
    def delete_new_customer(self, customer):
        sys.stderr.write("\nMessage: Unable to proceed with order. New customer will be removed from records.\n")
        self.record.remove_customer(customer) # deletes the new customer from the records

    # checks that the value entered by the user is correct and that there is enough stock for the product
    def check_quantity(self, quantity, product):
        if quantity > product.stock:          
            return False
        else:
            return quantity
    
    # captures all the different exceptions and prints out errors accordingly
    def raise_exception(self, exception):
        try:
            raise exception
        except LoadError:
            sys.stderr.write("\nLoadError: Unable to load files! Check that files are in the working directory/are not corrupted!\n\n")
        except IDError:
            sys.stderr.write("\nIDError: Product does not exist!\n")
        except ValueError:
            sys.stderr.write("\nValueError: Value entered is invalid. The rate must be a positive number (integer or float)!\n")
        except QuantityError:
            sys.stderr.write("\nQuantityError: Quantity entered is invalid. The quantity must be a postive integer.\n")
        except CustomerError:
            sys.stderr.write("\nCustomerError: New customers cannot order free items!\n")
        except PriceError:
            sys.stderr.write("\nPriceError: Product price has not been set!\n")
        except OutofStockError:
            sys.stderr.write("\nOutofStockError: Product is out of stock!\n")
        except StockError:
            sys.stderr.write("\nStockError: Insufficient stock to fulfil order!\n")
        except ZeroQuantityError:
            sys.stderr.write("\nZeroQuantityError: Cannot order 0 amount of product!\n")
        except ChoiceError:
            sys.stderr.write("\nChoiceError: User input not part of the available choices!\n")
        except LimitError:
            sys.stderr.write("\nLimitError: The discount rate cannot exceed 100%!\n")
        except NonIntegerError:
            sys.stderr.write("\nNonIntegerError: The input must be an integer!\n")
# --------------------------------------------------------------------------------------


# --------- #
# Front End
# --------- #

# This class will contain all user iteraction code and obtain any required user inputs
class MenuUI:
    menu = Menu()
    
    def run_manager(self):
        customer_file = None
        product_file = None

        try: # checks the command line arguements for any filenames that have been provided by the user
            customer_file = sys.argv[1]
            product_file = sys.argv[2]
        except: # if no files are given, it will use the customers.txt and products.txt files by default
            customer_file = "customers.txt"
            product_file = "products.txt"

        try: # checks for the customer and product files. 
            self.menu.record.readCustomers(customer_file)
            self.menu.record.readProducts(product_file)
        except: # raises an exception if one or more of the files cannot be found and will terminate the program
            self.menu.raise_exception(LoadError)
        else:   
            choice = self.menu_choice() # obtains the users menu choice
            
            while choice != "0":
                if choice == "1":
                    order_input = self.enter_new_order_menu() # brings up the menu to let the customer load/manually enter orders
                    order_details = None
                    while order_input != "0":
                        if order_input == "1":
                            self.load_order_file() # allows the user to load orders from an order file
                        elif order_input == "2": 
                            order_details = self.enter_order_details_menu() # allows the user to manually enter a new order for a customer (new or existing)
                            if order_details == False: # returns to the main menu if an order was not entered successfully
                                break
                        elif order_input == "3": # prints ID and name of the product that was ordered and shows the change in stock
                            self.display_product_information(order_details) 
                        order_input = self.enter_new_order_menu()
                elif choice == "2": # diplays all the customers (ID and name), the type of customer they are, their discount rate, as well as the total value of all orders made
                    self.menu.record.listCustomers()
                elif choice == "3": # displays all the products (ID and name), the price, as well as the quantity of product left in stock
                    self.menu.record.listProducts()
                elif choice == "4": # display all customer orders (all products and quantities ordered)
                    self.display_all_orders()
                elif choice == "5":
                    self.display_mvc() # displays the most valuable customer
                elif choice == "6": 
                    self.display_mpp() # displays the most popular product
                elif choice == "7": 
                    self.set_discount() # set customer discount rate
                elif choice == "8": 
                    self.set_threshold() # set wholesale customer threshold
                elif choice == "9":
                    self.replenish() # allows the user to replenish all product with stock below the user specified amount up to that amount
                
                choice = self.menu_choice()
            
            self.display_exit_message() # displays an exit message to the user
            self.menu.save_customer_file(customer_file) # updates the customer file based on any changes made by the user (rates/thresholds/new customers etc)
            self.menu.save_product_file(product_file) # updates the product file based on any changed made by the user (stock)

    # this function will print out all the messages and options for the main menu
    def menu_choice(self):
        message = "\n=====================\n"
        message += "  Inventory Manager \n"
        message += "=====================\n"
        message += "[1] Enter a new order\n"
        message += "[2] Display all existing customers\n"
        message += "[3] Display product information for all products\n"
        message += "[4] Display all products (and quantities) ordered for all customers\n"
        message += "[5] Display the most valuable customer\n"
        message += "[6] Display the most popular item\n"
        message += "[7] Set discount rate for a customer\n"
        message += "[8] Set the threshold for a wholesale customer\n"
        message += "[9] Replenish the stock for products\n"
        message += "[0] Exit\n"
        sys.stdout.write(message)
        
        choice = self.str_input("\nEnter an option: ")
        while "[" + choice + "]" not in message: # keeps asking the user for an input until a valid input is given
            self.menu.raise_exception(ChoiceError)
            choice = self.str_input("Please enter a valid choice: ")
        return choice
    
    # this function displays the menu options when the user selects to enter an order
    def enter_new_order_menu(self):
        message = "\n===============\n"
        message += "Enter new order\n"
        message += "===============\n"
        message += "[1] Load orders from an order file\n"
        message += "[2] Enter order details\n"
        message += "[3] Display change in product stock\n"
        message += "[0] Return to main menu\n"
        sys.stdout.write(message)
        
        choice = self.str_input("\nEnter an option: ")
        while "[" + choice + "]" not in message: # keeps asking the user for an input until a valid input is given
            self.menu.raise_exception(ChoiceError)
            choice = self.str_input("Please enter a valid choice: ")
        return choice
    
    # searches for the orders.txt file and asks the user if they want to load all the orders + print out all the order details
    def load_order_file(self):
        filename = self.str_input("Enter a filename (e.g. orders.txt): ")
        while not self.menu.load_file(filename):
            self.menu.raise_exception(LoadError)
            filename = self.str_input("Enter another filename: ")
        
    # reads the orders file and updates the quantity ordered for each customer, the customer total value, as well as the product stock accordingly.
        no_orders = self.menu.readOrders(filename) # stores the number of orders that were present orders file
        orders = self.menu.order_manager.orders
        recent_orders = orders[len(orders)-no_orders:len(orders)] # slice the orders list to give the most recently entered orders

        for order in recent_orders:
            # subsetting the order information
            customer = order.customer
            product = order.product
            quantity = order.quantity

            # calculating the product price based on the customer name and customer type
            if isinstance(customer, WholesaleCustomer):
                total = customer.get_discount(quantity*product.price)
                price = total/quantity
            elif isinstance(customer, RetailCustomer):
                price = customer.get_discount(product.price)
                total = quantity*price
                
            # updating the product stock and customer total value
            product.setStock = product.stock - quantity
            customer.update_total = round(total,2)
            self.display_order_details((customer, product, quantity, price, total))
    
    # This function allows the user to manually enter a new order for both new and existing customers.
    # This function checks the if the customer is new or existing, if a product price is valid, if a product has sufficient stock
    # as well applying any valid discounts. When an order is successfully created, it will print all the information of the order.
    def enter_order_details_menu(self):
        message = "\n===================\n"
        message += "Enter order details\n"
        message += "===================\n"
        sys.stdout.write(message)

        # check if the customer exists or if the customer is an new customer (after creating one)
        customer, new_customer = self.check_customer()
        if customer == False: # exits if customer does not exist and user does not want to create a new customer
            return False
        
        product = self.check_product("Enter product ID or name: ") # checks if price is not set or negative
        if product == False:
            if new_customer: # delete the new customer if the product price is negative or not set and returns to the main menu
                self.menu.delete_new_customer(customer)
            return False
        else:
            # checks if a new customer is trying to order a free product
            while new_customer and product.price == 0:
                self.menu.raise_exception(CustomerError)
                product = self.check_product("Please enter another product ID or product name: ")
                if product == False: # returns to main menu if the price is not set or negative
                    self.menu.delete_new_customer(customer)
                    return False
                
        # check the quantity ordered and that there is enough stock
        quantity = self.int_input("Enter quantity: ") # checks if the value given by the user is valid
        quantity = self.menu.check_quantity(quantity, product) # checks if there is enough stock
        while not quantity:
            if quantity > product.stock:
                self.menu.raise_exception(StockError)       
            quantity = self.int_input("Please enter a valid quantity: ")
            quantity = self.check_quantity(quantity, product)

        # updating the product stock if a valid quantity was given
        product.setStock = product.stock - quantity
        
        # checking if the customer is new or is an existing one and applies discounts appropriately 
        if new_customer:
            price = product.price
            total = price*quantity
        else:
            if isinstance(customer, WholesaleCustomer): # checks if the customer is a Wholesale customer
                total = customer.get_discount(quantity*product.price) # the discounts for wholesale customers apply to the total value of the order, not the individual products
                price = total/quantity # calculate the unit price after the discount has been applied
            else:
                price = customer.get_discount(product.price) # Retail customers have the discounts applied to the individual products
                total = quantity*price

        # updates the total value that a customer has orderd
        customer.update_total = total
        # adds the order to the list of orders
        self.menu.order_manager.add_order(customer, product, quantity)
        # displays the order details 
        self.display_order_details((customer, product, quantity, price, total))

        return (customer, product, quantity, price, total)
    
    # displays that customer name, the product, the quantity order, the unit price (with discount applied if eligible), as well as the total value of the order
    def display_order_details(self, order_details):
        message = "\n========================\n"
        message += "Displaying order details\n"
        message += "========================\n"
        sys.stdout.write(message)
        
        # setting the order information into their own variables for readability
        customer = order_details[0]
        product = order_details[1]
        quantity = order_details[2]
        price = order_details[3]
        total = order_details[4]

        sys.stdout.write(customer.name + " purchased " + str(quantity) + " x " + product.name + "\n")
        sys.stdout.write("Unit price: $%.2f\n" % price)
        sys.stdout.write("Total price: $%.2f\n" % total)
        sys.stdout.write("Remaining Stock: " + str(product.stock) + "\n")
            
    # takes the manually entered order and displays the remaining product stock
    def display_product_information(self, order_details):
        message = "\n=========================\n"
        message += " Change in product stock\n"
        message += "=========================\n"
        sys.stdout.write(message)
        
        # lets the user know that no order has been manually entered
        if order_details == None:
            sys.stdout.write("Message: No order has been manually entered. Please manually enter a new order first!\n")
        else:
        # display the product ID, name, stock before the order, and the remaining stock
            product = order_details[1]
            quantity = order_details[2]

            sys.stdout.write("Product ID: " + product.ID + "\n")
            sys.stdout.write("Product Name: " + product.name + "\n")
            sys.stdout.write("Previous Stock: " + str(product.stock + int(quantity)) + "\n")
            sys.stdout.write("Remaining Stock: " + str(product.stock) + "\n")

    # this method displays all products ordered (and quantities including 0) orderd by all the customers
    # it also displays the total value of all orders (present) made by customers
    # the number of orders containing a particular product as well as the total quantity of product that was orderd will be displayed
    def display_all_orders(self):
        message = "\n================================\n"
        message += " Displaying all customer orders\n"
        message += "================================\n"
        sys.stdout.write(message)

        # create a list of all the product IDs
        product_ids = []
        for product in self.menu.record.products:
            product_ids.append(product.ID)

        # stores the dictionary of all customers and the quantity of products ordered to a variable
        order_record = self.menu.customer_orders()

        # setting the format of the table to be printed and sets the header
        display_format = "{:<10}"+"{:<5}"*len(product_ids)+"{:<10}"+"\n"
        header = display_format.format(" "*10, *product_ids, "Total")
        sys.stdout.write(header)

        # this row format is specific to the rows with customer names due to the .2f for the total
        row_format = "{:<10}"+"{:<5}"*len(product_ids)+"${:<10.2f}"+"\n"

        # loops through the dictionary to print out the quantity of each product ordered by each of the customers
        for customer in order_record.keys():
            products = order_record[customer].values()
            row = row_format.format(customer.name, *products)
            sys.stdout.write(row)

        # printing the seperators
        seperators = ["_"*5]*(len(product_ids)+1)
        row = display_format.format("_"*10, *seperators)
        sys.stdout.write(row)

        # printing the number of orders containing each product
        orderNum = self.menu.orderNum()
        row = display_format.format("OrderNum", *orderNum.values())
        sys.stdout.write(row)

        # printing the total quantity of a product that has been ordered
        orderQty = self.menu.orderQty()
        row = display_format.format("OrderQty", *orderQty.values())
        sys.stdout.write(row)

    # displays the most valuable customer (mvc)
    def display_mvc(self):
        message = "\n=======================================\n"
        message += " Displaying the most valuable customer\n"
        message += "=======================================\n"
        sys.stdout.write(message)

        mvc = self.menu.determine_mvc()

        sys.stdout.write("Customer ID: " + mvc.ID + "\n")
        sys.stdout.write("Customer name: " + mvc.name + "\n")
        sys.stdout.write("Total value: $" + str(mvc.total) + "\n")

    # displays the most popular product (mpp)
    def display_mpp(self):
        message = "\n=====================================\n"
        message += " Displaying the most popular product\n"
        message += "=====================================\n"
        sys.stdout.write(message)

        orderNum = self.menu.orderNum()

        mpp, most_orders = self.menu.determine_mpp(orderNum)

        if most_orders == 0: # checks to see if any orders have been made, if no orders, a message will be printed
            sys.stdout.write("Message: No orders have been made for any products. Unable to determine most popular product.\n")
        else:
            sys.stdout.write("Product ID: " + mpp.ID + "\n")
            sys.stdout.write("Product name: " + mpp.name + "\n")
            sys.stdout.write("Product price: $" + str(mpp.price) + "\n")
            sys.stdout.write("Times ordered: " + str(most_orders) + "\n")

    # displays the exit message
    def display_exit_message(self):
        message = "\nMessage: Terminating program....updating customer and product files....\n\n"
        sys.stdout.write(message)

    # sets a customers discount rate
    def set_discount(self):
        message = "\n===================\n"
        message += " Set discount rate\n"
        message += "===================\n"
        sys.stdout.write(message)

        customer_detail = self.str_input("Enter customer ID or name: ")
        customer = self.menu.record.findCustomers(customer_detail)

        # checks that the customer exists and keeps asking until a valid customer is entered
        while customer == None:
            sys.stdout.write("Customer does not exist. Please enter another customer ID or name.\n")
            customer_detail = self.str_input("Enter a valid customer ID or name: ")
            customer = self.menu.record.findCustomers(customer_detail)
        
        rate = self.float_input("Enter new discount rate: ")

        # checks that a valid input is given (non-negative, not greater than 100, and is a number)
        while (not rate) or (float(rate) > 100):
            # check that discount is not greater than 100%           
            if float(rate) > 100:
                self.menu.raise_exception(LimitError)
            rate = self.float_input("Please enter a valid rate: ")

        # updates the customers discount rate and lets the user know that the discount rate has been successfully changed
        customer.setRate = rate
        sys.stdout.write("\nMessage: Discount rate for customer " + customer.name + " (Customer ID: " + customer.ID + ") has been changed to " + str(rate) + "%.\n")
    
    # sets the threshold amount for a wholesale customer
    def set_threshold(self):
        message = "\n==================================\n"
        message += " Set wholesale customer threshold\n"
        message += "==================================\n"
        sys.stdout.write(message)

        customer_detail = self.str_input("Enter customer ID or name: ")
        customer = self.menu.record.findCustomers(customer_detail)

        # checks that the customer exists and is a Wholesale customer
        while (customer == None) or (not isinstance(customer, WholesaleCustomer)):
            if customer == None: 
                sys.stdout.write("Customer does not exist. Please enter another customer ID or name.\n")
            elif not isinstance(customer, WholesaleCustomer):
                sys.stdout.write("Customer is not a Wholesale customer. Please enter another customer ID or name.\n")
            customer_detail = self.str_input("Enter a valid customer ID or name: ")
            customer = self.menu.record.findCustomers(customer_detail)

        threshold = self.float_input("Enter new threshold: ")

        # checks that the value given is a number and is non-negative
        while not threshold:
            threshold = self.float_input("Please enter a valid number: ")

        # updates the Wholsale customers threshold and lets the user know that the threshold has been successfully updated
        customer.setThreshold = threshold
        sys.stdout.write("\nMessage: Threshold for customer " + customer.name + " (Customer ID: " + customer.ID + ") has been changed to $" + str(threshold) + ".\n")

    # this method sets the stock of all products to a user specified amount (only if the stock of the product is below the given amount)
    def replenish(self):
        quantity = self.int_input("Enter a value to set the stock: ")

        while not quantity:
            quantity = self.int_input("Please enter a valid quantity: ")

        for product in self.menu.record.products:
            if product.stock < quantity: # checks if the current product stock is less than the replenished amount
                product.setStock = quantity # only changes if the if statment above is satisfied

    # check that a customer exists and ask the user if they want to create a new one if the customer does not exist
    def check_customer(self):
        customer_detail = self.str_input("Enter customer ID or name: ")
        customer = self.menu.record.findCustomers(customer_detail)
        # asks the user if they want to create a new customer if the customer does not exist
        if customer == None:
            message = "Customer does not exist. Do you wish to create a new customer [Y]/[N]?: "
            choice = self.str_input(message)
            while "[" + choice + "]" not in message:
                self.menu.raise_exception(ChoiceError)
                choice = self.str_input("Please enter a valid input: ")
            # gets the customer details using the function and creates a new customer
            if choice == "Y":
                return self.get_customer_details(), True # True here is to indicate that the customer is new
            # Goes back the main menu if the user does not want to create a new customer
            else:
                sys.stdout.write("\nMessage: Unable to proceed with order if customer does not exist. Returning to main menu. \n")                    
                return False, False
        else:
            # returns the customer object (containing all the info about the customer)
            return customer, False # False is to indicate that the customer is not new

    # checks if the product exists, if the product is in stock, and if the price of the product has been sent or is negative
    def check_product(self, prompt):
        product_detail = self.str_input(prompt)
        product = self.menu.record.findProducts(product_detail)
        
        # checks if the product exists, if not, ask for another product ID until an existing one is selected
        while product == None or product.stock == 0:
            if product == None:
                self.menu.raise_exception(IDError)
            elif product.stock == 0:
                self.menu.raise_exception(OutofStockError)
            product_detail = self.str_input("Please choose another product: ")
            product = self.menu.record.findProducts(product_detail)    
            
        # checks if the product has a valid price, if not, it will return false and will return to the main menu
        if product.price < 0 or product.price == None:
            self.menu.raise_exception(PriceError)
            sys.stdout.write("\nMessage: Returning to the main menu.\n")
            return False
        
        return product

    # obtains the new customers details and creates a new customer + returns the customer object
    def get_customer_details(self):
        message = "\n=====================\n"
        message += " Create new customer\n"
        message += "=====================\n"
        sys.stdout.write(message)
        
        name = self.str_input("Enter customer name: ")
        category = self.str_input("Retail or Wholesale customer (R/W)?: ")
        
        # generates a unique ID for the customer
        for id in range(0,1000):
            if self.menu.record.findCustomers(str(id)) == None: # checks that no existing customer has that ID
                customer_id = str(id)
                break
        
        # creates a customer and adds it to the list of customers and lets the user know the customer has been successfully created
        customer = self.menu.create_customer(customer_id, name, category)
        
        # proceeds with obtaining the rest of the order details
        sys.stdout.write("Proceeding with order...\n")
        message = "\n===================\n"
        message += "Enter order details\n"
        message += "===================\n"
        sys.stdout.write(message)
        
        return customer
    
    # this method handles any inputs from the user that are strings/characters
    def str_input(self, prompt):
        sys.stdout.write(prompt)
        sys.stdout.flush()
        user_input = sys.stdin.readline().strip()
        
        # checks that a value was entered by the user
        while len(user_input) == 0:
            sys.stdout.write("Please enter an input: ")
            sys.stdout.flush()
            user_input = sys.stdin.readline().strip()
        return user_input
    
    # this method handles obtaining positive integers for the quantity given by the user
    def int_input(self, prompt):
        user_input = self.str_input(prompt)

        if not user_input.isdecimal(): # checks this statement if it does not contain numbers ONLY (not including decimals)
            if user_input.lower().islower(): # enters this statement if it contains characters
                self.menu.raise_exception(QuantityError)
                return False
            else: # checks this statement if no characters (means special character present)
                try:
                    float(user_input) #tries to convert the input into a float
                except:
                    self.menu.raise_exception(QuantityError)
                    return False
                else:
                    try: # checks that the input is an integer
                        float(user_input) - int(user_input) != 0
                    except:
                        self.menu.raise_exception(NonIntegerError)
                        return False
                    else:
                        if float(user_input) < 0: # checks if the input is negative
                            self.menu.raise_exception(QuantityError)
                        return False
        # checks these statement if the input contains numbers (ONLY)
        elif int(user_input) == 0:
            self.menu.raise_exception(ZeroQuantityError)
            return False
        else:
            return int(user_input)

    # this method handles taking inputs from the user that are expected to be floats
    def float_input(self, prompt):
        user_input = self.str_input(prompt)

        if user_input.lower().islower(): # enters this statement if it contains characters
                self.menu.raise_exception(ValueError)
                return False
        else: # checks this statement if no characters (means special character present)
            try:
                float(user_input) # tries to convert the input into a float
            except:
                self.menu.raise_exception(ValueError)
                return False
            else:
                if float(user_input) < 0: # checks if the input is negative
                    self.menu.raise_exception(ValueError)
                    return False
            return float(user_input)
# ------------------------------------------------------------------------------------------------

inventory_manager = MenuUI()
inventory_manager.run_manager()