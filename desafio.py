# Allow access to command-line arguments
import sys

# Import the core and GUI elements of Qt
from PySide.QtCore import *
from PySide.QtGui import *

import sqlite3

# Every Qt application must have one and only one QApplication object;
# it receives the command line arguments passed to the script, as they
# can be used to customize the application's appearance and behavior
qt_app = QApplication(sys.argv)

class Desafio(QWidget):
    ''' The main window inherits from QWidget,
    a convenient widget for an empty window. '''

    def __init__(self):
        # Initialize the object as a QWidget and
        # set its title and minimum width
        QWidget.__init__(self)
        self.setWindowTitle('Show, Image')
        self.setMinimumWidth(400)

        # Create the QVBoxLayout that lays out the whole form
        self.layout = QVBoxLayout()

        # Create the form layout that manages the controls
        self.form_layout = QFormLayout()

        self.pixmap = QPixmap("planet.jpg")

        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)

        self.form_layout.addRow(self.lbl)

        # Create the choose button with its caption
        self.choose_button = QPushButton('Configurations', self)

        # Connect its clicked signal to our slot
        self.choose_button.clicked.connect(lambda: self.clicked_slot())

        self.form_layout.addRow(self.choose_button)

        self.layout.addLayout(self.form_layout)

        # Set the VBox layout as the window's main layout
        self.setLayout(self.layout)

    def run(self):
        # Show the form
        self.show()
        # Run the qt application
        qt_app.exec_()

    def clicked_slot(self):
        if self.layout.count():
            layout = self.layout.takeAt(0)
            self.clearLayout(layout)
            layout.deleteLater()

        # Create the QVBoxLayout that lays out the whole form
        layout = QVBoxLayout()

        # Create the form layout that manages the labeled controls
        self.form_layout2 = QFormLayout()

        # The images that we want to make available
        self.images = ['planet.jpg',
                            'cat.png',
                            'building.jpg']

        # Create and fill the combo box to choose the image
        self.image = QComboBox(self)
        self.image.addItems(self.images)

        # Get a cursor object
        cursor = db.cursor()
        cursor.execute('''SELECT name FROM images WHERE selected = ?''', (1,))
        image1 = cursor.fetchone()

        self.image.setCurrentIndex(self.image.findText(image1[0]))

        # Add it to the form layout with a label
        self.form_layout2.addRow('Select Image:', self.image)

        # Create the choose button with its caption
        self.save_button = QPushButton('Save', self)

        # Connect its clicked signal to our slot
        self.save_button.clicked.connect(lambda: self.saved_slot())

        self.form_layout2.addRow(self.save_button)

        layout.addLayout(self.form_layout2)

        self.layout.insertLayout(0, layout)
        self.layout.setAlignment(Qt.AlignVCenter)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def saved_slot(self):
        if self.layout.count():
            layout = self.layout.takeAt(0)
            self.clearLayout(layout)
            layout.deleteLater()

        # Get a cursor object
        cursor = db.cursor()
        cursor.execute('''UPDATE images SET selected = ?''', (0,))
        cursor.execute('''UPDATE images SET selected = ? WHERE name = ?''', (1, self.images[self.image.currentIndex()],))
        db.commit()

        # Create the QVBoxLayout that lays out the whole form
        layout = QVBoxLayout()

        # Create the form layout that manages the controls
        self.form_layout = QFormLayout()

        # Get a cursor object
        cursor = db.cursor()
        cursor.execute('''SELECT name FROM images WHERE selected = ?''', (1,))
        image1 = cursor.fetchone()

        self.pixmap = QPixmap(image1[0])

        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)

        self.form_layout.addRow(self.lbl)

        # Create the choose button with its caption
        self.choose_button = QPushButton('Configurations', self)

        # Connect its clicked signal to our slot
        self.choose_button.clicked.connect(lambda: self.clicked_slot())

        self.form_layout.addRow(self.choose_button)

        layout.addLayout(self.form_layout)

        self.layout.insertLayout(0, layout)

    def closeEvent(self, event):
        db.close()
        event.accept() # let the window close

# Create a database in RAM
db = sqlite3.connect(':memory:')
# Creates or opens a file called mydb with a SQLite3 DB
db = sqlite3.connect('data/mydb.sqlite')

stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='images' COLLATE NOCASE"
cursor = db.cursor()
cursor.execute(stmt)
result = cursor.fetchone()
if not result:
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''DROP TABLE IF EXISTS images''')
    cursor.execute('''
        CREATE TABLE images(id INTEGER PRIMARY KEY, name TEXT, selected INTEGER)
    ''')

    name1 = "planet.jpg"
    name2 = "cat.png"
    name3 = "building.jpg"

    # Insert image 1
    cursor.execute('''INSERT INTO images(name, selected)
                      VALUES(?, ?)''', (name1, 1))

    # Insert image 2
    cursor.execute('''INSERT INTO images(name, selected)
                      VALUES(?, ?)''', (name2, 0))

    # Insert image 3
    cursor.execute('''INSERT INTO images(name, selected)
                      VALUES(?, ?)''', (name3, 0))

    db.commit()

# Create an instance of the application window and run it
app = Desafio()
app.run()