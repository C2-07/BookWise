#<-----------MODULES------------>
import sys
import re
import os
import csv
from random import choice

#Graph Veiwing Module
import graphs

import pandas as pd
from tabulate import tabulate
from art import *

#------------PATHS--------------#    
# Saving The Current Working Dir of *File* to Root
root = os.path.dirname(os.path.abspath(__file__))
# Tells Python To Where to Look For modules
sys.path.append(root)
os.chdir(root)


# IMPORTing ALL THE CSV's
books = pd.read_csv(f"{root}\\csv\\books.csv" , index_col="BookID")
user = pd.read_csv(f"{root}\\csv\\user.csv" , index_col="ID")
requests = pd.read_csv(f"{root}\\csv\\requests.csv")
borrow = pd.read_csv(f"{root}\\csv\\borrow.csv")
stats = pd.read_csv(f"{root}\\csv\\statics.csv")
#----------Paths----------------#

# OUTPUT Beautification
def separator(heading: str = None):
    if heading is not None:
        line = text2art(heading)
        print('\n',line)
        print('_'*60 + '\n')
    else:
        print('\n' +"="*60 + '\n')

# Table Beautification
def tablefmt(data:list | dict | pd.DataFrame | pd.Series , index=False , style='presto') -> tabulate:
    """Formats a Pandas DataFrame or Series as a table.

        Args:
            data: A list, dict, DataFrame, or Series.

        Returns:
            A formatted table as a string.
    """
    if isinstance(data, pd.core.frame.Series):
        table = tabulate(data.to_frame() , headers=["Attribute" , "Value"], showindex=index, tablefmt=style , colalign=('right'))
    elif isinstance(data , pd.core.frame.DataFrame):
        table = tabulate(data , headers="keys" , tablefmt=style , colalign=('right'))
    elif isinstance(data, dict):
        table = tabulate(data , headers="keys", showindex=index , tablefmt=style , colalign=('right'))
    elif isinstance(data, list):
        table = tabulate(data , headers=["Search Result"], showindex=index , tablefmt=style , colalign=('right'))
    else:
        print("Please make sure *data* is DataFrame , Series , Dict")
        return
    return table

#Option Genrator
def options(data:list | dict | pd.DataFrame | pd.Series):
    """
    Agrs:
        data:A list , dict , pd.DataFrame , pd.Series

    process:
        convert arg *data* into list then you enumerate to create a dict
        for (key , value) relation. At last using for loop to itrate over dict
    
    Returns:
        A 
    """
    if isinstance(data, pd.core.frame.Series):
        options = data.index.tolist()
    elif isinstance(data , pd.core.frame.DataFrame):
        options = data.columns.tolist()
    elif isinstance(data, dict):
        options = list(data.keys())
    elif isinstance(data, list):
        options = data
    else:
        print("Please make sure *data* is DataFrame , Series , Dict")

    def select():
        option_dict = dict(enumerate(options,start=1))
        for key,value in option_dict.items():
            print(f"[{key}] {value}")
        separator()
        try:
            choice = int(input("Select : "))
        except ValueError:
            separator()
            print("ValueError Enter Integer Only!!")
            separator()
            return select()
        separator()
        result = option_dict.get(choice,"\nPlease Enter Right Number")
        if result != "\nPlease Enter Right Number":
            return result
        else:
            print(f"{result}\n")
            return select()
    return select()

# table selector
def tableVarToString(table: pd.Series = None) -> str:
    """uses global to build reverse relation between keys and values"""
    tables = {"Books":books,"User":user,"Borrow":borrow ,"Request":requests}
    if table is None:
        return tables.get(options(tables), books)
    else:
        # Convert variable name to string using globals()
        var_name_str = [name for name, value in globals().items() if value is table]
        return var_name_str[0]

