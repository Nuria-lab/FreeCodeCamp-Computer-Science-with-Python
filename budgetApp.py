

def truncate(n):
  multiplier = 10
  return int(n * multiplier / multiplier)


def getTotals(categories):
  total = 0
  breakdown = []
  for category in categories:
    total += category.get_withdrawls()
    breakdown.append(category.get_withdrawls())
  rounded = list(map(lambda x: truncate(x / total), breakdown))
  return rounded


def create_spend_chart(categories):
  output = "Percentage spent by category\n"

  
  total      = 0
  expenses   = []
  names     = []
  len_names = 0

  for item in categories:
    expense    = sum([-x['amount'] for x in item.ledger if x['amount'] < 0])
    total     += expense

    if len(item.name) > len_names:
      len_names = len(item.name)

    expenses.append(expense)
    names.append(item.name)


  expenses = [(x/total)*100 for x in expenses]
  names   = [name.ljust(len_names, " ") for name in names]

  
  for x in range(100,-1,-10):
    output += str(x).rjust(3, " ") + '|'
    for y in expenses:
      output += " o " if y >= x else "   "
    output += " \n"

  
  output += "    " + "---"*len(names) + "-\n"

  for i in range(len_names):
    output += "    "
    for name in names:
      output += " " + name[i] + " "
    output += " \n"

  return output.strip("\n")

   
class Category:

  def __init__(self, name):
    self.name = name
    self.ledger = list()

  def __str__(self):
  
    output = ""
    output += self.name.center(30,"*") + "\n"

    total = 0
    for item in self.ledger:
      total += item['amount']

      output += item['description'].ljust(23, " ")[:23]
      output += "{0:>7.2f}".format(item['amount'])
      output += "\n"

    output += "Total: " + "{0:.2f}".format(total)
    return output
   

  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description=""):
    if (self.check_funds(amount)):
      self.ledger.append({"amount": -amount, "description": description})
      return True
    return False

  def get_balance(self):
    total_cash = 0
    for item in self.ledger:
      total_cash += item["amount"]
    return total_cash

  def transfer(self, amount, category):
    if (self.check_funds(amount)):
      self.withdraw(amount, "Transfer to " + category.name)
      category.deposit(amount, "Transfer from " + self.name)
      return True
    return False

  def check_funds(self, amount):
    if (self.get_balance() >= amount):
      return True
    return False

  def get_withdrawls(self):
    total = 0
    for item in self.ledger:
      if item["amount"] < 0:
        total += item["amount"]
    return total
  
