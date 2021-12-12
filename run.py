import gspread
from google.oauth2.service_account import Credentials

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


def update_sales_worksheet(data):
    """
    Update sales worksheet, add a new row with the list data provided
    """
    print("Updating sales worksheet....\n")
    sales_worksheet = SHEET.worksheet('sales')#Access sales worksheet from Google gspread sheet
    sales_worksheet.append_row(data) #Appends a new row of data to our Google gspread sales_worksheet
    print("Sales worksheet updated successfully.\n")


data = get_sales_data()
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)
