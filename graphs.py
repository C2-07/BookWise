import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolor

import time
import os
import sys
import configparser
import calendar

# Saving The Current Working Dir of *File* to Root
root = os.path.dirname(os.path.abspath(__file__))
# Tells Python To Where to Look For modules
sys.path.append(root)
# Changing Current Working Path
os.chdir(root)

# Create Config file
config = configparser.ConfigParser()
# Config File for Graph Color
config.read('config.ini')
stats = pd.read_csv(f"{root}\\csv\\statics.csv")

# Accessing Calendar Class Attr Month_name
month_name = calendar.month_name[1:]
# converting str back to dict
month_color = eval(config['color']['colored_month'])

def draw(choice:str=None , plot_type:str =None):
    if plot_type is None:
        print(f'Please specify Correct Plot Type!!')
        return
    
    if True:
    #if Not None Then Continue    
        if plot_type == "Line-Graph":
            plt.figure(figsize=[14,7])
            plt.plot(stats[choice] , label=f'{choice} Revenue' , color ='purple')
            plt.xlabel('Months' , size=14 , labelpad=10)
            plt.ylabel('Revenue [₹]' , size=14 , labelpad=10)
            plt.xticks( np.arange(0,12), month_name)
            plt.legend()
            plt.grid(True, which='both', color='black', linewidth=0.4)
            plt.tight_layout()
            plt.show()
            plt.pause(10) # wait for 10 sec
            plt.close('all')        
        elif plot_type == "Bar-Graph":
            plt.figure(figsize=[14,7])
            plt.bar(month_name, stats[choice], label=f'{choice} Revenue' , color= month_color.values())
            plt.xlabel('Months' , size=14 , labelpad=10)
            plt.ylabel('Revenue[₹]' , size=14 , labelpad=10)
            plt.tight_layout()
            plt.show()
            return


