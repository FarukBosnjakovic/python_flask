# First Class Functions

def add(n1,n2):
    return n1 + n2

def subtract(n1,n2):
    return n1 - n2 

def multiply(n1, n2):
    return n1 * n2 

def divide(n1, n2):
    return n1 / n2 


# First-class objects, can be passed around as arguments e.g. int/string/float 
# We can create a function that uses the functions above 

def calculate(calc_function, n1, n2): 
    return calc_function(n1, n2)

result = calculate(multiply, 2, 3)
print(result)
print()


# Nested Functions

def outer_function():
    print('I am outer') 
    
    def nested_function():
        print('I am inner') 
        
    """Nested function needs to be called inside of the outer function
    in order to work and not get an error"""
    
    nested_function() # calling a nested function 

outer_function()
print()

# Functions can be returned from other functions 

def outer_function():
    print('I am outer') 
    
    def nested_function():
        print('I am inner')
        
    return nested_function 


inner_function = outer_function() # OUTPUT: I am outer
inner_function() # OUTPUT: I am inner