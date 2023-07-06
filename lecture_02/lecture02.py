class Food():
    def __init__(self, name, value, calories):
        self.name = name
        self.value = value
        self.calories = calories

    def get_value(self):
        return self.value

    def get_cost(self):
        return self.calories

    def density(self):
        return self.get_value()/self.get_cost()

    def __str__(self):
        return f'{self.name}: <{self.value}, {self.calories}>'


def build_menu(names, values, calories):
    """Create a list of Food. Names, values, calories lists of same length.

    Args:
        names (list[str]): List of food names.
        values (list[int]): List of food amount.
        calories (list[int]): list of food calories
    Return:
        menu (list[Food]): List of Foods
    """
    menu = [
        Food(name, val, cal) for name, val, cal in list(zip(names, values, calories))
    ]
    return menu


def max_val(to_consider, avail):
    """Assumes toConsider a list of items, avail a weight.
       Returns a tuple of the total value of a solution to the
       0/1 knapsack problem and the items of that solution"""
    if to_consider == [] or avail == 0:
        result = (0, ())
    elif to_consider[0].get_cost() > avail:
        #Explore right branch only
        result = max_val(to_consider[1:], avail)
    else:
        next_item = to_consider[0]
        #Explore left branch
        with_val, with_to_take = max_val(
            to_consider[1:], avail - next_item.get_cost()
        )
        with_val += next_item.get_value()
        #Explore right branch
        without_val, without_to_take = max_val(to_consider[1:], avail)
        #Choose better branch
        if with_val > without_val:
            result = (with_val, with_to_take + (next_item,))
        else:
            result = (without_val, without_to_take)
    return result
