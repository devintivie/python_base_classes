import tkinter as tk
from tkinter import messagebox

''''base_font
Easy Font creation by passing list of font values.
'''
def base_font(style = 'bold'):
    fontType = 'courier'
    fontSize = 8
    fontStyle = style
    return [fontType, fontSize, fontStyle]

'''LED CLass
    Led class using canvas and drawing circles.
'''
class LED(tk.Canvas):

    led_size = 25

    def __init__(self, master=None, backgroundColor = None, iVal = 0):
        #Constructor
        led_size = self.led_size
        tk.Canvas.__init__(self, master, bg = backgroundColor, height = led_size, width = led_size, highlightthickness = 0)
        led_size = self.led_size
        coord = 2,2,led_size-2, led_size-2
        self.create_rectangle(coord, fill = "black")
        coord = 4,4,led_size-4, led_size-4
        self.colorPrint = self.create_rectangle(coord, fill = "gray")


    def set_value(self, value, faultorstatus = 'fault'):
        '''Changes led color by passing 0 or integer'''
        if faultorstatus == 'fault' :
            if value == 0 :
                self.itemconfig(self.colorPrint, fill = "black")
            else:
                self.itemconfig(self.colorPrint, fill = "red")
        else:
            if value == 1:
                self.itemconfig(self.colorPrint, fill = "green")
            else:
                self.itemconfig(self.colorPrint, fill = "yellow")




'''ip_entry
Creates tk.Entry field to accept IP Addresses. Enables parse for IP addresses
and created warning message if invalid IP address is given.
'''
class ip_entry(tk.Entry):
    def __init__(self, iString = '', master=None, nWidth=None, strVar=None, setFunction = None):
        #Constructor
        tk.Entry.__init__(self, master, width = nWidth, bg = 'white',
                          highlightthickness = 2, highlightcolor = 'white', textvariable = strVar, font = base_font())
        
        self.insert(tk.INSERT, iString)


    def parse(self):
        #IP parse checks that values are integers are between 1 and 255 and that
        # there are 4 numbers in the ip address
        self.delete(15,30)
        temp_string = self.get()
        ipstring = ''

        try:
            ipsplits = temp_string.split('.')
            if(int(ipsplits[0]) > 0 and int(ipsplits[0]) < 256):
                ipstring += str(int(ipsplits[0])) +'.'
            if(int(ipsplits[1]) > 0 and int(ipsplits[1]) < 256):
                ipstring += str(int(ipsplits[1])) +'.'
            if(int(ipsplits[2]) > 0 and int(ipsplits[2]) < 256):
                ipstring += str(int(ipsplits[2])) +'.'
            if(int(ipsplits[3]) > 0 and int(ipsplits[3]) < 256):
                ipstring += str(int(ipsplits[3]))
            self['fg'] = 'black'

        except:
            self['fg'] = 'red'
            return 'iperror'

        return ipstring
    
    def enable_entry(self):
        self['state'] = 'normal'
        
    def disable_entry(self):
        self['state'] = 'disabled'

    def message_box_error(self):
        #Prints warning message
        messagebox.showwarning('IP Warning', 'Invalid IP Address')
        

