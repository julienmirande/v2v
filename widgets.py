# widgets.py
#
# Contains the classes corresponding to the
# elements appearing on the main application 
# page (ControlFrame, Console, Point and Map)

import tkinter as tk
from config import *
from communication_manager import *

class ControlFrame(tk.Frame):
    """ Main frame containing most of user input widgets """
    def __init__(self, parent_frame, row, column, console, connection_manager):
        super().__init__(parent_frame, 
                         borderwidth=1, 
                         relief="solid", 
                         highlightbackground=CONTROL_FRAME_BORDER_COLOR, 
                         highlightthickness=CONTROL_FRAME_BORDER_THICKNESS, 
                         bg=CONTROL_FRAME_BG_COLOR)
        self.console = console
        self.connection_manager = connection_manager

        # Divide the frame in two halves
        first_half_frame = tk.Frame(self, bg=CONTROL_FRAME_BG_COLOR);
        first_half_frame.grid(row=0, 
                              column=0, 
                              padx=0, 
                              pady=0, 
                              sticky="nsew")

        second_half_frame = tk.Frame(self, bg=CONTROL_FRAME_BG_COLOR);
        second_half_frame.grid(row=0, 
                              column=1, 
                              padx=0, 
                              pady=0, 
                              sticky="nsew")

        # Text labels
        first_half_label = tk.Label(first_half_frame, 
                                    text = "Paramétrage de la commande",
                                    bg=LABEL_BG_COLOR)
        first_half_label.grid(row = 0, column=0, padx=10, pady=10, columnspan=2)

        vehicle_choice_label = tk.Label(first_half_frame, 
                                        text = "Choix du véhicule",
                                        bg=LABEL_BG_COLOR)
        vehicle_choice_label.grid(row = 1, column=0, padx=10, pady=10)

        speed_choice_label = tk.Label(first_half_frame, 
                                      text = "Vitesse (en %)", 
                                      bg=LABEL_BG_COLOR)
        speed_choice_label.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        angle_choice_label = tk.Label(first_half_frame, 
                                      text = "Direction (en degrés)", 
                                      bg=LABEL_BG_COLOR)
        angle_choice_label.grid(row = 3, column=0, padx=10, pady=10)

        # List among which vehicle(s) we want to communicate to must be chosen
        self.vehicles_listbox = tk.Listbox(first_half_frame)
        for car in CARS:
            self.vehicles_listbox.insert(tk.END, car)
        self.vehicles_listbox.grid(row=1, column=1, padx=10, pady=10)

        # Slider to control the speed of the vehicle
        self.speed_scale = tk.Scale(first_half_frame,
                               from_=0, 
                               to=100, 
                               orient=tk.HORIZONTAL, 
                               bg=SCALE_BG_COLOR_IDLE, 
                               fg=SCALE_FG_COLOR_IDLE, 
                               activebackground=SCALE_BG_COLOR_ACTIVE)
        self.speed_scale.grid(row=2, column=1, padx=10, pady=10)

        # Slider to control the direction of the vehicle
        self.angle_scale = tk.Scale(first_half_frame, 
                               from_=-90, 
                               to=90, 
                               orient=tk.HORIZONTAL, 
                               bg=SCALE_BG_COLOR_IDLE, 
                               fg=SCALE_FG_COLOR_IDLE, 
                               activebackground=SCALE_BG_COLOR_ACTIVE)
        self.angle_scale.grid(row=3, column=1, padx=10, pady=10)

        # Button to reset the sliders to 0
        reset_button = tk.Button(first_half_frame, 
                                 text = 'Réinitialiser les sliders', 
                                 bg=BUTTON_BG_COLOR_IDLE, 
                                 fg=BUTTON_FG_COLOR_IDLE, 
                                 activebackground=BUTTON_BG_COLOR_ACTIVE, 
                                 activeforeground=BUTTON_FG_COLOR_ACTIVE,
                                 command=lambda: self.reset_sliders())
        reset_button.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)

        # Button that launches the demonstrator
        run_button = tk.Button(second_half_frame, 
                               text = 'Exécuter la commande', 
                               bg=BUTTON_BG_COLOR_IDLE, 
                               fg=BUTTON_FG_COLOR_IDLE, 
                               activebackground=BUTTON_BG_COLOR_ACTIVE, 
                               activeforeground=BUTTON_FG_COLOR_ACTIVE,
                                command=lambda: self.execute_run_command())
        run_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Button to stop the demonstrator
        stop_button = tk.Button(second_half_frame, 
                                text = 'Arrêter le démonstrateur', 
                                bg=BUTTON_BG_COLOR_IDLE, 
                                fg=BUTTON_FG_COLOR_IDLE, 
                                activebackground=BUTTON_BG_COLOR_ACTIVE, 
                                activeforeground=BUTTON_FG_COLOR_ACTIVE,
                                command=lambda: self.execute_stop_command())
        stop_button.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Make all widgets evenly spaced, even when window is being resized
        first_half_frame.grid_columnconfigure(0, weight=1)
        first_half_frame.grid_columnconfigure(1, weight=1)
        first_half_frame.grid_rowconfigure(0, weight=1)
        first_half_frame.grid_rowconfigure(1, weight=1)
        first_half_frame.grid_rowconfigure(2, weight=1)
        first_half_frame.grid_rowconfigure(3, weight=1)
        first_half_frame.grid_rowconfigure(4, weight=1)

        second_half_frame.grid_columnconfigure(0, weight=1)
        second_half_frame.grid_rowconfigure(0, weight=1)
        second_half_frame.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Finally display the whole frame
        self.grid(row=row, 
                  column=column, 
                  padx=CONTROL_FRAME_PADX, 
                  pady=CONTROL_FRAME_PADY, 
                  sticky="ew", 
                  columnspan=2)

    def execute_run_command(self):
        """ Send given speed and angle order to specified vehicles """
        
        # For all chosen vehicle(s), send speed and angle commands
        rcpt_vehicles = [] # Recipient vehicle list
        vehicle_choice = self.vehicles_listbox.curselection()
        if(not vehicle_choice): # User has not selected a vehicle
            self.console.add_text("Please select a vehicle to send the command to first.\n", "main")
            return

        if(vehicle_choice[0] == 0): # Add all vehicle to recipient list
            for i in range(1, 8):
                rcpt_vehicles.append(i)
        else:                # Add particular vehicle to recipient list
            rcpt_vehicles.append(vehicle_choice[0])

        # Get selected speed and angle
        speed = self.speed_scale.get()
        angle = self.angle_scale.get()

        # Send commands to all vehicles in recipient list via connection manager
        for vehicle in rcpt_vehicles:
            self.connection_manager.send_speed_order(vehicle, speed);
            self.connection_manager.send_speed_order(vehicle, angle + 90);

    def execute_stop_command(self):
        """ Send stop order to all vehicles """
        for vehicle in range(1, 8):
            self.connection_manager.send_stop_order(vehicle);

    def reset_sliders(self):
        """ Reset the Scale widgets to 0 """
        self.speed_scale.set(0)
        self.angle_scale.set(0)

