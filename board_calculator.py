#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#Script is a simple, object oriented, GUI calculator for DIY projects

##It has 3 functions:
    
    #Cicrumference:
        
        #Supply length of raw planks and dimenstions of room to calculate how 
        #many planks required to surround the room. Once calculation is complete
        #You may select "Next room", this will keep any offcuts left from this
        #calculation and attempt to use them in future "rooms", or "New calc"
        #which will discard any offcuts left from this calculation and start fresh.
        
    #Area:
        
        #Supply length and width of raw planks and dimenstions of room to 
        #calculate how many planks required to cover the area of the room.
        #Once calculation is complete You may select "Next room", this will
        #keep any offcuts left from this calculation and attempt to use them
        #in future "rooms", or "New calc" which will discard any offcuts 
        #left from this calculation and start fresh.
        
    #Custom:
        
        #Supply length and width of raw planks and length and width of any boards
        #you need to construct your project. This will find various combinations
        #of cuts from each plank and select the combinatoin with least wastage
        #from each. It will then tell you the minimum number of fresh planks
        #you need to complete your project



import tkinter
from tkinter import StringVar, ttk


##Class representing lengths of fresh wood to be used
class Plank:
    
    def __init__(self, length, width, woodstore):
        #Save woodstore so we can refer to it easily
        self.woodstore = woodstore
        
        #Define attributes of this length
        self.length = length
        self.width = width

    
    def cut_board(self, length, width, offcut):
        #Attempt to cut board of given size from this plank
        try:
            #Raise an exception if passed sizes are longet than this plank
            if length > self.length or width > self.width:
                raise ValueError
            
            #Cut board off this plank
            self.length = self.length - length
            
            #add cut board to list
            self.woodstore.boards.append(Board(length, width, self.woodstore))
            
            if offcut == False:
                #Add remainder of this plank to offcuts list
                if self.length > 0:
                    self.woodstore.offcuts.append(self)

    
                #If width of board is less than width of this length add to offcut list
                if self.width - width > 0:
                    self.woodstore.offcuts.append(Plank(length, self.width - width, self.woodstore))

        except ValueError:
            #If we have tried to cut a longer length than available inform user
            ##Shouldnt be able to trigger this
            Error_Message("You tried to cut off more than was available!!")
       
        


##Class representing boards cut for purpose
class Board:
    
    def __init__(self, length, width, woodstore):
        self.woodstore = woodstore
        self.length = length
        self.width = width


#Class to represent physical storage of cut pieces
class WoodStore:
    
    def __init__(self):
        #Define properties and initialize store
        self.planks = None
        self.boards = None
        self.offcuts = None
        self.empty_store()
        
        
        #Reset store to starting values
    def empty_store(self):
        #Counter to keep track of how many planks we use
        self.planks = 0
        
        
        #Lists to hold cut-to-size boards and offcuts
        self.boards = []
        self.offcuts = []
    
    
    def get_plank(self, length, width):
        #Increase count of planks used and give out plank for use
        self.planks = self.planks + 1
        return Plank(length, width, self)
        


#Class containing 2 option "confirmation" popup message
class Confirmation_Message:
    
    def __init__(self, parent, text):
        #Define confirmation popup window
        self.popup = tkinter.Toplevel()
        self.popup.geometry("450x150")
        self.popup.title("Continue?")
        self.popup.resizable(0, 0)
        
        #Define frame to hold text
        self.popup_frame = tkinter.Frame(
                self.popup, padx=30, pady=15)
        
        self.popup_frame.grid(
                row=1, column=1)
        
        #Define frame to hold buttons
        self.popup_button_frame = tkinter.Frame(
                self.popup, padx=30, pady=10)
        
        self.popup_button_frame.grid(
                row=2, column=1)
        
        #Define spacer for between buttons
        self.popup_spacer = tkinter.Frame(
                self.popup_button_frame, width=180)
        
        self.popup_spacer.grid(
                row=2, column=2)
        
        #Define warning message
        self.popup_label = tkinter.Label(
                self.popup_frame, text=text)
        
        self.popup_label.grid(
                row=1, column=1, columnspan=3)
        
        #Define buttons
        self.popup_cancel = tkinter.Button(
                self.popup_button_frame, text="Next room")
        
        self.popup_cancel.grid(
                row=2, column=1)
        
        self.popup_ok = tkinter.Button(
                self.popup_button_frame, text="New calc")
        
        self.popup_ok.grid(
                row=2, column=3)
               
    #Destructor to completely delete popup
    def close(self):
        self.popup.destroy()
        

