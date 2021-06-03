import multiprocessing
import copy

x = {
  "machine": {
    "outlets": {
      "count_n": 3
    },
    "total_items_quantity": {
      "hot_water": 500,
      "hot_milk": 500,
      "ginger_syrup": 100,
      "sugar_syrup": 100,
      "tea_leaves_syrup": 100
    },
    "beverages": {
      "hot_tea": {
        "hot_water": 200,
        "hot_milk": 100,
        "ginger_syrup": 10,
        "sugar_syrup": 10,
        "tea_leaves_syrup": 30
      },
      "hot_coffee": {
        "hot_water": 100,
        "ginger_syrup": 30,
        "hot_milk": 400,
        "sugar_syrup": 50,
        "tea_leaves_syrup": 30
      },
      "black_tea": {
        "hot_water": 300,
        "ginger_syrup": 30,
        "sugar_syrup": 50,
        "tea_leaves_syrup": 30
      },
      "green_tea": {
        "hot_water": 100,
        "ginger_syrup": 30,
        "sugar_syrup": 50,
        "green_mixture": 30
      },
    }
  }
}



# Beverage Object
class Beverage(object):

    def __init__(self, beverage_name):
        self.ingredients = {}
        self.beverage_name = beverage_name

    def add_ingredient(self, ingredient, quantity):

        if self.ingredients.get(ingredient, None) is not None:
            print('{} already exist'.format(ingredient))
            return

        self.ingredients[ingredient] = quantity
        print('{} added to beverage {}'.format(ingredient, self.beverage_name))


    def remove_ingredient(self, ingredient):

        if self.ingredients.get(ingredient, None) is None:
            print('{} does not exist'.format(ingredient))
            return

        del self.ingredients[ingredient]
        print('{} removed from beverage {}'.format(ingredient, self.beverage_name))


    def update_ingredient(self, ingredient, quantity, increase=True):

        if self.ingredients.get(ingredient, None) is None:
            print('{} does not exist'.format(ingredient))
            return

        if not increase:
            quantity *= -1

        self.ingredients[ingredient] += quantity
        print('Quantity of {} updated by {}'.format(ingredient, quantity))


    def get_ingredients(self):

        print('Ingredients for {}: '.format(self.beverage_name))
        for ingredient in self.ingredients.keys():
            print('{}: {}'.format(ingredient, self.ingredients[ingredient]))


# Coffee Machine
class Coffee_Machine(object):

    # Initializing coffee machine
    def __init__(self, n, items):
        # Number of outlets (n)
        self.outlets = []
        for i in range(n):
            outlet = (i+1)
            print('Coffee outlet {} created'.format(i+1))
            self.outlets.append(outlet)

        # Ingredient quantity (item_quantity)
        self.item_quantity = items
        # Assuming that the max quantity is the inital quantity which is given
        self.max_item_quantity = copy.copy(items)

    # To serve beverage
    def serve_beverage(self, beverage, beverage_name):
        '''
        param:
            beverage: Dictionary with ingredients and quantities
            beverage_name: Beverage Name string

        '''
        item_dict = beverage
        new_item_quantity = self.item_quantity
        is_available = True
        for item in item_dict.keys():
            if new_item_quantity.get(item, None) is None:
                print('{} cannot be prepared because {} is not available'.format(beverage_name, item))
                is_available = False
                break

            elif new_item_quantity.get(item) < item_dict.get(item):
                print('{} cannot be prepared because {} is not sufficient'.format(beverage_name, item))
                is_available = False
                break
            else:
                new_item_quantity[item] -= item_dict.get(item)

        if is_available:
            self.item_quantity = new_item_quantity
            print('{} is prepared'.format(beverage_name))
            print('----------------------------------')
            print('Remaining ingredients:')
            # Display ingredient quantity after serving beverage
            self.indicate()
            print('----------------------------------')

    # Serve with outlets
    def serve(self, beverage, beverage_name):
        '''
        param:
            beverage: Dictionary with ingredients and quantities
            beverage_name: Beverage Name string

        '''

        outlet = None
        # Check for any available outlets
        if len(self.outlets) > 0:
            outlet = self.outlets.pop()
            # Serve beverage with that outlet
            self.serve_beverage(beverage, beverage_name)
        else:
            print('No coffee outlet is available to serve beverage')
            return

        self.outlets.append(outlet)

    # To indicate quantity of available ingredients
    def indicate(self):
        '''
        param:
            No parameters required

        '''
        refill_ingredients = []
        for item in self.item_quantity.keys():
            # Checking if quantity is less than 20% of the maximum amount
            if self.item_quantity.get(item) < 0.2*self.max_item_quantity.get(item):
                refill_ingredients.append(item)
                print('{}: {} [ALERT] Low quantity'.format(item, self.item_quantity[item]))
            else:
                print('{}: {}'.format(item, self.item_quantity[item]))

        if len(refill_ingredients) > 0:
            print('Refilling Ingredients: {}'.format(','.join(refill_ingredients)))
            self.refill(refill_ingredients)

    # To refill ingredients
    def refill(self, ingredients=None, amount=None):
        '''
        param:
            ingredients: list of ingredient names to be refilled
            amount: amount of ingredient to be refilled

        '''
        # To refill specific ingredients
        if ingredients is not None:
            assert isinstance(ingredients, type([])), "Ingredients not provided in List"
            for ingredient in ingredients:
                # Refill ingredient with amount given
                if amount is not None:
                    self.item_quantity[ingredient] = float(amount)
                    print('{} refilled to {}'.format(ingredient, str(amount)))
                # Refill ingredient with the maximum amount
                else:
                    self.item_quantity[ingredient] = self.max_item_quantity.get(ingredient)
                    print('{}: {}| Refilled to max amount'.format(ingredient, self.item_quantity[ingredient]))

            return

        # If no ingredient is given refilling all ingredients
        self.item_quantity = self.max_item_quantity
        print('All ingredients refilled to max amount')


if __name__ == '__main__':
    n = x['machine']['outlets']['count_n']
    items = x['machine']['total_items_quantity']
    beverages = x['machine']['beverages']
    beverage_list = []
    for beverage in beverages.keys():
        obj = Beverage(beverage)
        beverage_list.append(obj)
        for ingredient in beverages[beverage].keys():
            obj.add_ingredient(ingredient, beverages[beverage][ingredient])

    m = Coffee_Machine(n, items)
    # This part should be ran in parallel for proper testing
    for beverage in beverage_list:
        # m.serve(beverage.ingredients, beverage.beverage_name)

        # m.serve_beverage(beverages.ingredients, beverage.beverage_name)
        # m.serve_beverage(beverages.ingredients, beverage.beverage_name)
        p1 = multiprocessing.Process(target=m.serve, args=(beverage.ingredients, beverage.beverage_name))
        p2 = multiprocessing.Process(target=m.serve, args=(beverage.ingredients, beverage.beverage_name))
        p3 = multiprocessing.Process(target=m.serve, args=(beverage.ingredients, beverage.beverage_name))
        # starting process 1
        p1.start()
        # starting process 2
        p2.start()
        # starting process 3
        p3.start()
        # wait until process 1 is finished
        p1.join()
        # wait until process 2 is finished
        p2.join()
        # wait until process 3 is finished
        p3.join()
        # both processes finished
    print("Done!")
