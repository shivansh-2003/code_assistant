#!/usr/bin/env python3
"""
This is a test file for code-analyzer.py.
It contains various code patterns to test the analyzer's capabilities.
"""

import os
import sys
import json
from datetime import datetime as dt
import random as rnd
import re

# Global variable - not ideal practice
GLOBAL_CONSTANT = "This is a global constant"
counter = 0

class GoodClass:
    """
    A properly formatted class with docstrings and good naming conventions.
    This class demonstrates good coding practices.
    """
    
    def __init__(self, name, value):
        """Initialize the class with a name and value.
        
        Args:
            name (str): The name of the instance
            value (int): The value to store
        """
        self.name = name
        self.value = value
        self._private_var = 100
    
    def calculate_something(self, multiplier=1):
        """Calculate a value based on the stored value and a multiplier.
        
        Args:
            multiplier (int, optional): Value to multiply by. Defaults to 1.
            
        Returns:
            int: The calculated value
        """
        return self.value * multiplier
    
    def complex_operation(self, input_data):
        """Perform a more complex operation with multiple branches.
        
        Args:
            input_data (dict): Input data to process
            
        Returns:
            dict: Processed data
        """
        result = {}
        
        if "name" in input_data:
            result["processed_name"] = input_data["name"].upper()
        
        if "values" in input_data:
            total = 0
            for value in input_data["values"]:
                if value > 0:
                    total += value
                else:
                    total -= value / 2
            
            result["total"] = total
            
            if total > 100:
                result["status"] = "high"
            elif total > 50:
                result["status"] = "medium"
            else:
                result["status"] = "low"
        
        return result


class badClassNaming:
    """This class has poor naming conventions and incomplete documentation."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # Missing docstring
    def do_stuff(self, z):
        # Cryptic variable names
        a = self.x + z
        b = self.y - z
        return a * b


# A function with good practices
def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.
    
    Args:
        numbers (list): A list of numeric values
        
    Returns:
        float: The average value, or 0 if the list is empty
    """
    if not numbers:
        return 0
    
    total = sum(numbers)
    return total / len(numbers)


# A poorly written function
def badFunc(x,y,z):
    # No docstring, poor naming, inconsistent spacing
    res=0
    if x>0:
        if y>0:
            res=x+y
        else:
            res=x-y
    else:
        res=z
    return res


# A function with too many responsibilities and excessive length
def process_data_file(filename):
    # Opening comment but no proper docstring
    # This function does too many things: reads a file, processes the data, and writes results
    
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found!")
        return False
    
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return False
    
    # Process the data - lots of code doing different things
    lines = content.split('\n')
    results = []
    
    for line in lines:
        if not line.strip():
            continue
        
        # Complex parsing logic
        parts = line.split(',')
        if len(parts) < 3:
            print(f"Invalid line format: {line}")
            continue
        
        try:
            id_val = int(parts[0])
            name = parts[1]
            value = float(parts[2])
            
            # Complex business logic
            if value < 0:
                category = "negative"
                processed_value = value * 1.1
            elif value < 100:
                category = "small"
                processed_value = value * 1.05
            elif value < 1000:
                category = "medium"
                processed_value = value * 1.02
            else:
                category = "large"
                processed_value = value * 1.01
            
            # More processing
            if name.startswith("A"):
                priority = "high"
            elif name.startswith("B"):
                priority = "medium"
            else:
                priority = "low"
            
            results.append({
                "id": id_val,
                "name": name,
                "original_value": value,
                "processed_value": processed_value,
                "category": category,
                "priority": priority,
                "timestamp": dt.now().isoformat()
            })
        except Exception as e:
            print(f"Error processing line: {line}, Error: {str(e)}")
    
    # Write the results to a new file
    output_file = f"{filename}_processed.json"
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Processed data written to {output_file}")
        return True
    except Exception as e:
        print(f"Error writing results: {str(e)}")
        return False


# Function with repeated code - violates DRY principle
def calculate_areas(shapes):
    """Calculate areas of different shapes.
    
    Args:
        shapes (list): List of shape dictionaries
        
    Returns:
        dict: Dictionary of calculated areas
    """
    results = {}
    
    for shape in shapes:
        if shape["type"] == "circle":
            # Calculate circle area
            radius = shape["radius"]
            area = 3.14159 * radius * radius
            results[shape["id"]] = area
        
        if shape["type"] == "rectangle":
            # Calculate rectangle area
            width = shape["width"]
            height = shape["height"]
            area = width * height
            results[shape["id"]] = area
        
        if shape["type"] == "square":
            # Calculate square area - repeating code instead of treating as a rectangle
            side = shape["side"]
            area = side * side
            results[shape["id"]] = area
        
        if shape["type"] == "triangle":
            # Calculate triangle area
            base = shape["base"]
            height = shape["height"]
            area = 0.5 * base * height
            results[shape["id"]] = area
    
    return results


# Some poorly formatted code with inconsistent indentation and style
def messy_function():
  """This function has inconsistent formatting."""
  x = 10
  if x > 5:
        print("X is greater than 5")
  else:
    print("X is not greater than 5")
    
    for i in range(10):
       if i % 2 == 0:
           print(f"Even: {i}")
       else:
         print(f"Odd: {i}")
  
  return x * 2


# Example of main function
def main():
    """Main function to demonstrate the test code."""
    # Create some instances
    good = GoodClass("example", 42)
    bad = badClassNaming(10, 20)
    
    # Use the functions
    numbers = [1, 2, 3, 4, 5]
    avg = calculate_average(numbers)
    
    result = badFunc(5, -3, 10)
    
    # Create some test data for the areas function
    shapes = [
        {"id": "circle1", "type": "circle", "radius": 5},
        {"id": "rect1", "type": "rectangle", "width": 10, "height": 5},
        {"id": "square1", "type": "square", "side": 7},
        {"id": "triangle1", "type": "triangle", "base": 8, "height": 4}
    ]
    
    areas = calculate_areas(shapes)
    
    # Print some results
    print(f"Good class calculation: {good.calculate_something(2)}")
    print(f"Bad class result: {bad.do_stuff(5)}")
    print(f"Average: {avg}")
    print(f"Bad function result: {result}")
    print(f"Areas: {areas}")
    print(f"Messy function result: {messy_function()}")


if __name__ == "__main__":
    main() 