

#######################################################################################################
# Imports ----------------------------------
from guizero import App, Text, Combo, PushButton, Box, Window


# Functions --------------------------------

def clear_list():
    newlist = [[None, None, None, None], [None, None, None, None]]
    return newlist


#
#   command called by 'open_window' combo
def you_chose(selected_value):
    # called by the Combo widget
    text2.value = "Value picked: " + combo.value
    # print("F you_chose1: ",combo.value)
    print("F you_chose3: ", selected_value)


#
# this code is working.
def exit_window(x, y, name):
    parm_list[x][y] = combo.value
    value_list[x][y] = name
    text_list[x][y].value = combo.value
    btext_list[x][y].bg = 'yellow'          # change text box back ground color
    print("F exit_window1: ", parm_list)
    print("F exit_window2: ", value_list)
    # print("F exit_window3: ", selected_value)
    w.destroy()


#
#   command called by 'getinput_pb' pushbutton
def open_window(x, y, name):
    global combo, text2, w
    print('F open_window1: ', name)
    w_title = "Choose the " + name + " value"
    w = Window(app, title=w_title, visible=False)
    w.show(wait=True)
    text1 = Text(w, text="Choose the  ''Number''  Value", height=1, width="fill")
    combo = Combo(w, options=inputlist, selected=inputinitial, command=you_chose, height=1, width=10)
    text2 = Text(w, text="Combo Value", height=1, width="fill")
    print('F open_window2: ', returncolor)
    pushbutton_f = PushButton(w, command=exit_window, args=[x, y, name], text='Exit window', height=1, width=10)
    print('F open_window3: ', combo.value)
    return 0


#
#   Pushbutton and Text widget function
def getinput_pb(x, y, name):
    height_box = 22  # Container height value
    height_container = 20  # Container height value
    textsize = 9  # Size of pushbutton and text widget
    global f_text
    print('F getinput_pb1: ', x, y, name)
    # create box to contain pushbotton/text box widgets.
    b_container = Box(app, height=height_box, width=292, border=1, grid=[x, y])
    # add left side space.
    b_left = Box(b_container, height=height_container, width=5, border=0, align="left")
    b_left.bg = "green"  # https://wiki.tcl-lang.org/page/Color+Names%2C+running%2C+all+screens
    #
    # pushbutton widget and set up
    b_pb = Box(b_container, height=height_container, width=125, border=1, align="left")
    b_pb.bg = "azure"
    f_pushbutton = PushButton(b_pb, command=open_window, text=name, args=[x, y, name], width='fill', align="right")
    f_pushbutton.text_size = textsize
    print('F getinput_pb2: ', parm_list)
    # add center space between pushbutton adn text box.
    Box(b_container, height=height_container, width=5, border=0, align="left")
    #
    # text box widget and set up
    b_tb = Box(b_container, height=height_container, width=150, border=1, align="left")
    btext_list[x][y] = b_tb
    b_tb.bg = "light yellow"
    # init_none = 'x , y ' + str(x) + '  ' + str(y)
    f_text = Text(b_tb, text=init_none, size=textsize, align="right")
    text_list[x][y] = f_text
    # add right side space.
    b_right = Box(b_container, height=height_container, width=5, border=0, align="left")
    b_right.bg = "green"
    return


# Variables --------------------------------

# grid which is a list containing [x,y] coordinates

returncolor = 'None1'
init_none = 'None1'
font_size = 10
inputlist = ["None", "zero", "one", "two", "three", "four", "five"]
inputinitial = inputlist[0]
print(inputinitial)

# App --------------------------------------
app = App(layout="grid")  # note 'app' is global
value_list = clear_list()
parm_list = clear_list()
text_list = clear_list()
btext_list = clear_list()
# print(value_list)
instructions = Text(app, text="Get numeric value", grid=[0, 0])

getinput_pb(0, 1, 'alpha')
getinput_pb(0, 2, 'beta')
getinput_pb(0, 3, 'trice')

app.display()
exit(4444)

#########################################################################################################

