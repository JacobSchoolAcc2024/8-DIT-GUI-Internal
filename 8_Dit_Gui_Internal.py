import tkinter as tk
from tkinter import messagebox
from idlelib.tooltip import Hovertip
import time
import threading


class GameLogic:
    def __init__(self, gui):
        self.gui = gui
        self.strength = 1
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
    
    def validate(self,current,required):
        if current >= required:
            return True
        else:
            return False

    def updateGUi(self):
        self.gui.oreLabel.config(text = f'Ores: {self.ores}')
        self.gui.productLabel.config(text = f'Product Made: {self.product1}')
        self.gui.moneyLabel.config(text = f'Money: ${self.money}')
        self.gui.oreGainLabel.config(text = f'Ore Gain: {self.baseOreGain}')
        self.gui.productValueLabel.config(text = f'Product Value: ${float(self.productValue*self.productValueMulti)}')
        self.gui.productValueMultiLabel.config(text = f'Product Value Multiplier: {float(self.productValueMulti)}')

        self.gui.oreUpgrade.config(text = f'(${self.upgradeOreRequirement}) Upgrade Ores')

    def start_timer(self, timer,label):
        for i in range(timer, -1, -1):
            label.config(text=f'{i}s')
            time.sleep(1)

    def start(self,btn,speed,label,after_func = None):
        def run():
            btn.config(state="disabled")
            self.start_timer(speed,label)
            btn.config(state="normal")
            label.config(text=f'')
            self.updateGUi()
            if after_func:
                after_func()
        threading.Thread(target=run).start()

    def mine_ores(self):
        btn = self.gui.mineButton
        label = self.gui.mineWait
        speed = self.baseMiningSpeed

        def finishedMining():
            self.ores += self.baseOreGain
            self.updateGUi()

        self.start(btn, speed, label, after_func=finishedMining)


    def make_product(self):
        okay = self.validate(self.ores, self.product1Requirement)
        missing = self.product1Requirement - self.ores
        def finishedProduct():
            self.product1 += self.baseProductGain
            self.updateGUi()
        if okay == True:
            btn = self.gui.makeButton
            speed = self.baseMakeSpeed
            label = self.gui.makeWait
            self.start(btn,speed,label, after_func=finishedProduct)
            self.ores -= self.product1Requirement
            self.updateGUi()
        else:
            messagebox.showerror("Insufficient Ores", f"You need {missing} more ores")

    def sell_product(self):
        okay = self.validate(self.product1,self.sellProduct1Requirement)
        selling = self.product1 * self.sellProduct1Requirement
        def finishedSelling():
            self.money += selling * (self.productValue * self.productValueMulti)
            self.productValue = 5 * self.productValueMulti
            self.updateGUi()
        if okay == True:
            pass
            btn = self.gui.sellButton
            speed = self.sellProductSpeed
            label = self.gui.sellWait
            self.start(btn,speed,label,after_func=finishedSelling)
            self.product1 -= selling
            self.updateGUi()
        else:
            messagebox.showerror("Insufficient product", f"You need {self.sellProduct1Requirement} product to sell")

    def upgradeOres(self):
        okay = self.validate(self.money,self.upgradeOreRequirement)
        buying = self.upgradeOreRequirement - self.money
        if okay == True:
            self.money -= self.upgradeOreRequirement
            self.baseOreGain += 1
            self.upgradeOreRequirement += 10
            self.updateGUi()
        else:
            messagebox.showerror("Insufficient money", f"You need ${float(buying)}")

    def upgradeProductValue(self):
        okay = self.validate(self.money,self.upgradeProductValueRequirement)
        buying = self.upgradeProductValueRequirement - self.money
        if okay == True:
            self.money -= self.upgradeProductValueRequirement
            self.productValueMulti += 0.5
            self.upgradeProductValueRequirement += 20
            self.updateGUi()
        else:
            messagebox.showerror("Insufficient money", f"You need ${float(buying)}")
    
    def combineProduct(self):
        okay = self.validate(self.product1,self.combineProductRequirement)
        combining = self.combineProductRequirement - self.product1

        def finishedCombining():
            self.productValue += 20
            self.updateGUi()

        if okay == True:
            btn = self.gui.combineButton
            speed = self.combineProductSpeed
            label = self.gui.combineButtonLabel
            self.start(btn,speed,label,after_func=finishedCombining)
            self.product1 -= self.combineProductRequirement
            self.updateGUi()
        else:
            messagebox.showerror("Insufficient Products", f"You need {combining} products to perform combination")

        
