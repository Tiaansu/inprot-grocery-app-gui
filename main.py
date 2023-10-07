import sqlite3 as sqlite
import customtkinter as ctk
from tkinter.messagebox import *
import random
from functools import partial
from PIL import Image
import os
from tabulate import tabulate

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

con = sqlite.connect('grocery-app.db')
cur = con.cursor()

APP_WIDTH = 800
APP_HEIGHT = 600
FG_COLOR = ['gray81', 'gray20']

shoppingCartItems = []

def getCategory(categoryId: int):
    category = 'unknown'

    match categoryId:
        case 0: category = 'Fruits'
        case 1: category = 'Vegetables'
        case 2: category = 'Meats'
        case 3: category = 'Seafoods'
        case 4: category = 'Dairy and eggs'
        case 5: category = 'Pantry items'
        case 6: category = 'Drinks'
        case 7: category = 'Others'
        case 8: category = 'Rice cakes'
        case 9: category = 'Sweets'

    return category

class LoadGroceryItemsFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.headerFont = parent.headerFont
        self.subtitleFont = parent.subtitleFont
        self.normalFont = parent.normalFont
        self.buttonFont = parent.buttonFont
        self.configure(fg_color=FG_COLOR)

        MAXIMUM_VALUE = 78
        MINIMUM_VALUE = 0
        
        self.pack()

        self.header = ctk.CTkLabel(self, text='Loading grocery items...', font=parent.headerFont)
        self.header.place(relx=0.5, rely=0.1, anchor='center')

        self.subtitle = ctk.CTkLabel(self, text='This might take a while.', font=parent.subtitleFont)
        self.subtitle.place(relx=0.5, rely=0.15, anchor='center')

        self.progress_bar = ctk.CTkProgressBar(self, orientation='horizontal', width=600, height=15)
        self.progress_bar.place(relx=0.5, rely=0.3, anchor='center')

        groceryItems = [
            [
                ["Mangoes",                 35],
                ["Bananas",                 30],
                ["Pineapples",              30],
                ["Papayas",                 25],
                ["Oranges",                 25],
                ["Apples",                  20],
                ["Grapes",                  35],
                ["Watermelons",             50],
                ["Cantaloupe",              40]
            ],
            [
                ["Broccoli",                15],
                ["Carrots",                 20],
                ["Cauliflower",             15],
                ["Celery",                   5],
                ["Onions",                  10],
                ["Potatoes",                15],
                ["Tomatoes",                15]
            ],
            [
                ["Chicken",                120],
                ["Pork",                   150],
                ["Beef",                   200],
                ["Hotdogs",                 30],
                ["Bacon",                   60],
                ["Sausage",                 40]
            ],
            [
                ["Fish",                   120],
                ["Shrimp",                 150],
                ["Squid",                  150],
                ["Crab",                   135],
                ["Tuna",                   200],
                ["Sardines",               135]
            ],
            [
                ["Milk",                    25],
                ["Cheese",                  40],
                ["Eggs (per tray)",         30],
                ["Yogurt",                  25],
                ["Butter",                  25],
                ["Ice cream",               20]
            ],
            [
                ["Rice (sack)",           1250],
                ["Bread",                   50],
                ["Flour",                   50],
                ["Sugar",                   25],
                ["Salt",                    25],
                ["Pepper",                  10],
                ["Garlic",                   5],
                ["Onions",                   5],
                ["Cooking oil",             10],
                ["Soy sauce",               10],
                ["Vinegar",                 10],
                ["Bagoong isda",            35],
                ["Bagoong alamang",         35],
                ["Patis",                   15],
                ["Sardines (canned)",       20],
                ["Tuna (canned)",           20],
                ["Corned beef",             20],
                ["Fruits (canned)",         20],
                ["Vegetables (canned)",     20],
                ["Instant noodles",         15],
                ["Pasta",                   20],
                ["Cereal",                  20],
                ["Chips",                   15],
                ["Cookies",                 10],
                ["Candy (pack)",            25]
            ],
            [
                ["Water",                   15],
                ["Juice",                   15],
                ["Soda",                    15],
                ["Coffee",                  15],
                ["Tea",                     15]
            ],
            [
                ["Shampoo",                 10],
                ["Soap",                    10],
                ["Toothpaste",              10],
                ["Deodorant",               10],
                ["Pet food",               100],
                ["Baby supplies",           50]
            ],
            [
                ["Puto",                    15],
                ["Bibingka",                25],
                ["Kutsinta",                 5],
                ["Kalamay",                 15]
            ],
            [
                ["Halo-halo",               15],
                ["Leche flan",              25],
                ["Turon",                   15],
                ["Taho",                    10]
            ]
        ]

        con.execute('DROP TABLE IF EXISTS grocery_items')
        con.execute("""
            CREATE TABLE grocery_items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category INTEGER NOT NULL,
                stocks INTEGER NOT NULL,
                price INTEGER NOT NULL
            )
        """)

        self.progress_text = ctk.CTkTextbox(self, width=600, height=300)
        self.progress_text.grid(padx=(20, 0), pady=(20, 0), sticky='nsew')
        self.progress_text.place(relx=0.5, rely=0.6, anchor='center')

        curIndex = 0
        for index, element in enumerate(groceryItems):
            for _, el in enumerate(element):
                curIndex += 1
                stocks = random.randint(0, 200)
                cur.execute('INSERT INTO grocery_items (name, price, category, stocks) VALUES (?, ?, ?, ?)', (el[0], el[1], index, stocks))
                con.commit()
                value = (((curIndex - MINIMUM_VALUE) / (MAXIMUM_VALUE - MINIMUM_VALUE)) * 100) / 100
                self.progress_bar.set(value)
                self.progress_text.insert('0.0', f'Added item {el[0]}, category {getCategory(index)}, stocks {stocks}, price ₱{el[1]}\n')
                self.update()

        self.progress_text.insert('0.0', 'Done loading items.\n')
        self.progress_text.configure(state='disabled')

        showinfo(title='Tindahan ni Aling Nena', message='Done loading grocery items.')

        self.backToMainMenu()

    def backToMainMenu(self):
        self = HomePageFrame(parent=self, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)

class BrowseCategoriesFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.headerFont = parent.headerFont
        self.subtitleFont = parent.subtitleFont
        self.normalFont = parent.normalFont
        self.buttonFont = parent.buttonFont
        self.configure(fg_color=FG_COLOR)

        self.pack()

        self.header = ctk.CTkLabel(self, text='Categories', font=parent.headerFont)
        self.header.place(relx=0.5, rely=0.1, anchor='center')

        self.categories_container = ctk.CTkScrollableFrame(self, label_text='Choose the category below:', width=475, label_font=parent.subtitleFont)
        self.categories_container.place(relx=0.5, rely=0.4, anchor='center')

        self.buttons = []
        for i in range(10):
            currentCategoryId = i
            browseCategoryItems = partial(self.browseCategoryItems, categoryId=currentCategoryId)
            btn = ctk.CTkButton(self.categories_container, text=getCategory(i), width=150, height=125, font=parent.buttonFont, command=browseCategoryItems)
            self.buttons.append(btn)

        currentColumn = 0
        currentRow = 0
        for index, _ in enumerate(self.buttons):
            if currentColumn + 1 > 3:
                currentColumn = 0
                currentRow += 1

            self.buttons[index].grid(row=currentRow, column=currentColumn, padx=5, pady=5)

            currentColumn += 1

        self.back_to_main_menu_button = ctk.CTkButton(self, text='Back to Main Menu', width=345, height=50, font=parent.buttonFont, command=self.backToMainMenu)
        self.back_to_main_menu_button.place(relx=0.25, rely=0.8, anchor='center')

        self.view_shopping_cart_button = ctk.CTkButton(self, text='View shopping cart', width=345, height=50, font=parent.buttonFont, command=self.viewShoppingCart)
        self.view_shopping_cart_button.place(relx=0.75, rely=0.8, anchor='center')

    def backToMainMenu(self):
        self = HomePageFrame(parent=self, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)

    def viewShoppingCart(self):
        if len(shoppingCartItems) <= 0:
            showerror(title='Tindahan ni Aling Nena - Shopping cart', message='Your shopping cart is still empty, please add items to your cart.')
        else:
            self = ShoppingCartFrame(parent=self, categoryId=-1, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)

    def browseCategoryItems(self, categoryId):
        self = BrowseCategoryItems(parent=self, category=categoryId, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)

