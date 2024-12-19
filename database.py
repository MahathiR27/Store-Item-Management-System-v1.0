# Importing required library 
import pygsheets 
import time
# start_time = time.time()
#
# print(f'----------------------------- {(time.time() - start_time):.23f}s -----------------------------')

class  Database:
  def __init__(self): #Connects to google api
    start_time = time.time()
    print('\n------------------------- Connecting to the Database -------------------------\n')
    client = pygsheets.authorize(service_account_file="token.json")
    client = client.open('Database v1') #Kon Spreadsheet open korbe drive theke.
    self.inventory_s = client.worksheet_by_title('inventory')
    self.invoice_s = client.worksheet_by_title('invoice')
    self.acc_s = client.worksheet_by_title('accounts')

    self.inventory = {}
    self.sell_dic = {}
    print(f'----------------------------- READY! Took {(time.time() - start_time):.2f}s ------------------------------\n')

  def login(self, username, password):
    start_time = time.time()
    cell = self.acc_s.find(username, matchEntireCell=True)
    if cell != []:
      loc = (cell[0].row,2)
      if self.acc_s.cell(loc).value == password:
        print(f'\n================= LOGIN {(time.time() - start_time):.3f}s =================\n')
        return True    
      return False
    else:
      return False

  def inventory_refresh(self):
    start_time = time.time()
    self.inventory = {}
    full = self.inventory_s.get_all_values(include_tailing_empty=False,include_tailing_empty_rows=False)
    for i in range(1,len(full)):
      x = full[i]
      item = x[0]
      stock = x[4]
      price = x[1]
      #inv.append(f"{item.lower()}({stock})-{price}$")
      self.inventory[item.lower()] = {'stock':int(stock),'price':int(price)}
    
    print(f'\n=============== INVENTORY {(time.time() - start_time):.3f}s ===============\n')

  def sell(self, item, amount):
    start_time = time.time()
    if item not in self.inventory.keys():
      return "IN"
    check = self.inventory[item]['stock']
    if amount > check or amount == 0:
      return 'SE' + str(check)
    else:
      self.inventory[item]['stock'] -= amount
      if item not in self.sell_dic:
        self.sell_dic[item] = {'amount': amount, "price": int(self.inventory[item]['price'])}
      else:
        self.sell_dic[item]['amount'] += amount
    print(f'\n================= SELL {(time.time() - start_time):.3f}s ===============\n')
    return "Clear"
  
  def remove(self, item, amount):
    start_time = time.time()
    check = self.sell_dic[item]['amount']
    if amount > check or amount == 0:
      return 'SE' + str(check)
    else:
      self.sell_dic[item]['amount'] -= amount
      self.inventory[item]['stock'] += amount
    print(f'\n================= SELL {(time.time() - start_time):.3f}s ===============\n')
    return "Clear"

  def invoice_clear(self):
    start_time = time.time()
    invoice = self.sell_dic
    item = []
    amount = []
    price = []
    for i in invoice.keys():
      item.append(i)
      amount.append(invoice[i]['amount'])
      price.append(invoice[i]['price'])
    end = str(len(item)+1)
    total_price = [int(amount[i]*price[i]) for i in range(int(end)-1)]
    self.invoice_s.update_values_batch([f'A2:A{end}',f'B2:B{end}',f'C2:C{end}',f'D2:F{end}'], [[item], [amount], [price],[total_price]], 'COLUMNS')

    amount = [self.inventory[i]['stock'] for i in self.inventory.keys()]
    end = str(len(amount)+1)
    self.inventory_s.update_values_batch({f'E2:E{end}'},[[amount]], "COLUMNS")
    self.sell_dic = {}
    print(f'\n=============== INVOICE_CLEAR {(time.time() - start_time):.3f}s ===============\n')


client  = Database() #Getting the main spreadsheet

#start_time = time.time()

#print(f'\n==================== {(time.time() - start_time):.3f}s ===================\n')