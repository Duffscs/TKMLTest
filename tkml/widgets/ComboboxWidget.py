from tkml.ObjectVar import ObjectVar
from tkml.widgets.IWidget import IWidget
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import ttk

from tkml import ArrayVar

class ComboboxWidget(IWidget):
    name = 'combobox'
    
    def create(self, element : ET.Element, parent : tk.Tk):
        values_var : ArrayVar = self.pageAssembler.handle_bindable_attribute_variable(element, parent, 'values', ArrayVar, '')
        widget = ttk.Combobox(parent, values=values_var.get(), state=element.get('state', 'normal'))
        values_var.trace_add('write', lambda *args: widget.config(values=values_var.get()))
        selected_item = self.pageAssembler.handle_bindable_attribute_variable(element, widget, 'selected_item', ObjectVar, None)
        selected_index = self.pageAssembler.handle_bindable_attribute_variable(element, widget, 'selected_index', tk.IntVar, 0)
        if selected_item.get() != None:
            print('selected_item', selected_item.get())
            widget.set(selected_item.get())
        else:
            print('selected_index', selected_index.get())
            widget.current(selected_index.current())

        def on_select(e):
            selected_index.set(widget.current())

        widget.bind('<<ComboboxSelected>>', on_select)
        previous_index = tk.IntVar(value=selected_index.get())
        previous_item = ObjectVar(value=selected_item.get())
        def on_selected_index(*args):
            if selected_index.get() == previous_index.get():
                return
            previous_index.set(selected_index.get())
            widget.selection_clear()
            if not (0 <= selected_index.get() < len(values_var)):
                previous_index.set(-1)
                selected_index.set(-1)
                previous_item.set(None)
                selected_item.set(None)
                return
            widget.current(selected_index.get())
            selected_item.set(values_var[selected_index.get()])

        def on_selected_item(*args):
            if selected_item.get() == previous_item.get():
                return
            previous_item.set(selected_item.get())
            if selected_item.get() not in values_var.innerData:
                selected_index.set(-1)
                return
            selected_index.set(values_var.index(selected_item.get()))
            
        selected_index.trace_add('write', on_selected_index)
        selected_item.trace_add('write', on_selected_item)

        selected_index.set(widget.current())
        return widget