# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
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
SHEET = GSPREAD_CLIENT.open('Love_sandwiches')

# sales = SHEET.worksheet('sales') this was to check if the APIs was working
# data = sales.get_all_values()    this was to check if the APIs was working

# print(data)                      this was to check if the APIs was working

def get_sales_data():
   """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """

   while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60.\n")

        data_str = input("Enter your data here: ")
        # print(f"The data provided is{data_str}")

        sales_data = data_str.split(",")   

        if validate_data(sales_data):  #calling the validata data
            print("Data Is Valid")
            break

   return sales_data
    
def validate_data(values):
    """
	Inside the try. converts all string values into integers
	Raise valueError if string cannot be converte into int,
	or if there aren't exactly 6 values.
	"""
# print(values)
    try:
        [int(value) for value in values]
        if len(values) != 6:
             raise ValueError(
                  f"Exactly 6 values required, you provided: {len(values)}"
             )

    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n") 
        return False

    return True

# function that will update the sales spreasheet

# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list data provided
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated successfully.\n")



# # function that will update the surples sheet

# def update_surplus_worksheet(data):
#     """
#     Update surples spreadsheet, add new row with the list data provided
#     """
#     print("Updating surples spreadsheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("Surples worksheet updated successfully.\n")
    

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")



def calculate_surplus_data(sales_row):
    """
    Compare sakes with stock abd canculate the surples fir each item type.

    The surples is define as the sales figure subtracted from the stock.
    - Posititve surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculation surples......\n")
    stock = SHEET.worksheet("stock").get_all_values()
    # pprint(stock)
    stock_row = stock[-1]
    # print(stock_row)
    # print(f"Stock_row: {stock_row}")
    # print(f"sales_row: {sales_row}")
    surples_data = []
    for stock, sales in zip(stock_row, sales_row):
        surples = int(stock) - sales
        surples_data.append(surples)
    # print(surples_data)
    
    return surples_data

def get_last_5_entries_Sales():
    """
    Collects collumns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data 
    as a list of list.
    """

    sales = SHEET.worksheet("sales")
    # column = sales.col_values(3)
    # print(column)

    collumns = []
    for ind in range(1, 7):
        #print(ind)
        collumn = sales.col_values(ind)
        collumns.append(collumn[-5:]) # slice [-5] to get only the last 5 entry of the list.
    # pprint(collumns)

    return collumns

def calculate_stock_data(data):
    """
    Calculate the average of each item type, adding 10%
    """
    print("Calculating stock data..... \n")
    new_stock_data = []

    for collumn in data:
        int_collumn = [int(num) for num in collumn]
        average = sum(int_collumn) / len(int_collumn)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data



def main():

    data = get_sales_data()
    # print(data) to confirm if is working
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_collumns = get_last_5_entries_Sales()
    stock_data = calculate_stock_data(sales_collumns)
    update_worksheet(stock_data, "stock")
  

print("Welcome to Love Sandwiches Data Automation.\n")
main()