### End of ControlFrame ###

#class SSHFrame(tk.Frame):
#    """ Frame for managing ssh connections """
#    def __init__(self, parent_frame, row, column):
#        super().__init__(parent_frame, borderwidth=1, relief="solid", highlightbackground=CONTROL_FRAME_BORDER_COLOR, highlightthickness=CONTROL_FRAME_BORDER_THICKNESS, bg=CONTROL_FRAME_BG_COLOR)
#        self.parent_frame = parent_frame
#
#        self.ssh_manager = ssh.SSHConnectionManager()
#        self.grid_columnconfigure(0, weight=1)
#        tk.Label(self, text = "Choix du véhicule", bg=LABEL_BG_COLOR).grid(row = 0, column=0)
#        tk.Label(self, text = "Vitesse (en %)", bg=LABEL_BG_COLOR).grid(row=1, column=0, sticky="ew")
#        tk.Label(self, text = "Direction (en degrés)", bg=LABEL_BG_COLOR).grid(row = 2, column=0)
#        speed_scale = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, bg=SCALE_BG_COLOR_IDLE, fg=SCALE_FG_COLOR_IDLE, activebackground=SCALE_BG_COLOR_ACTIVE)
#        vehicles = tk.Listbox(self)
#        for car in CARS:
#            vehicles.insert(tk.END, car)
#        angle_scale = tk.Scale(self, from_=-90, to=90, orient=tk.HORIZONTAL, bg=SCALE_BG_COLOR_IDLE, fg=SCALE_FG_COLOR_IDLE, activebackground=SCALE_BG_COLOR_ACTIVE)
#        vehicles.grid(row=0, column=1, padx=10, pady=10)
#        speed_scale.grid(row=1, column = 1)
#        angle_scale.grid(row=2, column = 1)
#        tk.Button(self, text="Se connecter", command=lambda: self.init_connection(host, user, password), bg=BUTTON_BG_COLOR_IDLE, fg=BUTTON_FG_COLOR_IDLE, activebackground=BUTTON_BG_COLOR_ACTIVE, activeforeground=BUTTON_FG_COLOR_ACTIVE).grid(row=0, column=2, padx=5, pady=5)
#        tk.Button(self, text = 'Quitter', command = parent_frame.quit, bg=BUTTON_BG_COLOR_IDLE, fg=BUTTON_FG_COLOR_IDLE, activebackground=BUTTON_BG_COLOR_ACTIVE, activeforeground=BUTTON_FG_COLOR_ACTIVE).grid(row=3, column=0, sticky="w", padx=5, pady=5)
#        tk.Button(self, text = 'Appliquer', command = lambda: self.send_control_cmds(speed_scale.get(), angle_scale.get()), bg=BUTTON_BG_COLOR_IDLE, fg=BUTTON_FG_COLOR_IDLE, activebackground=BUTTON_BG_COLOR_ACTIVE, activeforeground=BUTTON_FG_COLOR_ACTIVE).grid(row = 3, column = 1, sticky="w", padx=5, pady=5)
#        tk.Button(self, text = 'Reset', command = lambda: self.stop_cmd(speed_scale, angle_scale), bg=BUTTON_BG_COLOR_IDLE, fg=BUTTON_FG_COLOR_IDLE, activebackground=BUTTON_BG_COLOR_ACTIVE, activeforeground=BUTTON_FG_COLOR_ACTIVE).grid(row=3, column=2, sticky="e", padx=5, pady=5)
#        host="10.3.141.73" # Car we want to connect to #TODO: Make this parameterized according to selected listbox
#        user="pi"
#        password="PFA_V2X"
#        self.grid(row=row, column=column, padx=CONTROL_FRAME_PADX, pady=CONTROL_FRAME_PADY, sticky="ew", columnspan=2)
#
#    def send_control_cmds(self, speed, angle):
#        self.ssh_manager.cmd_set_angle(angle+90)
#        self.ssh_manager.cmd_set_speed(speed)
#
#    def stop_cmd(self, speed_scale, angle_scale):
#        speed_scale.set(0)
#        angle_scale.set(0)
#        self.ssh_manager.cmd_stop()
#
#    def init_connection(self, host, user, password):
#        self.ssh_manager.init_connection(host, user, password)
#        #TODO: print connection result

