#!/usr/bin/env python
import datetime

import pysnooper
import pandas as pd
import csv
from IPython.display import display
from tabulate import tabulate
from datetime import date,datetime as dt,timedelta

class travel_route:
    def __init__(self,destination,dangerous,urgency,length,width,height,weight):
        self.destination = destination
        self.dangerous = dangerous
        self.urgency = urgency
        self.length = length
        self.width = width
        self.height = height

class air(travel_route):
    def __init__(self):
        super().init__()

    def travel_check(self):
        if self.dangerous == "unsafe":
            return False
        elif self.urgency == 'urgent':
            return True

    def charge(self,length,width,height,weight):
        if weight*10 > length*width*height*20:
            return weight*10
        else:
            return length*width*height*20

class truck(travel_route):
    def __init__(self):
        super().__init__()

    def travel_check(self):
        if self.destination == 'overseas':
            return False
        else:
            return True

    def charge(self):
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
    year, month, day = map(int, delivery_date.split('/'))
    date = datetime.date(year, month, day)
    future = datetime.date.today() + datetime.timedelta(days=3)
    if date > future:
        return "not urgent"
    else:
        return "urgent"


def destination_check():
    dest = input("Is this package remaining in (c)ountry, or (o)verseas: ")
    # use Try and except to handle wrong letter input.
    if dest == 'c':
        return 'country'
    elif dest == 'o':
        return 'overseas'
    else:
        print("Use 'c' or 'o'.")

def danger_check():
    danger = input("Does the package contain anything dangerous (y/n): ")
    # use Try and except to handle wrong letter input.
    if danger == 'n':
        return 'Safe'
    elif danger == 'y':
        return 'unsafe'
    else:
        print("Is it safe or unsafe? (y/n)")

def next_customer():
    next = input("Is there another customer: (y/n)")
    if next == 'y':
        return True
    else:
        return False

def main():
    customer = True
    while customer == True:
        customer_name = input("Please enter customer name: ")
        destination = destination_check()
        package_desc = input("General description of package: ")
        dangerous = danger_check()
        delivery_date = input("When do they want the package to arrive: yyyy/dd/mm ")
        urgency = urgent_check(delivery_date)
        weight = input("Weight in kilograms: ")
        length = input("L: ")
        width = input("W: ")
        height = input("H: ")
        df = pd.read_csv('records.csv', index_col= 0)
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
        df.to_csv('records.csv', index=True)
        print(new_row)

        print(df.last_valid_index())
        customer = next_customer()






if __name__ == "__main__":
    main()
