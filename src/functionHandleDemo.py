
# Define a function
def saySomething():
    print("\n\tIs there anybody out there?\n")
    return

# run it-- no surprises;   
saySomething()      # output:  Is there anybody out there?

# Assign the function 'handle' to x (just the function name, NO PARANTHESES)
x = saySomething 


# Run x( ), and you can verify you're running the same function
x()                 # output:  Is there anybody out there?

# Assign a function handle this way-- it's equivalent, but definite overkill
x = lambda: saySomething()

# Run x( ), and you can verify you're running the same function
x()                 # output:  Is there anybody out there?

# Define a function that accepts 1 arg,  q (assumed to be a function handle)# Try to run  q( )
def doSomething(q):
    q()
    return
    

# Now call the function and pass in function handle, x
doSomething(x)          # output:  Is there anybody out there?



