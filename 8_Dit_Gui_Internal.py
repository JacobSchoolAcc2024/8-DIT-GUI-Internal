import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import sys
import time
import threading


class GameLogic:
    def __init__(self, gui, root):
        self.gui = gui
        self.root = root
        self.toast = None
        self.money = 0

        self.ores = 0
        self.baseMiningSpeed = 5
        self.baseOreGain = 1

        self.product1 = 0
        self.product1Requirement = 2
        self.baseMakeSpeed = 5
        self.baseProductGain = 1
        self.productValue = 5
        self.productValueMulti = 1 

        self.sellProduct1Requirement = 1
        self.sellProductSpeed = 5

        self.upgradeOreRequirement = 5
        self.upgradeProductValueRequirement = 10

        self.combineProductRequirement = 3
        self.combineProductSpeed = 10

    def show_toast(self, message, duration=1000):
        if self.toast:
            self.toast.destroy()
    
        toast = tk.Toplevel(self.root)
        toast.withdraw()
        toast.overrideredirect(True)
        toast.configure(bg="#1e1e2f") 
        toast.attributes("-topmost", True)

        toast.update_idletasks()  
        x = self.root.winfo_x() + self.root.winfo_width() - 300
        y = self.root.winfo_y() + self.root.winfo_height() - 120
        toast.geometry(f"280x50+{x}+{y}")

        tk.Label(
            toast,
            text=message,
            bg="#1e1e2f",
            fg="#ffcc00",
            font=("Arial", 14),
            padx=10,
            pady=10
        ).pack(fill="both", expand=True)

        toast.deiconify()
        toast.after(duration, toast.destroy)


    
    def validate(self,current,required):
        if current >= required:
            return True
        else:
            return False

    def update_gui(self):
        self.gui.oreLabel.config(text = f'Ores: {self.ores}')
        self.gui.productLabel.config(text = f'Product Made: {self.product1}')
        self.gui.moneyLabel.config(text = f'Money: ${self.money}')
        self.gui.oreGainLabel.config(text = f'Ore Gain: {self.baseOreGain}')
        self.gui.productValueLabel.config(text = f'Product Value: ${float(self.product1*(self.productValue*self.productValueMulti))}')
        self.gui.productValueMultiLabel.config(text = f'Multiplier: {float(self.productValueMulti)}')

        self.gui.oreUpgrade.config(text = f'(${self.upgradeOreRequirement}) Upgrade Ores')
        self.gui.productUpgrade.config(text = f'(${self.upgradeProductValueRequirement}) Upgrade Produce Value')

    def start_timer(self, timer,label):
        for i in range(timer, -1, -1):
            label.config(text=f'{i}s')
            time.sleep(1)

    def start(self,btn,speed,label,after_func = None):
        def run():
            btn.config(state="disabled")
            self.start_timer(speed,label)
            label.config(text=f'')
            self.update_gui()
            if after_func:
                after_func()
            btn.config(state="normal")
        threading.Thread(target=run).start()

    def mine_ores(self):
        btn = self.gui.mineButton
        label = self.gui.mineWait
        speed = self.baseMiningSpeed

        def finishedMining():
            self.ores += self.baseOreGain
            self.show_toast(f"+ {self.baseOreGain} ore")
            self.update_gui()

        self.start(btn, speed, label, after_func=finishedMining)


    def make_product(self):
        okay = self.validate(self.ores, self.product1Requirement)
        missing = self.product1Requirement - self.ores
        def finishedProduct():
            self.product1 += self.baseProductGain
            self.show_toast(f"+ {self.baseProductGain} product")
            self.update_gui()
        if okay == True:
            btn = self.gui.makeButton
            speed = self.baseMakeSpeed
            label = self.gui.makeWait
            self.start(btn,speed,label, after_func=finishedProduct)
            self.ores -= self.product1Requirement
            self.update_gui()
        else:
            self.show_toast(f"Need {missing} ores to make a product!")

    def sell_product(self):
        okay = self.validate(self.product1,self.sellProduct1Requirement)
        selling = self.product1 * self.sellProduct1Requirement
        increase = selling * (self.productValue * self.productValueMulti)
        def finishedSelling():
            self.money += increase
            self.productValue = 5 * self.productValueMulti
            self.show_toast(f"+ ${increase}")
            self.update_gui()
        if okay == True:
            btn = self.gui.sellButton
            speed = self.sellProductSpeed
            label = self.gui.sellWait
            self.start(btn,speed,label,after_func=finishedSelling)
            self.product1 -= selling
            self.update_gui()
        else:
            self.show_toast("No products to sell!")

    def upgrade_ores(self):
        okay = self.validate(self.money,self.upgradeOreRequirement)
        buying = self.upgradeOreRequirement - self.money
        if okay == True:
            self.money -= self.upgradeOreRequirement
            self.baseOreGain += 1
            self.upgradeOreRequirement += 10
            self.show_toast(f"Ore gain + 1")
            self.update_gui()
        else:
            self.show_toast(f"You need ${float(buying)}")

    def upgrade_product_value(self):
        okay = self.validate(self.money,self.upgradeProductValueRequirement)
        buying = self.upgradeProductValueRequirement - self.money
        if okay == True:
            self.money -= self.upgradeProductValueRequirement
            self.productValueMulti += 0.5
            self.upgradeProductValueRequirement += 20
            self.show_toast("Product Value + 50%")
            self.update_gui()
        else:
            self.show_toast(f"You need ${float(buying)}")

    def combine_product(self):
        okay = self.validate(self.product1,self.combineProductRequirement)
        combining = self.combineProductRequirement - self.product1

        def finishedCombining():
            self.productValue += 20
            self.show_toast("Product Value + 20")
            self.update_gui()

        if okay == True:
            btn = self.gui.combineButton
            speed = self.combineProductSpeed
            label = self.gui.combineButtonLabel
            self.start(btn,speed,label,after_func=finishedCombining)
            self.product1 -= self.combineProductRequirement
            self.update_gui()
        else:
            self.show_toast( f"Need {combining} products to combine")

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.user_name = ""

        PRIMARY_BG = "#1e1e2f"
        SECONDARY_BG = "#2c2c3c"
        ACCENT = "#ffcc00"
        TEXT_COLOR = "#ffffff"
        SUBTEXT_COLOR = "#bbbbbb"
        BUTTON_BG = "#3e3e5e"
        BUTTON_FG = "#ffffff"
        BUTTON_ACTIVE_BG = "#00c896"

        root.configure(bg=PRIMARY_BG)

        for i in range(3):
            root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(0, weight=0)
        for i in range(3):
            root.grid_rowconfigure(i+1, weight=1)

        status_frame = tk.Frame(root, bg=SECONDARY_BG)
        status_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        for i in range(4):
            status_frame.grid_columnconfigure(i, weight=1)

        creation_frame = tk.Frame(root, bg=PRIMARY_BG)
        creation_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        for i in range(2):
            creation_frame.grid_columnconfigure(i, weight=1)

        upgrade_frame = tk.Frame(root, bg=SECONDARY_BG)
        upgrade_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        for i in range(2):
            upgrade_frame.grid_columnconfigure(i, weight=1)
        
        name_frame = tk.Frame(root, bg=PRIMARY_BG)
        name_frame.grid(row=3,column=0, columnspan=3, sticky="nsew",padx=5,pady=5)

        name_frame.grid_columnconfigure(0, weight=1)
        name_frame.grid_columnconfigure(1, weight=3)  # This column should get more weight for centering
        name_frame.grid_columnconfigure(2, weight=1)

                # Modern Fonts
        FONT_LARGE = ('Roboto', 20, 'bold')
        FONT_MEDIUM = ('Roboto', 18)

        # Status Labels
        self.moneyLabel = tk.Label(status_frame, text="Money: $0", font=FONT_LARGE, fg=ACCENT, bg=SECONDARY_BG)
        self.moneyLabel.grid(row=0, column=0, sticky="w")

        self.productValueLabel = tk.Label(status_frame, text="Product Value: 0", font=FONT_MEDIUM, fg=ACCENT, bg=SECONDARY_BG)
        self.productValueLabel.grid(row=1, column=0, sticky="w")

        self.oreLabel = tk.Label(status_frame, text="Ores: 0", font=FONT_LARGE, fg=TEXT_COLOR, bg=SECONDARY_BG)
        self.oreLabel.grid(row=0, column=1)

        self.oreGainLabel = tk.Label(status_frame, text="Ore Gain: 1", font=FONT_MEDIUM, fg=TEXT_COLOR, bg=SECONDARY_BG)
        self.oreGainLabel.grid(row=1, column=1)

        self.productLabel = tk.Label(status_frame, text="Product Made: 0", font=FONT_LARGE, fg=TEXT_COLOR, bg=SECONDARY_BG)
        self.productLabel.grid(row=0, column=3, sticky="e")

        self.productValueMultiLabel = tk.Label(status_frame, text="Multiplier: 1.0", font=FONT_MEDIUM, fg=TEXT_COLOR, bg=SECONDARY_BG)
        self.productValueMultiLabel.grid(row=1, column=3, sticky="e")

        # Creation Buttons
        self.sellButton = tk.Button(creation_frame, text="Sell Product", font=FONT_LARGE, fg=BUTTON_FG, bg=BUTTON_BG,
                                    activebackground=BUTTON_ACTIVE_BG, width=10)
        self.sellButton.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.sellWait = tk.Label(creation_frame, text="", font=FONT_MEDIUM, fg=SUBTEXT_COLOR, bg=PRIMARY_BG)
        self.sellWait.grid(row=1, column=0, sticky="n", padx=10)

        self.combineButton = tk.Button(creation_frame, text="Combine Product", font=FONT_LARGE, fg=BUTTON_FG,
                                       bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, width=15)
        self.combineButton.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        self.combineButtonLabel = tk.Label(creation_frame, text="", font=FONT_MEDIUM, fg=SUBTEXT_COLOR, bg=PRIMARY_BG)
        self.combineButtonLabel.grid(row=3, column=0, sticky="n", padx=10)

        self.mineButton = tk.Button(creation_frame, text="Mine Ores", font=FONT_LARGE, fg="#ff6666",
                                    bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, width=15)
        self.mineButton.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        self.mineWait = tk.Label(creation_frame, text="", font=FONT_MEDIUM, fg=SUBTEXT_COLOR, bg=PRIMARY_BG)
        self.mineWait.grid(row=1, column=1, sticky="n", padx=10)

        self.makeButton = tk.Button(creation_frame, text="Make Product", font=FONT_LARGE, fg="#ff6666",
                                    bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, width=15)
        self.makeButton.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

        self.makeWait = tk.Label(creation_frame, text="", font=FONT_MEDIUM, fg=SUBTEXT_COLOR, bg=PRIMARY_BG)
        self.makeWait.grid(row=3, column=1, sticky="n", padx=10)

        # Upgrade Buttons
        self.oreUpgrade = tk.Button(upgrade_frame, text="($5) Upgrade Ores", font=FONT_LARGE, fg=TEXT_COLOR,
                                    bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, width=15)
        self.oreUpgrade.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        self.productUpgrade = tk.Button(upgrade_frame, text="($10) Upgrade Product Value", font=FONT_LARGE,
                                        fg=TEXT_COLOR, bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, width=15)
        self.productUpgrade.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.name = tk.Label(name_frame, text="Idle", font=FONT_LARGE,
                                        fg=TEXT_COLOR, bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, width=15)
        self.name.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.ask_name()

    def ask_name(self):
        while True:
            name = simpledialog.askstring("Enter name", "Please enter your name (max 10 letters):")

            # If user clicks Cancel or closes the dialog
            if name is None:
                messagebox.showinfo("Exit", "Name is required to play. Exiting game.")
                self.root.destroy()
                sys.exit()

            name = name.strip()

            # If user presses OK with empty or whitespace-only name
            if not name:
                messagebox.showerror("Invalid Name", "Name cannot be empty.")
                continue

            # Name too long
            if len(name) < 3 or len(name) > 10:
                messagebox.showerror("Invalid Name", "Name must be 10 characters or fewer.")
                continue

            # Name contains non-letter characters
            if not name.isalpha():
                messagebox.showerror("Invalid Name", "Name must contain letters only (no numbers or symbols).")
                continue

            # If all checks pass
            self.user_name = name.capitalize()
            break

class GuiController:
    def __init__(self,gui,logic):
        self.gui = gui
        self.logic = logic

    def handleMining(self):
        self.logic.mine_ores()
    
    def handleProduct(self):
        self.logic.make_product()

    def handleSelling(self):
        self.logic.sell_product()

    def handleOreUpgrade(self):
        self.logic.upgrade_ores()
    
    def handleCombination(self):
        self.logic.combine_product()
    
    def handleProductValueUpgrade(self):
        self.logic.upgrade_product_value()
        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")
    root.title("Idle Game")

    gui = GameGUI(root)
    logic = GameLogic(gui,root)
    controller = GuiController(gui, logic)

    gui.name.config(text=f'{gui.user_name}: The Epic Miner')

    gui.mineButton.config(command=controller.handleMining) 
    gui.makeButton.config(command=controller.handleProduct)
    gui.sellButton.config(command=controller.handleSelling)
    gui.oreUpgrade.config(command=controller.handleOreUpgrade)
    gui.combineButton.config(command=controller.handleCombination)
    gui.productUpgrade.config(command=controller.handleProductValueUpgrade)

    root.mainloop()