class Error_Message:

    def ok(self):
            self.warning.destroy()
      
    def __init__(self, text):
        
        #Define error popup
        self.warning = tkinter.Toplevel()
        self.warning.geometry("275x100")
        self.warning.resizable(0, 0)
        self.warning.title("Error")
        
        #Define frame to hold widgets
        self.warning_frame = tkinter.Frame(
                self.warning, padx=20, pady=10,)
        
        self.warning_frame.pack()
        
        #Only insert spacer if there is only one line of text in the warning message
        if len(text.split("\n")) < 2 :
            #Define spacer for between text and button
            self.warning_spacer = tkinter.Frame(
                    self.warning_frame, height=10,)
        
            self.warning_spacer.grid(
                    row=2, column=2)
        
        #Define warning message
        self.warning_label = tkinter.Label(
                self.warning_frame, text=text, wraplength=200)
        
        self.warning_label.grid(
                row=1, column=1, columnspan=3)
        
        #Define ok button
        self.warning_ok = tkinter.Button(
                self.warning_frame, text="Ok", command=self.ok)
        
        self.warning_ok.grid(
                row=3, column=2)
        


class Area_View:
    
    def __init__(self, root, welcome):
        self.root = root
        self.welcome = welcome
        self.woodstore = self.welcome.woodstore
        
        #Make sure woodstore is empty
        self.woodstore.empty_store()
        
        
        self.frame = tkinter.Frame(self.root)
        self.frame.pack(fill="both", expand=True)
        
        
        self.top_spacer = tkinter.Frame(self.frame, width=60, height=30)
        self.top_spacer.grid(row=0, column=0)
        
        self.title_label = tkinter.Label(self.frame, text="Calculate area")
        self.title_label.grid(row=1, column=1, pady=10, columnspan=2)
        
        self.heading_label = tkinter.Label(self.frame,\
                                           text="Please enter details below")
        self.heading_label.grid(row=2, column=1, columnspan=2, pady=10)
        
        
        self.width_label = tkinter.Label(self.frame, text="Width of room: ")
        self.width_label.grid(row=3, column=1, pady=10)

        self.width_entry = tkinter.Entry(self.frame)
        self.width_entry.grid(row=3, column=2, pady=10)
        
        self.width_unit_label = tkinter.Label(self.frame, text="mm")
        self.width_unit_label.grid(row=3, column=3, pady=10)
        
        
        self.length_label = tkinter.Label(self.frame, text="Length of room: ")
        self.length_label.grid(row=4, column=1, pady=10)

        self.length_entry = tkinter.Entry(self.frame)
        self.length_entry.grid(row=4, column=2, pady=10)
        
        self.length_unit_label = tkinter.Label(self.frame, text="mm")
        self.length_unit_label.grid(row=4, column=3, pady=10)
        
        
        self.plank_width_label = tkinter.Label(self.frame, text="Width of planks: ")
        self.plank_width_label.grid(row=5, column=1, pady=10)

        self.plank_width_entry = tkinter.Entry(self.frame)
        self.plank_width_entry.grid(row=5, column=2, pady=10)
        
        self.plankw_unit_label = tkinter.Label(self.frame, text="mm")
        self.plankw_unit_label.grid(row=5, column=3, pady=10)
        
        
        self.plank_length_label = tkinter.Label(self.frame, text="Length of planks: ")
        self.plank_length_label.grid(row=6, column=1, pady=10)

        self.plank_length_entry = tkinter.Entry(self.frame)
        self.plank_length_entry.grid(row=6, column=2, pady=10)
        
        self.plankl_unit_label = tkinter.Label(self.frame, text="mm")
        self.plankl_unit_label.grid(row=6, column=3, pady=10)
        
        self.direction_label = tkinter.Label(self.frame, text="Which direction are you laying boards?")
        self.direction_label.grid(row=7, column=1, columnspan=2, pady=10)
        
        self.direction_options = ["Lengthwise", "Widthwise"]
        self.direction = StringVar()
        
        self.direction_menu = ttk.Combobox(
                self.frame, textvariable=self.direction,\
                values=self.direction_options, width=15)
        self.direction_menu.grid(row=8, column=2, pady=10)
        self.direction_menu.set("Lengthwise")
        
        self.back_button = tkinter.Button(self.frame, text="Back", command=self.welcome.back, width=12, height=3)
        self.back_button.grid(row=9, column=1, pady=20)
        
        
        self.calculate_button = tkinter.Button(self.frame, text="Calculate", command=self.calculate, width=12, height=3)
        self.calculate_button.grid(row=9, column=2, columnspan=2, pady=20, sticky="e")
        


    def add_room(self):
        #Close popup and leave woodstore intact to continue calculating
        self.info.close()
    
    def new_calc(self):
        #Empty woodstore for next calculation
        self.woodstore.empty_store()
        self.info.close()
            

    def calculate(self):
        self.error = False
        #check user has supplied all relevant information
        try:
            self.room_length = int(self.length_entry.get())
            self.room_width = int(self.width_entry.get())
            self.plank_length = int(self.plank_length_entry.get())
            self.plank_width = int(self.plank_width_entry.get())
        
        
        #If any details have been given in incorrect format alert user and halt processing
        except:
            Error_Message("Please check your input!")
            self.error = True

        
        #If no errors gathering information we can proceed
        if self.error == False:
            
            #Send data to function to fill given area, accounting for direction of boards
            
            #If boards to be layed lengthwise in room
            if self.direction.get() == "Lengthwise":
                self.fill_area(self.room_length, self.room_width)
                
                
            #If boards to be layed widthwise in room
            else:
                self.fill_area(self.room_width, self.room_length)
                
            #Display result to user
            self.info = Confirmation_Message(self, "You need {} planks!".format(self.woodstore.planks))
            #Configure "next room" button
            self.info.popup_cancel.config(command=self.add_room)
            #Configure "new calculation button
            self.info.popup_ok.config(command = self.new_calc)



    def fill_area(self, length, width):
        
        while width > 0:
            #Set length for next strip of boards
            this_strip = length
            
            while this_strip > 0:
                #If there is enough room to cut a full width board
                if width >= self.plank_width:
                    
                    
                    #If enough space for a full plank take one from store and reduce length of this strip accordingly
                    if this_strip > self.plank_length:
                        self.woodstore.get_plank(self.plank_length, self.plank_width)
                        this_strip = this_strip - self.plank_length
                    
                    else:
                        #Check offcuts to see if we can use one of them
                        for i in self.woodstore.offcuts:
                            if i.length > this_strip and this_strip > 0 and self.plank_width == i.width:
                                i.cut_board(this_strip, self.plank_width, True)

                                #if we have used all of this offcut remove it from the list
                                if i.length == 0:
                                    self.woodstore.offcuts.remove(i)
                                this_strip = 0
                                
                                
                        #If we didnt have an offcut to use cut from a new plank                                
                        if this_strip > 0 and this_strip <= self.plank_length:
                            #get fresh plank from woodstore
                            this_plank = self.woodstore.get_plank(self.plank_length, self.plank_width)
                            
                            #Cut plank to needed size and keep offcut for use
                            this_plank.cut_board(this_strip, self.plank_width, False)

                            this_strip = 0
                
                        #reduce width to cover by width of boards cut
                        width = width - self.plank_width
                
                #If there is not enough width left for a full plank
                else:
                    #If theres enough space for a full plank cut one to width
                    if this_strip > self.plank_length:
                        this_plank = self.woodstore.get_plank(self.plank_length, self.plank_width)
                        this_plank.cut_board(self.plank_length, width, False)
                        this_strip = this_strip - self.plank_length
                        
                        #If we have completed the last strip reduce width to 0
                        if this_strip == 0:
                            width = 0
                    
                    
                    else:
                        #Check offcuts to see if we can use one of them
                        for i in self.woodstore.offcuts:
                            if i.length >= this_strip and this_strip > 0 and i.width >= width:
                                i.cut_board(this_strip, width, True)

                                #if we have used all of this offcut remove it from the list
                                if i.length == 0:
                                    self.woodstore.offcuts.remove(i)
                                this_strip = 0
                                width = 0
                                
                                
                        #If we didnt have an offcut to use cut from a new plank                                
                        if this_strip > 0 and this_strip <= self.plank_length:
                            #get fresh plank from woodstore
                            this_plank = self.woodstore.get_plank(self.plank_length, self.plank_width)
                            
                            #Cut plank to needed size and keep offcut for use
                            this_plank.cut_board(this_strip, width, False)

                            this_strip = 0
                            width = 0

                            





