import datetime as dt
import sqlite3 as sqlite
import customtkinter as ctk
from tkinter.messagebox import *
import random
from functools import partial
from PIL import Image
import os

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

con = sqlite.connect('grocery-app.db')
cur = con.cursor()

APP_WIDTH = 800
APP_HEIGHT = 600

def getDateNow():
    now = dt.datetime.now()
    weekday = now.strftime('%A')
    month = now.strftime('%B')
    day = now.strftime('%d')
    year = now.strftime('%Y')
    hour = now.strftime('%I')
    minute = now.strftime('%M')
    second = now.strftime('%S')
    meridian = now.strftime('%p')
    return f'{weekday}, {month} {day}, {year} - {hour}:{minute}:{second} {meridian}'

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

        self.pack()

        self.header = ctk.CTkLabel(self, text='Categories', font=parent.headerFont)
        self.header.place(relx=0.5, rely=0.1, anchor='center')

        self.categories_container = ctk.CTkScrollableFrame(self, label_text='Choose the category below:', width=475)
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

        self.back_to_main_menu_button = ctk.CTkButton(self, text='Back to Main Menu', width=700, height=50, font=parent.buttonFont, command=self.backToMainMenu)
        self.back_to_main_menu_button.place(relx=0.5, rely=0.8, anchor='center')

    def backToMainMenu(self):
        self = HomePageFrame(parent=self, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)

    def browseCategoryItems(self, categoryId):
        self = BrowseCategoryItems(parent=self, category=categoryId, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)

class BrowseCategoryItems(ctk.CTkFrame):
    def __init__(self, parent, category, **kwargs):
        super().__init__(parent, **kwargs)
        self.headerFont = parent.headerFont
        self.subtitleFont = parent.subtitleFont
        self.normalFont = parent.normalFont
        self.buttonFont = parent.buttonFont

        self.pack()

        self.header = ctk.CTkLabel(self, text=getCategory(category), font=parent.headerFont)
        self.header.place(relx=0.5, rely=0.1, anchor='center')

        self.items_container = ctk.CTkScrollableFrame(self, label_text='Choose the item(s) below:', width=625, height=300)
        self.items_container.place(relx=0.5, rely=0.45, anchor='center')

        result = cur.execute('SELECT * FROM grocery_items WHERE category = ?', [(category)])
        result = result.fetchall()

        groceryItems = []
        
        for element in result:
            id, name, categoryId, stocks, price = element
            groceryItems.append([id, name, getCategory(categoryId), stocks if stocks > 0 else 'out of stock', price])

        self.item_frames = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        for index, element in enumerate(groceryItems):
            currentItem = index
            currentElement = element
            promptInputQuantityDialog = partial(self.promptInputQuantityDialog, currentIndex=currentItem, element=currentElement)

            item_frame = ctk.CTkFrame(self.items_container, width=200, height=125)

            item_name = ctk.CTkLabel(item_frame, text=element[1], font=parent.normalFont)
            item_name.place(relx=0.2, rely=0.05)

            item_preview = ctk.CTkLabel(item_frame, text='', image=ctk.CTkImage(Image.open(os.path.join(current_dir, 'Images', 'products', f'{element[1]}.png'))))
            item_preview.place(relx=0.05, rely=0.05)

            item_price_and_stock = ctk.CTkLabel(item_frame, text=f' Price: ₱{element[4]}\nStocks: {element[3]}', font=parent.normalFont)
            item_price_and_stock.place(relx=0.05, rely=0.35)
            
            item_add_to_cart_button = ctk.CTkButton(item_frame, text='Add to cart', font=parent.buttonFont, command=promptInputQuantityDialog)
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

        self.back_to_main_menu_button = ctk.CTkButton(self, text='Back to Categories', width=700, height=50, font=parent.buttonFont, command=self.backToCategories)
        self.back_to_main_menu_button.place(relx=0.5, rely=0.9, anchor='center')
    
    def backToCategories(self):
        self = BrowseCategoriesFrame(parent=self, width=APP_WIDTH, height=APP_HEIGHT, corner_radius=0)

    def promptInputQuantityDialog(self, currentIndex, element):
        DIALOG_WIDTH = 400
        DIALOG_HEIGHT = 200
        dialog = ctk.CTkInputDialog(title=f'Tindahan ni Aling Nena - Add {element[1]} to cart', text=f'Please enter the quantity below: (Make sure it\'s lower than {element[3]})')
        
        x = (self.winfo_screenwidth() // 2) - (DIALOG_WIDTH // 2)
        y = (self.winfo_screenheight() // 2) - (DIALOG_HEIGHT // 2)
        dialog.geometry('{}x{}+{}+{}'.format(DIALOG_WIDTH, DIALOG_HEIGHT, x, y))
        
        if not dialog.get_input().isnumeric():
            self.promptInputQuantityDialog(currentIndex, element)
        else:
            print('yey!')

class HomePageFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.headerFont = parent.headerFont
        self.subtitleFont = parent.subtitleFont
        self.normalFont = parent.normalFont
        self.buttonFont = parent.buttonFont

        self.pack()

        self.header = ctk.CTkLabel(self, text='Tindahan ni Aling Nena', font=parent.headerFont)
        self.header.place(relx=0.5, rely=0.1, anchor='center')

        self.subtitle = ctk.CTkLabel(self, text='Made with ♥ by Marlon & Jerico', font=parent.subtitleFont)
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