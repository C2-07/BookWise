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

value = int(input(f"Enter : ")) if value else 5
print(value)