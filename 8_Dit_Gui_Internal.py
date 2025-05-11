import tkinter as tk
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
        self.baseMakeSpeed = 5
        self.baseProductGain = 1
        self.productValue = 5

    def updateGUi(self):
        self.gui.oreLabel.config(text = f'Ores: {self.ores}')
        self.gui.makeLabel.config(text = f'')

    def start_timer(self, timer,label):
        for i in range(timer, -1, -1):

            label.config(text=f'{i}s')
            time.sleep(1)

    def start(self,btn,speed,label):
        def run():
            btn.config(state="disabled")
            self.start_timer(speed,label)
            btn.config(state="normal")
            label.config(text=f'Wait {speed}')
            self.updateGUi()
        threading.Thread(target=run).start()

    def mine_ores(self):
        btn = self.gui.mineButton
        label = self.gui.mineWait
        speed = self.baseMiningSpeed
        self.ores += self.baseOreGain
        self.start(btn,speed,label)

    def make_product(self):
        btn = self.gui.makeButton
        label = self.gui.makeWait
        speed = self.baseMakeSpeed
        self.product1 += self.baseProductGain

        
        

    
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
        for i in range(3):
            creationFrame.grid_columnconfigure(i, weight=1)
        for i in range(4):
            creationFrame.grid_rowconfigure(i, weight=0)

        optionFrame = tk.Frame(root, bg="grey")
        optionFrame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        for i in range(3):
            optionFrame.grid_columnconfigure(i, weight=1)
        ############################################################

        
        ############################################################
        self.moneyLabel = tk.Label(statusFrame, text="Money: $0", font=('Arial', 20),
                 fg="yellow", bg='grey')
        self.moneyLabel.grid(row=0, column=0, sticky="w")
        
        self.oreLabel = tk.Label(statusFrame, text="Ores: 0", font=('Arial', 20),
                 fg="white", bg='grey')
        self.oreLabel.grid(row=0, column=1)

        self.strengthLabel = tk.Label(statusFrame, text="Strength: 0", font=('Arial', 20),
                 fg='red', bg='grey')
        self.strengthLabel.grid(row=0, column=2, sticky="e")

        self.productLabel = tk.Label(statusFrame, text="Product Made: 0", font=('Arial', 20),
                                     fg='red', bg='grey')
        self.productLabel.grid(row=0,column=3,sticky="e")

        self.sellButton = tk.Button(creationFrame, text="Sell Product", font=('Arial', 20),
                  fg='yellow', bg='black', width=15)
        self.sellButton.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.sellWait = tk.Label(creationFrame, text="Waiting: 1s", font=('Arial', 16),
                 fg='white', bg='black')
        self.sellWait.grid(row=1, column=0, sticky="n", padx=10)

        self.mineButton = tk.Button(creationFrame, text="Mine Ores", font=('Arial', 20),
                  fg='red', bg='black', width=15)
        self.mineButton.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        self.mineWait = tk.Label(creationFrame, text="Waiting: 1s", font=('Arial', 16),
                 fg='white', bg='black')
        self.mineWait.grid(row=1, column=1, sticky="n", padx=10)

        self.makeButton = tk.Button(creationFrame, text="Make Product", font=('Arial', 16),
                  fg='red', bg='black', width=15)
        self.makeButton.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

        self.makeWait = tk.Label(creationFrame, text="Waiting: 1s", font=('Arial', 16),
                 fg='white', bg='black')
        self.makeWait.grid(row=3, column=1, sticky="n", padx=10)
        ############################################################


class GuiController:
    def __init__(self,gui,logic):
        self.gui = gui
        self.logic = logic
    
    def handleMining(self):
        self.logic.mine_ores()
    
    def handleProduct(self):
        self.logic.make_product()
        


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")
    root.title("Idle Gym")

    gui = GameGUI(root)
    logic = GameLogic(gui)
    controller = GuiController(gui, logic)

    gui.mineButton.config(command=controller.handleMining) 

    root.mainloop()

