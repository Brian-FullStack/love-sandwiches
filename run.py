import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales input from the user
    """
    while True:
        #Instructions to the user
        print("Please enter sales data from the last market.")
        print("Data should be six numbers seperated by commas.")
        print("Example: 10,20,30,40,50,60\n") #\n creates a space under the instructions
        #User input
        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",") #.split(",") removes the commas in our data_str input
        
        if validate_data(sales_data):
            print("Data is Valid!")
            break

    return sales_data  


def validate_data(values):
    """
    Inside the try, convert all string values into intergers.
    Raise a ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values
    """
    try:
        [int(value) for value in values] #List Comprehension: for each value in the values list, convert it to an int
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e: #e is python standard for error
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

"""
def update_sales_worksheet(data):
    
    #Update sales worksheet, add a new row with the list data provided
    
    print("Updating sales worksheet....\n")
    sales_worksheet = SHEET.worksheet('sales')#Access sales worksheet from Google gspread sheet
    sales_worksheet.append_row(data) #Appends a new row of data to our Google gspread sales_worksheet
    print("Sales worksheet updated successfully.\n")

def update_surplus_worksheet(data):
    
    #Update surplus worksheet, add a new row with the list data provided
    
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus") #Access the surplus worksheet from Google gspread sheet
    surplus_worksheet.append_row(data) #Appends a new row of data to our Google gspread surplus_worksheet
    print("Surplus worksheet updated successfully.\n")
"""

# ^^ Refactored update worksheet function. Uses one function to do the same work as two
def update_worksheet(data, worksheet):
    """
    Recieves a list of intergers to be added into a worksheet
    Update the relevent worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet")
    worksheet_to_update = SHEET.worksheet(worksheet) #Access relevent worksheet from Google gspread sheet
    worksheet_to_update.append_row(data) #Appends a new row of data to our relevent Google gspread worksheet
    print(f"{worksheet} worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplue indicates waste.
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1] #Gets the last row using the slice method
    
    #Using the zip() method to iterate through two or more lists at the same time.
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales #int() converts the stock into an interger
        surplus_data.append(surplus)
    
    return surplus_data

def get_last_5_entries_sales():
    """
    Collects collumns of data from the sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales") #Access sales worksheet from Google gspread
    # column = sales.col_values() #Get the values of the 3rd column
    # print(column)

    columns = []
    for ind in range(1, 7): #Columns in sales worksheet start at 1. range(start, stop)
        column = sales.col_values(ind)
        columns.append(column[-5:]) #The ":" in the slice operator tells python its a slice and not an index

    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data

def get_stock_values(data):
    """
    Tell the user how much stock to prepare for the next market.
    """
    print("Make the following number of sandwiches for next market:\n")
    headings = SHEET.worksheet("stock").get_all_values()
    headings_row = headings[0]    
    stock_dict = dict(zip(headings_row, data))
    
    print(stock_dict)
    

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    get_stock_values(stock_data)

print("Welcome to Love Sandwiches Data Automation")
main()