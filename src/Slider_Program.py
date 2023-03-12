
#####  SLIDER program
####   slider function code  # over designed code for using a SLIDER widget, goal is to make this a function.

#working code
import math
from guizero import Text, Slider, ListBox, App, Box, PushButton

#
# Enter the Start and End of numeric range, and size of step levels.
variable_f = 'Year' # Function Variable name.       - parameter
start_r = 1800      # Range start number    programmable        - parameter
end_r   = 2024      # Range end number              - parameter
step_r  = 50        # Range step number             - default
interval_r  = 10    # Slider interval of numbers    - default

noneskip_value = 'None: skip'
initalslide_value = 'Range value'
print('1: ', start_r, end_r)
#
# TKINTER slider requires: start < end, step_r needs to be positive
step_r = abs(step_r)    # insure r_step is positive
if start_r > end_r:     # make sure Start is less than End
    start_r, end_r = end_r, start_r # flip order

# get range between Start and End.
range_r = end_r - start_r

print('2: ', start_r, end_r, range_r)

idxa_r = range_r/step_r     # number of steps
idx_r = math.ceil(idxa_r)   # round to next integer.

print('3: ', idxa_r, idx_r)

#
# Create/initial range_steps list:
# step format: label, start value, end value, slider interval value.
range_steps = [[noneskip_value,0,0,1],[f'Range: {start_r} / {end_r}',start_r, end_r, range_r]]
print(range_steps)

#
# set slider step interval to '10'. This will give us 5 steps, with step of 50.
step_interval = 10
# Create a step 'parameters' list and append it to the range_steps list.
low_r = high_r = start_r    # Initial starting variables to the 'start' value.
for idx in range(idx_r):
    high_r += step_r
    step_parms = [f'Step:  {low_r} / {high_r}',low_r, high_r, step_interval]
    range_steps.append(step_parms)
    low_r = high_r

print('4: ', range_steps)

#
# range_list - a list of the step labels, used for the listbox.
range_list=[]                               # create an empty step label list.
for idx in range(len(range_steps)):
    range_list.append(range_steps[idx][0])  # get the step label

print('5: ', range_list)

def save_value(name_f):
    # Return: Function Variable name / Range value
    # If no 'Step' was selected, Handle as 'cancel_value'
    # Hide/Destroy function and exit this function.
    value = t_rangestep.value
    if (t_rangestep.value == initalslide_value):
        value = 'None'
    return_dict = {name_f : value}
    print("SAVE Button was pressed: ",return_dict)


def cancel_value(name_f):
    # Return: Function Variable name / 'None' value
    # Hide/Destroy function and exit this function.
    return_dict = {name_f: 'None'}
    print("CANCEL Button was pressed: ",return_dict)

def slider_changed(slider_value):
    if (t_selectedstep.value != noneskip_value):
        t_rangestep.value = slider_value

def select_step(value):
    t_selectedstep.value = value
    listid = range_list.index(value)  #range_listx
    #
    # How to change Guizero Widgets Constructors
    # Check: https://lawsie.github.io/guizero/usingtk/
    start_step = range_steps[listid][1]             # 'start' value
    end_step = range_steps[listid][2]               # 'end' value
    interval_step = range_steps[listid][3]          # 'interval' value
    slider.tk.config(from_=start_step)              # Set new start(tk - from_) value.
    slider.tk.config(to=end_step)                   # Set new end(tk - to) value.
    slider.tk.config(tickinterval=interval_step)    # Set new interval value.
    slider.value=start_step                         # Default slider value to 'new' start value.
    print('6, from_: ', range_steps[listid][1],'xx  to: ', range_steps[listid][2],  'xx  tickinterval: ', range_steps[listid][3])
    if (value == noneskip_value):
        t_rangestep.value = 'None'
        print('None: skip')
    else:
        t_rangestep.value = start_step

app = App()

box = Box(app,width=300,height=300,border=1)
box_l = Box(box,align='left',width=200,height=300,border=1)
box_r = Box(box,align='right',width=100,height=300,border=1)

# Function text
txt1 = "Function: " + variable_f
t_function = Text(box_l, text=txt1, width='fill')
t_function.bg='light cyan'
t_function.relief='suken'

# Range step label
t_rangelabel = Text(box_l, text='Range steps', width='fill')
t_rangelabel.relief='suken'

# Listbox ranges
lb_rangesteps = ListBox(
    box_l,
    items=range_list,
    selected="None",
    command=select_step,
    width = 200,
    height = 200,
    scrollbar=True)
lb_rangesteps.text_size = 10

t_selectedstep = Text(box_l, text='Selected step')
t_selectedstep.text_size = 10
#t = Text(app, text="Its a ListBox", color="black")

pb_save = PushButton(box_l, text="save", command=save_value, args=[variable_f], width=10, align='left')
pb_save.bg='yellow2'
pb_save.relief='GROOVE'
pb_cancel = PushButton(box_l, text="cancel", command=cancel_value, args=[variable_f], width=10, align='right')
pb_cancel.bg='yellow3'
pb_cancel.relief='GROOVE'

t_rangestep = Text(box_r, text=initalslide_value ,bg='light yellow')
t_rangestep.tk.config(bd=4)
t_rangestep.tk.config(width=30)
slider = Slider(box_r, command=slider_changed, horizontal=False, height="fill",width='fill',align="bottom",start=start_r, end=end_r)
slider.justfy="left"
slider.bg='azure'
slider.tk.config(tickinterval=range_r)   # Check ++>> https://lawsie.github.io/guizero/usingtk/
print('6a, from_: ', start_r,'xx to: ', end_r, 'xx  tickinterval: ', range_r)


app.display()

exit(199)

