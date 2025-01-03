import os
import sys
from CONSTANTS import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QFormLayout
from PyQt6.QtGui import QIcon

margin = True
_message_display_window = None
icon_path = os.path.join(os.getcwd(), 'icon')


def message_display_window(window_title, message):
    global _message_display_window
    _message_display_window = QWidget()
    _message_display_window.setWindowTitle(window_title)
    # Set the window icon
    if window_title == 'Error':
        _message_display_window.setWindowIcon(QIcon(os.path.join(icon_path, 'error.png')))
    else:
        _message_display_window.setWindowIcon(QIcon(os.path.join(icon_path, 'printer_icon.png')))

    _message_display_window.setGeometry(100, 100, 280, 80)
    error_msg = QLabel(message, parent=_message_display_window)
    error_msg.move(60, 15)
    _message_display_window.show()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.main_window = MainWindow()

    def init_ui(self):
        # Initialize and configure UI elements
        self.setWindowTitle('3D Printing Cost Calculator')
        # Set the window icon
        self.setWindowIcon(QIcon(os.path.join(icon_path, 'printer_icon.png')))

        # Create QLabel
        start_label = QLabel('\t\t       Hola Amigo\n\nKindly review and update the constants in CONSTANTS.py')

        # Create QPushButton
        start_button = QPushButton("Let's Get Started", self)
        start_button.clicked.connect(self.on_start_button_click)  # noqa

        layout = QVBoxLayout()

        # Create a vertical layout
        layout.addWidget(start_label)
        layout.addWidget(start_button)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_start_button_click(self):
        self.main_window.show()
        self.close()


from PyQt6.QtWidgets import QCheckBox, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.value3 = None
        self.value2 = None
        self.value1 = None
        self.window()

    def window(self):
        # Initialize and configure UI elements
        self.setWindowTitle('3D Printing Cost Calculator')
        # Set the window icon
        self.setWindowIcon(QIcon(os.path.join(icon_path, 'printer_icon.png')))

        # Initialize a form Box layout
        form_box = QFormLayout()
        self.setLayout(form_box)

        # Create a checkbox for margin
        margin_check_box = QCheckBox('Margin', self)
        form_box.addRow(margin_check_box)
        margin_check_box.setChecked(True)
        margin_check_box.stateChanged.connect(self.margin_state_changed)

        label1 = QLabel('Weight (Kgs.gms)')
        self.value1 = QLineEdit()

        label2 = QLabel('Printing time (HH.mm) ')
        self.value2 = QLineEdit()

        label3 = QLabel('Assembly time (HH.mm) ')
        self.value3 = QLineEdit()

        form_box.addRow(label1, self.value1)
        form_box.addRow(label2, self.value2)
        form_box.addRow(label3, self.value3)

        # Create QPushButton
        start_button = QPushButton('Calculate', self)
        form_box.addRow(start_button)

        start_button.clicked.connect(self.on_calculate_button_click)  # noqa

    def on_calculate_button_click(self):
        _weight = None
        _print_time = None
        _assembly_time = None
        try:
            _weight = float(self.value1.text())
            _print_time = float(self.value2.text())
            _assembly_time = float(self.value3.text())

        except ValueError as e:
            message_display_window('Error', 'Enter values in Float and int"')
            print(f'Error Raised as {e}')

        else:
            self.close()
            cost = COST()
            total_cost = cost.calculate_cost(weight_of_material=_weight,
                                             time_to_print=_print_time,
                                             assembly_time=_assembly_time
                                             )
            message_display_window('Result', f'Total Printing cost is : {int(total_cost)}')

    @staticmethod
    def margin_state_changed(state):
        global margin
        if state == 2:
            margin = True
            print('Margin is applied')
        else:
            margin = False
            print('Margin in not added')


class COST:
    # Calculate the total material cost
    @staticmethod
    def material_cost(weight: float, cost_of_spool):
        return weight * cost_of_spool * MATERIAL_CONSTANT

    # Calculate the total labour cost
    @staticmethod
    def labour_charges(time):
        return PRINT_ASSEMBLY_COST * time

    # Calculate the total printer degradation cost
    @staticmethod
    def running_cost(printing_time):
        return printing_time * PRINTER_RUNNING_COST

    # Calculate the total electricity cost
    @staticmethod
    def electricity_cost(printing_time):
        return printing_time * ELECTRICITY_CHARGES

    def calculate_cost(self, weight_of_material, time_to_print, assembly_time):

        # Start the App
        print('Welcome to 3D printing cost calculator:\n')

        if assembly_time != '':
            total_assembly_time = time_validation(float(assembly_time))

        else:
            total_assembly_time = 0

        total_printing_time = time_validation(time_to_print)

        total_cost = self.material_cost(weight_of_material, COST_OF_SPOOL) + self.labour_charges(
            total_assembly_time) + self.running_cost(total_printing_time) + self.electricity_cost(total_printing_time)

        if margin:
            total_cost = total_cost * MARGIN

        return total_cost


def time_validation(time):
    time_hours = int(time)
    if time_hours != 0:
        time_minutes = (round(time % time_hours, 2))
    else:
        time_minutes = time
    time_minutes = time_minutes * 100
    while time_minutes > 60:
        time = int(
            input("Minutes can't be more than 60. Enter the time in given format(HH.mm):\n"))
        time_minutes = (round(time % time_hours, 2)) * 100

    time_minutes = time_minutes / 60

    return time_hours + time_minutes


def main():
    app = QApplication(sys.argv)
    button_window = Window()
    button_window.show()
    app.exec()


if __name__ == "__main__":
    main()
