"""This file runs an incremental idle game."""

# Required imports for GUI, dialogs, multithreading, and system control
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import sys
import time
import threading


class GameLogic:
    """Handle the Idle Game's logic including upgrades and buttons."""

    def __init__(self, gui, root):
        """Tnitialise the class GameLogic instance with gui elements, main root.

            And variables for upgrades, stats, and buttons.

            Prameters:
                the gui is the main interface
                (the main class this one is a support one)
                for displaying the game.
                THe root (tk.Tk) basically the root of tkinter for the game.
        """
        self.gui = gui
        self.root = root
        self.toast = None  # Initialise toast variable as none to store
        self.money = 0  # Got some inital values for my variables

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
        """Show a small popup notif thing on screen.

        Pops up a lil message in the corner of the game window. Mainly used
        to show stuff like "+1 Ore" or whatever the user just did.
        Only shows one at a time, so if there's already one showing,
        it gets removed first.

        Args:
            message (str): What the popup should say
            duration (int): How long it stays up for (in ms). Defaults to 1000

        Stuff it does:
            - deletes any existing toast popup
            - makes a new window with no borders etc
            - places it near the bottom-right of the main app
            - destroys it automatically after a bit
        """
        if self.toast:
            self.toast.destroy()  # If there's one already showing, kill it

        toast = tk.Toplevel(self.root)  # New popup window
        toast.withdraw()  # Hide it while setting it up
        toast.overrideredirect(True)  # No borders/titlebar
        toast.configure(bg="#1e1e2f")  # dark bg
        toast.attributes("-topmost", True)  # stay above other windows

        toast.update_idletasks()
        # make sure sizes are updated before placing it

        # try to stick it near the bottom right
        x = self.root.winfo_x() + self.root.winfo_width() - 300
        y = self.root.winfo_y() + self.root.winfo_height() - 120
        toast.geometry(f"280x50+{x}+{y}")  # size and position

        # slap the label into the window
        tk.Label(
            toast,
            text=message,
            bg="#1e1e2f",
            fg="#ffcc00",
            font=("Arial", 14),
            padx=10,
            pady=10
        ).pack(fill="both", expand=True)

        toast.deiconify()  # finally show it
        toast.after(duration, toast.destroy)  # make it disappear later

    def validate(self, current, required):
        """Check if u got enough of a thing to do it.

        Args:
            current - how much u have currently
            required - how much u need

        Returns:
            True if u got enough, False if nope
        """
        if current >= required:  # got enough stuff
            return True
        else:  # not enough bro
            return False

    def update_gui(self):
        """Make sure all labels are updated with right values."""
        self.gui.ore_label.config(text=f'Ores: {self.ores}')

        self.gui.product_label.config(text=f'Product Made: {self.product1}')

        self.gui.money_label.config(text=f'Money: ${self.money}')

        self.gui.ore_gain_label.config(text=f'Ore Gain: {self.baseOreGain}')

        self.gui.product_value_label.config(text=
        'Product Value:'
        f'${float(self.product1*(self.productValue*self.productValueMulti))}')

        self.gui.product_value_multi_label.config(text=
        f'Multiplier: {float(self.productValueMulti)}') 

        self.gui.ore_upgrade.config(text=
        f'(${self.upgradeOreRequirement}) Upgrade Ores')

        self.gui.product_upgrade.config(text=
        f'(${self.upgradeProductValueRequirement}) Upgrade Produce Value')

    def start_timer(self, timer, label):
        """Start a countdown and updates the label every sec.


        Like a basic timer thing, counts down from 'timer' to 0
        """


        # go from timer down to 0
        for i in range(timer, -1, -1):
            # update the label to show how much time left
            # through each iteration of i, it decreases
            # instead of increasing cuz of -1
            # also made it start at -1 so it ends at 0
            label.config(text=f'{i}s')

            # wait a second before going again
            time.sleep(1)

    def start(self, btn, speed, label, after_func=None):
        """Start the button action, runs timer and updates labels.

        This one disables the button, runs a countdown timer,
        updates the UI, and then re-enables the button when done.
        If theres a function to run after, it runs that too.
        """
        def run():
            # disable the button while it's running to prevent double-clicks
            btn.config(state="disabled")

            # start the countdown timer using the function
            self.start_timer(speed, label)

            # reset the label text once the timer is done
            label.config(text=f'')

            # update the game status on the UI
            self.update_gui()

            # if there's an after function, run it
            if after_func:
                after_func()

            # re-enable the button after everything is done
            btn.config(state="normal")

        # run this in a separate thread so the UI doesn't freeze
        # really important step as running time.sleep
        # will freeze whole gui so doing it
        # in the background was the workaround
        threading.Thread(target=run).start()

    def mine_ores(self):
        """Mine ores, updates the UI and shows a little notification.

        This starts the mining action, disables the button while its running,
        then after the timer is done, adds ores to the stock, shows a toast
        with the ore gained, and updates the game interface.
        """
        btn = self.gui.mine_button
        label = self.gui.mine_wait
        speed = self.baseMiningSpeed

        def finished_mining():
            # adds ores to the stock after mining is finished
            self.ores += self.baseOreGain
            # show the little popup message
            self.show_toast(f"+ {self.baseOreGain} ore")
            # update the game stats in the GUI
            self.update_gui()

        # call the start function to handle the timer and actions
        self.start(btn, speed, label, after_func=finished_mining)

    def make_product(self):
        """Try to make a product if you got enough ores, and updates the stats.

        First, checks if you have enough ores to make a product,
        if so, it starts the making process,
        then updates your inventory and shows a notification.
        Otherwise, it'll show how many ores you still need to continue.
        """
        okay = self.validate(self.ores, self.product1Requirement)
        missing = self.product1Requirement - self.ores

        def finished_product():
            self.product1 += self.baseProductGain
            self.show_toast(f"+ {self.baseProductGain} product")
            self.update_gui()
        if okay is True:  # if we have enough ores, proceed
            btn = self.gui.make_button
            speed = self.baseMakeSpeed
            label = self.gui.make_wait
            self.start(btn, speed, label, after_func=finished_product)
            self.ores -= self.product1Requirement  # subtract the ores used
            self.update_gui()
        else:
            # show a message how many ores you stil need
            self.show_toast(f"Need {missing} ores to make a product!")

    def sell_product(self):
        """Sell product if there's enough.
        Increases money, and updates stats."""
        okay = self.validate(self.product1,
                             self.sellProduct1Requirement)
        selling = self.product1 * self.sellProduct1Requirement
        increase = selling * (self.productValue * self.productValueMulti)

        def finished_selling():
            self.money += increase
            self.productValue = 5 * self.productValueMulti
            self.show_toast(f"+ ${increase}")
            self.update_gui()
        if okay is True:  # we got enough product
            btn = self.gui.sell_button
            speed = self.sellProductSpeed
            label = self.gui.sell_wait
            self.start(btn, speed, label, after_func=finished_selling)
            self.product1 -= selling  # take the products away after selling
            self.update_gui()
        else:
            self.show_toast("No products to sell!")

    def upgrade_ores(self):
        """Upgrade ore gain if you have enough money."""
        okay = self.validate(self.money, self.upgradeOreRequirement)
        buying = self.upgradeOreRequirement - self.money
        if okay is True:  # check if we can afford the upgrade
            self.money -= self.upgradeOreRequirement
            self.baseOreGain += 1
            self.upgradeOreRequirement += 10  # price increases after each upgrade
            self.show_toast(f"Ore gain + 1")
            self.update_gui()
        else:
            self.show_toast(f"You need ${float(buying)}")  # Using float to show decimals


    def upgrade_product_value(self):
        """Upgrade product value if you have enough money."""
        okay = self.validate(self.money, self.upgradeProductValueRequirement)
        buying = self.upgradeProductValueRequirement - self.money
        if okay is True:
            self.money -= self.upgradeProductValueRequirement
            self.productValueMulti += 0.5
            self.upgradeProductValueRequirement += 20  # cost goes up each time
            self.show_toast("Product Value + 50%")
            self.update_gui()
        else:
            self.show_toast(f"You need ${float(buying)}")

    def combine_product(self):
        """Combine products to increase product value."""
        okay = self.validate(self.product1, self.combineProductRequirement)
        combining = self.combineProductRequirement - self.product1

        def finishedCombining():
            self.productValue += 20
            self.show_toast("Product Value + 20")
            self.update_gui()

        if okay is True:
            btn = self.gui.combine_button
            speed = self.combineProductSpeed
            label = self.gui.combine_buttonLabel
            self.start(btn, speed, label, after_func=finishedCombining)
            self.product1 -= self.combineProductRequirement  # take away the products used
            self.update_gui()
        else:
            self.show_toast(f"Need {combining} products to combine")


