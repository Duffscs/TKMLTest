import tkinter as tk
from typing import List
import xml.etree.ElementTree as ET
from tkml.widgets import IWidget, ButtonWidget, CanvasWidget, CheckbuttonWidget, ComboboxWidget, EntryWidget, FrameWidget, LabelWidget, ListboxWidget, RadiobuttonWidget, ScrollbarWidget, TextWidget

if 1 == 0:
    from tkml.TkmlPageAssembler import TkmlPageAssembler

class WidgetResolver:

    def __init__(self, pageAssember : 'TkmlPageAssembler'):
        self.widgets : List[IWidget] = [
            ButtonWidget(pageAssember),
            CanvasWidget(pageAssember),
            CheckbuttonWidget(pageAssember),
            ComboboxWidget(pageAssember),
            EntryWidget(pageAssember),
            FrameWidget(pageAssember),
            LabelWidget(pageAssember),
            ListboxWidget(pageAssember),
            RadiobuttonWidget(pageAssember),
            ScrollbarWidget(pageAssember),
            TextWidget(pageAssember)
        ]

    def resolve(self,  element : ET.Element, parent : tk.Tk):
        for widget in self.widgets:
            if widget.validate(element):
                return widget.create(element, parent)