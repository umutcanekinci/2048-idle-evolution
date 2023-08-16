"""
Program to Define a Custom Text Class
 
This program defines a custom class called `text` that inherits from the str class.
The text class overrides the __init__ method to initialize the object with a default text.
 
"""

class text(str):
    def __init__(self) -> None:
        super().__init__("this is a text")
 
 
if __name__ == "__main__":
    b = text()
    print(b)