class GameGUI:
    """Create the main window for the game.

    This includes the layout for status display,creation buttons

    (like Mine, Make, Sell), upgrade options, and a name entry prompt.
    """

    def __init__(self, root):
        """Initialize game window, configure the layout.

        Fonts, colors, and the UI elements for displaying the

        player's stats and interaction buttons.

        Args:
            root (tk.Tk): The main tkinter window.
        """
        self.root = root
        self.user_name = ""

        # Color Scheme
        PRIMARY_BG = "#1e1e2f"
        SECONDARY_BG = "#2c2c3c"
        ACCENT = "#ffcc00"
        TEXT_COLOR = "#ffffff"
        SUBTEXT_COLOR = "#bbbbbb"
        BUTTON_BG = "#3e3e5e"
        BUTTON_FG = "#ffffff"
        BUTTON_ACTIVE_BG = "#00c896"

        # Set the background color of the root window
        root.configure(bg=PRIMARY_BG)

        # Grid configuration for the window
        # using range to set it up for easy editing
        # weight = 1 allows grid to expand
        for i in range(3):
            root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(0, weight=0)
        for i in range(3):
            root.grid_rowconfigure(i+1, weight=1)

        # Frames for the status, creation buttons, and upgrades
        status_frame = tk.Frame(root, bg=SECONDARY_BG)
        status_frame.grid(row=0, column=0, columnspan=4,
                          sticky="ew", padx=5, pady=5)
        for i in range(4):
            status_frame.grid_columnconfigure(i, weight=1)

        creation_frame = tk.Frame(root, bg=PRIMARY_BG)
        creation_frame.grid(row=1, column=0, columnspan=4,
                            sticky="nsew", padx=5, pady=5)
        for i in range(2):
            creation_frame.grid_columnconfigure(i, weight=1)

        upgrade_frame = tk.Frame(root, bg=SECONDARY_BG)
        upgrade_frame.grid(row=2, column=0, columnspan=4,
                           sticky="nsew", padx=5, pady=5)
        for i in range(2):
            upgrade_frame.grid_columnconfigure(i, weight=1)

        # Name entry frame
        name_frame = tk.Frame(root, bg=PRIMARY_BG)
        name_frame.grid(row=3, column=0, columnspan=3,
                        sticky="nsew",
                        padx=5, pady=5)

        name_frame.grid_columnconfigure(0, weight=1)
        name_frame.grid_columnconfigure(1, weight=3)
        # This column more weight for centering
        name_frame.grid_columnconfigure(2, weight=1)

        # Fonts
        FONT_LARGE = ('Roboto', 20, 'bold')
        FONT_MEDIUM = ('Roboto', 18)

        # Status Labels
        self.money_label = tk.Label(status_frame,
                                    text="Money: $0",
                                    font=FONT_LARGE,
                                    fg=ACCENT,
                                    bg=SECONDARY_BG)
        self.money_label.grid(row=0, column=0,
                              sticky="w")

        self.product_value_label = tk.Label(status_frame,
                                            text="Product Value: 0",
                                            font=FONT_MEDIUM,
                                            fg=ACCENT,
                                            bg=SECONDARY_BG)
        self.product_value_label.grid(row=1, column=0,
                                      sticky="w")

        self.ore_label = tk.Label(status_frame,
                                  text="Ores: 0",
                                  font=FONT_LARGE,
                                  fg=TEXT_COLOR,
                                  bg=SECONDARY_BG)
        self.ore_label.grid(row=0, column=1)

        self.ore_gain_label = tk.Label(status_frame,
                                       text="Ore Gain: 1",
                                       font=FONT_MEDIUM,
                                       fg=TEXT_COLOR,
                                       bg=SECONDARY_BG)
        self.ore_gain_label.grid(row=1, column=1)

        self.product_label = tk.Label(status_frame,
                                      text="Product Made: 0",
                                      font=FONT_LARGE,
                                      fg=TEXT_COLOR,
                                      bg=SECONDARY_BG)
        self.product_label.grid(row=0, column=3,
                                sticky="e")

        self.product_value_multi_label = tk.Label(status_frame,
                                                  text="Multiplier: 1.0",
                                                  font=FONT_MEDIUM,
                                                  fg=TEXT_COLOR,
                                                  bg=SECONDARY_BG)
        self.product_value_multi_label.grid(row=1,
                                            column=3, sticky="e")

        # Creation Buttons
        self.sell_button = tk.Button(creation_frame,
                                     text="Sell Product",
                                     font=FONT_LARGE,
                                     fg=BUTTON_FG,
                                     bg=BUTTON_BG,
                                     activebackground=BUTTON_ACTIVE_BG,
                                     width=10)
        self.sell_button.grid(row=0, column=0,
                              sticky="ew", padx=10, pady=10)

        self.sell_wait = tk.Label(creation_frame,
                                  text="",
                                  font=FONT_MEDIUM,
                                  fg=SUBTEXT_COLOR,
                                  bg=PRIMARY_BG)
        self.sell_wait.grid(row=1, column=0,
                            sticky="n", padx=10)

        self.combine_button = tk.Button(creation_frame,
                                        text="Combine Product",
                                        font=FONT_LARGE,
                                        fg=BUTTON_FG,
                                        bg=BUTTON_BG,
                                        activebackground=BUTTON_ACTIVE_BG,
                                        width=15)
        self.combine_button.grid(row=2, column=0,
                                 sticky="ew", padx=10, pady=10)

        self.combine_buttonLabel = tk.Label(creation_frame,
                                            text="",
                                            font=FONT_MEDIUM,
                                            fg=SUBTEXT_COLOR,
                                            bg=PRIMARY_BG)
        self.combine_buttonLabel.grid(row=3, column=0,
                                      sticky="n", padx=10)

        self.mine_button = tk.Button(creation_frame,
                                     text="Mine Ores",
                                     font=FONT_LARGE, fg="#ff6666",
                                     bg=BUTTON_BG,
                                     activebackground=BUTTON_ACTIVE_BG,
                                     width=15)
        self.mine_button.grid(row=0, column=1,
                              sticky="ew", padx=10, pady=10)

        self.mine_wait = tk.Label(creation_frame,
                                  text="",
                                  font=FONT_MEDIUM, fg=SUBTEXT_COLOR,
                                  bg=PRIMARY_BG)
        self.mine_wait.grid(row=1, column=1,
                            sticky="n", padx=10)

        self.make_button = tk.Button(creation_frame,
                                     text="Make Product",
                                     font=FONT_LARGE,
                                     fg="#ff6666",
                                     bg=BUTTON_BG,
                                     activebackground=BUTTON_ACTIVE_BG,
                                     width=15)
        self.make_button.grid(row=2, column=1, sticky="ew",
                              padx=10, pady=10)

        self.make_wait = tk.Label(creation_frame,
                                  text="",
                                  font=FONT_MEDIUM,
                                  fg=SUBTEXT_COLOR,
                                  bg=PRIMARY_BG)
        self.make_wait.grid(row=3, column=1,
                            sticky="n", padx=10)

        # Upgrade Buttons
        self.ore_upgrade = tk.Button(upgrade_frame,
                                     text="($5) Upgrade Ores",
                                     font=FONT_LARGE,
                                     fg=TEXT_COLOR,
                                     bg=BUTTON_BG,
                                     activebackground=BUTTON_ACTIVE_BG,
                                     width=15)
        self.ore_upgrade.grid(row=0, column=1, sticky="ew",
                              padx=10, pady=10)

        self.product_upgrade = tk.Button(upgrade_frame,
                                         text="($10) Upgrade Product Value",
                                         font=FONT_LARGE,
                                         fg=TEXT_COLOR, bg=BUTTON_BG,
                                         activebackground=BUTTON_ACTIVE_BG,
                                         width=15)
        self.product_upgrade.grid(row=0, column=0, sticky="ew",
                                  padx=10, pady=10)

        # Name Label
        self.name = tk.Label(name_frame, text="Idle",
                             font=FONT_LARGE,
                             fg=TEXT_COLOR, bg=BUTTON_BG,
                             activebackground=BUTTON_ACTIVE_BG,
                             width=15)
        self.name.grid(row=0, column=1, sticky="nsew",
                       padx=10, pady=10)

        # Prompt for the user to enter their name
        self.ask_name()

    def ask_name(self):
        """Ask the user for their name and check it's valid."""
        while True:
            name = simpledialog.askstring("Enter name",
                                          "Please enter your name (max 10 letters):")

            # If user clicks Cancel or closes the dialog
            if name is None:
                messagebox.showinfo("Exit",
                                    "Name is required to play. Exiting game.")
                self.root.destroy()
                sys.exit()

            name = name.strip() # removes whitelines, space, tabs,etc

            # If user presses OK with empty or whitespace-only name
            if not name:
                messagebox.showerror("Invalid Name", "Name can't be empty.")
                continue

            # Name too short or too long
            if len(name) < 3 or len(name) > 10:
                messagebox.showerror("Invalid Name",
                                     "Name has to be less than 10 or more than 3 characters.")
                continue

            # Name has stuff that ain't letters
            if not name.isalpha():
                messagebox.showerror("Invalid Name",
                                     "Name should have only letters (no numbers or symbols).")
                continue

            # If all good
            self.user_name = name.capitalize()
            break


