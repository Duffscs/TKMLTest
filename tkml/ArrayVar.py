import tkinter as tk
from typing import List

class ArrayVar(tk.Variable):
    """
    tk.ArrayVar is a subclass of tk.Variable that manages a list of values.
    It allows you to append, remove and modify the list dynamically.
    """

    def __init__(self, master=None, value=None, transform:callable=None, name=None):
        self.transform = transform
        if transform == None:
            self.transform = lambda x: x
        self.innerData : List[object] = value
        transformedData = [self.transform(x) for x in value]
        super().__init__(master, value=transformedData or [], name=name)
        super().set(transformedData or [])

    def set(self, value):
        """Sets the value of the array (must be a list)."""
        if not isinstance(value, list):
            raise ValueError("Value must be a list")
        self.innerData = value
        value = [self.transform(x) for x in value]
        super().set(value) 

    def get(self):
        """Returns the list of values."""
        return list(super().get())
    
    def get_inner(self):
        """Returns the list of inner values."""
        return self.innerData
    
    def append(self, item):
        """Appends an item to the list."""
        current_list = self.get()
        self.innerData.append(item)
        current_list.append(self.transform(item))
        super().set(current_list)

    def remove(self, item):
        """Removes an item from the list."""
        current_list = self.get()
        if item in current_list:
            self.innerData.remove(item)
            current_list.remove(self.transform(item))
            super().set(current_list)

    def pop(self, index=-1):
        """Removes and returns an item from the list at the specified index."""
        current_list = self.get()
        item = self.innerData.pop(index)
        current_list.pop(index)
        super().set(current_list)
        return item

    def clear(self):
        """Clears the list."""
        self.innerData.clear()
        super().set([])

    def insert(self, index, item):
        """Inserts an item at a specified index."""
        current_list = self.get()
        self.innerData.insert(index, item)
        current_list.insert(index, self.transform(item))
        super().set(current_list)

    def index(self, item):
        """Returns the index of an item in the list."""
        return self.innerData.index(item)

    def sort(self, reverse=False):
        """Sorts the list."""
        current_list = self.get()
        self.innerData.sort(reverse=reverse)
        current_list = [self.transform(x) for x in self.innerData]
        super().set(current_list)

    def reverse(self):
        """Reverses the list."""
        current_list = self.get()
        self.innerData.reverse()
        current_list.reverse()
        super().set(current_list)

    def __getitem__(self, index):
        """Allows you to access an element via array_var[index]."""
        return self.innerData[index]

    def __setitem__(self, index, value):
        """Allows you to modify an element via array_var[index] = value."""
        current_list = self.get()
        self.innerData[index] = value
        current_list[index] = self.transform(value)
        super().set(current_list)

    def __delitem__(self, index):
        """Allows you to delete an element via del array_var[index]."""
        current_list = self.get()
        del self.innerData[index]
        del current_list[index]
        super().set(current_list)

    def __len__(self):
        """Returns the length of the list."""
        return len(self.innerData)
