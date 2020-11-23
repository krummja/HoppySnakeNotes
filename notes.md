
# Table of Contents

1.  [PEP 8 Style Guide](#orgb89045b)
2.  [Antipatterns](#org8125033)



<a id="orgb89045b"></a>

# PEP 8 Style Guide

PEP, or Python Enhancement Proposals, are a collection of &#x2026; well, proposals aimed at enhancing Python. One of the most important is PEP 8, or the Style Guide. Coding style is, in many ways, a matter of programmer taste, but many of the recommendations in PEP 8 have become accepted standard, and they make code consistent and portable over time.

There are a few major changes we can make to the code to make it much more readable and generally better formatted.

-   All indentation should be equivalent to 4 spaces. The indents in your code are 3 spaces.
-   There should be a space between `#` and the comment string following.

``` python
    # this is a formatted comment 
```

-   There should be two spaces preceding a `#` following code.

``` python
    print("Hello, world!")  # this is a comment following code
```

-   Surround top-level function and class definitions with two blank lines.

``` python
    def some_function():
        # some business code


    class SomeClass:
        # some class definitions
```

<a id="org8125033"></a>

# Antipatterns

There are a few major antipatterns in your code that you want to try to avoid. The biggest I see is the use of the `global` keyword, which you should avoid using at all costs. There are very few good reasons to use it. It is better to explicitly declare a variable in the global scope, and then pass it into whatever functions or classes require it.

In the context of your code, you can declare these "global" variables as local to the `main()` function and then pass them in. Better yet, you can make a class that represents the game instance, and keep those important variables in the scope of that instance instead.

``` python
    class Game:
        """Contains all of the core game logic."""
    
        def __init__(self):
    	    self.score = 0
    	    self.running = False    
```

It is generally a good idea to make your variable names semantically transparent. A variable like `p1` or `ao` doesn't tell us anything about what they represent. Instead, use things like `player` or `active_objects`.

``` python
    player = Player(x=-200, y=0, canvas=window)
```

Note as well that I've passed in arguments to the `Player` class as keyword arguments. This is the more Pythonic way of doing things, but it's not strictly required.

For the sake of making the code more readable, you also want to avoid variables that mirror the name of the classes they're contained in. For example, it is not entirely clear what `Player.player` is meant to represent. What it appears to be referring to is actually the graphical component of the player, so we can change this to something like `Player.sprite` and make it much clearer.

``` python
    class Player:
    
        def __init__(self, x, y, canvas):
    	    # ...
    	    self.sprite = turtle.RawTurtle(canvas)
```

When defining a variable, there is no need to create a local variable and then assign that variable to a class property:

``` python
    class OtherClass:
    
        def __init__(self, x):
    	    self.x = x
    
    
    class SomeClass:
    
        def __init__(self):
    	    self.other = OtherClass(10)
```

I would recommend making some of these functions that you have in the global namespace into members of a class instead. In the following, I will show how I would approach the design of this program, with commentary as necessary.

Your initial setup is basically fine. I would just make the variable name for the game window more explicit. I will also be opting to encapsulate the entire game inside of a class to put everything in a safer scope.

``` python
    import random
    import turtle
    import time
    
    
    class Game:
        def __init__(self):
    	    self.window = turtle.Screen()
    	    self.window.tracer(0)
    	    self.score = 0
    	    self.running = False
```
