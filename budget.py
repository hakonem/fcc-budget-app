class Category:
  instances = []
  
  def __init__(self, name):
    self.__class__.instances.append(self)
    ledger = []
    self.name = name
    self.ledger = ledger
    self.amount_deposit = 0
    self.amount_withdrawal = 0
    self.balance = 0

  def __str__(self):
    list = self.name.center(30, "*") + "\n"
    list += '\n'.join(f"{x['description'][:23]}{'{:7.2f}'.format(x['amount']).rjust(30-len(x['description']))}" for x in self.ledger)
    list += "\n" + f"Total: {self.balance}"
    return list

  def check_funds(self, amount):
      if amount > self.balance:
        return False
      else:
        return True
    
  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})
    self.amount_deposit += amount
    self.balance += amount

  def withdraw(self, amount, description=""):
    if not self.check_funds(amount):
      return False
    else:
      self.ledger.append({"amount": - amount, "description": description})
      self.amount_withdrawal += amount
      self.balance -= amount
      return True

  def get_balance(self):
    return self.balance

  def transfer(self, amount, name):
    if not self.check_funds(amount):
      return False
    else:
      self.ledger.append({"amount": - amount, "description": f'Transfer to {name.name}'})
      self.amount_withdrawal += amount
      self.balance -= amount
      name.ledger.append({"amount": amount, "description": f'Transfer from {self.name}'})
      name.amount_deposit += amount
      name.balance += amount
      return True

def create_spend_chart(categories):  
  total = 0
  for cat in categories:
    total += cat.amount_withdrawal      # calculate total expenditure across all categories

  chart = "Percentage spent by category\n"
  for i in range(100, -1, -10):
    chart += f"{i}|".rjust(4)
    for c in categories:
      # check rounded spend amount of each category against % value on y-axis:
      rounded = round(c.amount_withdrawal/10)*10
      if rounded/total * 100 >= i:
        chart += " o "              # print "o" if reaches threshold
      else:
        chart += "   "              # else print blank space
    chart += " \n"

  chart += "    " + "-" * ((len(categories) * 3) + 1)    # separator line 
  chart += "\n     "
  
  # find longest category name - this is number of times to iterate through categories list to print characters
  longest_name = int(len(categories[0].name))
  for c in categories:
    if len(c.name) > longest_name:
      longest_name = int(len(c.name))

  # for each iteration, check if the length of the category name has been reached
  for i in range(longest_name):  
    for c in categories:
      if i < len(c.name):
        chart += c.name[i] + "  "    # print the character if available
      else:  
        chart += "   "            # otherwise print blank space
    chart += "\n     "          # start each iteration on new line
  
  chart = chart.strip() + "  "

  return chart