class GuiController:
    """Connect the gui buttons to the actual game logic functions."""

    def __init__(self, gui, logic):
        """Set up the controller with gui + logic references."""
        self.gui = gui
        self.logic = logic

    def handle_mining(self):
        """When the mine button is pressed."""
        self.logic.mine_ores()

    def handle_product(self):
        """When the make product button is pressed."""
        self.logic.make_product()

    def handle_selling(self):
        """When the sell button is pressed."""
        self.logic.sell_product()

    def handleore_upgrade(self):
        """When the ore upgrade button is pressed."""
        self.logic.upgrade_ores()

    def handle_combination(self):
        """When the combine button is pressed."""
        self.logic.combine_product()

    def handle_value_upgrade(self):
        """When the product value upgrade button is pressed."""
        self.logic.upgrade_product_value()


# this is the starting point of the game, runs if file is run directly
# sets up tkinter window, hooks up gui, logic, and controller stuff

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")
    root.title("Idle Game")

    gui = GameGUI(root)
    logic = GameLogic(gui, root)
    controller = GuiController(gui, logic)

    # put player's name in the top label
    gui.name.config(text=f'{gui.user_name}: The Epic Miner')

    # hook up all the buttons to the controller methods
    gui.mine_button.config(command=controller.handle_mining)
    gui.make_button.config(command=controller.handle_product)
    gui.sell_button.config(command=controller.handle_selling)
    gui.ore_upgrade.config(command=controller.handleore_upgrade)
    gui.combine_button.config(command=controller.handle_combination)
    gui.product_upgrade.config(command=controller.handle_value_upgrade)

    # start the game loop
    root.mainloop()


