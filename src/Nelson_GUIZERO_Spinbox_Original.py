# ------------------------------
# App
# ------------------------------


# Imports ---------------

# Functions -------------

# App -------------------

# Display ---------------
#99999999999999999999999999999999999999999999

# ------------------------------
# Imports
# ------------------------------

import math
from guizero import Text, App, Box
from tkinter import Spinbox

# ------------------------------
# Functions
# ------------------------------

# array to pass parameters between functions.
def clear_list():
    newlist = [[None, None, None, None], [None, None, None, None]]
    return newlist

# sb_range command function.
def sb_range_cmd(x, y, name):
    sb_value = sb_range.get()             # get selected spinbox 'range' value.
    print('\n sb_range_cmd: ',x, y, name)
    print('\n sb_range_cmd: ',sb_value)
# sb_range command function.
def sb_range_cmdx(x, y, name):
    sb_value = sb_range.get()             # get selected spinbox 'range' value.
    print('\n sb_range_cmd: ',sb_value)
    listid = range_list.index(sb_value)   # get 'range','start'/'end' 'step' value list
#
#   How to change Guizero Widgets Constructors
#   Check: https://lawsie.github.io/guizero/usingtk/
    start_step = range_steps[listid][1]  # 'start' value
    end_step = range_steps[listid][2]    # 'end' value
    print('>select_stepa: ',start_step,end_step)
    print('sb_value == sb_initial: ', sb_value, sb_initial)
    if sb_value == sb_initial:
        # Check ++>> https://lawsie.github.io/guizero/usingtk/
        sb_step.config(values= sb_noneflag)
    else:
        sb_step.config(values= start_step)               # set sb_step initial value
        sb_step.config(values='')                        # disable value/list mode
        sb_step.config(from_= start_step, to= end_step)  # set start and stop spinbox values

# sb_range command function.
def sb_step_cmd(x, y, name):
    #print('here i am33')
    sb_value = sb_step.get()   # Spinbox value selected.
    print('sb_step_cmd: ',sb_value)
    print('\n sb_step_cmd: ',x, y, name)

#
#   Get user spinbox input #1.
#   uses TKINTER spinbox widget (2 spinboxes).
def getinput_sb1(x, y, variable_f, start_r, end_r):
    #
    # x, y       - grid coordinates.        - parameter
    # variable_f - Function Variable name.  - parameter
    # start_r    - Range start number       - parameter
    # end_r      - Range end number         - parameter
    step_r = 50  # Range step number        - default

    #
    # Box - widget container box.
    box_height = 24     # Container height value
    box_width = 300    # Container height value  268

    global sb_step, sb_range
    global f_text
    print('F getinput_pb1: ', x, y, variable_f)