class GameGUI:
    def __init__(self, root):
        self.root = root

        for i in range(3):
            root.grid_columnconfigure(i, weight=1)

        root.grid_rowconfigure(0, weight=0)
        for i in range(2):
            root.grid_rowconfigure(i+1, weight=1)
            
        statusFrame = tk.Frame(root, bg="grey")
        statusFrame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        for i in range(4):
            statusFrame.grid_columnconfigure(i, weight=1)
  
        creationFrame = tk.Frame(root, bg="black")
        creationFrame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        for i in range(2):
            creationFrame.grid_columnconfigure(i, weight=1)
        for i in range(4):
            creationFrame.grid_rowconfigure(i, weight=0)

        upgradeFrame = tk.Frame(root, bg="grey")
        upgradeFrame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        for i in range(2):
            upgradeFrame.grid_columnconfigure(i, weight=1)
        ############################################################

        
        ############################################################

        self.moneyLabel = tk.Label(statusFrame, text="Money: $0", font=('Arial', 20),
                 fg="yellow", bg='grey')
        self.moneyLabel.grid(row=0, column=0, sticky="w")

        self.productValueLabel = tk.Label(statusFrame, text="Product Value: $5.0", font=('Arial', 20),
                 fg="yellow", bg='grey')
        self.productValueLabel.grid(row=1, column=0, sticky="w")

        self.productValueMultiLabel = tk.Label(statusFrame, text="Product Value Multiplier: 1.0", font=('Arial', 20),
                 fg="yellow", bg='grey')
        self.productValueMultiLabel.grid(row=2, column=0, sticky="w")
        
        self.oreLabel = tk.Label(statusFrame, text="Ores: 0", font=('Arial', 20),
                 fg="white", bg='grey')
        self.oreLabel.grid(row=0, column=1)

        self.oreGainLabel = tk.Label(statusFrame, text="Ore Gain: 1", font=('Arial', 20),
                 fg="white", bg='grey')
        self.oreGainLabel.grid(row=1, column=1)

        self.productLabel = tk.Label(statusFrame, text="Product Made: 0", font=('Arial', 20),
                                     fg='white', bg='grey')
        self.productLabel.grid(row=0,column=3,sticky="e")

        self.sellButton = tk.Button(creationFrame, text="Sell Product", font=('Arial', 20),
                  fg='yellow', bg='black', width=15)
        self.sellButton.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.sellWait = tk.Label(creationFrame, text="", font=('Arial', 16),
                 fg='white', bg='black')
        self.sellWait.grid(row=1, column=0, sticky="n", padx=10)

        self.combineButton = tk.Button(creationFrame, text="Combine Product", font=('Arial', 20),
                  fg='yellow', bg='black', width=15)
        self.combineButton.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        self.combineButtonLabel = tk.Label(creationFrame, text="", font=('Arial', 16),
                 fg='white', bg='black')
        self.combineButtonLabel.grid(row=3, column=0, sticky="n", padx=10)

        self.mineButton = tk.Button(creationFrame, text="Mine Ores", font=('Arial', 20),
                  fg='red', bg='black', width=15)
        self.mineButton.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        self.mineWait = tk.Label(creationFrame, text="", font=('Arial', 16),
                 fg='white', bg='black')
        self.mineWait.grid(row=1, column=1, sticky="n", padx=10)

        self.makeButton = tk.Button(creationFrame, text="Make Product", font=('Arial', 20),
                  fg='red', bg='black', width=15)
        self.makeButton.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

        self.makeWait = tk.Label(creationFrame, text="", font=('Arial', 16),
                 fg='white', bg='black')
        self.makeWait.grid(row=3, column=1, sticky="n", padx=10)

        ############################################################

        self.oreUpgrade = tk.Button(upgradeFrame, text="($5) Upgrade Ores", font=('Arial', 20),
                  fg='white', bg='grey', width=15)
        self.oreUpgrade.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        Hovertip(self.oreUpgrade, "Increases ores gained from mining by 1", hover_delay=100)

        self.productUpgrade = tk.Button(upgradeFrame, text="($10) Upgrade Product Value", font=('Arial', 20),
                  fg='white', bg='grey', width=15)
        self.productUpgrade.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        Hovertip(self.productUpgrade,"Increases product value by 2", hover_delay=100)

        
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
        self.logic.upgradeOres()
    
    def handleCombination(self):
        self.logic.combineProduct()
    
    def handleProductValueUpgrade(self):
        self.logic.upgradeProductValue()
        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")
    root.title("Idle Gym")

    gui = GameGUI(root)
    logic = GameLogic(gui)
    controller = GuiController(gui, logic)

    gui.mineButton.config(command=controller.handleMining) 
    gui.makeButton.config(command=controller.handleProduct)
    gui.sellButton.config(command=controller.handleSelling)
    gui.oreUpgrade.config(command=controller.handleOreUpgrade)
    gui.combineButton.config(command=controller.handleCombination)
    gui.productUpgrade.config(command=controller.handleProductValueUpgrade)

    root.mainloop()

