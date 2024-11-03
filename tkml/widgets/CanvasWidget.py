from tkml.widgets.IWidget import IWidget
import tkinter as tk
import xml.etree.ElementTree as ET

class CanvasWidget(IWidget):
    name = 'canvas'
    
    def create(self, element : ET.Element, parent : tk.Tk):
        return tk.Canvas(parent)