# <-----------MODULES------------>
import sys
import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
from art import *

# ------------PATHS--------------#    
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)

# importing ALL THE CSV
books = pd.read_csv(f"{root}\\csv\\books.csv", index_col="ID")
user = pd.read_csv(f"{root}\\csv\\user.csv", index_col="ID")
requests = pd.read_csv(f"{root}\\csv\\requests.csv", index_col="ID")
borrow = pd.read_csv(f"{root}\\csv\\borrow.csv", index_col="ID")
stats = pd.read_csv(f"{root}\\csv\\stats.csv", index_col="ID")


def update_csv():
    global books, user, requests, borrow, stats
    books = pd.read_csv(f"{root}\\csv\\books.csv", index_col="ID")
    user = pd.read_csv(f"{root}\\csv\\user.csv", index_col="ID")
    requests = pd.read_csv(f"{root}\\csv\\requests.csv", index_col="ID")
    borrow = pd.read_csv(f"{root}\\csv\\borrow.csv", index_col="ID")
    stats = pd.read_csv(f"{root}\\csv\\stats.csv", index_col="ID")


# ----------Paths----------------#


# OUTPUT Beautification
def separator(heading: str = None, decorate = True):
    if heading is not None and decorate is True:
        head = text2art(heading)
        print(f'\n {head}')
        print('-' * 80 + '\n')
    elif heading is not None and decorate is False:
        print(f'\n{heading:-^80}\n')
    else:
        print('\n' + "=" * 80 + '\n')


# Table Beautification
def tablet(data: list | dict | pd.DataFrame | pd.Series, index=False, style='presto') -> tabulate:
    if isinstance(data, pd.core.frame.Series):
        table = tabulate(data.to_frame(), headers=["Attribute", "Value"], showindex=index, tablefmt=style)
    elif isinstance(data, pd.core.frame.DataFrame):
        table = tabulate(data, headers="keys", tablefmt=style)
    elif isinstance(data, dict):
        table = tabulate(data, headers="keys", showindex=index, tablefmt=style)
    elif isinstance(data, list):
        table = tabulate(data, headers=["Search Result"], showindex=index, tablefmt=style)
    else:
        print("Please make sure *data* is DataFrame , Series , Dict")
        return
    return table


# Option Generator
def options(data: list | dict | pd.DataFrame | pd.Series):
    if isinstance(data, pd.core.frame.Series):
        options = data.index.tolist()
    elif isinstance(data, pd.core.frame.DataFrame):
        options = data.columns.tolist()
    elif isinstance(data, dict):
        options = list(data.keys())
    elif isinstance(data, list):
        options = data
    else:
        print("Not a -> DataFrame , Series , Dict")

    def select():
        option_dict = dict(enumerate(options, start=1))
        for key, value in option_dict.items():
            print(f"|{key}| {value}")
        separator()
        try:
            choice = int(input("Select : "))
        except ValueError:
            separator()
            print("ValueError Enter Integer Only!!")
            separator()
            return select()
        separator()
        result = option_dict.get(choice, "\nPlease Enter Right Number")
        if result != "\nPlease Enter Right Number":
            return result
        else:
            print(f"{result}\n")
            return select()

    return select()


# table selector
def tableVarToString(table=None) -> str | None:
    tables = {"Books": books, "User": user, "Borrow": borrow, "Request": requests}
    if table is None:
        print("No Table Inputed")
        return None
    else:
        # Convert variable name to string using globals()
        var_name_str = [name for name, value in globals().items() if value is table]
        return var_name_str[0]


# searching...
def search(table=None, column: str = None, pattern: str = None, display: bool = False, select_result: bool = False):
    if table is None:
        table = table_select(table)
    if column is None:
        column = options(table.columns.tolist())
    separator(' SEARCH ', decorate=False)
    if pattern is None:
        try:
            pattern = input(f"Enter {column} : ")
        except:
            separator()
            raise TypeError('Error : String Only')
            separator()
            return
    separator()
    match = []
    try:
        match = [item for item in table[column] if pattern.lower() in item.lower()]
    except TypeError:
        pass
    if display:  # Check If Display = True
        if match:  # if any match found
            if select_result:
                result_choice = options(match)
                return result_choice
            else:
                for i in match:
                    print(i)
        else:
            print("No Match Found!!")
            return None


# subscription Checker
def subscription(name: str = None):
    if name is not None:
        name_index = user.index[user["first_name"] == name].tolist()[0]
        separator(' SUBSCRIPTION STATUS ', decorate=False)
        if name_index:
            print(f"{name}, Your subscription Status : {user.loc[name_index, 'subscription_status']}")
        else:
            print("You're not a member")
    else:
        print(f"You Don't have Any Subscription as it is a Guest Account!!")


