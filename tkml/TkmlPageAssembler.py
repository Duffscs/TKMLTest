import re
import tkinter as tk
import xml.etree.ElementTree as ET
from tkml import WidgetResolver, TkmlPage
from tkml.WidgetResolver import WidgetResolver
from tkml.ArrayVar import ArrayVar

class TkmlPageAssembler:
    def __init__(self, tkml_page : 'TkmlPage'):
        self.tkml_page = tkml_page
        self.widget_resolver = WidgetResolver(self)

    def assemble(self, tkml_string):
        root_element = ET.fromstring(tkml_string)
        if root_element.tag != 'Window':
            raise ValueError('TKML string must start with a Window element.')
        
        if isinstance(self.tkml_page.root, tk.Tk):
            self.tkml_page.root.title(self.resolve_template(root_element.attrib.get('title', 'TKML Window')))
            self.tkml_page.root.geometry(f"{root_element.attrib.get('width', '300')}x{root_element.attrib.get('height', '200')}")
        
        layout = root_element.attrib.get('layout', 'pack').lower()
        self.create_widgets(root_element, self.tkml_page.root, layout)
        self.tkml_page.on_window_ready()


    def resolve_template(self, text):
        for var_name in dir(self.tkml_page):
            var_value = getattr(self.tkml_page, var_name)
            if isinstance(var_value, tk.StringVar):
                text = text.replace(f"{{{{ {var_name} }}}}", var_value.get())
        return text
    
    def create_widgets(self, element, parent, layout):
        if layout == 'grid':
            self.configure_grid(parent, element)

        for child in element:
            widget = self.create_widget(child, parent)
            if widget:
                self.layout_widget(widget, child, layout)

                if isinstance(widget, (tk.Frame, tk.Canvas)):
                    child_layout = child.attrib.get('layout', layout).lower()
                    self.create_widgets(child, widget, child_layout)

    def configure_grid(self, parent, element):
        row_weights = element.attrib.get('row_weights', '').split(',')
        col_weights = element.attrib.get('col_weights', '').split(',')

        for row, weight in enumerate(row_weights):
            try:
                weight = int(weight)
                parent.rowconfigure(row, weight=weight)
            except ValueError:
                pass

        for col, weight in enumerate(col_weights):
            try:
                weight = int(weight)
                parent.columnconfigure(col, weight=weight)
            except ValueError:
                pass

    def create_widget(self, element : ET.Element, parent):
        widget_type = element.tag.lower()
        widget = None
        name = element.attrib.get('name', None)

        widget = self.widget_resolver.resolve(element, parent)

        bind_var = element.attrib.get('bind', None)
        if bind_var:
            bind_var_value = self.get_or_create_variable(bind_var)
            if widget_type == 'label':
                bind_var_value.trace_add('write', lambda *args: self.update_widget(widget, bind_var))
        if name:
            self.tkml_page.named_widgets[name] = widget

        return widget
    
    def layout_widget(self, widget, element, layout):
        if layout == 'grid':
            row = int(element.attrib.get('row', 0))
            column = int(element.attrib.get('column', 0))
            rowspan = int(element.attrib.get('rowspan', 1))
            colspan = int(element.attrib.get('colspan', 1))
            sticky = element.attrib.get('sticky', '')
            widget.grid(row=row, column=column, rowspan=rowspan, columnspan=colspan, sticky=sticky, padx=5, pady=5)
        else:
            fill = element.attrib.get('fill', None)
            expand = element.attrib.get('expand', 'False').lower() == 'true'
            if fill:
                widget.pack(fill=fill, expand=expand, padx=5, pady=5)
            else:
                widget.pack(padx=5, pady=5)

    def update_widget(self, widget, var_name):
        widget.config(text=self.get_or_create_variable(var_name).get())
    
    def get_or_create_variable(self, var_name, type, default_value):
        if not var_name:
            return None
        if not hasattr(self.tkml_page, var_name):
            setattr(self.tkml_page, var_name, type(value=default_value, master=self.tkml_page.root))
        return getattr(self.tkml_page, var_name)

    def is_bind(self, element, attribute):
        content = element.attrib.get(attribute, '')
        return re.match(r'^\{\s*Binding\s+\w+\s*\}$', content)
    
    def get_bind_name(self, element, attribute):
        content = element.attrib.get(attribute, '')
        match = re.match(r'^\{\s*Binding\s+(\w+)\s*\}$', content)
        if match:
            return match.group(1)
        return None

    def handle_bindable_attribute_variable(self, element, widget, attribute, type, default_value) -> tk.Variable:
        bind_var = None
        if self.is_bind(element, attribute):
            bind_name = self.get_bind_name(element, attribute)
            bind_var = self.get_or_create_variable(bind_name, type, default_value)
        else:
            value = element.attrib.get(attribute, default_value)
            if type == ArrayVar:
                value = value.split(",")
                if value == ['']:
                    value = []
            bind_var = self.get_or_create_variable(str(widget.winfo_id()) + "." + attribute, type, value)
        return bind_var
