#<-----------MODULES------------>
import sys
import re
import os
from random import choice

#------------PATHS--------------#    
# Saving The Current Working Dir of *File* to Root
root = os.path.dirname(os.path.abspath(__file__))
# Tells Python To Where to Look For modules
sys.path.append(root)
# Changing Current Working Path
os.chdir(root)

#Graph Veiw Module
import statistics

# Error Handling for ModuleNotFoundError
try:
    import pandas as pd , matplotlib.pyplot as plt
    import calendar
    from tabulate import tabulate

except ModuleNotFoundError as e:
    from module import setup
    setup.module_install()
    print("ALL SET , RESTART THE SCRIPT")
    exit(1)


# IMPORTing ALL THE CSV's
books = pd.read_csv(f"{root}\\csv\\books.csv" , index_col="BookID")
user = pd.read_csv(f"{root}\\csv\\user.csv" , index_col="ID")
requests = pd.read_csv(f"{root}\\csv\\requests.csv")
borrow = pd.read_csv(f"{root}\\csv\\borrow.csv")
stats = pd.read_csv(f"{root}\\csv\\statics.csv")
#----------Paths----------------#

class Library:
    #Constructor
    username = None
    def __init__(self):
         person = Library.options(["Admin" , "User"])
         Library.seprator("WELCOME TO NESX LIBRARY")
         Library.username = input("Name : ")
         Library.seprator()
         if person == "Admin":
             Library.admin_menu()
         else:
             Library.user_menu()

    # OUTPUT Beautification
    @staticmethod
    def seprator(heading:bool = None):         
        if heading != None:
            line = "____________________________________________________________"
            print(line)
            if heading == "NESX LIBRARY":
                print(f"\n\t\t   {heading.upper()}")
            elif len(heading) in range(1,8):
                print(f"\n\t\t      {heading.upper()}")
            else:
                print(f"\n{heading}")
            print(f"{line}\n")
        else:
            line = "============================================================"
            print(f"\n{line}\n")

    # Table Beautification
    @staticmethod
    def tablefmt(data:list | dict | pd.DataFrame | pd.Series , index=False) -> tabulate:
        """Formats a Pandas DataFrame or Series as a table.

            Args:
                data: A list, dict, DataFrame, or Series.

            Returns:
                A formatted table as a string.
        """
        if isinstance(data, pd.core.frame.Series):
            table = tabulate(data.to_frame() , headers=["Attribute" , "Value"], showindex=index, tablefmt="presto")
        elif isinstance(data , pd.core.frame.DataFrame):
            table = tabulate(data , headers="keys", showindex=index , tablefmt="presto")
        elif isinstance(data, dict):
            table = tabulate(data , headers="keys", showindex=index , tablefmt="presto")
        elif isinstance(data, list):
            # data = dict(enumerate(data , start=1))
            table = tabulate(data , headers=["Search Result"], showindex=index , tablefmt="presto")
        else:
            print("Please make sure *data* is DataFrame , Series , Dict")
            return
        return table

    #Option Genrator
    @staticmethod
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

        def selection():
            option_dict = dict(enumerate(options,start=1))
            for key,value in option_dict.items():
                print(f"[{key}] {value}")
            Library.seprator()
            try:
                choice = int(input("Select : "))
            except ValueError:
                Library.seprator()
                print("ValueError Enter Integer Only!!")
                return
            Library.seprator()
            result = option_dict.get(choice,"\nPlease Enter Right Number")
            if result != "\nPlease Enter Right Number":
                return result
            else:
                print(f"{result}\n")
                return selection()
        return selection()

    # table selector
    @staticmethod
    def selection(table: pd.Series = None) -> list:
        """uses global to build reverse relation between keys and values"""
        tables = {"Books":books,"User":user,"Borrow":borrow ,"Request":requests}
        if table is None:
            return tables.get(Library.options(tables), books)
        else:
            # Convert variable name to string using globals()
            var_name_str = [name for name, value in globals().items() if value is table]
            return var_name_str
    
    #searching...
    @staticmethod
    def search(table:pd.DataFrame =None, column:str =None, item_search:str =None, display:bool =False):
        """
        args:
            table:pd.DataFrame, column:str, item_search:str, display:bool
        process: This Function search the item in One particular column if column not specified it asks
        for column name(do same in case of table , item). if the display = True then the result matching
        the query will be shown. default:False (will not be shown)
        """
        table , column = Library.null_handler(table,column)
        if item_search is None: 
            try:   
                item_search = input(f"Enter {column} : ")
            except:
                print("ValueError: Please Enter Integer Only")
                return
        Library.seprator()
        match = [item for item in table[column] if re.search(item_search ,item ,re.IGNORECASE)]
        if display: #Check If Display = True
            if match: #if
                for i in match:
                    print(i)
            else:
                print("No Match Found For The Book.")
    
    # Suggestion
    @staticmethod
    def suggest() -> str:
        Library.seprator()
        print(f"Suggestation : {choice(books['Title'].tolist())}")
        Library.seprator()
    
    #subscription Checker
    @staticmethod
    def subs(name: str = None) -> str:
        if name is not None:
            match = Library.search(table=user,column="first_name" ,item_search=name)
            if match:
                name_index = user.index[user["first_name"]==name].tolist()[0]
                print(f"Your Subscription will end on : {user.loc[name_index , 'subscription_status']}")
            else:
                print(f"Your Subscription will end on : {choice(user['subscription_status'].tolist())}")
        else:
            print("ValueError")

    # Return Dtype of pandas Objects
    @staticmethod
    def dtype(table:pd.DataFrame=None,column:str=None , Index=None):
        try:
            if table[column].dtype == "object":
                value = input(f"Enter {column} : ") or None
            elif table[column].dtype == "int64":
                value = int(input(f'Enter {column} : '))
            elif table[column].dtype == "float64":
                value = float or str(input(f'Enter {column} : '))
            if value=="":
                value = table.at[Index,column]
        except ValueError:
            print("Incorrect Input Type For Int or Float64 Type Value")
            value = table.at[Index,column]
        finally:
            return value

    # Make Requests for New Book
    @staticmethod
    def request(table: pd.DataFrame = None) -> None:
        Library.seprator()
        book_request = input("Book Name : ")
        if book_request not in table["Title"].tolist():
            new_row = {'Title': book_request , "By User": Library.username}  # Create a dict W new row data
            new_request = pd.DataFrame([new_row])  # Create a DataFrame with the new row
            request = pd.concat([table, new_request], ignore_index=True)  # Concatenate the DataFrames
            Library.seprator("Done!!")
            request.to_csv(f"{root}\\csv\\requests.csv")
        else:
            print(f'{book_request} is Already Available!')

    #Edit Value from CSV
    @staticmethod
    def edit(table: pd.DataFrame =None):
        """Uses pd.dataframe.at[] to change the value in csv and save it
        """
        table , column = Library.head_tail(table ,column="False")
        Library.seprator()
        try:
            index = int(input("Enter Index Number : "))
        except ValueError:
            Library.seprator()
            print("ValueError: Please Enter Intger Only")
            return
        table_name = Library.selection(table)
        if index in table.index:
            for cols in table.columns.tolist():
                value = Library.dtype(table, cols, index)
                table.at[index,cols] = value
            Library.seprator("Done!")
            table.to_csv(f"{root}\\csv\\{table_name[0]}.csv")
            return Library.admin_menu()
        else:
            print("Please Enter Valid Index Number!!")
            
    # Delete Value from CSV
    @staticmethod
    def delete(table:pd.DataFrame =None, choice:bool =False):
        table , column = Library.head_tail(table , column="False")
        Library.seprator()

        try:
            index = int(input("Enter Index Number : "))
        except ValueError:
            Library.seprator()
            print("ValueError: Please Enter Intger Only.")
            return

        table_name = Library.selection(table)
        if index in table.index:
            for position in table.index:
                if position == index:
                    table = table.drop(index ,axis=0)
                    Library.seprator("Done!")
                    table.to_csv(f"{root}\\csv\\{table_name[0]}.csv")
        else:
            print("Please Enter Valid Index Number!!")
            delete()

    #Give Starting or Ending Values
    @staticmethod   
    def head_tail(table:pd.DataFrame =None , column:str =None):
        table , column = Library.null_handler(table,column)
        if choice:
            #head tail here refers to the head and tail of pandas
            print("View Starting[head] or Ending[Tail] Values?\n")
            head_or_tail = Library.options(["Head","Tail"])
            
            try:
                how_much = input(f"Number of {head_or_tail} Values : ")
                how_much = int(how_much)
            except:
                how_much = 5

            Library.seprator()
            if head_or_tail == "Head":
                print(table.head(how_much))
            else:
                print(table.tail(how_much))
        return table , column
    
    #Handles Null Value if table and Column is not specified
    @staticmethod
    def null_handler(table:pd.DataFrame =None,column:str =None):
        if table is None and column is None:
            table = Library.selection()
            column = Library.options(table.columns.tolist())
            return table , column
        elif table is None:
            table = Library.selection()
            if column == "False":
                column= table.iloc[:,0]
                return table , column
            else:
                return table
        elif column is None:
            column = Library.options(table.columns.tolist())
            return column
        else:
            return table , column

    # User Menu Recursion
    @staticmethod
    def user_menu():     
        user_options = [
            "View Available Books",
            "Check availability a Book",
            "Request Addition of a New Book",
            "Check Your Library Subscription",
            "Contact Library Staff",
            "Exit"]

        option = Library.options(user_options) #option function
        if option:
            if option != "Exit":
                if option == "View Available Books":
                    all_books = books["Title"]
                    print(Library.tablefmt(all_books , index=True))
                    Library.seprator()               
                elif option == "Check availability a Book":
                    Library.search(table=books , column="Title" , display=True)
                elif option =="Request Addition of a New Book":
                    Library.request(table=requests)             
                elif option == "Check Your Library Subscription":
                    Library.subs(name=Library.username)              
                elif option == "Contact Library Staff":
                    Library.seprator("CONTACT DETAILS")
                    print("Mail : nesx@hub.com \n\nPhone Number : 69696xxxxx\n\nTele-Phone : 1321-3123-3123")
                    Library.seprator()                
                elif option == "Exit":
                    print("Ty For Visiting!!")
                    Library.seprator()
                    exit(1)
                Library.seprator()
                resume = input("Continue To Menu? [y/n] : ")
                Library.seprator()
                if resume == "n":
                    exit(1)

                Library.user_menu()
        else:
            return
    
    @staticmethod
    def revenue(choice:str =None):
        plot_type = Library.options(['Line-Graph', 'Bar-Graph'])
        statistics.graph(choice , plot_type)
    
    # Admin Menu Recursion
    @staticmethod
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
        
        option = Library.options(admin_options) #option function
        if option != "Exit":
            if option == "Add/Remove Book":
                choice = Library.options(["Add a Book" , "Delete a Book"])
                if choice == "Add a Book":
                    Library.request(table=books)
                else:
                    Library.delete(table=books)
            elif option == "Check Books Request":
                print(Library.tablefmt(requests))
            elif option =="Users Fined":
                print(Library.tablefmt(user[["first_name" , "last_name" , "Fine ($)"]]))
            elif option == "Books Borrowed By users":
                borrowed_books = borrow[["user","borrowed"]]
                borrowed_books.index.name = "Index"
                print(Library.tablefmt(borrowed_books , index=True))
            elif option=="Delete Data From [Any]table":
                Library.delete()
            elif option=="Edit Data From [Any]table":
                Library.edit()
            elif option == "Revenue":
                option_list = stats.columns.tolist()[1:]
                choice = Library.options(option_list)
                Library.revenue(choice)
            elif option == "Exit":
                print("Ty For Visiting!!")
                Library.seprator()
                exit(1)
            Library.seprator()
            resume = input("Back To Menu? [y/n] : ")
            Library.seprator()
            if resume == "n":
                exit(1)
            Library.admin_menu()
        else:
            exit(1)

lib = Library()


