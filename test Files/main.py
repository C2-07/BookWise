#Changing current working directory...
import sys , os , keyboard
# Saving The Current Working Dir of *File* to Root
root = os.path.dirname(os.path.abspath(__file__))
# Tells Python To Where to Look For modules
sys.path.append(root)
# Changing Current Working Path
os.chdir(root)

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
user = pd.read_csv(f"{root}\\csv\\user.csv")
request = pd.read_csv(f"{root}\\csv\\requests.csv")
borrow = pd.read_csv(f"{root}\\csv\\borrow.csv")
stats = pd.read_csv(f"{root}\\csv\\statics.csv")


plt.figure(figsize=[14,7],facecolor="black", frameon=True)
# Get the figure manager and toggle fullscreen mode
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()

month = list(calendar.month_name[1:])
plt.style.use("dark_background")
plt.plot(stats["Total"] ,linestyle="dotted" ,marker="o",color="red" , label="Growth")
plt.title("Library's Revenue in 2023" , fontsize=20)
plt.ylabel("Total Revenue" , labelpad=10 , fontsize=15)
plt.xlabel("Months" , labelpad=10 ,fontsize=18)
plt.tight_layout(pad=2)
plt.autoscale(enable=True)
plt.legend()
plt.xticks(range(len(month)), month , rotation=15)
plt.grid(True,linewidth=0.2)
plt.show(block=False) 
plt.pause(5)
plt.close("all")

