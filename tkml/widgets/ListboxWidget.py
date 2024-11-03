from tkml.widgets.IWidget import IWidget
import tkinter as tk
import xml.etree.ElementTree as ET

from tkml.ObjectVar import ObjectVar
from tkml.ArrayVar import ArrayVar

class ListboxWidget(IWidget):
    name = 'listbox'
    
    def create(self, element : ET.Element, parent : tk.Tk):
        selectmode = element.get('selectmode', 'single')
        values_var = self.pageAssembler.handle_bindable_attribute_variable(element, parent, 'values', ArrayVar, '')

        widget = tk.Listbox(parent, selectmode=selectmode, listvariable=values_var)
        if selectmode == 'multiple':
            self._create_multiple_listbox(widget, element, values_var)
        elif selectmode == 'disabled':
            self._create_disabled_listbox(widget)
        else:
            self._create_single_listbox(widget, element, values_var)

        return widget
    
    def _create_single_listbox(self, widget : tk.Listbox,  element : ET.Element, values_var : ArrayVar):
        print('Creating single listbox')
        selected_item = self.pageAssembler.handle_bindable_attribute_variable(element, widget, 'selected_item', ObjectVar, None)
        selected_index = self.pageAssembler.handle_bindable_attribute_variable(element, widget, 'selected_index', tk.IntVar, 0)

        def on_select(e):
            if widget.curselection().__len__() == 0:
                selected_index.set(-1)
                selected_item.set(None)
                return
            selected_index.set(widget.curselection()[0])
        
        widget.bind('<<ListboxSelect>>', on_select)
        previous_index = tk.IntVar(value=selected_index.get())
        previous_item = ObjectVar(value=selected_item.get())
        def on_selected_index(*args):
            if selected_index.get() == previous_index.get():
                return
            previous_index.set(selected_index.get())
            widget.selection_clear(0, tk.END)
            if not (0 <= selected_index.get() < len(values_var)):
                previous_index.set(-1)
                selected_index.set(-1)
                previous_item.set(None)
                selected_item.set(None)
                return
            widget.selection_set(selected_index.get())
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

        selected_index.set(selected_index.get())

    def _create_disabled_listbox(self, widget):
        widget.config(activestyle=tk.NONE)
        def on_select(e):
            widget.selection_clear(0, tk.END)
        
        widget.bind('<<ListboxSelect>>', on_select)

    def _create_multiple_listbox(self, widget : tk.Listbox,  element : ET.Element, values_var : ArrayVar):
        print('Creating multiple listbox')
        selected_items = self.pageAssembler.handle_bindable_attribute_variable(element, widget, 'selected_items', ArrayVar, '')
        selected_indices = self.pageAssembler.handle_bindable_attribute_variable(element, widget, 'selected_indices', ArrayVar, '')
        print(selected_items.get())
        def on_select(e):
            selected_indices.set(list(widget.curselection()))
        
        widget.bind('<<ListboxSelect>>', on_select)

        previous_indices = ArrayVar(value=selected_indices.get())
        previous_items = ArrayVar(value=selected_items.get())
        def on_selected_indices(*args):
            if selected_indices.get() == previous_indices.get():
                return
            previous_indices.set(selected_indices.get())
            previous_items.set([values_var[i] for i in selected_indices.get()])
            widget.selection_clear(0, tk.END)
            for i in selected_indices.get():
                widget.selection_set(i)
            widget.see(selected_indices[0]) if selected_indices.get() else None
            selected_items.set(list(previous_items.get()))
            print(selected_items.get())
            print(selected_indices.get())


        def on_selected_items(*args):
            if selected_items.get() == previous_items.get():
                return
            previous_items.set(selected_items.get())
            selected_indices.set([values_var.index(item) for item in selected_items.get() if item in values_var.innerData])
            print(selected_indices.get())

        selected_items.trace_add('write', on_selected_items)
        selected_indices.trace_add('write', on_selected_indices)

        selected_indices.set(list(widget.curselection()))