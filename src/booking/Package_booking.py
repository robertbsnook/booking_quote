#!/usr/bin/env python
import datetime
import pysnooper
import pandas as pd
from tabulate import tabulate
from datetime import date,datetime as dt,timedelta


class TravelRoute:
    def __init__(self,destination,dangerous,urgency,length,width,height,weight):
        self.destination = destination
        self.dangerous = dangerous
        self.urgency = urgency
        self.length = float(length)
        self.width = float(width)
        self.height = float(height)
        self.weight = float(weight)

    def __str__(self):
        return str(self.charge)


class Air(TravelRoute):
    def __init__(self,destination,dangerous,urgency,length,width,height,weight):
        super().__init__(destination,dangerous,urgency,length,width,height,weight)

    def charge(self):
        if self.dangerous == "unsafe":
            return 0
        elif self.weight*10 > self.length*self.width*self.height*20:
            return float(self.weight*10)
        else:
            return float(self.length * self.width * self.height * 20)


class Truck(TravelRoute):
    def __init__(self,destination,dangerous,urgency,length,width,height,weight):
        super().__init__(destination,dangerous,urgency,length,width,height,weight)

    def charge(self):
        if self.destination == 'overseas':
            return 0
        elif self.urgency == 'urgent':
            return 45
        else:
            return 25


class Boat(TravelRoute):
    def __init__(self,destination,dangerous,urgency,length,width,height,weight):
        super().__init__(destination,dangerous,urgency,length,width,height,weight)

    def charge(self):
        if self.destination == 'c':
            return 0
        elif self.urgency == 'urgent':
            return 0
        else:
            return 30


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
    dest = input("Is this package remaining in (c)ountry, or (o)verseas: ").lower()
    # use Try and except to handle wrong letter input.
    if dest == 'c':
        return 'in-country'
    elif dest == 'o':
        return 'overseas'
    else:
        print("Use 'c' or 'o'.")


def danger_check():
    danger = input("Does the package contain anything dangerous (y/n): ").lower()
    # use Try and except to handle wrong letter input.
    if danger == 'n':
        return 'Safe'
    elif danger == 'y':
        return 'unsafe'
    else:
        print("Is it safe or unsafe? (y/n)").lower()


def next_customer():
    next_c = input("Is there another customer: (y/n)").lower()
    if next_c == 'y':
        return True
    else:
        return False

def delivery_options(destination, dangerous, urgency, length, width, height, weight):
    options = {}
    air_option = Air(destination, dangerous, urgency, length, width, height, weight)
    truck_option = Truck(destination, dangerous, urgency, length, width, height, weight)
    boat_option = Boat(destination, dangerous, urgency, length, width, height, weight)
    if air_option.charge() > 0.0:
        options['Air'] = air_option.charge()
    if truck_option.charge() > 0.0:
        options['Truck'] = truck_option.charge()
    if boat_option.charge() > 0.0:
        options['Boat'] = boat_option.charge()
    df2 = pd.DataFrame(list(options.items()), columns=['Option', 'Cost'])
    print(tabulate(df2, tablefmt='psql'))




def main():
    customer = True
    while customer:
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
        df = pd.read_csv('booking_quotes.csv', index_col= 0)
        df.index.name = 'ID'
        df = df.reset_index(drop=True)
        new_row = {'Customer_Name': customer_name.title(),
               'Destination': destination,
               'Package_desc': package_desc,
               'Dangerous': dangerous,
               'Delivery_date': delivery_date,
               'Urgency': urgency,
               'Weight': weight,
               'Length': length,
               'Width': width,
               'Height': height}
        df = df.append(new_row,ignore_index=True)
        df.to_csv('booking_quotes.csv', index=True)
        row = df.tail(1).transpose()
        print(tabulate(row,tablefmt='psql'))
        delivery_options(destination, dangerous, urgency, length, width, height, weight)


# select option and have it append to the customer line

        print("Order ID:",df.last_valid_index())
        customer = next_customer()






if __name__ == "__main__":
    main()