class Console(tk.Text):
    """ Console displaying information about the state of the running application """
    def __init__(self, parent_frame, row, column):
        super().__init__(parent_frame,
                         width=CONSOLE_WIDTH, 
                         height=CONSOLE_HEIGHT, 
                         bg=CONSOLE_BG_COLOR)
        self.parent_frame = parent_frame

        # Make console read-only
        self.configure(state="disabled") 

        # Main text will be white on black, alert text will be red on yellow
        self.tag_config('main', background=CONSOLE_MAIN_LINE_BG_COLOR, foreground=CONSOLE_MAIN_LINE_FG_COLOR, font=CONSOLE_MAIN_LINE_FONT) 
        self.tag_config('alert', background=CONSOLE_ALERT_LINE_BG_COLOR, foreground=CONSOLE_ALERT_LINE_FG_COLOR, font=CONSOLE_ALERT_LINE_FONT) 
        # Display the whole console
        self.grid(row=row, 
                  column=column, 
                  padx=CONSOLE_PADX, 
                  pady=CONSOLE_PADY, 
                  sticky="ew")

    def add_text(self, text, tag):
        """ Add a line of text at the end of console """
        self.configure(state="normal")
        self.insert(tk.END, text, tag)
        self.configure(state="disabled")
        self.parent_frame.update_idletasks() # Refresh the page so that the text is immediatly displayed