class BrowseCategoryItems(ctk.CTkFrame):
    def __init__(self, parent, category, **kwargs):
        super().__init__(parent, **kwargs)
        self.headerFont = parent.headerFont
        self.subtitleFont = parent.subtitleFont
        self.normalFont = parent.normalFont
        self.buttonFont = parent.buttonFont
        self.category = category
        self.configure(fg_color=FG_COLOR)

        self.pack()

        self.header = ctk.CTkLabel(self, text=getCategory(category), font=parent.headerFont)
        self.header.place(relx=0.5, rely=0.1, anchor='center')

        self.items_container = ctk.CTkScrollableFrame(self, label_text='Choose the item(s) below:', width=625, height=300, label_font=parent.subtitleFont)
        self.items_container.place(relx=0.5, rely=0.45, anchor='center')

        result = cur.execute('SELECT * FROM grocery_items WHERE category = ?', [(category)])
        result = result.fetchall()

        groceryItems = []
        
        for element in result:
            id, name, categoryId, stocks, price = element
            groceryItems.append([id, name, getCategory(categoryId), stocks, price])

        self.item_frames = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        for index, element in enumerate(groceryItems):
            currentElement = element
            promptInputQuantityDialog = partial(self.promptInputQuantityDialog, element=currentElement)

            item_frame = ctk.CTkFrame(self.items_container, width=200, height=125, fg_color=FG_COLOR)

            item_name = ctk.CTkLabel(item_frame, text=element[1], font=parent.normalFont)
            item_name.place(relx=0.2, rely=0.05)

            item_preview = ctk.CTkLabel(item_frame, text='', image=ctk.CTkImage(Image.open(os.path.join(current_dir, 'Images', 'products', f'{element[1]}.png'))))
            item_preview.place(relx=0.05, rely=0.05)

            item_price_and_stock = ctk.CTkLabel(item_frame, text=f' Price: ₱{element[4]}\nStocks: {element[3] if element[3] > 0 else "out of stock"}', font=parent.normalFont)
            item_price_and_stock.place(relx=0.05, rely=0.35)
            
            item_add_to_cart_button = ctk.CTkButton(item_frame, text='Add to cart', font=parent.buttonFont, command=promptInputQuantityDialog)
            if element[3] <= 0:
                item_add_to_cart_button.configure(state='disabled')
            item_add_to_cart_button.place(relx=0.15, rely=0.675)

            self.item_frames.append(item_frame)

        currentColumn = 0
        currentRow = 0
        for index, _ in enumerate(self.item_frames):
            if currentColumn + 1 > 3:
                currentColumn = 0
                currentRow += 1
            
            self.item_frames[index].grid(row=currentRow, column=currentColumn, padx=5, pady=5)

            currentColumn += 1

        self.back_to_main_menu_button = ctk.CTkButton(self, text='Back to Categories', width=345, height=50, font=parent.buttonFont, command=self.backToCategories)
        self.back_to_main_menu_button.place(relx=0.25, rely=0.875, anchor='center')

        self.view_shopping_cart_button = ctk.CTkButton(self, text='View shopping cart', width=345, height=50, font=parent.buttonFont, command=self.viewShoppingCart)
        self.view_shopping_cart_button.place(relx=0.75, rely=0.875, anchor='center')
    
    def backToCategories(self):
        self = BrowseCategoriesFrame(parent=self, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)

    def viewShoppingCart(self):
        if len(shoppingCartItems) <= 0:
            showerror(title='Tindahan ni Aling Nena - Shopping cart', message='Your shopping cart is still empty, please add items to your cart.')
        else:
            self = ShoppingCartFrame(parent=self, categoryId=self.category, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)

    def promptInputQuantityDialog(self, element):
        DIALOG_WIDTH = 400
        DIALOG_HEIGHT = 200

        for items in shoppingCartItems:
            if items[2] == element[1]:
                dialog = ctk.CTkInputDialog(title=f'Tindahan ni Aling Nena - Add {element[1]} to cart', text=f'Please enter the new quantity below: (Make sure it\'s lower than {element[3]})')

                x = (dialog.winfo_screenwidth() // 2) - (DIALOG_WIDTH // 2)
                y = (dialog.winfo_screenheight() // 2) - (DIALOG_HEIGHT // 2)
                dialog.geometry('{}x{}+{}+{}'.format(DIALOG_WIDTH, DIALOG_HEIGHT, x, y))

                value = dialog.get_input()

                if value != None:
                    if value.isnumeric():
                        finalValue = int(value)

                        if finalValue <= 0:
                            self.promptInputQuantityDialog(element)
                            return

                        if element[3] - finalValue < 0:
                            dialog = askyesno(title=f'Tindahan ni Aling Nena - Add {element[1]} to cart', message=f'Item {element[1]}\'s stock is not enough to your entered quantity, want to continue? (This will override your selected quantity to available stock)')

                            if dialog:
                                finalValue = element[3]
                            else:
                                self.promptInputQuantityDialog(element)
                        
                        dialog = askyesno(title=f'Tindahan ni Aling Nena - Add {element[1]} to cart', message=f'Want to add {element[1]} with {finalValue} quantity to your shopping cart? It will add ₱{element[4] * finalValue} to your total price.')

                        if dialog:
                            items[1] = finalValue
                        else:
                            self.promptInputQuantityDialog(element)
                    else:
                        self.promptInputQuantityDialog(element)
                return
            break

        dialog = ctk.CTkInputDialog(title=f'Tindahan ni Aling Nena - Add {element[1]} to cart', text=f'Please enter the quantity below: (Make sure it\'s lower than {element[3]})')
        
        x = (self.winfo_screenwidth() // 2) - (DIALOG_WIDTH // 2)
        y = (self.winfo_screenheight() // 2) - (DIALOG_HEIGHT // 2)
        dialog.geometry('{}x{}+{}+{}'.format(DIALOG_WIDTH, DIALOG_HEIGHT, x, y))

        value = dialog.get_input()

        if value != None:
            if value.isnumeric():
                finalValue = int(value)

                if finalValue <= 0:
                    self.promptInputQuantityDialog(element)
                    return

                if element[3] - finalValue < 0:
                    dialog = askyesno(title=f'Tindahan ni Aling Nena - Add {element[1]} to cart', message=f'Item {element[1]}\'s stock is not enough to your entered quantity, want to continue? (This will override your selected quantity to available stock)')

                    if dialog:
                        finalValue = element[3]
                    else:
                        self.promptInputQuantityDialog(element)

                dialog = askyesno(title=f'Tindahan ni Aling Nena - Add {element[1]} to cart', message=f'Want to add {element[1]} with {finalValue} quantity to your shopping cart? It will add ₱{element[4] * finalValue} to your total price.')

                if dialog:
                    shoppingCartItems.append([element[0], finalValue, element[1], element[4]])
                else:
                    self.promptInputQuantityDialog(element)
            else:
                self.promptInputQuantityDialog(element)

class ShoppingCartFrame(ctk.CTkFrame):
    def __init__(self, parent, categoryId = -1, **kwargs):
        super().__init__(parent, **kwargs)
        self.headerFont = parent.headerFont
        self.subtitleFont = parent.subtitleFont
        self.normalFont = parent.normalFont
        self.buttonFont = parent.buttonFont
        self.configure(fg_color=FG_COLOR)
        self.categoryId = categoryId

        if len(shoppingCartItems) <= 0:
            if categoryId == -1:
                self = BrowseCategoriesFrame(parent=self, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)
            else:
                self = BrowseCategoryItems(parent=self, category=categoryId, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)
            return

        self.pack()

        self.header = ctk.CTkLabel(self, text='Your shopping cart', font=parent.headerFont)
        self.header.place(relx=0.5, rely=0.1, anchor='center')

        self.items_container = ctk.CTkScrollableFrame(self, label_text='Choose the item(s) below:', width=625, height=300, label_font=parent.subtitleFont)
        self.items_container.place(relx=0.5, rely=0.45, anchor='center')

        self.item_frames = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        for index, element in enumerate(shoppingCartItems):
            currentElement = element
            updateItemDialog = partial(self.updateItemDialog, element=currentElement)

            item_frame = ctk.CTkFrame(self.items_container, width=200, height=150, fg_color=FG_COLOR)

            item_name = ctk.CTkLabel(item_frame, text=element[2], font=parent.normalFont)
            item_name.place(relx=0.2, rely=0.05)

            item_preview = ctk.CTkLabel(item_frame, text='', image=ctk.CTkImage(Image.open(os.path.join(current_dir, 'Images', 'products', f'{element[2]}.png'))))
            item_preview.place(relx=0.05, rely=0.05)

            item_summary = ctk.CTkLabel(item_frame, text=f'Price: ₱{element[3]}\nQuantity: {element[1]}\n\nTotal Price: ₱{element[3] * element[1]}', font=parent.normalFont)
            item_summary.place(relx=0.05, rely=0.25)

            item_update_button = ctk.CTkButton(item_frame, text='Update', font=parent.buttonFont, command=updateItemDialog)
            item_update_button.place(relx=0.15, rely=0.750)

            self.item_frames.append(item_frame)

        currentColumn = 0
        currentRow = 0
        for index, _ in enumerate(self.item_frames):
            if currentColumn + 1 > 3:
                currentColumn = 0
                currentRow += 1

            self.item_frames[index].grid(row=currentRow, column=currentColumn, padx=5, pady=5)

            currentColumn += 1

        self.back_to_last_section_button = ctk.CTkButton(self, text=f'Back to {getCategory(categoryId)} section' if categoryId != -1 else 'Back to Categories', width=345, height=50, font=parent.buttonFont, command=lambda: self.backToLastSection(categoryId))
        self.back_to_last_section_button.place(relx=0.25, rely=0.875, anchor='center')

        self.checkout_button = ctk.CTkButton(self, text='Checkout', width=345, height=50, font=parent.buttonFont, fg_color='#009c0d', hover_color='#006609', command=self.checkoutShoppingCartItems)
        self.checkout_button.place(relx=0.75, rely=0.875, anchor='center')

    def backToLastSection(self, categoryId):
        if categoryId == -1:
            self = BrowseCategoriesFrame(parent=self, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)
        else:
            self = BrowseCategoryItems(parent=self, category=categoryId, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)

    def checkoutShoppingCartItems(self):
        if len(shoppingCartItems) <= 0:
            self = BrowseCategoriesFrame(parent=self, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)
        else:
            DIALOG_WIDTH = 400
            DIALOG_HEIGHT = 200
            
            totalPrice = 0
            for item in shoppingCartItems:
                totalPrice += item[1] * item[3]

            dialog = ctk.CTkInputDialog(title='Tindahan ni Aling Nena - Checkout shopping cart items', text=f'Please enter your money below: (Make sure it\'s higher than ₱{totalPrice})')

            x = (dialog.winfo_screenwidth() // 2) - (DIALOG_WIDTH // 2)
            y = (dialog.winfo_screenheight() // 2) - (DIALOG_HEIGHT // 2)
            dialog.geometry('{}x{}+{}+{}'.format(DIALOG_WIDTH, DIALOG_HEIGHT, x, y))

            value = dialog.get_input()

            if value != None:
                if value.isnumeric():
                    finalValue = int(value)

                    if totalPrice > finalValue:
                        dialog = showwarning(title='Tindahan ni Aling Nena - Checkout shopping cart items', message=f'Insufficient money, you still need ₱{totalPrice - finalValue} to continue.')

                        self.checkoutShoppingCartItems()
                        return
                    self = CheckoutPageFrame(parent=self, money=finalValue, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)
                else:
                    self.checkoutShoppingCartItems()

    def updateItemDialog(self, element):
        DIALOG_WIDTH = 400
        DIALOG_HEIGHT = 200

        result = cur.execute('SELECT * FROM grocery_items WHERE category = ?', [(self.categoryId)]) if self.categoryId != -1 else cur.execute('SELECT * FROM grocery_items')
        result = result.fetchall()

        groceryItems = []
        for dbEl in result:
            id, name, categoryId, stocks, price = dbEl
            groceryItems.append([id, name, getCategory(categoryId), stocks, price])

        if len(shoppingCartItems) <= 0:
            self = BrowseCategoriesFrame(parent=self, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)
        else:
            for index, item in enumerate(shoppingCartItems):
                if item[2] == element[2]:
                    id, quantity, name, price = element
                    dialog = ctk.CTkInputDialog(title=f'Tindahan ni Aling Nena - Update {name}', text=f'Please enter the new quantity below: (Make sure it\'s lower than {quantity})')

                    x = (dialog.winfo_screenwidth() // 2) - (DIALOG_WIDTH // 2)
                    y = (dialog.winfo_screenheight() // 2) - (DIALOG_HEIGHT // 2)
                    dialog.geometry('{}x{}+{}+{}'.format(DIALOG_WIDTH, DIALOG_HEIGHT, x, y))

                    value = dialog.get_input()

                    if value != None:
                        if value.isnumeric():
                            finalValue = int(value)

                            if finalValue <= 0:
                                dialog = askyesno(title=f'Tindahan ni Aling Nena - Remove {name}', text=f'Want to remove item {name} with {quantity} of quantity in your shopping cart? It will decrease your shopping cart\'s total price by ₱{quantity * price}')

                                if dialog:
                                    shoppingCartItems.pop(index)

                                    if len(shoppingCartItems) <= 0:
                                        if self.categoryId == -1:
                                            self = BrowseCategoriesFrame(parent=self, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)
                                        else:
                                            self = BrowseCategoryItems(parent=self, category=self.categoryId, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)
                                else:
                                    self.updateItemDialog(element)
                                return

                            for _, el in enumerate(groceryItems):
                                id, name, category, stocks, price = el
                                if name == element[2]:
                                    if stocks - finalValue <= 0:
                                        dialog = askyesno(title=f'Tindahan ni Aling Nena - Update {element[2]}', message=f'Item {element[2]}\'s stock is not enough to your entered quantity, want to continue? (This will override your selected quantity to available stock)')

                                        if dialog:
                                            finalValue = stocks
                                        else:
                                            self.updateItemDialog(element)
                                    
                                    dialog = askyesno(title=f'Tindahan ni Aling Nena - Update {element[2]}', message=f'Want to set item {element[2]}\'s quantity to {finalValue} ({element[1]} before)? Its total price will be ₱{finalValue * price}')

                                    if dialog:
                                        item[1] = finalValue

                                        self = ShoppingCartFrame(parent=self, categoryId=self.categoryId, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)
                                    else:
                                        self.updateItemDialog(element)
                        else:
                            self.updateItemDialog(element)

class CheckoutPageFrame(ctk.CTkFrame):
    def __init__(self, parent, money, **kwargs):
        super().__init__(parent, **kwargs)
        self.headerFont = parent.headerFont
        self.subtitleFont = parent.subtitleFont
        self.normalFont = parent.normalFont
        self.buttonFont = parent.buttonFont
        self.configure(fg_color=FG_COLOR)
        self.money = money

        self.pack()

        self.header = ctk.CTkLabel(self, text='Checkout item(s)', font=parent.headerFont)
        self.header.place(relx=0.5, rely=0.1, anchor='center')

        self.checkout_text = ctk.CTkTextbox(self, width=600, height=300, font=ctk.CTkFont('Consolas', 24))
        self.checkout_text.grid(padx=(20, 0), pady=(20, 0), sticky='nsew')
        self.checkout_text.place(relx=0.5, rely=0.45, anchor='center')

        headers = ['Item', 'Quantity', 'Price']
        table = []
        totalPrice = 0

        for index, element in enumerate(shoppingCartItems):
            totalPrice += element[3] * element[1]
            table.append([element[2], element[1], f'₱{element[3]}'])
            cur.execute(f'UPDATE grocery_items SET stocks = stocks - {element[1]} WHERE id = ?', [(element[0])])
            con.commit()

        table.append(['-------', '----------', '-------'])
        table.append([' ', 'Subtotal', f'₱{totalPrice}'])
        table.append([' ', 'Payment', f'₱{self.money}'])
        table.append([' ', 'Change', f'₱{self.money - totalPrice}'])

        self.checkout_text.insert('0.0', tabulate(table, headers, tablefmt='simple'))
        self.checkout_text.configure(state='disabled')

        self.back_to_main_menu_button = ctk.CTkButton(self, text='Back to Main Menu', width=700, height=50, font=parent.buttonFont, command=self.backToMainMenu)
        self.back_to_main_menu_button.place(relx=0.5, rely=0.9, anchor='center')

    def backToMainMenu(self):
        self = HomePageFrame(parent=self, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)

class HomePageFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.headerFont = parent.headerFont
        self.subtitleFont = parent.subtitleFont
        self.normalFont = parent.normalFont
        self.buttonFont = parent.buttonFont
        self.configure(fg_color=FG_COLOR)

        self.pack()

        self.header = ctk.CTkLabel(self, text='Tindahan ni Aling Nena', font=parent.headerFont)
        self.header.place(relx=0.5, rely=0.1, anchor='center')

        self.subtitle = ctk.CTkLabel(self, text='Made with ♥ by Marlon & Jericho', font=parent.subtitleFont)
        self.subtitle.place(relx=0.5, rely=0.15, anchor='center')

        self.buttons_message_label = ctk.CTkLabel(self, text='Choose the action below:', font=parent.normalFont)
        self.buttons_message_label.place(relx=0.5, rely=0.4, anchor='center')

        self.load_items_button = ctk.CTkButton(self, text='Generate Grocery Items (re-stock)', width=700, height=50, font=parent.buttonFont, command=self.loadGroceryItems)
        self.load_items_button.place(relx=0.5, rely=0.475, anchor='center')

        self.browse_categories_button = ctk.CTkButton(self, text='Browse Categories', width=700, height=50, font=parent.buttonFont, command=self.browseCategories)
        self.browse_categories_button.place(relx=0.5, rely=0.575, anchor='center')

    def loadGroceryItems(self):
        self = LoadGroceryItemsFrame(parent=self, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)

    def browseCategories(self):
        self = BrowseCategoriesFrame(parent=self, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.update_idletasks()
        self.headerFont = ctk.CTkFont('Cascadia Code', size=24, weight='bold')
        self.subtitleFont = ctk.CTkFont('Cascadia Code', size=14, weight='normal')
        self.normalFont = ctk.CTkFont('Cascadia Code', size=12, weight='normal')
        self.buttonFont = ctk.CTkFont('Cascada Code', size=18, weight='bold')

        self.title('Tindahan ni Aling Nena')
        self.iconbitmap('Images/grocery.ico', 'Images/grocery.ico')
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # It is used to center the CustomTKinter (TKinter) window.
        # Thanks to this answer at stackoverflow: https://stackoverflow.com/a/65782505
        x = (self.winfo_screenwidth() // 2) - (APP_WIDTH // 2)
        y = (self.winfo_screenheight() // 2) - (APP_HEIGHT // 2)
        self.geometry('{}x{}+{}+{}'.format(APP_WIDTH, APP_HEIGHT, x, y))
        
        self.resizable(width=False, height=False)
        self.minsize(APP_WIDTH, APP_HEIGHT)

        self = HomePageFrame(parent=self, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)

if __name__ == '__main__':
    app = App()
    app.mainloop()