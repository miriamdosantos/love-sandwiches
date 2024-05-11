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
SHEET = GSPREAD_CLIENT.open(' love')

sales = SHEET.worksheet('sales')

data = sales.get_all_values()

print(data)

def get_sales_data():
    '''
    Get sales figures input from the user
    Run a while loop to collect a valid string of data from the user via the terminal, which must be a string of 6 numbers separted
    by commas. The loop will repeatedly request data, until it is valid.
    '''
    while True:
        print("Please enter sales data from tge last market.")
        print("Data should be six number, separeted by commas.")
        print("Example:10,20,30,40,50,60\n")

        data_str = input("Enter your data here:")
    
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data
  
    
def validate_data(values):
    '''
    Inside the try, converts all string values into integers.
    Raise valueErros if strings cannot be converte into int, or if there arent exatcly 6 values
    '''
    try:
        [int(values) for value in values]
        if len(values) !=6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
            )
        
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False
    return True
    
def update_sales_worksheet(data):
    '''
    Update sales worsheet, add row with the list data provided.
    '''
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheets("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet update succesfuly.\n")

def calculate_surplus_dat(sales_row):
    '''
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure substracde from the stock:
    -Positive surplis indicates waste
    - Negative surplus indicates extra made when stock was sold out.

    '''
    print("Calculating surplus data... \n")
    stock = SHEET.worksheet("STOCK").get_all_values()
    stock_row = stock[-1]
    print(stock_row)


def main():
    '''
    Run all program functions
    '''
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)

print("Welcome to Love Sandwiches Data Automation")
main()