#####

    #
    # default initial 'Range and Step' spinbox value.
    sb_initial = '*1 Range Step'  # spinbox 'range' initial value
    sb_noneflag = 'None'  # spinbox 'step' initial value

    print('1: ', start_r, end_r)
    #
    # TKINTER spinbox requires: start < end, step_r needs to be positive
    step_r = abs(step_r)  # insure r_step is positive
    if start_r > end_r:  # make sure Start is less than End
        start_r, end_r = end_r, start_r  # flip order

    range_r = end_r - start_r  # get range between Start and End.
    print('2: ', start_r, end_r, range_r)

    #
    # create the range step list (format):
    #   ['*1 Range Step', 'None', 'None'] > [sb_initial,sb_noneflag,sb_noneflag]
    #   ['R2 1800/2049', 1800, 2049]      > [f'R2 {start_r}/{end_r}',start_r, end_r]
    #
    # if range is greater than range step number; create steps:
    #   ['S2 1800/1850', 1800, 1850]
    #   ['S3 1850/1900', 1850, 1900]  >> etc to 'S7 2000/2050'
    idxa_r = range_r / step_r  # number of steps
    idx_r = math.ceil(idxa_r)  # round to next greater integer.
    print('3: ', idxa_r, idx_r)
    range_steps = [[sb_initial, sb_noneflag, sb_noneflag],
                   [f'R2 {start_r}/{end_r}', start_r, end_r]]
    #
    # Create a step 'parameters' list and append it to the range_steps list.
    stepindex = 3  # initial step index: *1, R2, S'stepindex'
    low_r = high_r = start_r  # Initial starting variables to the 'start' value.
    if range_r > step_r:  # if 'range' > 'step'; create range steps.
        for idx in range(idx_r):
            high_r += step_r
            step_parms = [f'S{stepindex} {low_r}/{high_r}', low_r, high_r]
            range_steps.append(step_parms)
            low_r = high_r
            stepindex += 1

    #
    # range_list - a list of the step labels, used for the spinbox 'range' widget.
    range_list = []  # create an empty range label list.
    for idx in range(len(range_steps)):
        range_list.append(range_steps[idx][0])  # get the range label

    print('range_steps,range_list 5: ', range_steps, '\n', range_list)

    ###
    # define the box to hold the text and 2 spinbox widgets.
    b_container = Box(app, height=box_height, width=box_width, border=1, layout='grid', grid=[x, y])

    #
    #(layout="grid"
    # 1. Padding, left side
    pad_l = Box(b_container, height=22, width=5, grid = [0,0])
    # set bg - background color.  Colors - https://wiki.tcl-lang.org/page/Color+Names%2C+running%2C+all+screens
    pad_l.bg = "green"

    #
    # 2. Text widget - variable name.
    text = Text(b_container, size = 8, width=14, text=variable_f, grid = [1,0])
    text.bg = "azure"
    # Check ++>> https://lawsie.github.io/guizero/usingtk/
    # relief – type of the border which can be sunken, raised, groove, ridge.
    # https://www.geeksforgeeks.org/python-tkinter-text-widget/
    text.tk.config(relief='ridge')

    #
    # 3. Padding, left center
    pad_lc = Box(b_container, height=22, width=6, grid = [2,0])
    pad_lc.bg = "green2"

    #
    range_list = ['one', 'two']
    # 4. Spinbox widget - range steps.
    #, args = [x, y, name]
    # https: // www.tutorialspoint.com / passing - arguments - to - a - tkinter - button - command
    #:~:text=The%20Button%20widget%20in%20Tkinter,is%20triggered%20by%20the%20user.
    #pushbutton_f = PushButton(w, command=exit_window, args=[x, y, name], text='Exit window', height=1, width=10)
    #sb_range = Spinbox(b_container.tk, values=range_list, width=13, justify='left', wrap=1,  state='readonly')
    #b = ttk.Button(win, text="Insert", command=lambda: update_name("Tutorialspoint"))
    sb_range = Spinbox(b_container.tk, command=lambda: sb_range_cmd(x, y, variable_f), values=range_list,
                       width=13, justify='left', wrap=1, state='readonly')
    sb_range_value = sb_range.get()
    #print('sb_range: ',sb_range_value) # Get initial spinbox value.
    sb_range_b = b_container.add_tk_widget(sb_range, grid=[3,0])
    sb_range_b.bg = "wheat2"

    #
    # 5. Padding, right center
    pad_rc = Box(b_container, height=22, width=5, grid = [4,0])
    pad_rc.bg = "green2"

    #
    # 6. Spinbox widget - range value.    command=sb_step_cmd
    #sb_step = Spinbox(b_container.tk, from_=0, to=14, )
    sb_step = Spinbox(b_container.tk,  command=lambda: sb_step_cmd(x, y, variable_f), from_=0, to=14,
                       width=13, justify='left', wrap=1, state='readonly')
    # set initial 'step' vaule depending on the initial 'range' value/
    #if sb_range_value == sb_initial:
    #    sb_step.config(values= sb_noneflag)   # Check ++>> https://lawsie.github.io/guizero/usingtk/
   #else:
     #   sb_step.config(from_= start_r, to=end_r)

    sb_step_b = b_container.add_tk_widget(sb_step,grid=[5,0])
    sb_step_b.bg = "light yellow"

    #
    # 7. Padding, right side.
    pad_r = Box(b_container, height=22, width=6,grid = [6,0])
    pad_r.bg = "green"


# ------------------------------
# App
# ------------------------------

app = App(layout="grid")  # note 'app' is global
value_list = clear_list()   #
parm_list = clear_list()    #
text_list = clear_list()    #
btext_list = clear_list()   #
print('>> value_list: ', value_list)


instructions = Text(app, text="Get numeric value", grid=[0, 0])

getinput_sb1(0, 1, 'Year', 1800, 2049)
getinput_sb1(0, 2, 'Volume', 0, 400)
getinput_sb1(0, 3, 'Day', 1, 31)

app.display()

