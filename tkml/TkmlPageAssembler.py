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
            self.tkml_page.root.title(self.resolve_template(root_element.get('title', 'TKML Window')))
            self.tkml_page.root.geometry(f"{root_element.get('width', '300')}x{root_element.get('height', '200')}")
        
        layout = root_element.get('layout', 'pack').lower()
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
                    child_layout = child.get('layout', layout).lower()
                    self.create_widgets(child, widget, child_layout)

    def configure_grid(self, parent, element):
        row_weights = element.get('row_weights', '').split(',')
        col_weights = element.get('col_weights', '').split(',')

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
        name = element.get('name', None)

        widget = self.widget_resolver.resolve(element, parent)

        bind_var = element.get('bind', None)
        if bind_var:
            bind_var_value = self.get_or_create_variable(bind_var)
            if widget_type == 'label':
                bind_var_value.trace_add('write', lambda *args: self.update_widget(widget, bind_var))
        if name:
            setattr(self.tkml_page, name, widget)

        return widget
    
    def layout_widget(self, widget, element, layout):
        if layout == 'grid':
            self.apply_grid_layout(widget, element)
        elif layout == 'place':
            self.apply_place_layout(widget, element)
        else:
            self.apply_pack_layout(widget, element)

    def apply_grid_layout(self, widget, element):
        row = int(element.get('row', 0))
        column = int(element.get('column', 0))
        rowspan = int(element.get('rowspan', 1))
        colspan = int(element.get('colspan', 1))
        sticky = element.get('sticky', '')
        padx = int(element.get('padx', 5))
        pady = int(element.get('pady', 5))
        widget.grid(row=row, column=column, rowspan=rowspan, columnspan=colspan, sticky=sticky, padx=padx, pady=pady)

    def apply_place_layout(self, widget, element):
        x = int(element.get('x', 0))
        y = int(element.get('y', 0))
        width = element.get('width', None)
        height = element.get('height', None)
        relx = float(element.get('relx', 0))
        rely = float(element.get('rely', 0))
        widget.place(x=x, y=y, width=width, height=height, relx=relx, rely=rely)

    def apply_pack_layout(self, widget, element):
        fill = element.get('fill', None)
        expand = element.get('expand', 'False').lower() == 'true'
        side = element.get('side', None)
        padx = int(element.get('padx', 5))
        pady = int(element.get('pady', 5))
        if fill or expand or side:
            widget.pack(fill=fill, expand=expand, side=side, padx=padx, pady=pady)
        else:
            widget.pack(padx=padx, pady=pady)

    def update_widget(self, widget, var_name):
        widget.config(text=self.get_or_create_variable(var_name).get())
    
    def get_or_create_variable(self, var_name, type, default_value):
        if not var_name:
            return None
        if not hasattr(self.tkml_page, var_name):
            setattr(self.tkml_page, var_name, type(value=default_value, master=self.tkml_page.root))
        return getattr(self.tkml_page, var_name)

    def is_bind(self, element, attribute):
        content = element.get(attribute, '')
        return re.match(r'^\{\s*Binding\s+\w+\s*\}$', content)
    
    def get_bind_name(self, element, attribute):
        content = element.get(attribute, '')
        match = re.match(r'^\{\s*Binding\s+(\w+)\s*\}$', content)
        if match:
            return match.group(1)
        return None

    def handle_bindable_attribute_variable(self, element, widget, attribute, type, default_value) -> tk.Variable:
        bind_var = None
        if self.is_bind(element, attribute):
            bind_name = self.get_bind_name(element, attribute)
            if type == ArrayVar:
                default_value = []
            bind_var = self.get_or_create_variable(bind_name, type, default_value)
        else:
            value = element.get(attribute, default_value)
            if type == ArrayVar:
                value = value.split(",")
                if value == ['']:
                    value = []
            bind_var = self.get_or_create_variable(str(widget.winfo_id()) + "." + attribute, type, value)
        return bind_var

    def getComponent(self, name):
        if not hasattr(self.tkml_page, name):
            raise ValueError(f'Component {name} not found in page.')
        return getattr(self.tkml_page, name)