#searching...
def search(table:pd.DataFrame =None, column:str =None, item_search:str =None, display:bool =False , select_result=False):
    """
    args:
        table:pd.DataFrame, column:str, item_search:str, display:bool
    process: This Function search the item in One particular column if column not specified it asks
    for column name(do same in case of table , item). if the display = True then the result matching
    the query will be shown. default:False (will not be shown)
    """
    if table is None:
        table = table_select(table)
    if column is None:
        column = options(table.columns.tolist())
    if item_search is None: 
        try:   
            item_search = input(f"Enter {column} : ")
        except:
            separator()
            print("ValueError: Please Enter Integer Only")
            separator()
            return
    separator()
    match = [item for item in table[column] if re.search(item_search ,item ,re.IGNORECASE)]
    if display: #Check If Display = True
        if match: #if
            if select_result:
                result_choice = options(match)
                return result_choice
            else:
                for i in match:
                    print(i)
        else:
            print("No Match Found!!")

# Suggestion
def suggest() -> str:
    separator()
    print(f"Suggestation : {choice(books['Title'].tolist())}")
    separator()

#subscription Checker
def subs(name: str = None) -> str:
    if name is None:
        name = search(table=user,column="first_name" , display=True , select_result=True)
        if name is not None:
            name_index = user.index[user["first_name"]==name].tolist()[0]
            print(f"Your subscription will end on : {user.loc[name_index , 'subscription_status']}")
    else:
        print(f"Your subscription will end on : {choice(user['subscription_status'].tolist())}")

# Return Dtype of pandas Objects
def dataType(table:pd.DataFrame=None,column:str=None , Index=None):
    value = None
    try:
        if table[column].dtype == "object":
            value = input(f"Enter {column} : ") or None
        elif table[column].dtype == "int64":
            value = int(input(f'Enter {column} : '))
        elif table[column].dtype == "float64":
            value = float(input(f'Enter {column} : '))
        if value=="" and Index is not None:
            value = table.at[Index,column]
    except ValueError:
        print("Incorrect Input Type For Int or Float64 Type Value\n setting... Default")
        value = table.at[Index,column]
    finally:
        return value

def addRow(table=None):
    newRow = {}
    csvName = tableVarToString(table=table)
    
    for col in table.columns.tolist():
        value = dataType(column=col , table=table)
        newRow[col] = value
        
    newRow_df = pd.DataFrame([newRow])
    table = pd.concat([table, newRow_df], ignore_index=True)
    table.to_csv(f"{root}\\csv\\{csvName}.csv" , index=False)
    separator('Done!!')
    table.index.name = 'Index'
    table.index = table.index + 1
    print(tablefmt(table))
    
#Edit Value from CSV
def editRow(table=None):
    """Uses pd.dataframe.at[] to change the value in csv and save it
    """
    table= head_tail(table)
    separator()
    try:
        index = int(input("Enter Index Number : "))
    except ValueError:
        separator()
        print("ValueError: Please Enter Intger Only")
        return
    table_name = tableVarToString(table)
    if index in table.index:
        for cols in table.columns.tolist():
            value = dataType(table, cols, index)
            table.at[index,cols] = value
        table.to_csv(f"{root}\\csv\\{table_name}.csv")
        print(tablefmt(table))
        separator("Done!")
        
        return admin_menu()
    else:
        print("Please Enter Valid Index Number!!")

# Delete Value from CSV
def deleteRow(table:pd.DataFrame =None, choice:bool =False):
    table = head_tail(table)
    separator()

    try:
        index = int(input("Enter Index Number : "))
    except ValueError:
        separator()
        print("ValueError: Please Enter Intger Only.")
        return

    table_name = tableVarToString(table)
    if index in table.index:
        for position in table.index:
            if position == index:
                table = table.drop(index ,axis=0)
                separator("Done!")
                table.to_csv(f"{root}\\csv\\{table_name}.csv")
                print(tablefmt(table))
    else:
        print("Please Enter Valid Index Number!!")
        delete(table , choice)

