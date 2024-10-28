from tkml.widgets.IWidget import IWidget
import tkinter as tk
import xml.etree.ElementTree as ET

from tkml.ArrayVar import ArrayVar

class ListboxWidget(IWidget):
    name = 'listbox'
    
    def create(self, element : ET.Element, parent : tk.Tk | tk.Toplevel | tk.Frame):
        selectmode = element.attrib.get('selectmode', 'single')
        values_var = self.pageAssembler.handle_bindable_attribute_variable(element, parent, 'values', ArrayVar, '')
        print(values_var.get())
        widget = tk.Listbox(parent, selectmode=selectmode, listvariable=values_var)

        selected_item = self.pageAssembler.handle_bindable_attribute_variable(element, widget, 'selected_item', tk.StringVar, '')
        selected_index = self.pageAssembler.handle_bindable_attribute_variable(element, widget, 'selected_index', tk.IntVar, 0)
        selected_items = self.pageAssembler.handle_bindable_attribute_variable(element, widget, 'selected_items', ArrayVar, '')
        selected_indices = self.pageAssembler.handle_bindable_attribute_variable(element, widget, 'selected_indices', ArrayVar, '')

        if widget.size() != 0:
            if selected_item.get() != '':
                index = widget.get(0, tk.END).index(selected_item.get())
                widget.select_set(index)
                widget.see(index)
                selected_index.set(index)
                selected_indices.set(list(widget.curselection()))
                selected_items.set([widget.get(i) for i in selected_indices.get()])
            elif selected_index.get() != 0:
                widget.select_set(selected_index.get())
                widget.see(selected_index.get())
                selected_item.set(widget.get(selected_index.get()))
                selected_indices.set(list(widget.curselection()))
                selected_items.set([widget.get(i) for i in selected_indices.get()])
            elif selected_indices.get() != []:
                print(selected_indices.get())
                for index in selected_indices.get():
                    widget.select_set(index)
                selected_items.set([widget.get(i) for i in selected_indices.get()])
                selected_item.set(widget.get(selected_index.get()))
                selected_index.set(widget.curselection()[0])
            elif selected_items.get() != []:
                for item in selected_items.get():
                    index = widget.get(0, tk.END).index(item)
                    widget.select_set(index)
                selected_indices.set(widget.curselection())
                selected_index.set(widget.curselection()[0])
                selected_item.set(widget.get(selected_index.get()))
            else:
                widget.select_set(0)
                widget.see(0)
                selected_index.set(widget.curselection()[0])
                selected_item.set(widget.get(selected_index.get()))
                selected_indices.set(list(widget.curselection()))
                selected_items.set([widget.get(i) for i in selected_indices.get()])

        def on_select(e):
            if widget.curselection().__len__() == 0:
                return
            selected_index.set(widget.curselection()[0])
            selected_item.set(widget.get(selected_index.get()))
            selected_indices.set(list(widget.curselection()))
            selected_items.set([widget.get(i) for i in selected_indices.get()])
        
        widget.bind('<<ListboxSelect>>', on_select)

        def on_selected_index(*args):
            if selected_index.get() == widget.curselection()[0]:
                return
            widget.select_clear(0, tk.END)
            widget.select_set(selected_index.get())
            widget.see(selected_index.get())
            selected_item.set(widget.get(selected_index.get()))
            selected_indices.set(list(widget.curselection()))
            selected_items.set([widget.get(i) for i in selected_indices.get()])

        def on_selected_item(*args):
            if selected_item.get() == '':
                return
            index = widget.get(0, tk.END).index(selected_item.get())
            if selected_item.get() == widget.get(index):
                return
            widget.select_clear(0, tk.END)
            widget.select_set(index)
            widget.see(index)
            selected_index.set(index)
            selected_indices.set(list(widget.curselection()))
            selected_items.set([widget.get(i) for i in selected_indices.get()])

        def on_selected_indices(*args):
            if selected_indices.get() == list(widget.curselection()):
                return
            widget.select_clear(0, tk.END)
            for index in selected_indices.get():
                widget.select_set(index)
            selected_items.set([widget.get(i) for i in selected_indices.get()])
            selected_item.set(widget.get(selected_index.get()))
            selected_index.set(widget.curselection()[0])

        def on_selected_items(*args):
            if selected_items.get() == [widget.get(i) for i in selected_indices.get()]:
                return
            widget.select_clear(0, tk.END)
            for item in selected_items.get():
                index = widget.get(0, tk.END).index(item)
                widget.select_set(index)
            selected_indices.set(widget.curselection())
            selected_index.set(widget.curselection()[0])
            selected_item.set(widget.get(selected_index.get()))

        selected_index.trace_add('write', on_selected_index)
        selected_item.trace_add('write', on_selected_item)
        selected_items.trace_add('write', on_selected_items)
        selected_indices.trace_add('write', on_selected_indices)

        if widget.size() != 0 and selected_item.get() != '' and selected_index.get() != 0 and selected_indices.get() != [] and selected_items.get() != []: 
            selected_index.set(widget.curselection()[0])
            selected_item.set(widget.get(selected_index.get()))
            selected_indices.set(list(widget.curselection()))
            selected_items.set([widget.get(i) for i in selected_indices.get()])

        return widget