# Return Dtype of pandas Objects
def dataType(table=None, column: str = None, Index=None):
    value = None
    try:
        if table[column].dtype == "object":
            value = input(f"Enter {column} : ") or None
        elif table[column].dtype == "int64":
            value = int(input(f'Enter {column} : '))
        elif table[column].dtype == "float64":
            value = float(input(f'Enter {column} : '))
        if value is None and Index is not None:
            value = table.at[Index, column]
    except ValueError:
        print("\nInput Type Should be Int or Float64\n")
        value = table.at[Index, column]
    finally:
        return value


def addRow(table=None):
    newRow = []
    table = table_select(table)
    csvName = tableVarToString(table=table)
    separator(' EXTEND DATA ', decorate=False)
    try:
        index_name = table.index.name
    except:
        index_name = "ID"
    for col in table.columns.tolist():
        value = dataType(column=col, table=table)
        newRow.append(value)
    print(newRow)
    table.loc[len(table)] = newRow
    if len(newRow) == 1:
        return
    table.index.name = index_name
    table.to_csv(f"{root}\\csv\\{csvName}.csv")
    separator('Done!!')
    table.index.name = 'ID'
    table.index = table.index + 1
    print(tablet(table))
    return table


# Edit Value from CSV
def editRow(table=None, editProfile_of_name=None):
    if editProfile_of_name is None:
        table = head_tail(table)
        separator(' MODIFY ', decorate=False)
        try:
            index = int(input("Enter Index Number : "))
        except ValueError:
            separator()
            print("ValueError: Please Enter Intger Only")
            return
    elif editProfile_of_name is not None:
        # tolist()[0] to assign the first value of list to index value
        index = table[table['first_name'] == editProfile_of_name].index.tolist()[0]
    else:
        print('An Error Occured')
        return

    table_name = tableVarToString(table)
    if index in table.index:
        for cols in table.columns.tolist():
            value = dataType(table, cols, index)
            table.at[index, cols] = value
        table.to_csv(f"{root}\\csv\\{table_name}.csv")
        separator("Done!")
        print(tablet(table))
    else:
        print("Please Enter Valid Index Number!!")


# Delete Value from CSV
def deleteRow(table: pd.DataFrame = None, choice: bool = False):
    table = head_tail(table)
    separator(' DELETE ', decorate=False)
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
                table = table.drop(index, axis=0)
                separator("Done!")
                table.to_csv(f"{root}\\csv\\{table_name}.csv")
                print(tablet(table))
    else:
        print("Please Enter Valid Index Number!!")
        deleteRow(table, choice)


# Give Starting or Ending Values +917978274272
def head_tail(table=None):
    table = table_select(table)
    separator(' HEAD | TAIL ', decorate=False)
    # head tail here refers to the head and tail method of pandas
    head_or_tail = options(["Head", "Tail"])

    try:
        num_of_rows = input(f"Number of {head_or_tail} Values : ")
        num_of_rows = int(num_of_rows)
    except:
        num_of_rows = 5

    separator()
    if head_or_tail == "Head":
        print(tablet(table.head(num_of_rows)))
    else:
        print(tablet(table.tail(num_of_rows)))
    return table


# Handles Null Value if table and Column is not specified
def table_select(table: pd.DataFrame = None):
    if table is None:
        tableDict = {'books': books, 'requests': requests,
                     'user': user, 'statics': stats, 'borrow': borrow}
        choice = options(tableDict)
        table = tableDict.get(choice)
        return table
    else:
        return table


def graphs(choice, plot_type):
    colored_month = {'January': 'lightcoral', 'February': 'steelblue', 'March': 'lavender', 'April': 'chartreuse',
                     'May': 'cyan', 'June': 'fuchsia', 'July': 'cornflowerblue', 'August': 'mediumturquoise',
                     'September': 'whitesmoke', 'October': 'rebeccapurple', 'November': 'crimson',
                     'December': 'lightslategray'}
    month_name = list(colored_month.keys())
    month_color = list(colored_month.values())

    def draw(choice: str = None, plot_type: str = None):
        if plot_type == "Line-Graph":
            plt.figure(figsize=(14, 7))
            plt.plot(stats[choice], label=f'{choice} Revenue', color='purple')
            plt.xlabel('Months', size=14, labelpad=10)
            plt.ylabel('Revenue [₹]', size=14, labelpad=10)
            plt.xticks(np.arange(0, 12), month_name)
            plt.legend()
            plt.grid(True, which='both', color='black', linewidth=0.4)
            plt.tight_layout()
            plt.show()
        elif plot_type == "Bar-Graph":
            plt.figure(figsize=(14, 7))
            plt.bar(month_name, stats[choice], label=f'{choice} Revenue', color=month_color)
            plt.xlabel('Months', size=14, labelpad=10)
            plt.ylabel('Revenue[₹]', size=14, labelpad=10)
            plt.tight_layout()
            plt.show()
            return

    draw(choice, plot_type)