#Give Starting or Ending Values   
def head_tail(table=None):
    table = table_select(table)
    separator()
    #head tail here refers to the head and tail of pandas
    print("View Starting[head] or Ending[Tail] Values?\n")
    head_or_tail = options(["Head","Tail"])

    try:
        num_of_rows = input(f"Number of {head_or_tail} Values : ")
        num_of_rows = int(num_of_rows)
    except:
        num_of_rows = 5

    separator()
    if head_or_tail == "Head":
        print(tablefmt(table.head(num_of_rows)))
    else:
        print(tablefmt(table.tail(num_of_rows)))
    return table

#Handles Null Value if table and Column is not specified
def table_select(table: pd.DataFrame = None):
    if table is None:
        tableDict = {'books':books ,'requests': requests,
                    'user':user, 'statics':stats ,'borrow':borrow}
        choice = options(tableDict)
        table = tableDict.get(choice)
        return table
    else:
        return table

# User Menu Recursion
def user_menu():     
    user_options = [
        "View Available Books",
        "Check availability a Book",
        "Request Addition of a New Book",
        "Check Your Library subscription",
        "Contact Library Staff",
        "Search Books by Author Name",
        "Your Profile",
        "Exit"]

    choice = options(user_options) #choice function
    if choice:
        if choice == "View Available Books":
            all_books = books["Title"]
            print(tablefmt(all_books , index=True))
        elif choice == "Check availability a Book":
            search(table=books , column="Title" , display=True)
        elif choice =="Request Addition of a New Book":
            addRow(table=requests)             
        elif choice == "Check Your Library subscription":
            subs(name=username)              
        elif choice == "Contact Library Staff":
            separator("CONTACT DETAILS")
            print("Mail : nesx@hub.com \n\nPhone Number : 69696xxxxx\n\nTele-Phone : 1321-3123-3123")
        elif choice == "Search Books by Author Name":
            result = search(table=books, display=True ,column='Author')
            print(result)
        elif choice == "Your Profile":
            result = search(table=user, display=True , select_result=True , column='first_name')
            print(tablefmt(user[user['first_name']==result],style='plain'))
        elif choice == "Exit":
            print(text2art("Bybye, Thank You!!"))
            separator()
            exit(1)
                
        separator()
        resume = input("Continue To Menu? [y/n] : ")
        separator()
        if resume == "n":
            exit(1)

        user_menu()
    else:
        return

def revenue(choice:str =None):
    plot_type = options(['Line-Graph', 'Bar-Graph'])
    graphs.draw(choice , plot_type)

# Admin Menu Recursion
def admin_menu():
    admin_options = [
        "Revenue",
        "Users Fined",
        "Add/Remove Book",
        "Check Books Request",
        "Edit Data From [Any]table",
        "Delete Data From [Any]table",
        "Books Borrowed By users",
        "Exit"]
    
    choice = options(admin_options) #choice function
    if choice == "Add/Remove Book":
        choice = options(["Add a Book" , "Delete a Book"])
        if choice == "Add a Book":
            addRow(table=books)
        else:
            deleteRow(table=books)
    elif choice == "Check Books Request":
        print(requests)
    elif choice =="Users Fined":
        print(tablefmt(user[["first_name" , "last_name" , "Fine ($)"]]))
    elif choice == "Books Borrowed By users":
        borrowed_books = borrow[["user","borrowed"]]
        borrowed_books.index.name = "Index"
        print(tablefmt(borrowed_books , index=True))
    elif choice=="Delete Data From [Any]table":
        deleteRow()
    elif choice=="Edit Data From [Any]table":
        editRow()
    elif choice == "Revenue":
        option_list = stats.columns.tolist()[1:]
        choice = options(option_list)
        revenue(choice)
    elif choice == "Exit":
        print(text2art("Bybye, Thank You!!"))
        separator()
        exit(1)
    separator()
    resume = input("Back To Menu? [y/n] : ")
    separator()
    if resume == "n":
        exit(1)
    admin_menu()


if __name__ == '__main__':

    username = None
    separator()
    person = options(["Admin" , "User"])
    separator("WELCOME TO NESX LIBRARY")
    username = input("Name : ")

    username = None if username == '' else username
    
    separator()
    if person == "Admin":
        admin_menu()
    else:
        user_menu()
        
