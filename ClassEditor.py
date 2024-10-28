from ComboDialog import ComboDialog, DialogResult
from DataManager import DataManager
from tkml import ArrayVar, TkmlPage
from classes import Property, Instance, Class
import tkinter as tk
from tkinter import messagebox, simpledialog

class ClassEditor(TkmlPage):
    def __init__(self, parent, _class : Class, data_manager : DataManager):
        super().__init__(parent=parent) 
        self._class = _class
        self.data_manager = data_manager
        self.properties = ArrayVar(value=self._class.properties if self._class else [], transform=lambda prop: f"{prop.id_property} ({prop.type})")
        self.linked_classes = ArrayVar(value=self._class.connected_classes if self._class else [])
        self.classe = tk.StringVar(value=self._class.classe if self._class else "")
        self.selected_property_index = tk.IntVar(value=-1)
        self.selected_class_index = tk.IntVar(value=-1)

    def get_tkml(self):
        return """
        <Window title="Éditeur de Classe" width="600" height="400" layout="grid" row_weights="1,0,0" col_weights="1,1">
            <Label text="Nom de la Classe :" row="0" column="0" sticky="w" />
            <Entry value="{Binding classe}" row="0" column="1" sticky="ew" />

            <!-- Listbox des Propriétés -->
            <Label text="Propriétés:" row="1" column="0" sticky="w" />
            <Listbox name="lb_properties" values="{Binding properties}" selected_index="{Binding selected_property_index}"
                row="2" column="0" sticky="nsew" />

            <!-- Section Classes Liées -->
            <Label text="Classes Liées:" row="1" column="1" sticky="w" />
            <Listbox name="lb_classes" values="{Binding linked_classes}" selected_index="{Binding selected_class_index}" 
                row="2" column="1" sticky="nsew" />

            <!-- Boutons -->
            <Frame row="3" column="0" sticky="ew" layout="grid">
                <Button text="Ajouter Propriété" command="add_property" row="0" column="0" />
                <Button text="Supprimer Propriété" command="delete_property" row="1" column="0" />
            </Frame>
            
            <Frame row="3" column="1" sticky="ew" layout="grid">
                <Button text="Ajouter Classe" command="add_linked_class" row="0" column="0" />
                <Button text="Supprimer Classe" command="remove_linked_class" row="1" column="0" />
            </Frame>
            <Button text="Sauvegarder" row="4" column="1" command="save" />

        </Window>
        """

    def add_property(self):
        prop_name = simpledialog.askstring("Nouvelle propriété", "Entrez le nom de la propriété:")
        type_dialog = ComboDialog(
            title="Type de propriété",
            text="Sélectionnez le type de la propriété:",
            items=["int", "str", "float", "bool"], 
        )
        type_dialog.show()
        if type_dialog.result != DialogResult.OK:
            return
        prop_type = type_dialog.selected_item.get()
        if prop_name and prop_type:
            new_property = Property(prop_name, prop_type)
            self.properties.append(new_property)

    def delete_property(self):
        if self.selected_property_index.get() == -1:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une propriété à supprimer.")
            return
        self.properties.pop(self.selected_property_index.get())
        self.selected_property_index.set(-1)

    def add_linked_class(self):
        classes = set()
        for instance in self.data_manager.instances:
            if instance.classe not in self._class.connected_classes:
                classes.add(instance.classe)

        if len(classes) == 0:
            messagebox.showwarning("Aucune classe", "Toutes les classes sont déjà liées.")
            return
        
        dialog = ComboDialog(
            title="Choix de la classe liée",
            text="Sélectionnez une classe liée:",
            items=list(classes), 
        )
        
        dialog.show()
        
        if dialog.selected_index.get() == -1:
            print("Annulé")
            return
        
        print("Sélectionné:", dialog.selected_item.get())

        class_name = dialog.selected_item.get()
        if class_name:
            self.linked_classes.append(class_name)
            print("Classes liées:", self.linked_classes.get())

    def remove_linked_class(self):
        if self.selected_class_index.get() == -1:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une classe liée à supprimer.")
            return
        self.linked_classes.pop(self.selected_class_index.get())

    def save(self):
        class_data = Class(
            classe=self.classe.get(),
            connected_classes=self.linked_classes.get(),
            properties=self.properties.get()
        )

        if self._class:
            index = self.data_manager.classes.index(self._class)
            self.data_manager.classes[index] = class_data
        else:
            self.data_manager.classes.append(class_data)

        self.close()