### End of Console ###
        
class Point:
    """ Point appearing on a Map object, whose state is defined by its x-axis and y-axis coordinates """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas):
        """ Draw the point on the map """
        map_width = canvas.winfo_width()
        map_height = canvas.winfo_height()

        # Compute actual x coordinate in regard of the map coordinate
        top_right_x = (map_width / 2) + (self.x * (map_width / MAP_GRADUATION_UNIT)) - (POINT_DIAMETER / 2) 

        # Compute actual y coordinate in regard of the map coordinate
        top_right_y = (map_height / 2) - (self.y * (map_height / MAP_GRADUATION_UNIT)) - (POINT_DIAMETER / 2) 

        # Draw the actual point
        canvas.create_oval(
            top_right_x,
            top_right_y, 
            top_right_x + POINT_DIAMETER, 
            top_right_y + POINT_DIAMETER, 
            outline=POINT_OUTLINE_COLOR, fill=POINT_FILL_COLOR, width=1)

### End of Point ###

class Map(tk.Canvas):
    """ Map displaying the poistion of vechicles when it has been given """
    def __init__(self, parent_frame, row, column):
        super().__init__(parent_frame,
                         width=MAP_WIDTH, 
                         height=MAP_HEIGHT, 
                         bg=MAP_BG_COLOR)
        self.parent_frame = parent_frame
        self.points = []

        # Display the whole map
        self.grid(row=row, column=column, padx=MAP_PADX, pady=MAP_PADY, sticky="e")
        self.draw_origin()

    def draw_origin(self):
        """ Draw the x and y axis with graduation appearing """
        self.parent_frame.update() # Needed so that the actual widget sizes are correctly computed
        map_width = self.winfo_width()
        map_height = self.winfo_height()

        # X axis
        self.create_line(        
                0,               # x1
                map_height / 2,  # y1
                map_width,       # x1
                map_height / 2,  # y2
                fill=MAP_ORIGIN_COLOR)

        # Y axis
        self.create_line(        
                map_width / 2,   # x1
                0,               # y1
                map_width / 2,   # x2
                map_height,      # y2
                fill=MAP_ORIGIN_COLOR)

        # Drawing the little graduation bars
        for i in range(20):
            # X axis graduation
            self.create_line(    
                i * (map_width / 20),
                (map_height / 2) - (MAP_DIVISION_LINE / 2),
                i * (map_width / 20),
                (map_height / 2) + (MAP_DIVISION_LINE / 2),
                fill=MAP_ORIGIN_COLOR)

            # Y axis graduation
            self.create_line(
                (map_width / 2) - (MAP_DIVISION_LINE / 2),
                i * (map_height / 20),
                (map_width / 2) + (MAP_DIVISION_LINE / 2),
                i * (map_height / 20),
                fill=MAP_ORIGIN_COLOR)

    def add_point(self, point):
        """ Add point to the map list of points """
        self.points.append(point)

    def draw_points(self):
        """ Draw all points contained in the map list of points """
        for point in self.points:
            point.draw(self)

### End of Map ###

    
