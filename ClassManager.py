from ComboDialog import ComboDialog
from DataManager import DataManager
from tkml import ArrayVar, TkmlPage
from tkinter import messagebox
from ClassEditor import ClassEditor

class ClassManager(TkmlPage):
    def __init__(self, data_manager : DataManager):
        super().__init__()
        self.data_manager = data_manager
        self.data_manager.load_data()
        self.instances = self.data_manager.instances
        self.classes = ArrayVar(value=self.data_manager.classes, transform=lambda e: e.classe + " - " + e.classe)


    def get_tkml(self):
        return """
        <Window title="Gestion des classes" width="600" height="400" layout="grid" row_weights="1,0" col_weights="1,1">
            <Listbox name="lb_classes" values="{Binding classes}" selected_index="{Binding selected_index}" row="0" column="0" sticky="nsew" />
            <Frame row="0" column="1" sticky="nsew" layout="grid">
                <Button text="Créer" command="on_create" row="0" column="0" />
                <Button text="Modifier" command="on_edit" row="1" column="0" />
                <Button text="Supprimer" command="on_delete" row="2" column="0" />
            </Frame>
        </Window>
        """

    def on_create(self):
        ClassEditor(self.root, None, self.instances, self.classes).show()
        self.data_manager.save_data()

    def on_edit(self):
        if self.selected_index.get() != -1 and not None:
            ClassEditor(self.root, self.classes[self.selected_index.get()], self.data_manager).show()
            self.data_manager.save_data()
        else:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une classe à modifier.")

    def on_delete(self):
        if self.selected_index.get() != -1:
            self.classes.pop(self.selected_index.get())
            self.data_manager.save_data()
        else:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une classe à supprimer.")



app = ClassManager(DataManager())

app.show()