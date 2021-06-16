#!/usr/bin/env python
import datetime
import pandas as pd
from tabulate import tabulate


class TravelRoute:
    def __init__(self, destination, dangerous, urgency, dimension, weight):
        self.destination = destination
        self.dangerous = dangerous
        self.urgency = urgency
        self.dimension = float(dimension)
        self.weight = float(weight)

    def __str__(self):
        return str(self.charge)


class Air(TravelRoute):
    def __init__(self, destination, dangerous, urgency, dimension, weight):
        super().__init__(destination, dangerous, urgency, dimension, weight)

    def charge(self):
        if self.dangerous == "unsafe":
            return 0
        elif self.weight*10 > self.dimension*20:
            return float(self.weight*10)
        else:
            return float(self.dimension * 20)


class Truck(TravelRoute):
    def __init__(self, destination, dangerous, urgency, dimension, weight):
        super().__init__(destination, dangerous, urgency, dimension, weight)

    def charge(self):
        if self.destination == 'overseas':
            return 0
        elif self.urgency == 'urgent':
            return 45
        else:
            return 25


class Boat(TravelRoute):
    def __init__(self, destination, dangerous, urgency, dimension, weight):
        super().__init__(destination, dangerous, urgency, dimension, weight)

    def charge(self):
        if self.destination == 'in-country':
            return 0
        elif self.urgency == 'urgent':
            return 0
        else:
            return 30




def urgent_check(delivery_date):
    future = datetime.datetime.today() + datetime.timedelta(days=3)
    if delivery_date > future:
        return "not urgent"
    else:
        return "urgent"


def destination_check():
    while True:
        dest = input("Is this package remaining in (c)ountry, or (o)verseas: ").lower()
        if dest == 'c':
            return 'in-country'
        elif dest == 'o':
            return 'overseas'
        else:
            print("Use 'c' or 'o'.")


def danger_check():
    while True:
        danger = input("Does the package contain anything dangerous (y/n): ").lower()
        if danger == 'n':
            return 'Safe'
        elif danger == 'y':
            return 'unsafe'
        else:
            print("Is it safe or unsafe? (y/n)")


def next_customer():
    next_c = input("Is there another customer: (y/n)").lower()
    if next_c == 'y':
        return True
    else:
        return False


def delivery_options(destination, dangerous, urgency, dimension, weight):
    options = {}
    air_option = Air(destination, dangerous, urgency, dimension, weight)
    truck_option = Truck(destination, dangerous, urgency, dimension, weight)
    boat_option = Boat(destination, dangerous, urgency, dimension, weight)
    if air_option.charge() > 0.0:
        options['Air'] = air_option.charge()
    if truck_option.charge() > 0.0:
        options['Truck'] = truck_option.charge()
    if boat_option.charge() > 0.0:
        options['Boat'] = boat_option.charge()
    df2 = pd.DataFrame(list(options.items()), columns=['Option', 'Cost'])
    print(tabulate(df2, tablefmt='psql'))
    selection = 0
    while selection == 0:
        try:
            delivery_choice = input("Choose the delivery method:")
            delivery_choice = int(delivery_choice)

            if delivery_choice < 0 or delivery_choice > df2.last_valid_index():
                print("Please select a valid method of transport")
            else:
                selection = 1
        except ValueError:
            print('Please enter a valid shipping option')
    df2_option = df2.at[delivery_choice, 'Option']
    df2_cost = df2.at[delivery_choice, 'Cost']
    return df2_option, df2_cost


def print_customer(df):
    row = df.tail(1).transpose()
    print("Order ID:", df.last_valid_index())
    print(tabulate(row, tablefmt='psql'))


def get_name():
    while True:
        try:
            name = input("Please enter customer name: ")
            if not name:
                raise ValueError("Please enter a valid name.  Cannot be blank")
            else:
                break
        except ValueError as e:
            print(e)
    return name


def get_description():
    while True:
        try:
            description = input("General description of package: ")
            if not description:
                raise ValueError("Please enter a description.  Cannot be blank")
            else:
                break
        except ValueError as e:
            print(e)
    return description


def get_delivery_date():
    day = 0
    while day == 0:
        d_date = input("When do they want the package to arrive: yyyy/dd/mm ")
        try:
            d_date = datetime.datetime.strptime(d_date, '%Y/%m/%d')
            if d_date <= datetime.datetime.today():
                print("Please enter a delivery date at least one day in advance.")
            else:
                day = 1
        except ValueError:
            print("Incorrect date format, should be YYYY/MM/DD.")
    return d_date


def get_dimensions():
    print("Minimum dimension size is 0.1 meter.\n  "
          "Anything smaller should be rounded up to 0.1.\n"
          "Minimum overall size is 0.5m")
    while True:
        try:
            length = float(input("L: "))
            if not length:
                raise ValueError("Please enter a length.")
            elif length < 0.1:
                print("Please enter a dimension greater than 0.0999.")
            else:
                break
        except ValueError as e:
            print(e)
    while True:
        try:
            width = float(input("W: "))
            if not width:
                raise ValueError("Please enter a width.")
            elif width < 0.1:
                print("Please enter a dimension greater than 0.0999.")
            else:
                break
        except ValueError as e:
            print(e)
    while True:
        try:
            height = float(input("H: "))
            if not height:
                raise ValueError("Please enter a height.")
            elif height < 0.1:
                print("Please enter a dimension greater than 0.0999.")
            else:
                break
        except ValueError as e:
            print(e)
    if length*width*height < 0.5:
        dimension = 0.5
    else:
        dimension = length*width*height
    return dimension


def size_check(dimension):
    if dimension > 124.999:
        print("Sorry, but this package is too large to be shipped by our methods.  Please reduce the size to less "
              "than 5x5x5")
        return False
    else:
        return True


def get_weight():
    while True:
        try:
            weight = float(input("How many kilograms does it weigh: "))
            if not weight:
                raise ValueError("Please enter a weight.  Cannot be blank")
            elif weight <= 0:
                print("Please enter a positive weight.")
            else:
                break
        except ValueError as e:
            print(e)
    return weight


def weight_check(weight):
    if weight > 9.999:
        print("Sorry, but this package weighs too much.  Please reduce the weight to under 10kg")
        return False
    else:
        return True


def main():
    customer = True
    while customer:
        customer_name = get_name()
        destination = destination_check()
        package_desc = get_description()
        dangerous = danger_check()
        delivery_date = get_delivery_date()
        urgency = urgent_check(delivery_date)
        weight = get_weight()
        weight_check(weight)
        dimension = get_dimensions()
        df = pd.read_csv('booking_quotes.csv', index_col=0)
        df.index.name = 'ID'
        df = df.reset_index(drop=True)
        new_row = {'Customer_Name': customer_name.title(),
                'Destination': destination,
                'Package_desc': package_desc,
                'Dangerous': dangerous,
                'Delivery_date': delivery_date.date(),
                'Urgency': urgency,
                'Weight': weight,
                'Size': round(dimension,2),
                'Shipping_option': '',
                'Cost': ''}
        df = df.append(new_row, ignore_index=True)
        print_customer(df)
        d_option, d_cost = delivery_options(destination, dangerous, urgency, dimension, weight)
        df.at[df.last_valid_index(), 'Shipping_option'] = d_option
        df.at[df.last_valid_index(), 'Cost'] = d_cost
        df.to_csv('booking_quotes.csv', index=True)
        print_customer(df)
        customer = next_customer()


if __name__ == "__main__":
    main()
