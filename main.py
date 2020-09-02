# main.py
#
# Entry point of the application 

import sys
import time
import tkinter as tk
from tkinter import ttk

from config import *
from widgets import *

def on_resizing(event):
    """ Routine executed when window is being resized """
    coord_map.delete("all")  # Clear map
    coord_map.draw_origin()  # Draw the origin again
    coord_map.draw_points()  # Draw the points again

if __name__ == "__main__":
    # Initialization of main window
    window = tk.Tk()
    window.wm_title(APP_TITLE)
    position_right = int(window.winfo_screenwidth()/2 - WINDOW_WIDTH/2)
    position_down = int(window.winfo_screenheight()/2 - WINDOW_HEIGHT/2)
    window.geometry("{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT, position_right, position_down)) # Set window dimensions and position
    window.minsize(WINDOW_WIDTH, WINDOW_HEIGHT) # User cannot reduce the window more than the initial size
    window.grid_columnconfigure(0, weight=1) # To make widgets inside window evenly spaced
    window.configure(background=WINDOW_BG_COLOR) # Main window background

    # Configuring style
    style = ttk.Style(window)
    style.configure("TNotebook", background=WINDOW_BG_COLOR) # Tab bar
    style.configure("TNotebook.Tab", background=TAB_HEADER_BG_COLOR_IDLE, foreground=TAB_HEADER_FG_COLOR_IDLE) # Tab header's main color
    style.map("TNotebook.Tab", 
              background=[("selected", TAB_HEADER_BG_COLOR_SELECTED), 
              ("active", TAB_HEADER_BG_COLOR_ACTIVE)], foreground=[("selected", TAB_HEADER_FG_COLOR_SELECTED), 
              ("active", TAB_HEADER_FG_COLOR_ACTIVE)]) # Tab header's colors when selected or focused on

    style.configure("TFrame", background=TAB_FRAME_BG_COLOR) # Tab frame color

    # Initialization of tab manager
    tab_control = ttk.Notebook(window) # Tab manager
    main_tab = ttk.Frame(tab_control) # Tab to deal with the demonstrator
    main_tab.grid_columnconfigure(0, weight=1)
    #config_tab = ttk.Frame(tab_control) # Tab to connect to vehicles via ssh
    #config_tab.grid_columnconfigure(0, weight=1)
    tab_control.add(main_tab, text=MAIN_TAB_NAME)
    #tab_control.add(config_tab, text=CONFIG_TAB_NAME)
    tab_control.grid(row=0, column=0, padx=NOTEBOOK_PADX, pady=NOTEBOOK_PADY, sticky="ew")

    # Instantiate a communication manager
    connection_manager = ITSG5Manager();

    # Initialization of all window elements
    console = Console(main_tab, 1, 0)                                               # Output console region
    control_frame = ControlFrame(main_tab, 0, 0, console, connection_manager)       # Main frame where user gives input
    coord_map = Map(main_tab, 1, 1)                                                 # Map of vehicle coordinates

    # Adding some text to console frame
    console.add_text("Connexion réussie !\n", "main")
    console.add_text("Texte random\n", "main")
    console.add_text("Autre texte random d'alerte\n", "alert")
    console.add_text("Autre texte random\n", "main")
    console.add_text("Ici on est dans l'onglet principal\n", "main")
    console.add_text("Et donc on affichera ici toutes les infos relatives à l'exécution du démonstrateur \n", "main")

    # Adding some points to map
    coord_map.add_point(Point(5.0, 5.0))
    coord_map.add_point(Point(5.3, 0.0))
    coord_map.add_point(Point(-0.5, -3.0))
    coord_map.add_point(Point(-3.2, 4.5))
    coord_map.add_point(Point(-5.2, 1.1))
    coord_map.add_point(Point(-4.2, -2.3))
    coord_map.add_point(Point(1.0, 5.9))
    coord_map.add_point(Point(3.0, -1.9))
    coord_map.draw_points()

#---WORKING ZONE BEGIN---###################################################################################""
    
    #def on_select(event):
    #    w = event.widget
    #    index = int(w.curselection()[0])
    #    value = w.get(index)

    #ssh_frame = SSHFrame(config_tab, 0, 0) 
    #ssh_console = Console(config_tab, 1, 0)
    #ssh_console.add_text("Connexion réussie !\n", "main")
    #ssh_console.add_text("Cette console ne se chargera que des retours des connexions SSH\n", "main")
    #ssh_console.add_text("Mais ça s'utilise de la même façon que l'autre console de l'autre onglet\n", "main")
    #ssh_console.add_text("Donc c'est cool\n", "alert")

#---WORKING ZONE END---###################################################################################""

    window.bind("<Configure>", on_resizing) # Binding resizing event to on_resizing function
    window.mainloop()

### End of main ###