def aggregate(choice):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    opt = options(['Sum', 'Maxium', 'Maxium', 'Average'])
    print(opt, 'Value is :')
    if opt == 'Maxium':
        maximum = max(stats[choice])
        month = months[stats[stats[choice] == maximum].index.tolist()[0]]
        print(f'{month} -> ₹{maximum}')
    elif opt == 'Minimum':
        minimum = min(stats[choice])
        month = months[stats[stats[choice] == minimum].index.tolist()[0]]
        print(f'{month} -> ₹{minimum}')
    elif opt == 'Average':
        average = int(round(sum(stats[choice].tolist()) / 12))
        print(f'Average Revenue : ₹{average}')
    else:
        total = sum(stats[choice].tolist())
        print(f'Year -> ₹{total}')


def revenue():
    opt = options(['Aggregate Functions', 'Visualization'])
    col_choice = options(stats.columns.tolist()[1:])
    if opt == 'Visualization':
        plot_type = options(['Line-Graph', 'Bar-Graph'])
        graphs(col_choice, plot_type)  # graphs Function

    else:
        aggregate(col_choice)


# User Menu Recursion
def user_menu():
    user_options = [
        "View Available Books",
        "Check availability a Book",
        "Request Addition of a New Book",
        "Check Your Library subscription",
        "Contact Library Staff",
        "Search Books by Author Name",
        "Edit Your Profile",
        "Your Profile",
        "Exit"]

    separator(' USER MENU ', decorate=False)
    choice = options(user_options)  # choice function
    if choice == "View Available Books":
        books.index = books.index + 1
        all_books = books["Title"]
        print(tablet(all_books, index=True))
    elif choice == "Check availability a Book":
        result = search(table=books, column="Title", display=True, select_result=True)
        if result is not None:
            print(tablet(books[books['Title'] == result]))
    elif choice == "Request Addition of a New Book":
        addRow(table=requests)
    elif choice == "Check Your Library subscription":
        result = search(table=user, column='first_name', select_result=True, display=True)
        subscription(name=result)
    elif choice == "Contact Library Staff":
        separator("CONTACT DETAILS")
        print("Mail : nesx@hub.com \n\nPhone Number : 69696xxxxx\n\nTele-Phone : 1321-3123-3123")
    elif choice == "Search Books by Author Name":
        result = search(table=books, display=True, column='Author', select_result=True)
        print(tablet(books[books['Author'] == result]))
    elif choice == "Edit Your Profile":
        result = search(table=user, display=True, select_result=True, column='first_name')
        print(tablet(user[user['first_name'] == result]))
        if result is not None:
            editRow(table=user, editProfile_of_name=result)
    elif choice == "Your Profile":
        result = search(table=user, display=True, select_result=True, column='first_name')
        if result is not None:
            print(tablet(user[user['first_name'] == result]))
    elif choice == "Exit":
        print(text2art("Bybye, Thank You!!"))
        separator()
        exit(1)
    separator()
    resume = input("Continue To Menu? [Y/N] : ")
    separator()

    update_csv()  # Updating CSV
    if resume in 'nN':
        exit(1)
    user_menu()


# Admin Menu Recursion
def admin_menu():
    admin_options = [
        "Revenue",
        "Users Fined",
        "Add/Remove Book",
        "Check Books Request",
        "Add Data into [Any]table",
        "Edit Data From [Any]table",
        "Delete Data From [Any]table",
        "Books Borrowed By users",
        "Exit"]
    separator(' ADMIN MENU ', decorate=False)
    choice = options(admin_options)  # choice function
    if choice == "Add/Remove Book":
        choice = options(["Add a Book", "Delete a Book"])
        if choice == "Add a Book":
            addRow(table=books)
        else:
            deleteRow(table=books)
    elif choice == "Add Data into [Any]table":
        addRow()
    elif choice == "Check Books Request":
        print(requests)
    elif choice == "Users Fined":
        user.index.name = 'Index'
        user.index = user.index + 1
        print(tablet(user[["first_name", "last_name", "Fine ($)"]]))
    elif choice == "Books Borrowed By users":
        borrowed_books = borrow[["user", "borrowed"]]
        borrowed_books.index.name = "Index"
        print(tablet(borrowed_books))
    elif choice == "Delete Data From [Any]table":
        deleteRow()
    elif choice == "Edit Data From [Any]table":
        editRow()
    elif choice == "Revenue":
        revenue()
    elif choice == "Exit":
        print(text2art("Bybye, Thank You!!"))
        separator()
        exit(1)
    separator()
    resume = input("Back To Menu? [Y/N] : ")
    separator()

    update_csv()  # Updating CSV
    if resume in "nN":
        exit(1)
    admin_menu()


if __name__ == '__main__':
    update_csv()
    separator()
    person = options(["Admin", "User"])
    separator("WELCOME")
    username = input("Name : ")
    username = None if username == '' else username
    if person == "Admin":
        admin_menu()
    else:
        user_menu()
