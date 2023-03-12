
import sys
import math
from guizero import Text, App, Box
from tkinter import Spinbox

class SpinBoxRanged:

    name                = ''
    x                   = 0
    y                   = 0
    
    # Spinbox setup values
    textList            = []            # List of (string) values to populate guiSpinBoxText
    numericList         = []            # List of (numeric) values to populate guiSpinBoxNumeric
    start               = 0             # integer start value
    stop                = 0             # integer stop value
    maxSize             = 0             # Don't allow the numeric spinbox to have more than this number of values
    dictRangeValues     = {}            # Dictionary that's keyed by the text description of range (e.g. 'S1: 1800/1850')
                                        #   and valued by the numeric range (e.g. [1800, 1801, 1802, ... 1850] )
    
    # GUI components
    guiApp              = []            # Main app
    guiContainer        = []            # TK Box object
    guiSpinBoxText      = []            # Spinbox, holding text/descriptive ranges
    guiSpinBoxNumeric   = []            # Spinbox, holding numeric values    
    guiSpinBoxTextTK    = []            # TK object after placing inside guiContainer
    guiSpinBoxNumericTK = []            # TK object after placing inside guiContainer
    guiPaddings         = []            # GUI objects used for padding

    # FINAL USER OUTPUTS STORED HERE:
    output              = {}            # Dictionary, stores the final values selected by the user
    value               = 0             # Stores user-selected value... same as .output['value']
            
    def __init__(self, app, x,y, name, start, stop, maxSize):
        """
        __init__(app, x,y, name, start, stop, maxSize)
        
        DESCRIPTION:
        Constructor, builds the GUI components and fills out the ranges.
        This is the only method that needs to be run.
        
        Inputs:
               app:     GUIZERO app
               x,y:     int, the x,y grid placement for this pair of spinboxes
              name:     str, Name of this spinbox
             start:     int, start value for the full range of numbers
              stop:     int, stop/end value for the full range of numbers
           maxSize:     int, max number of values to use in the numeric spinbox.
                        This determines how many separate ranges we split the stop-start range into.
        """
        self.name  = name
        self.x     = x
        self.y     = y
        
        # Error check... returns an error if this isn't right
        assert stop > start, "Error in SpinBoxRanged.__init__():\n\tConstructor argument 'stop' must be > 'start'"
        
        self.start = start
        self.stop  = stop
        self.maxSize  = maxSize
        self.output = { 'name'      :   name,       # Name of this spinbox
                        'range'     :   '',         # Spinbox #1 text (descriptive range) value stored here
                        'value'     :   0,          # Spinbox #2 numeric value
                        }
                        
                        
        self.guiApp = app
        self.guiContainer = Box(app, height=24, width=300, border=1, layout='grid', grid=[x,y])

        # Used for debugging
        # self.textList          = [ 'one', 'two', 'three', 'four', 'five', 'six', 'seven' ]
        # self.numericList       = list(range(0,7))
        
        dictRangeValues = {}        # Dictionary to hold all text "ranges" and corresponding numeric values        
        numRanges = math.ceil( (stop-start)/maxSize )   
        
        self.textList = []          # List of ALL text range descriptions, needed for .guiSpinBoxText
        
        # Split the full start ==> stop range into numRanges 
        k=0
        for k in range(numRanges):
            valStart = start+k*maxSize                                  # numeric start of 1 range           
            valStop  = start+(k+1)*maxSize-1                            # numeric end of 1 range
            if ( valStop > stop ):
                valStop = stop
            values   = list(range(valStart, valStop+1))                 # All numeric values for spinbox (dictionary value)
            text     = "S{}:  {}/{}".format(k+1, valStart,valStop)      # text description of range (dictionary key)
            dictRangeValues[text] = values                              # Store text description and value 
            self.textList.append(text)                                  # Throw this text description in the list
            
        textRange              = self.textList[0]                       # Initially, pick the first text range
        self.numericList       = dictRangeValues[textRange]             # Extract corresponding numeric range from dictionary        
        self.dictRangeValues   = dictRangeValues;                       # Store the dictionary in the class
        
        self.output['range']   = textRange                              # Initialize output (text) range in dictionary
        self.output['value']   = self.numericList[0]                    # Initialize output value in dictionary
        
        
        # NOW BUILD THE GUI STUFF        
        self.guiSpinBoxText    = Spinbox(self.guiContainer.tk, command=lambda: self.getValueSpinBoxText(),    values=self.textList,    width=13, justify='left', wrap=1, state='readonly')       
        self.guiSpinBoxNumeric = Spinbox(self.guiContainer.tk, command=lambda: self.getValueSpinBoxNumeric(), values=self.numericList, width=13, justify='left', wrap=1, state='readonly')
        # self.guiSpinBoxNumeric = Spinbox(self.guiContainer.tk, command=lambda: self.getValueSpinBoxNumeric(), from_=0, to=20, width=13, justify='left', wrap=1, state='readonly')
        
        # Place all GUI objs (spacers, text, & Spinboxes) in .guiContainer, on a grid, left to right
        guiPadL                 = Box(self.guiContainer,  height=22, width=5,                   grid=[0,0] )
        guiTxtName              = Text(self.guiContainer, size = 8,  width=14, text=self.name,  grid=[1,0] )
        guiPadLC                = Box(self.guiContainer,  height=22, width=6,                   grid=[2,0] )        
        self.guiSpinBoxTextTK   = self.guiContainer.add_tk_widget(self.guiSpinBoxText,          grid=[3,0] )          
        guiPadRC                = Box(self.guiContainer,  height=22, width=5,                   grid=[4,0] )        
        self.guiSpinBoxNumericTK= self.guiContainer.add_tk_widget(self.guiSpinBoxNumeric,       grid=[5,0] )  
        
        # Store these, so they don't go out of scope
        self.guiPaddings.append(guiPadL)
        self.guiPaddings.append(guiTxtName)
        self.guiPaddings.append(guiPadLC)
        self.guiPaddings.append(guiPadRC)
        
        return
        
    def getValueSpinBoxText(self):
        txt = self.guiSpinBoxText.get()                         # get selected spinbox text 'range' value.
        self.output['range'] = txt                              # Store the text range value in .output dict
        numericList = self.dictRangeValues[txt]                 # Get the new list of numeric values in that range
        self.guiSpinBoxNumeric.configure(values=numericList)    # Update the numeric spinner with new values
        
        # Also have to update the value, since user switched ranges
        val = self.guiSpinBoxNumeric.get()                      # Store selected spinbox numeric value
        self.output['value'] = val                              # Store selected spinbox numeric value in dict
        self.value = val                                        # Store selected spinbox numeric value in .value
        return 

    def getValueSpinBoxNumeric(self):
        val = self.guiSpinBoxNumeric.get()                      # get selected spinbox numeric value
        self.output['value'] = val                              # store selected spinbox numeric value in dict
        self.value = val                                        # Store selected spinbox numeric value in .value
        return


if __name__ == '__main__':

    app = App(layout="grid")    # note 'app' is global        
    guiInstructions   = Text(app, text="Get numeric value", grid=[0,0])
    # app.display()
      
    x = 1
    y = 2
    name = 'Day'
    start = 1
    stop  = 31
    maxSize = 7
    
    sbYear = SpinBoxRanged(app, 0, 0, 'Year',  1800, 2049,  50)   # args:  (app, x, y, name, start, stop, maxSize)    
    sbVol  = SpinBoxRanged(app, 0, 1, 'Volume', 0,    400,  50)   # args:  (app, x, y, name, start, stop, maxSize)
    sbDay  = SpinBoxRanged(app, 0, 2, 'Day',    1,    31,   7)   # args:  (app, x, y, name, start, stop, maxSize)
    
    app.display()
    
    print("\nFinal .output Dictionaries from each SpinBoxRanged object:")
    print(sbYear.output)
    print(sbVol.output)
    print(sbDay.output)
    
    # You can also ignore the dictionary since we also stored selected value in .value property
    print("\n\nUser selected year={}, volume={}, day={}\n".format(sbYear.value, sbVol.value, sbDay.value))

    sys.exit()