class Circumference_View:
    
    def __init__(self, root, welcome):
        self.root = root
        self.welcome = welcome
        self.woodstore = self.welcome.woodstore
        
        #Make sure woodstore is empty
        self.woodstore.empty_store()
        
        
        self.frame = tkinter.Frame(self.root)
        self.frame.pack(fill="both", expand=True)
        
        self.top_spacer = tkinter.Frame(self.frame, width=50, height=30)
        self.top_spacer.grid(row=0, column=0, pady=10)
        
        self.title_label = tkinter.Label(self.frame, text="Calculate circumference")
        self.title_label.grid(row=1, column=1, pady=10, columnspan=2)
        
        self.heading_label = tkinter.Label(self.frame,\
                                           text="Please enter details below")
        self.heading_label.grid(row=2, column=1, columnspan=2, pady=10)
        
        
        self.width_label = tkinter.Label(self.frame, text="Width of room: ")
        self.width_label.grid(row=3, column=1, pady=10)

        self.width_entry = tkinter.Entry(self.frame)
        self.width_entry.grid(row=3, column=2, pady=10)
        
        self.width_unit_label = tkinter.Label(self.frame, text="mm")
        self.width_unit_label.grid(row=3, column=3, pady=10)
        
        
        self.length_label = tkinter.Label(self.frame, text="Length of room: ")
        self.length_label.grid(row=4, column=1, pady=10)

        self.length_entry = tkinter.Entry(self.frame)
        self.length_entry.grid(row=4, column=2, pady=10)
        
        self.length_unit_label = tkinter.Label(self.frame, text="mm")
        self.length_unit_label.grid(row=4, column=3, pady=10)
                
        
        self.plank_length_label = tkinter.Label(self.frame, text="Length of planks: ")
        self.plank_length_label.grid(row=5, column=1, pady=10)

        self.plank_length_entry = tkinter.Entry(self.frame)
        self.plank_length_entry.grid(row=5, column=2, pady=10)
        
        self.plank_unit_label = tkinter.Label(self.frame, text="mm")
        self.plank_unit_label.grid(row=5, column=3, pady=10)

        
        self.back_button = tkinter.Button(self.frame, text="Back", command=self.welcome.back, width=12, height=3)
        self.back_button.grid(row=6, column=1, pady=20)
        
        self.calculate_button = tkinter.Button(self.frame, text="Calculate", command = self.calculate, width=12, height=3)
        self.calculate_button.grid(row=6, column=2, columnspan=2, pady=20, sticky="e")
        
        


    def calculate(self):
        
        self.error = False
        #check user has supplied all relevant information
        try:
            self.room_length = int(self.length_entry.get())
            self.room_width = int(self.width_entry.get())
            self.plank_length = int(self.plank_length_entry.get())
        
        
        #If any details have been given in incorrect format alert user and halt processing
        except:
            Error_Message("Please enter whole numbers only!")
            self.error = True

        
        #If no errors gathering information we can proceed
        if self.error == False:
            #Cut boards for 2 longer sides
            for i in range(2):
                wall = self.room_length
                self.cut_for_wall(wall)
            
            #Cut booards for 2 shorter sides
            for i in range(2):
                wall = self.room_width
                self.cut_for_wall(wall)
                
                
            self.info = Confirmation_Message(self, "You need {} planks!".format(self.woodstore.planks))
            #Configure "next room" button
            self.info.popup_cancel.config(command=self.add_room)
            #Configure "new calculation button
            self.info.popup_ok.config(command = self.new_calc)
            



            
            
    def add_room(self):
        #Close popup and leave woodstore intact to continue calculating
        self.info.close()
    
    def new_calc(self):
        #Empty woodstore for next calculation
        self.woodstore.empty_store()
        self.info.close()
            
            
            
    def cut_for_wall(self, wall):
        while wall > 0:
            #If wall length is longer than plank length take whole plank and reduce length of wall
            #to calculate accordingly
            if wall > self.plank_length:
                self.woodstore.get_plank(self.plank_length, 0)
                wall = wall - self.plank_length
 
                
            #if plank is long enough to cover remaining section of wall 
            else:
                #Check offcuts to see if we can use one of them
                for i in self.woodstore.offcuts:
                    if i.length > wall and wall > 0:
                        i.cut_board(wall, 0, True)

                        #if we have used all of this offcut remove it from the list)
                        if i.length == 0:
                            self.woodstore.offcuts.remove(i)
                        wall = 0
                        
                        
                #If we didnt have an offcut to use cut from a new plank                                
                if wall > 0:
                    #get fresh plank from woodstore
                    this_plank = self.woodstore.get_plank(self.plank_length, 0)
                    
                    #Cut plank to needed size and keep offcut for use
                    this_plank.cut_board(wall, 0, False)

                    wall = 0
                 
