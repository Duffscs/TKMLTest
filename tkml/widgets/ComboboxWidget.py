from tkml.widgets.IWidget import IWidget
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import ttk

from tkml import ArrayVar

class ComboboxWidget(IWidget):
    name = 'combobox'
    
    def create(self, element : ET.Element, parent : tk.Tk | tk.Toplevel | tk.Frame):
        values_var = self.pageAssembler.handle_bindable_attribute_variable(element, parent, 'values', ArrayVar, '')
        widget = ttk.Combobox(parent, values=values_var.get(), state=element.attrib.get('state', 'normal'))
        values_var.trace_add('write', lambda *args: widget.config(values=values_var.get()))
        selected_item = self.pageAssembler.handle_bindable_attribute_variable(element, widget, 'selected_item', tk.StringVar, '')
        selected_index = self.pageAssembler.handle_bindable_attribute_variable(element, widget, 'selected_index', tk.IntVar, 0)
        if selected_item.get() != '':
            widget.set(selected_item.get())
        else:
            widget.current(selected_index.get())

        def on_select(e):
            selected_item.set(widget.get())
            selected_index.set(widget.current())

        widget.bind('<<ComboboxSelected>>', on_select)

        def on_selected_index(*args):
            if selected_index.get() == widget.current():
                return
            widget.current(selected_index.get())
            selected_item.set(widget.get())

        def on_selected_item(*args):
            if selected_item.get() == widget.get():
                return
            widget.set(selected_item.get())
            selected_index.set(widget.current())
            
        selected_index.trace_add('write', on_selected_index)
        selected_item.trace_add('write', on_selected_item)

        selected_item.set(widget.get())
        selected_index.set(widget.current())
        return widget