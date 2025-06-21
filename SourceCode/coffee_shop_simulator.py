# Import needed modules

# Import items from the random module to generate weather
import pickle
import random
import re
import numpy
import json


class CoffeeShopSimulator:

    # Minimum and maximum temperatures
    TEMP_MIN = 20
    TEMP_MAX = 90

    SERIES_DENSITY = 300

    # Save game file
    SAVE_FILE = "savegame.dat"

    def __init__(self):

        # Get name and store name
        print("Let's collect some information before we start the game.\n")
        self.player_name = self.prompt("What is your name?", True)
        self.shop_name = self.prompt("What do you want to name your coffee shop?", True)

        # Current day number
        self.day = 1

        # Cash on hand at start
        self.cash = 100

        # Inventory at start
        self.coffee_inventory = 100

        # Sales list
        self.sales = []

        # Possible temperature
        self.temps = self.make_temp_distribution()

    def run(self):
        print("\nOk, let's get started. Have fun!")

        # The main game loop 
        running = True
        while running:
             # Display the day and add a "fancy" text effect
             self.day_header()

             # Get the weather
             temperature = self.weather

             # Display the cash and weather
             self.daily_stats(temperature)

             # Get price of a cup of coffee (But provide an escape)
             response = self.prompt("What do you want to charge per cup of coffee? (Type exit to quit)")
             if re.search("exit", response, re.IGNORECASE):
                 running = False
                 continue
             else:
                 cup_price = int(response)

             # Do they want to buy more coffee invetory?
             print("\nIt costs $1 for the necessary inventory to make a cup of coffee.")
             response = self.prompt("Want to buy more coffee? (hit Enter for none or enter a number)", False)

             if response:
                 if not self.buy_coffee(response):
                     print("Could not buy additional coffee.")

             # Get price of a cup of coffee
             print("\nYou can buy advertising to help promote sales.")
             advertising = self.prompt("How much do you want to spend on advertising (0 for none)? ", False)

             # Convert advertising into a float
             advertising = self.convert_to_float(advertising)
    

             # Deduct advertising from cash on hand
             self.cash -= advertising

             # Simulate today's sales
             cups_sold = self.simulate(temperature, advertising, cup_price)
             gross_profit = cups_sold * cup_price

             # Display the results
             print("You sold " + str(cups_sold) + " cups of coffee today.")
             print("You made $" + str(gross_profit) + ".")

             # Add the profit to our coffers
             self.cash += gross_profit

             # Subtract inventory
             self.coffee_inventory -= cups_sold

             if self.cash < 0:
                 print("\n:( Game Over! You ran out of cash.")
                 running = False
                 continue

             # Before we loop around, add a day
             self.increment_day()

             # Save the game
             with open(self.SAVE_FILE, mode="wb") as f:
                 pickle.dump(self, f)
                 
        with open("sales.json", "w") as f:
            json.dump(self.sales, f, indent=4)
        print("Sales data saved to sales.json")
             

    def simulate(self, temperature, advertising, cup_price):

        # Find out how many cups were sold
        cups_sold = self.daily_sales(temperature, advertising, cup_price)

        # Save the sales data for today
        self.sales.append({
            "day": self.day,
            "coffee_inv": self.coffee_inventory,
            "advertising": advertising,
            "temp": temperature,
            "cup_price": cup_price,
            "cups_sold": cups_sold
        })

        return cups_sold

    def buy_coffee(self, amount):
        try:
            i_amount = int(amount)
        except ValueError:
            return False
        
        if i_amount <= self.cash:
            self.coffee_inventory += i_amount
            self.cash -= i_amount
            return True
        else:
            return False

    def make_temp_distribution(self):

        # Create series of numbers between TEMP_Min and TEMP_MAX
        series = numpy.linspace(self.TEMP_MIN, self.TEMP_MAX, self.SERIES_DENSITY)

        # Obtain mean and standard deviation from the series
        mean = numpy.mean(series)
        std_dev = numpy.std(series)

        return (numpy.pi * std_dev) * numpy.exp( -0.5 * ( ( series - mean ) / std_dev ) ** 2 )
            
    def increment_day(self):
        self.day += 1

    def daily_stats(self, temperature):
        print("You have $" + str(self.cash) + " cash on hand and the temperature is " + str(temperature) + ".")
        print("You have enough coffee on hand to make " + str(self.coffee_inventory) + " cups.\n")

    def day_header(self):
        print("\n-----| Day " + str(self.day) + " @ " + self.shop_name + " |-----")

    def daily_sales(self, temperature, advertising, cup_price):

        adv_coefficient = random.randint(20, 80) / 100

        price_coefficient = int( ( cup_price * ( random.randint( 50, 250 ) / 100 ) ) )

        sales = int( (self.TEMP_MAX - temperature) * (advertising * adv_coefficient) )
        
        if price_coefficient > sales:
            sales = 0
        else:
            sales -= price_coefficient
        
        if sales > self.coffee_inventory:
            sales = self.coffee_inventory
            print("You would have sold more coffee but you ran out. Be sure to buy additional inventroy.")
        return sales
  
                    
    @property
    def weather(self):
        return int( random.choice( self.temps ) )
    
    @staticmethod
    def prompt(display="Please input a string", require=True):
        if require:
            s = False
            while not s:
                s = input(display + " ")
        else:
            s = input(display + " ")
        return s
    
    @staticmethod
    def convert_to_float(s):
        # If conversion fails, assign it to 0
        try:
            f = float(s)
        except ValueError:
            f = 0
        return f
    
    @staticmethod
    def x_of_y(x, y):
        num_list = []
        # Return a list of x numbers of y
        for i in range(x):
            num_list.append(y)
        return num_list
    
    