class Custom_View:
    
    def __init__(self, root, welcome):
        self.root = root
        self.welcome = welcome
        self.woodstore = self.welcome.woodstore
        
        #Make sure woodstore is empty
        self.woodstore.empty_store()
        
        #Counter to keep track of next available row of widgets
        self.row_counter = 2
        #dictionary to store generated widgets in using row number as key
        self.widgets = {}
        #List to hold initial row of board input widgets
        row0 = []


        self.container = tkinter.Frame(self.root)
        
        self.canvas = tkinter.Canvas(
                self.container, width=435, height=600) 
        
        #Define scrollbar
        self.scrollbary = tkinter.Scrollbar(
                self.container, orient="vertical",\
                command=self.canvas.yview)

        #Create the top frame to hold widgets        
        self.frame = tkinter.Frame(self.canvas)
        
        
        #Define scrollable region of canvas
        self.frame.bind(
                "<Configure>", lambda e:
                    self.canvas.configure(
                            scrollregion=self.canvas.bbox(
                                    "all")))
        self.canvas.create_window(
                (0, 0), window=self.frame, anchor="nw")
        
        #Configure the commands for interacting with scrollbars
        self.canvas.configure(
                yscrollcommand=self.scrollbary.set)

        
        #attach container to parent
        self.container.pack()
        
        
        #Define positioning of scrollbars
        self.scrollbary.grid(
                row=1, column=2, sticky="ns")
            
        #pack canvas into container and span full area of container
        self.canvas.grid(
                row=1, column=1, sticky="nsew")
        
        
        self.top_spacer = tkinter.Frame(self.frame, width=60, height=30)
        self.top_spacer.grid(row=0, column=0)

        self.title_label = tkinter.Label(self.frame, text="Custom project")
        self.title_label.grid(row=1, column=1, pady=10, columnspan=2)
        
        self.heading_label = tkinter.Label(self.frame,\
                                           text="Please enter sizes of raw plank of timber")
        self.heading_label.grid(row=2, column=1, columnspan=2, pady=10)
        

        self.plank_length_label = tkinter.Label(self.frame, text="Length of planks: ")
        self.plank_length_label.grid(row=3, column=1, pady=10)

        self.plank_length_entry = tkinter.Entry(self.frame)
        self.plank_length_entry.grid(row=3, column=2, pady=10)
        
        self.plankl_unit_label = tkinter.Label(self.frame, text="mm")
        self.plankl_unit_label.grid(row=3, column=3, pady=10)
        
        self.plank_width_label = tkinter.Label(self.frame, text="Width of planks: ")
        self.plank_width_label.grid(row=4, column=1, pady=10)

        self.plank_width_entry = tkinter.Entry(self.frame)
        self.plank_width_entry.grid(row=4, column=2, pady=10)
        
        self.plankw_unit_label = tkinter.Label(self.frame, text="mm")
        self.plankw_unit_label.grid(row=4, column=3, pady=10)

        self.table_heading = tkinter.Label(self.frame, text="Please enter boards you need for your project")
        self.table_heading.grid(row=5, column=1, columnspan=3, pady=10)
        
        #Frame to hold table of dynamic entries
        self.board_frame = tkinter.Frame(self.frame)
        self.board_frame.grid(row=6, column=1, columnspan=3, sticky="nsew")
        
        
        self.length_heading = tkinter.Label(self.board_frame, text="L")
        self.length_heading.grid(row=0, column=1, pady=10)
        
        self.length_entry = tkinter.Entry(self.board_frame, width=7)
        self.length_entry.grid(row=1, column=1, pady=10, padx=5)
        row0.append(self.length_entry)
                
        self.x_label = tkinter.Label(self.board_frame, text="X")
        self.x_label.grid(row=1, column=2, pady=10, padx=5)
        row0.append(self.x_label)        
        
        self.width_heading = tkinter.Label(self.board_frame, text="W")
        self.width_heading.grid(row=0, column=3, pady=10)
        
        self.width_entry = tkinter.Entry(self.board_frame, width=7)
        self.width_entry.grid(row=1, column=3, pady=10, padx=5)
        row0.append(self.width_entry)
        
        self.unit_label = tkinter.Label(self.board_frame, text="mm")
        self.unit_label.grid(row=1, column=4, pady=10, padx=5)
        row0.append(self.unit_label)
        
        
        
        #Add initially generated row of board input widgets to dictionary
        self.widgets[0] = row0
        
        
        #########Here will be generated rows for adding more boards
        
    
        
        self.row_button = tkinter.Button(self.frame, text="+", command=self.add_row, height=3, width=5)
        self.row_button.grid(row=7, column=1, pady=10, sticky="e")
        
        self.back_button = tkinter.Button(self.frame, text="Back", command=self.welcome.back, width=12, height=3)
        self.back_button.grid(row=8, column=1, pady=10)
        
        self.calculate_button = tkinter.Button(self.frame, text="Calculate", command=self.calculate, width=12, height=3)
        self.calculate_button.grid(row=8, column=2, columnspan=2, pady=10, sticky="e")
        
        

    
    
    #Add another row of widgets to display
    def add_row(self):
        
        
        #Define list to hold widgets
        this_row = []
        
        #Define widgets for this row, add each to list
        length_entry = tkinter.Entry(self.board_frame, width=7)
        length_entry.grid(row=self.row_counter, column=1, pady=10)
        this_row.append(length_entry)
        
        x_label = tkinter.Label(self.board_frame, text="X")
        x_label.grid(row=self.row_counter, column=2, pady=10)
        this_row.append(x_label)
        
        width_entry = tkinter.Entry(self.board_frame, width=7)
        width_entry.grid(row=self.row_counter, column=3, pady=10)
        this_row.append(width_entry)
        
        unit_label = tkinter.Label(self.board_frame, text="mm")
        unit_label.grid(row=self.row_counter, column=4, pady=10)
        this_row.append(unit_label)
        
        
        remove_button = tkinter.Button(self.board_frame, text="-", command=lambda x=self.row_counter:self.del_row(x))
        remove_button.grid(row=self.row_counter, column=5, pady=10)
        this_row.append(remove_button)
        
        #Store list of widgets in dictionary using row number as key
        self.widgets[self.row_counter] = this_row
        
        #Increase row counter for next row
        self.row_counter = self.row_counter + 1
        
    def add_room(self):
        #Close popup and leave woodstore intact to continue calculating
        self.info.close()
    
    def new_calc(self):
        #Empty woodstore for next calculation
        self.woodstore.empty_store()
        self.info.close()

    
    def del_row(self, i):
        #Loop over list of widgets stored under passed row number
        #And destroy all
        for j in self.widgets[i]:
            j.destroy()
        #Remove entry from dictionary to avoid errors when reading in data
        del self.widgets[i]
            

    def calculate(self):

        #Function to sort list of boards
        def sort_func(x):
            return x.length
        
        #Bool flag to toggle if any errors reading in data
        self.error = False
        
        #Declare list to hold boards we need to cut
        self.boards = []
        
        
        try:
            
            
            ###Read in data from widgets, halt processing if any errors encountered
            
            #pull info on size of raw lengths
            self.raw_length = int(self.plank_length_entry.get())
            self.raw_width = int(self.plank_width_entry.get())
            
            
            #create board objects from supplied dimensions, hold in list
            for value in self.widgets.values():
            
                
                #Check the sizes of board required are within sizes of raw plank
                if int(value[0].get()) <= self.raw_length and int(value[2].get()) <= self.raw_width:
                    self.boards.append(Board(int(value[0].get()), int(value[2].get()), self.woodstore))
                
                
                #If above failed check if the supplied lehgth and width for this board wave been reversed
                elif int(value[2].get()) <= self.raw_length and int(value[0].get()) <= self.raw_width:
                    self.boards.append(Board(int(value[2].get()), int(value[0].get()), self.woodstore))
                
                
                else:
                    #If we couldnt get this board to fit within supplied dimensions for raw plank
                    #Inform user and halt processing
                    Error_Message("One of your boards is too big to cut from these planks!")
                    self.error = True
            

            
        
        except:
            Error_Message("Please enter whole numbers only!")
            self.error = True
        
        ###Provided there were no errors encountered building data, sort list of boards to cut by length    
        
        #If we ran into any problems gathering data halt processing
        if self.error == False:
            #sort list of boards by length, largest to smallest
            self.boards.sort(reverse=True, key=sort_func)       
            
            ##While list contains something##
            while len(self.boards) > 0:
                

                
                
                
                ###Start with longest board that needs cut, cut this from fresh plank and remove from list of
                ###boards to be cut
                
                
                #Check offcuts to see if any will fit this board 
                found = False
                for i in self.woodstore.offcuts:
                    if i.length >= self.boards[0].length:
                        i.cut_board(self.boards[0].length, self.boards[0].width, True)
                        found = True
                        this_length = i
                        

                        
                        
                        
                #If there wasnt an offcut that fit this board just take a new plank from stores
                if found == False:
                    #take length from woodstore, cut longest board in list
                    this_length = self.woodstore.get_plank(self.raw_length, self.raw_width)
                    this_length.cut_board(self.boards[0].length, self.boards[0].width, False)
                    
                    

                    
                
                
                #Delete board we just cut from list of required boards
                del self.boards[0]
            
                
                ###Loop over remaining boards and see if any can be cut from remainder of this plank, save any that fit
                ###into list and save list and reference to starting board in dictionaries (stored as 2 dictionaries with
                ###starting board reference as key to avoid issues if more than one combination gives the same wastage)
                
                
                ###Repeat this process until we have lists of every combination of boards we can cut from
                ###the remainder of this plank
                
                
                #Dictionary to hold results from passes over boards
                attempts = {}
                results = {}
                
                
                for i in range(len(self.boards)):
                    #Save remaining length in this plank
                    remaining_length = this_length.length
                    
                    #List to hold boards for this pass
                    this_pass = []
                
                    
                    #look at next longest board and see if there's enough left for it
                    if self.boards[i].length <= remaining_length:
                        remaining_length = remaining_length - self.boards[i].length
                        #Save index reference for board
                        this_pass.append(self.boards[i])
                        
                        #Loop over remaining boards and see if any more will fit
                        for j in range(len(self.boards) - i):
                            if self.boards[j+i].length <= remaining_length:
                                remaining_length = remaining_length - self.boards[j+i].length
                                #Save index reference for board
                                this_pass.append(self.boards[j+i])
                                
                        
                        #Save list of results in dictionary using starting board index as key
                        attempts[i] = this_pass
                        results[i] = remaining_length




                
                ###Examine combinations we found and see which one leaves us the least left over material
                ###Then cut these boards and remove them from list of boards to be cut




                
                wastage = 999999
                permutation = None
                #Make sure we found something before trying to process
                if attempts != {}:
                    #Check results to find least wastage
                    for key, value in results.items():
                        if value < wastage:
                            wastage = value
                            permutation = key #key is the key of the combination of boards we want to cut from plank
                    

                    

                    
                    #Loop over boards in chosen permutation and cut them from plank
                    for i in range(len(attempts[permutation])):
                        #Delete board from list of boards to be cut
                        try:
                            self.boards.remove(attempts[permutation][i])
                            this_length.cut_board(attempts[permutation][i].length, attempts[permutation][i].width, False)

                        #In case we try to delete a board that isnt in the list anymore
                        #Shouldnt happen                            
                        except:
                            
                            pass
                    
                    
                    
            self.info = Error_Message( "You need {} planks!".format(self.woodstore.planks))
             
            
            


