import tkinter as tk
from tkinter import messagebox as msg
from tkinter import ttk
from database import client as db
import time

class MyApp():
  def __init__(self, root):
    self.root = root
    window = self.root
    self.admin = False

    window.title("Login") #Window Title
    window.geometry("1080x720") #Window Opening Dimensions
    window.iconphoto(False, tk.PhotoImage(file = 'icon.png')) #Window Icon on top left
    window.configure(bg=c2) #Window BG

    self.frame = tk.Frame(window, bg=c2)
    frame = self.frame
    frame.place(relx=0.5, rely=0.45, anchor=tk.CENTER) #To get the frame in the center. relx = left side theke koto dur 1 max 0 min
    
    # self.top_frame = tk.Frame(window, bg=c2)
    # self.top_frame.place(relx=0, rely=0.1)

    self.login_page()

  def login_page(self):
    frame = self.frame
    frame.columnconfigure(0, weight=1) #1st Col weight 1
    frame.columnconfigure(1, weight=2) #2nd Col weight 1
    frame.columnconfigure(2, weight=1) #3rd Col weight 1
    frame.columnconfigure(3, weight=1) #3rd Col weight 1

    self.login_text = tk.Label(frame, text='Log in to Continue', font=h1, bg=c2, fg=c1)
    self.login_text.grid(row=0, column=1, sticky='nsew',columnspan=2,pady=10)

    self.username_label = tk.Label(frame, text='Username ', font=t1, bg=c2, fg=c1)
    self.username_label.grid(row=1, column=1, sticky='W',padx=(0,5), pady=10)
    
    self.username_entry = tk.Entry(frame, font=t1)
    self.username_entry.grid(row=1, column=2, sticky='E',padx=(5,0), pady=10)

    self.password_label = tk.Label(frame, text='Password ', font=t1, bg=c2, fg=c1)
    self.password_label.grid(row=2, column=1, sticky='W',padx=(0,5), pady=10)

    self.password_entry = tk.Entry(frame, font=t1, show= "*") #Password entry korle jate * dekhay
    self.password_entry.grid(row=2, column=2, sticky='E',padx=(5,0), pady=10)

    self.password_entry.bind('<KeyRelease>', self.login_enter)

    self.login_button = tk.Button(frame, text='Login', font=t1, bg=c1, fg=c2, activebackground=c3, command=self.login)
    self.login_button.grid(row=3, column=1, sticky='nsew',columnspan=2, pady=10)

  def sell_page(self):
    self.clear_frame(self.root)
    #Inventory frame
    self.inventory_frame = tk.LabelFrame(self.frame, text="Inventory", font=h1,  bg=c2, fg=c1)
    inventory_frame = self.inventory_frame
    inventory_frame.grid(row=0, column=0, sticky='nsew')

    self.inventory_list = ttk.Treeview(inventory_frame, columns=('item', 'stock', 'price'), show='headings')
    
    self.inventory_list.column('item',anchor=tk.W, width=120)
    self.inventory_list.column('stock',anchor=tk.CENTER, width=60)
    self.inventory_list.column('price',anchor=tk.CENTER, width=60)

    self.inventory_list.heading('item', text='Item', anchor=tk.CENTER)
    self.inventory_list.heading('stock', text='Stock', anchor=tk.CENTER)
    self.inventory_list.heading('price', text='Price', anchor=tk.CENTER)
    self.inventory_list.bind("<ButtonRelease>", self.fill_item_entry)

    self.inventory_list.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)

    self.inventory_refresh_button = tk.Button(inventory_frame, text="Refresh", font=t1, bg=c1, fg=c2, activebackground=c3, command=self.inventory_refresh) # Button that will refresh the inventory
    self.inventory_refresh_button.grid(row=1,column=0, columnspan=3, sticky="nsew", padx=10,pady=10)

    #Sell Frame
    #Adding
    self.sell_frame = tk.LabelFrame(self.frame, text='Sell Menu',font=h1, bg=c2, fg=c1)
    sell_frame = self.sell_frame
    sell_frame.grid(row=0, column=1,sticky='nsew', padx=20)

    self.item_name = tk.Label(sell_frame, text='Item Name', font=t1, bg=c2, fg=c1)
    self.item_name.grid(row=0, column=0, sticky='w', pady=10, padx=10)
    self.item_entry = tk.Entry(sell_frame, font=t1)
    self.item_entry.grid(row=0, column=1, sticky='nsew', pady=10, padx=10)

    self.item_amount = tk.Label(sell_frame, text='Item Amount', font=t1, bg=c2, fg=c1)
    self.item_amount.grid(row=1, column=0, sticky='w', pady=10, padx=10)
    self.item_amount_entry = tk.Spinbox(sell_frame, font=t1, from_=0, to='infinity') #Number updown alabox. Have to check if its a number
    self.item_amount_entry.grid(row=1, column=1, sticky='nsew', pady=10, padx=10)
    self.item_amount_entry.bind('<KeyRelease>', self.sell_enter)
    
    self.add_button = tk.Button(sell_frame, text='Add', font=t1, bg=c1, fg=c2, activebackground=c3, command=self.sell)
    self.add_button.grid(row=2, column=0, sticky='nsew',columnspan=2, padx=10, pady=(0,10))

    #Removing
    self.item_name_remove = tk.Label(sell_frame, text='Remove Item', font=t1, bg=c2, fg=c1)
    self.item_name_remove.grid(row=3, column=0, sticky='w', pady=10, padx=10)
    self.item_remove_entry = tk.Entry(sell_frame, font=t1)
    self.item_remove_entry.config(state="disabled")
    self.item_remove_entry.grid(row=3, column=1, sticky='nsew', pady=10, padx=10)

    self.item_amount = tk.Label(sell_frame, text='Item Amount', font=t1, bg=c2, fg=c1)
    self.item_amount.grid(row=4, column=0, sticky='w', pady=10, padx=10)
    self.item_amount_remove_entry = tk.Spinbox(sell_frame, font=t1, from_=0, to='infinity') #Number updown alabox. Have to check if its a number
    self.item_amount_remove_entry.grid(row=4, column=1, sticky='nsew', pady=10, padx=10)
    self.item_amount_remove_entry.bind('<KeyRelease>', self.remove_enter)

    self.remove_button = tk.Button(sell_frame, text='Remove', font=t1, bg=c1, fg=c2, activebackground=c3, command=self.remove)
    self.remove_button.grid(row=5, column=0, sticky='nsew',columnspan=2, padx=10, pady=(0,10))

    self.clear_button = tk.Button(sell_frame, text='CLEAR', font=t1, bg=c1, fg=c2, activebackground=c3, command=self.sell_clear)
    self.clear_button.grid(row=6, column=0, sticky='nsew',columnspan=2, padx=10, pady=(20,10))

    #Invoice frame
    self.invoice_frame = tk.LabelFrame(self.frame, text='Invoice Menu',font=h1, bg=c2, fg=c1)
    invoice_frame = self.invoice_frame
    invoice_frame.grid(row=0, column=2,sticky='nsew', padx=20)

    self.invoice_list = ttk.Treeview(invoice_frame, columns=('item', 'amount', 'price', 'total'), show='headings')
    
    self.invoice_list.column('item',anchor=tk.W, width=120)
    self.invoice_list.column('amount',anchor=tk.CENTER, width=60)
    self.invoice_list.column('price',anchor=tk.CENTER, width=60)
    self.invoice_list.column('total',anchor=tk.E, width=90)

    self.invoice_list.heading('item', text='Item', anchor=tk.CENTER)
    self.invoice_list.heading('amount', text='Amount', anchor=tk.CENTER)
    self.invoice_list.heading('price', text='Price', anchor=tk.CENTER)
    self.invoice_list.heading('total', text='Total', anchor=tk.CENTER)
    self.invoice_list.bind("<ButtonRelease>", self.fill_item_remove)

    self.invoice_list.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)

    self.invoice_total= tk.Label(invoice_frame, text=f"Total:", font=h1, bg=c2, fg=c1)
    self.invoice_total.grid(row=2,column=0, columnspan=2, sticky="W", padx=10,pady=10)

    self.invoice_print_button = tk.Button(invoice_frame, text="Confirm", font=t1, bg=c1, fg=c2, activebackground=c3, command=self.invoice_clear) # Button that will refresh the inventory
    self.invoice_print_button.grid(row=3,column=0, columnspan=3, sticky="nsew", padx=10,pady=(20, 10))

    self.item_entry.bind("<Key>", self.search_inventory) #Checks for Key stroke
    self.inventory_refresh()

  def login(self):
    user = self.username_entry.get() #Get the username
    password = self.password_entry.get() #Get the password
    if db.login(user, password): #True:
      self.clear_frame(self.frame)
      if user == 'Admin':
        self.admin = True
      self.sell_page()
    else:
      self.password_entry.delete(0, tk.END) #Wrong input clears the password text box
      self.password_entry.insert(0, "") #Sob textbox e there must be a empty string
      msg.showerror("Error", "Invalid Username or Password") #If username or password is incorrect

  def invoice_clear(self): #Prints the invoice and clear it
    db.invoice_clear()
    self.invoice_total_value.destroy()
    self.invoice_total_value= tk.Label(self.invoice_frame, text=f'0', font=h1, bg=c2, fg=c1)
    self.invoice_total_value.grid(row=2,column=2, sticky="E", padx=10,pady=10)
    for i in self.invoice_list.get_children():
      self.invoice_list.delete(i)
    self.inventory_refresh()

  def remove(self):
    item = self.item_remove_entry.get().lower()
    if item == None:
      msg.showerror("Error", "Select an item from invoice to remove!")
    else:
      amount = int(self.item_amount_remove_entry.get())
      action = db.remove(item, amount)
      if action[:2] == 'SE':
        msg.showerror("Amount Error", f'There are only {action[2:]} {item} in invoice.')
        self.item_amount_remove_entry.delete(0, tk.END)
        self.item_amount_remove_entry.insert(0, "")
      else:
        self.sell_clear()
        self.invoice_total_value.destroy()
        self.invoice_refresh()

  def sell(self):
    if db.inventory == {}:
      msg.showerror("Error", "Inventory not loaded!")
    else:
      item = self.item_entry.get().lower()
      amount = int(self.item_amount_entry.get())
      action = db.sell(item, amount)
      if action[:2] == 'IN':
        self.item_entry.delete(0, tk.END) #Wrong input clears the password text box
        self.item_entry.insert(0, "")
        msg.showerror("Error", "Incorrect Item!")
      elif action[:2] == 'SE':
        msg.showerror("Amount Error", f'There are only {action[2:]} {item} in stock.')
        self.item_amount_entry.delete(0, tk.END)
        self.item_amount_entry.insert(0, "")
      else:
        self.sell_clear()
        self.invoice_refresh()

  def invoice_refresh(self):
    start_time = time.time()
    if db.sell_dic == {}:
      msg.showerror("Error", "No items added to the invoice!")
    else:
      self.sell_clear()
      rmv = self.invoice_list.get_children()
      if rmv != ():
        for i in rmv:
          self.invoice_list.delete(i)
      ID = 0
      net_payable = 0
      for i in db.sell_dic.keys():
        item = db.sell_dic[i]
        amount = int(item['amount'])
        price = int(item['price'])
        total = amount*price
        val = (i, amount , price , total)
        self.invoice_list.insert(parent='',index='end', iid=ID, values=val)
        ID += 1
        net_payable += total
    self.invoice_total_value= tk.Label(self.invoice_frame, text=f'{net_payable}', font=h1, bg=c2, fg=c1)
    self.invoice_total_value.grid(row=2,column=2, sticky="E", padx=10,pady=10)
    print(f'\n================= INVOICE_REFRESH {(time.time() - start_time):.3f}s ===============\n')

  def search_inventory(self, event): #Searches in inventory List
    name = self.item_entry.get().lower()
    rmv = self.inventory_list.get_children()
    if rmv != ():
      for i in rmv:
        self.inventory_list.delete(i)
    if name == '':
      data = db.inventory.keys()
    else:
      data = [i for i in db.inventory.keys() if name in i] #Searches in
    ID = 0
    for i in data:
        item = db.inventory[i]
        val = (i, item['stock'], item['price'])
        self.inventory_list.insert(parent='',index='end', iid=ID, values=val)
        ID += 1

  def inventory_refresh(self):
    self.sell_clear()
    rmv = self.inventory_list.get_children()
    if rmv != ():
      for i in rmv:
        self.inventory_list.delete(i)
    ID = 0
    db.inventory_refresh()
    for i in db.inventory.keys():
      item = db.inventory[i]
      val = (i, item['stock'], item['price'])
      self.inventory_list.insert(parent='',index='end', iid=ID, values=val)
      ID += 1

  def sell_clear(self):
    self.item_remove_entry.config(state='normal')
    self.item_entry.delete(0, tk.END)
    self.item_amount_entry.delete(0, tk.END)
    self.item_remove_entry.delete(0, tk.END)
    self.item_amount_remove_entry.delete(0, tk.END)

    self.item_entry.insert(0, '')
    self.item_amount_entry.insert(0, '')
    self.item_remove_entry.insert(0,'')
    self.item_amount_remove_entry.insert(0, '')
    self.item_remove_entry.config(state='disabled')

  def login_enter(self, event):
    if event.keysym == 'Return':
      self.login()

  def sell_enter(self, event):
    if event.keysym == 'Return':
      self.sell()

  def remove_enter(self, event):
    if event.keysym == 'Return':
      self.remove()

  def fill_item_entry(self, event):  #Fills the item entry box with the selected item
    self.item_entry.delete(0, tk.END)
    selected = self.inventory_list.focus()
    values = self.inventory_list.item(selected,'values')
    self.item_entry.insert(0, values[0])
  
  def fill_item_remove(self, event):
    self.item_remove_entry.config(state="normal")

    self.item_remove_entry.delete(0, tk.END)
    selected = self.invoice_list.focus()
    values = self.invoice_list.item(selected,'values')
    self.item_remove_entry.insert(0, values[0])

    self.item_remove_entry.config(state="disabled")
    
  def clear_frame(self, frame):
    for widget in self.frame.winfo_children(): #Destroying the page self.frame.destroy()
      widget.destroy()



#Formats
c1 = "#FFFFFF"
c2 = "#212121" #"#101010"
c3 = "#A0A0A0"
h1 = ('sans-serif', 14, "bold")
t1 = ('sans-serif', 12)
t1b = ('sans-serif', 12, 'bold')


root = tk.Tk()
MyApp(root)
root.mainloop()