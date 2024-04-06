import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QMdiArea, QMdiSubWindow, QTextEdit, QWidget, QLabel, QFileDialog
from PySide6.QtGui import QIcon, QKeySequence
from ui_maindisplay import Ui_MainDisplay
from ui_documentwindow import Ui_Doc_Window
from functools import partial

# Set the class for the SubWindows

class DocumentWindow (QWidget, Ui_Doc_Window):
    def __init__ (self):
        super(). __init__ ()
        self.setupUi(self)
        self.current_file = None # Set initial current_file value for document windo title
        self.saved_content = None # Track saved or unsaved changes
        
    # Create a close event to check unsaved boxes before closing document window with "close button"
        
    def closeEvent (self, event):
        if self.check_unsaved_changes():
            main_display = self.find_main_display()
            if main_display:
                reply = QMessageBox.question(self, "Unsaved Changes", "There are unsaved document changes. Save them before closing?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
                if reply == QMessageBox.Save:
                    main_display.file_save()
                elif reply == QMessageBox.Cancel:
                    event.ignore()
                    return
        event.accept()
        
    # Look for and locate "save_as" method in parent (MainWindow)
        
    def find_main_display (self):
        parent = self.parent()
        while parent:
            if isinstance(parent, MainDisplay):
                return parent
            parent = parent.parent()
        return None
        
    def set_doc_title (self, file_path):
        if file_path:
            file_name = os.path.basename(file_path)
            self.setWindowTitle(f"{file_name}")
        else:
            self.setWindowTitle("Untitled")
            
    def check_unsaved_changes (self): # Check for unsaved document changes before closing
        if self.current_file:
            text_edit = self.textEdit
            current_content = text_edit.toPlainText()
            return current_content != self.saved_content
        else:
            return True
        
# Set the class for the MainWindow

class MainDisplay (QMainWindow, Ui_MainDisplay):
    def __init__ (self, app):
        super(). __init__ ()
        self.setupUi(self)
        self.app = app
        
        # Set Window Title title and icon
        
        self.setWindowTitle("ASO Text Editor")
        self.setWindowIcon(QIcon("C:/Users/wesse/OneDrive\Python - Projects/txt_editor/icons/as_logo.png"))
        
        # Set up the QMdiArea below mainwindow for other widgets
        
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)
        
        # Set up the slots
        
        self.actionExit.triggered.connect(self.quit)
        self.actionCopy.triggered.connect(self.copy)
        self.actionCut.triggered.connect(self.cut)
        self.actionPaste.triggered.connect(self.paste)
        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)
        self.actionAbout.triggered.connect(self.about)
        self.actionAbout_Qt.triggered.connect(self.aboutQt)
        
        # Slots for mananging files
        
        self.actionNew.triggered.connect(self.new_document)
        self.actionOpen.triggered.connect(self.file_open)
        self.actionSave_As.triggered.connect(self.file_save_as)
        self.actionSave.triggered.connect(self.file_save)
        self.actionClose.triggered.connect(self.file_close)
        
        # Create Keyboard Shortcuts
        
        self.actionNew.setShortcut(QKeySequence.New)
        self.actionOpen.setShortcut(QKeySequence.Open)
        self.actionSave.setShortcut(QKeySequence.Save)
        self.actionCut.setShortcut(QKeySequence.Cut)
        self.actionCopy.setShortcut(QKeySequence.Copy)
        self.actionPaste.setShortcut(QKeySequence.Paste)
        
    # Define the function for each slot. Each function, except new, is set to to be triggered by the active subwindow
        
    def quit (self):
        self.app.quit()
    
    def copy (self):
        active_subwindow = self.mdi_area.activeSubWindow()
        if active_subwindow:
            text_edit = active_subwindow.widget().textEdit
            text_edit.copy()
    
    def cut (self):
        active_subwindow = self.mdi_area.activeSubWindow()
        if active_subwindow:
            text_edit = active_subwindow.widget().textEdit
            text_edit.cut()
    
    def paste (self):
        active_subwindow = self.mdi_area.activeSubWindow()
        if active_subwindow:
            text_edit = active_subwindow.widget().textEdit
            text_edit.paste()
    
    def undo (self):
        active_subwindow = self.mdi_area.activeSubWindow()
        if active_subwindow:
            text_edit = active_subwindow.widget().textEdit
            text_edit.undo()
    
    def redo (self):
        active_subwindow = self.mdi_area.activeSubWindow()
        if active_subwindow:
            text_edit = active_subwindow.widget().textEdit
            text_edit.redo()
    
    def about (self):
        QMessageBox.information(self, "About ASO Text Editor", "Autumns Skies Online Personal Text Editor, created with Python and PySide6, ulitilzing the Qt Framework.\n\n" "Designed to showcase the integration of Python with a graphical framework to deploy and run an application with a graphical interface in a Windows environment.\n\n" "Version 1.01  |  (c) 2024-present Autumn Skies Online. All rights reserved.")
    
    def aboutQt (self):
        QApplication.aboutQt()
        
    # Define the functions for the "window" menu item
    
    def window_menu (self):
        self.menuWindow.clear()
        windows = self.mdi_area.subWindowList()
        for window in windows:
            action = self.menuWindow.addAction(window.windowTitle())
            action.triggered.connect(partial(self.activate_subwindow, window))
            
    def activate_subwindow (self, subwindow):
        subwindow.setFocus() # Change the active document window
        
    # Define the functions for working with document files  
        
    def new_document (self):
        self.doc_window = DocumentWindow()
        self.mdi_area.addSubWindow(self.doc_window)
        self.doc_window.show()
        self.window_menu() # Update "window" menu item
        
    def file_open (self):
        open_file, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;  HTML (*.htm);; All Files (*.*)")
        if open_file:
            with open(open_file, "r") as file:
                content = file.read()
            doc_window = DocumentWindow()
            if open_file.endswith(".htm"):
                doc_window.textEdit.setHtml(content)
            else:
                doc_window.textEdit.setPlainText(content)
            doc_window.current_file = open_file
            doc_window.set_doc_title(open_file) # Update document window title
            doc_window.saved_content = content # Update saved_content after saving
            self.mdi_area.addSubWindow(doc_window)
            doc_window.show()
        self.window_menu() # Update "window" menu item
            
    def file_save_as (self):
        doc_window = self.mdi_area.activeSubWindow()
        if doc_window:
            widget = doc_window.widget()
            text_edit = widget.textEdit
            content = text_edit.toPlainText()
            saved_file, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;  HTML (*.htm);; All Files (*.*)")
            if saved_file:
                with open(saved_file, "w") as file:
                    file.write(content)
                widget.current_file = saved_file
        widget.set_doc_title(saved_file) # Update document window title
        self.window_menu() # Update "window" menu item
        
    def file_save (self):
        doc_window = self.mdi_area.activeSubWindow()
        if doc_window:
            text_edit = doc_window.widget().textEdit
            content = text_edit.toPlainText() # Get content from active window
            current_file = getattr(doc_window.widget(), "current_file", None)
            if current_file: # Check if file has alreayd been opened or saved
                with open(current_file, "w") as file:
                        file.write(content)
                doc_window.widget().saved_content = content # Update saved_content after saving
            else:
                self.file_save_as()
        self.window_menu() # Update "window" menu item
                
    def file_close (self):
        active_subwindow = self.mdi_area.activeSubWindow()
        if active_subwindow:
            doc_window = active_subwindow.widget()
            if doc_window.check_unsaved_changes():
                reply = QMessageBox.question(self, "Unsaved Changes", "There are unsaved document changes. Save them before closing?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
                if reply == QMessageBox.Save:
                    self.file_save()
                elif reply == QMessageBox.Discard:
                    active_subwindow.close()
            else:
                active_subwindow.close()
        self.window_menu() # Update "window" menu item
            
        

