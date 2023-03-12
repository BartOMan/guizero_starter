
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
        
    
    # GUI components
    guiApp              = []            # Main app
    guiContainer        = []            # TK Box object
    guiSpinBoxText      = []            # Spinbox, holding text/descriptive ranges
    guiSpinBoxNumeric   = []            # Spinbox, holding numeric values    
    guiSpinBoxTextTK    = []            # TK object after placing inside guiContainer
    guiSpinBoxNumericTK = []            # TK object after placing inside guiContainer

    output              = {}            # Dictionary, stores the final values selected by the user
    
    def __init__(self):
    
        return
        
    def initialize(self, app, x,y, name, start, stop, maxSize):
        """
        initialize(app, x,y, name, start, stop, maxSize)
        
        DESCRIPTION:
        Builds the GUI components and fills out the ranges.
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
        
        assert stop > start, "Error in SpinBoxRanged.initialize():\n\tArgument 'stop' must be > 'start'"
        self.start = start
        self.stop  = stop
        self.maxSize  = maxSize
        self.output = { 'name'      :   name,       # Name of this spinbox
                        'range'     :   '',         # Spinbox #1 text (descriptive range) value stored here
                        'value'     :   0,          # Spinbox #2 numeric value
                        }
                        
                        
        self.guiApp = app
        self.guiContainer = Box(app, height=24, width=300, border=1, layout='grid', grid=[x,y])
        
        self.textList          = [ 'one', 'two', 'three', 'four', 'five', 'six', 'seven' ]
        self.numericList       = list(range(0,7))
        
        dictRangeValues = {}        # Dictionary to hold all text "ranges" and corresponding numeric values        
        numRanges = math.ceil( (stop-start)/maxSize )   
        
        self.textList = []          # List of ALL text range descriptions, needed for .guiSpinBoxText
        
        # Split the full start ==> stop range into numRanges 
        k=0
        for k in range(numRanges):
            valStart = start+k*maxSize                                  # numeric start of 1 range           
            valStop  = start+(k+1)*maxSize                              # numeric end of 1 range
            values   = list(range(valStart, valStop+1))                 # All numeric values for spinbox (dictionary value)
            text     = "S{}:  {}/{}".format(k+1, valStart,valStop)      # text description of range (dictionary key)
            dictRangeValues[text] = values                              # Store text description and value 
            self.textList.append(text)                                  # Throw this text description in the list
            
        textRange              = self.textList[0]                       # Initially, pick the first text range
        self.numericList       = dictRangeValues[textRange]             # Extract corresponding numeric range from dictionary        
        
        self.output['range']   = textRange                              # Initialize output (text) range in dictionary
        self.output['value']   = self.numericList[0]                    # Initialize output value in dictionary
        
        self.guiSpinBoxText    = Spinbox(self.guiContainer.tk, command=lambda: self.getValueSpinBoxText(),    values=self.textList,    width=13, justify='left', wrap=1, state='readonly')       
        self.guiSpinBoxNumeric = Spinbox(self.guiContainer.tk, command=lambda: self.getValueSpinBoxNumeric(), values=self.numericList, width=13, justify='left', wrap=1, state='readonly')
        # self.guiSpinBoxNumeric = Spinbox(self.guiContainer.tk, command=lambda: self.getValueSpinBoxNumeric(), from_=0, to=20, width=13, justify='left', wrap=1, state='readonly')

        self.guiSpinBoxTextTK    = self.guiContainer.add_tk_widget(self.guiSpinBoxText,    grid=[0,0])  
        self.guiSpinBoxNumericTK = self.guiContainer.add_tk_widget(self.guiSpinBoxNumeric, grid=[1,0])  
        return
        
    def getValueSpinBoxText(self):
        self.output['range'] = self.guiSpinBoxText.get()        # get selected spinbox text 'range' value.
        return 

    def getValueSpinBoxNumeric(self):
        self.output['value'] = self.guiSpinBoxNumeric.get()     # get selected spinbox numeric value
        return



if __name__ == '__main__':

    app = App(layout="grid")    # note 'app' is global        
    guiInstructions   = Text(app, text="Get numeric value", grid=[0,0])
    # app.display()
      
    x           = 3
    y           = 2
    name        = 'Year'
    start       = 1800
    stop        = 2049
    maxSize     = 50            # No more than 50 years in the numeric spinbox
    
    sbYear = SpinBoxRanged()
    self   = sbYear
    sbYear.initialize(app, x, y, name,  start, stop, maxSize)   # args:  (app, x, y, name, start, stop, maxSize)
    
    # sbYear = SpinBoxClass(app, 0, 1, 'Year',   1800, 2049, 50)   # args:  (app, x, y, name, start_r, end_r, step_r)
    # sbVol  = SpinBoxClass(app, 0, 2, 'Volume', 0,    400,  50)   # args:  (app, x, y, name, start_r, end_r, step_r)
    # sbDay  = SpinBoxClass(app, 0, 3, 'Day',    1,    31,   31)   # args:  (app, x, y, name, start_r, end_r, step_r)
    
    app.display()
    
    print("\nFinal Values from the user:")
    # print(sbYear.output)
    # print(sbVol.output)
    # print(sbDay.output)

    # print(str(sbc))