class Welcome_view:
    
    def __init__(self, root):
        
        self.root = root
        
        #Initialize woodstore so we can store our wood
        self.woodstore = WoodStore()
        
        #Create display
        self.create_view()
    
    def create_view(self):
    
        self.frame = tkinter.Frame(self.root)
        self.frame.pack(fill="both", expand=True)    
        
        self.top_spacer = tkinter.Frame(self.frame, width=80, height=50)
        self.top_spacer.grid(row=0, column=0)
        
        self.heading_label = tkinter.Label(self.frame, text="What are you trying to calculate today?")
        self.heading_label.grid(row=1, column=1, pady=20)
        
        self.area_button = tkinter.Button(self.frame, text="Area", command=self.area, width=12, height=3)
        self.area_button.grid(row=2, column=1, pady=20)
        
        self.circumference_button = tkinter.Button(self.frame, text="Circumference", command=self.circumference, width=12, height=3)
        self.circumference_button.grid(row=3, column=1, pady=20)
        
        self.custom_button = tkinter.Button(self.frame, text="Custom", command=self.custom, width=12, height=3)
        self.custom_button.grid(row=4, column=1, pady=20)
        

    def destroy_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def area(self):
        self.destroy_view()
        Area_View(self.root, self)        
    
    def circumference(self):
        self.destroy_view()
        Circumference_View(self.root, self)
        
    def custom(self):
        self.destroy_view()
        Custom_View(self.root, self)
    
    def back(self):
        #Destroy current view and re-create welcome screen
        self.destroy_view()
        self.create_view()







#Define root window
root = tkinter.Tk()

root.title("Board calculator V1.0")
root.geometry("450x600")

view = Welcome_view(root)


if __name__ == "__main__":
    root.mainloop()