class User:
    person = None 
    def seprator(self, heading=None):
         
        if heading != None:
            lines = "__________________________________________________"
            print(lines)
            if heading == "NESX LIBRARY":
                print(f"\n\t\t    {heading.upper()}")
            elif len(heading) in range(1,8):
                print(f"\n\t\t       {heading.upper()}")
            else:
                print(f"\n{heading}")
            print(f"{lines}\n")
        else:
            lines = "=================================================="
            print(f"\n{lines}\n")

    # Table Beautification
    def tabulate_table_convert(self ,data):
        if isinstance(data, pd.core.frame.Series):
            table = tabulate(data.to_frame() , headers=["Attribute" , "Value"], showindex=False, tablefmt="pretty")
        elif isinstance(data , pd.core.frame.DataFrame):
            table = tabulate(data , headers="keys", showindex=False , tablefmt="pretty")
        elif isinstance(data, dict):
            table = tabulate(data , headers="keys", showindex=False , tablefmt="pretty")
        elif isinstance(data, list):
            table = tabulate(data, hearder="values", showindex=False, tablefmt="pretty")
        else:
            print("Please make sure Input's only is DataFrame , Series , Dict")
        return table
    
    # locate index Number of Any Item
    def locate(self, item=None):
        if item != None:
            print("Search Using : \n")
            search_option = self.option(user.column_items)
            
        
    #creates options    
    def option(self , data):
        if isinstance(data, pd.core.frame.Series):
            options = data.index.tolist()
        elif isinstance(data , pd.core.frame.DataFrame):
            options = data.columns.tolist()
        elif isinstance(data, dict):
            options = list(data.keys())
        elif isinstance(data, list):
            options = data
        else:
            print("Please make sure Input's only is DataFrame , Series , Dict")

        def selection():
            keys , values = [] , []
            for i in range(0,len(options)):
                print(f"[{i+1}] {options[i]}")
                keys.append(i+1)
                values.append(options[i])
            options_relation = dict(zip(keys,values))
            self.seprator()
            opt_choice = int(input("\nSelect : "))
            print("")
            self.seprator()
            result = options_relation.get(opt_choice,"\nPlease Enter Right Number")
            if result != "\nPlease Enter Right Number":
                return result
            else:
                return selection()
        return selection()
               
    def table_select(self):
        tables = {"books":books , "user" : user}
        selected_table = self.option(tables) # Returning Selected table "Name" is str
        return tables.get(selected_table , books)

    #search
    def search(self , table_to_search=None):
        if table_to_search is None:
            self.seprator("TABLES")
            table_to_search = self.table_select()
        self.seprator("search")
        print("You want to *SEARCH* Using :\n")
        search_option = self.option(table_to_search.columns.tolist())
        search_item = input(f"\nEnter {search_option} : ")
        if_available = False
        for i in table_to_search[str(search_option)]: # looking for i in {table}.{column_items}
            if search_item == i:
                print(f"\nYes , Book '{search_item}' is Avilable!\n")
                if_available == True
        if if_available==False:
            print(f"\nNo, Book's not Available!")

    def login(self):
        self.seprator("\t    WELCOME TO NESX LIBRARY!")
        print("Login as :")
        opt = self.option(["User" , "Admin"])
        person = "" #input(f"\nEnter The {opt} :\n")
        if opt=="Admin":
            print(f"\nlogged into *SERVER* with Admin Creds")
            return opt
        elif opt== "User" and person != "":
            print(f"Hey , {person}")
            self.seprator()
            return opt
        else:
            return opt

    def subscription_status(self , person):
        if person == "Admin":
            pass            
        else:
            for user in user["id"]:
                index_number = locate()

    def insert(self , csv_name=books):
        columns = csv_name.columns.tolist()
        for cols in columns:
            if "ID" in cols:
                item = int(input(f"Enter {cols} : "))
            else:
                item = input(f"Enter {cols} : ")
            csv_name[cols]= item
        csv_name.to_csv("requests.csv")
    def delete(self):
        bookid = int(input("Enter BookID : "))
        if bookid:
            for bookid in books.index:
                if bookid == bookid:
                    book = books.drop(bookid ,axis=0)
                    self.seprator("Done!")
                    book.to_csv("books.csv")
                    return
        else:
            print("Please Enter Valid BookID!")
            delete()
    def profit(self , opt):
        self.seprator("Data Representation Format :")
        choice = self.option(["Line-Graph","Bar-Graph", "Histogram"])
        if choice == "Line-Graph":
            pass
        elif choice == "Bar-Graph":
            pass
        else:
            pass
        
    def user_menu(self):         
        user_options = [
            "View Available Books",
            "Search for a Book",
            "Request Addition of a New Book",
            "Check Library Subscription",
            "Check Late Submission Fines",
            "Library Hours and Location",
            "Contact Library Staff",
            "Exit"]

        opt = self.option(user_options) #option function
        if opt:
            if opt != "Exit":
                if opt == "View Available Books":
                    all_books = books["Title"]
                    print(self.tabulate_table_convert(all_books))
                    self.seprator()               
                elif opt == "Search for a Book":
                    self.search(books)
                    self.seprator()                
                elif opt =="Request Addition of a New Book":
                    self.insert(request)
                    self.seprator()                
                elif opt == "Check Library Subscription":

                    self.seprator()                
                elif opt == "Check Late Submission Fines":
                    self.seprator()                
                elif opt == "Library Hours and Location":
                    self.seprator()                
                elif opt == "Contact Library Staff":
                    self.seprator("CONTACT DETAILS")
                    print("""
                    Mail : nesx@hub.com
                    
                    Phone Number : 69696xxxxx

                    Tele-Phone : 1321-3123-3123
                    """)
                    self.seprator()                
                elif opt == "Exit":
                    print("Ty For Visiting!!")
                    self.seprator()
                    exit(1)
                resume = input("Continue To Menu? (y/n) : ")
                if resume == "n":
                    exit(1)

                self.user_menu()
        else:
            return

    def admin_menu(self):
        admin_options = [
            "Add New Book",
            "Remove Book",
            "View All Books",
            "View Earnings & Fines",  
            "View Fines",
            "Library stats",
            "Exit"]
        
        opt = self.option(admin_options) #option function
        if opt != "Exit":
            if opt == "Add New Book":
                self.insert()
                self.seprator()                
            elif opt == "Remove Book":
                self.delete()
            elif opt =="View All Books":
                all_books = books["Title"]
                print(self.tabulate_table_convert(all_books))
                self.seprator()
            elif opt == "View Borrowed Books":
                borrowed_books = borrow[["user","borrowed"]]
                print(self.tabulate_table_convert(borrowed_books))
                self.seprator()
            elif opt == "View Earnings & Fines":
                pass
            elif opt == "Library stats":
                pass
            elif opt == "Exit":
                print("Ty For Visiting!!")
                self.seprator()
                exit(1)
            resume = input("Continue To Menu? (y/n) : ")
            if resume == "n":
                exit(1)
            self.admin_menu()
        else:
            exit(1)
        
    def statics(self):
        stats_options = [
            "View Growth",
            "View Profit",
            "Back"]
        
        opt = self.option(stats_options) #option function
        if opt == "Back":
            self.seprator()
            return self.admin_menu()
        else:
            return self.graph(opt)
        resume = input("Continue To Menu? (y/n) : ")
        if resume == "n":
            exit(1)
        else:
            return self.statics()

    def graph(self, opt : str):
        Representation_type = rt = self.option(["Line-Graph" , "Bar-Graph" , "Histogram"])
        if rt == "Line-Graph":
            if opt == "View Growth":
                plt.plot(user)
                plt.show()
        elif rt == "Bar-Graph":
            pass
        else:
            pass
        
        return self.statics()
# user = User()
# person = user.login()
# while True:
#     if person == "Admin":
#         user.admin_menu()
#     else:
#         user.user_menu()


