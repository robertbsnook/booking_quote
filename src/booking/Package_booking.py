#!/usr/bin/env python
import datetime

import pysnooper
import pandas as pd
import csv
from IPython.display import display
from tabulate import tabulate
from datetime import date,datetime as dt,timedelta


class air:
    def __init__(self,destination,dangerous,urgency):
        self.destination = destination
        self.dangerous = dangerous
        self.urgency = urgency

    def travel_check(self):
        if self.dangerous == "unsafe":
            return False
        elif self.urgency == 'urgent':
            return True

    def air_charge(self,length,width,height,weight):
        if weight*10 > length*width*height*20:
            return weight*10
        else:
            return length*width*height*20

class truck:
    def __init__(self,destination,urgency):
        self.destination = destination
        self.urgency = urgency

    def travel_check(self,length,width,height,weight):
        if self.destination == 'overseas':
            return False
        else:
            return True

    def truck_charge(self):
        if self.urgency == 'urgent':
            return 45
        else:
            return 25



def weight_check(weight):
    if weight > 9.999:
        print("Sorry, but this package weighs too much.  Please reduce the weight to under 10kg")
        return False
    else:
        return True

def size_check(length,width,height):
    if length * width * height > 124.999:
        print("Sorry, but this package is too large to be shipped by our methods.  Please reduce the size to less "
              "than 5x5x5")
        return False
    else:
        return True

def urgent_check(delivery_date):
    due = input("When package is due:")
    year, month, day = map(int, due.split('/'))
    date = datetime.date(year, month, day)
    future = datetime.date.today() + datetime.timedelta(days=3)
    if date > future:
        return "not urgent"
    else:
        return "urgent"



def main():
    while True:
        customer_name = input("Please enter customer name: ")
        dest = input("Is this package remaining in (c)ountry, or (o)verseas: ")
# use Try and except to handle wrong letter input.
        if dest == 'c':
            destination = 'country'
        elif dest == 'o':
            destination = 'overseas'
        else:
            print("Use 'c' or 'o'.")
        package_desc = input("General description of package: ")
        danger = input("Does the package contain anything dangerous (y/n): ")
    # use Try and except to handle wrong letter input.
        if danger == 'n':
            dangerous = 'Safe'
        elif danger == 'y':
            dangerous = 'unsafe'
        else:
            print("Is it safe or unsafe? (y/n)")
        delivery_date = input("When do they want the package to arrive: yyyy/dd/mm ")
        urgency = urgent_check(delivery_date)
        weight = input("Weight in kilograms: ")
        length = input("L: ")
        width = input("W: ")
        height = input ("H: ")
    df = pd.read_csv('records.csv')
    new_row = {'customer_name': customer_name,
               'destination': destination,
               'package_desc': package_desc,
               'dangerous': dangerous,
               'delivery_date': delivery_date,
               'urgency': urgency,
               'weight': weight,
               'length': length,
               'width': width,
               'height': height}
    df = df.append(new_row,ignore_index=True)
    df.to_csv('records.csv', index=False)
    entry = (customer_name,destination,package_desc,dangerous,delivery_date,weight,length,width,height)
    print(entry)






if __name__ == "__main__":
    main()
