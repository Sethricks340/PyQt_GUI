import sys 
import random

from PyQt6.QtWidgets import (QApplication, QMainWindow, 
    QWidget, QPushButton, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QSizePolicy, QSpacerItem, QGridLayout, QStyle, QWidget, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QPalette, QFont, QPixmap, QKeySequence,QShortcut

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CoUGARS_GUI")
        scale = 300  # dev usage for manually scaling the window
        self.resize(QSize(4 * scale, 3 * scale))

        ###This is how the coug info gets into the GUI
        self.feedback_dict = {
            #0->negative, 1->positive, 2->waiting
            #Cougs 1-3 connections
            "Wifi_connections": {1: 0, 2: 1, 3: 2},
            "Radio_connections": {1: 0, 2: 0, 3: 0},
            "Modem_connections": {1: 0, 2: 0, 3: 0},

            #0->negative, 1->positive, 2->waiting
            #Cougs 1-3 sensors
            "Modem_sensors": {1: 0, 2: 0, 3: 0},
            "DVL_sensors": {1: 0, 2: 0, 3: 0},
            "GPS_sensors": {1: 2, 2: 1, 3: 0},
            "IMU_sensors": {1: 0, 2: 0, 3: 0},

            #Cougs 1-3 status messages
            "Status_messages": {1: "", 2: "", 3: ""},

            #Cougs 1-3 last messages
            "Last_messages": {1: "", 2: "", 3: ""}
        }

        #"x" symbol -> SP_DialogNoButton
        #"check" symbol -> SP_DialogYesButton
        # "waiting" symbol -> SP_TitleBarContextHelpButton (for now, probably will change)
        self.icons_dict = {
            0: QStyle.StandardPixmap.SP_DialogNoButton,
            1: QStyle.StandardPixmap.SP_DialogYesButton,
            2: QStyle.StandardPixmap.SP_TitleBarContextHelpButton
        }

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(False)

        #Placeholders for the tabs
        self.tab_dict = {
            "General": [None, QHBoxLayout()],
            "Coug 1": [None, QHBoxLayout()],
            "Coug 2": [None, QHBoxLayout()],
            "Coug 3": [None, QHBoxLayout()]
        }

        #create the widgets from the tab dict, assign layouts, and add each to self.tabs
        for name in self.tab_dict:
            # Create content layout
            content_widget = QWidget()
            content_layout = QVBoxLayout()

            # Main content widget
            content = QWidget()
            content.setLayout(self.tab_dict[name][1])

            # Add line and content to layout
            content_layout.addWidget(self.make_hline())
            content_layout.addWidget(content)

            # Set the combined layout
            content_widget.setLayout(content_layout)
            self.tab_dict[name][0] = content_widget

            # Add to tabs
            self.tabs.addTab(content_widget, name)
            self.set_background(content_widget, "cadetblue")

        self.set_general_page_widgets()

        #Emergency exit GUI button
        self.emergency_exit_gui_button = QPushButton("Close GUI")
        self.emergency_exit_gui_button.clicked.connect(self.close_window)


        #Random data -> for dev till we have data
        self.random_data_button = QPushButton("Random Data Button")
        self.random_data_button.clicked.connect(self.set_random_data)

        #Ctrl+C shortcut to close the window
        shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        shortcut.activated.connect(self.close)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.tabs)
        self.confirm_reject_label = QLabel("Confirmation/Rejection messages from command buttons will appear here")
        self.main_layout.addWidget(self.confirm_reject_label, alignment=Qt.AlignmentFlag.AlignTop)
        self.main_layout.addSpacing(40)
        self.main_layout.addWidget(self.random_data_button)
        self.main_layout.addWidget(self.emergency_exit_gui_button)

        self.container = QWidget()
        self.container.setLayout(self.main_layout)
        self.setCentralWidget(self.container)

    def close_window(self):
        print("closing the window now...")
        self.close()  

    def print_all_widgets_in_layout(self, layout, indent=0):
        spacer = "  " * indent
        for i in range(layout.count()):
            item = layout.itemAt(i)
            
            # If the item is a widget, print its name and class
            widget = item.widget()
            if widget:
                print(f"{spacer}Widget: {widget.objectName()} ({widget.__class__.__name__})")
            
            # If the item is a layout itself, recurse into it
            child_layout = item.layout()
            if child_layout:
                print(f"{spacer}Layout:")
                print_all_widgets_in_layout(child_layout, indent + 1)

    def set_random_data(self):
        print("setting random data...")
        value = random.randint(0,2)
        value1 = random.randint(0,2)

        # self.print_all_widgets_in_layout(self.general_page_C1_layout)

        random_messages = ["running", "no connection", "waiting", "garbage data"]

        for key, value in self.feedback_dict.items():
            if key in ["Status_messages", "Last_messages"]:
                for coug_number, data in value.items():
                    random_int = random.randint(0,3)
                    self.feedback_dict[key][coug_number] = random_messages[random_int]
                    status_color, _ = self.get_status_message_color(random_messages[random_int])
                    new_label = QLabel(random_messages[random_int])
                    layout = getattr(self, f"general_page_C{coug_number}_layout")
                    widget = getattr(self, f"general_page_C{coug_number}_widget")
                    self.replace_label(f"{key}{coug_number}", layout, widget, new_label, color=status_color)
            else:
                for coug_number, data in value.items():
                    random_int = random.randint(0,2)
                    self.feedback_dict[key][coug_number] = random_int
                    prefix = key.split("_")[0]
                    new_label = self.create_icon_and_text(prefix, self.icons_dict[self.feedback_dict[key][coug_number]], self.tab_spacing)
                    layout = getattr(self, f"general_page_C{coug_number}_layout")
                    widget = getattr(self, f"general_page_C{coug_number}_widget")
                    self.replace_label(f"{key}{coug_number}", layout, widget, new_label)

    def replace_label(self, widget_name, parent_layout, parent_widget, new_label, color=""):
        temp_widget = parent_widget.findChild(QWidget, widget_name)
        if temp_widget:
            index = parent_layout.indexOf(temp_widget)
        else:
            print("widget_name not found")
            return

        parent_layout.removeWidget(temp_widget)
        temp_widget.setParent(None)

        # Insert new_label at the same index
        new_label.setObjectName(widget_name)
        new_label.setStyleSheet(f"color: {color};")
        parent_layout.insertWidget(index, new_label)

    def get_status_message_color(self, message):
        if message.lower() == "running": message_color = "green"
        elif message.lower() == "no connection": message_color = "red"
        elif message.lower() == "waiting": message_color = "yellow"
        elif not message: 
            message_color = "orange"
            message = "No message to be read"
        else: 
            message = "Status flag unrecognized: " + message
            message_color = "blue"
        return message_color, message

    "/*Override the resizeEvent method in the sub class*/"
    def resizeEvent(self, event):
        size = self.size()
        width_px = self.width() // 4
        self.resizeTabs(width_px)
        super().resizeEvent(event)  # Call the base class method after doing custom resizing

    "/*resize the tabs according to the width of the window*/"
    def resizeTabs(self, width_px):
        self.tabs.setStyleSheet(f"""
        QTabBar::tab {{
            height: 30px;
            width: {width_px - 15}px;
            font-size: 12pt;
            padding: 5px;
            background: lightgray;  /* background color of non-selected tab */
            color: black;           /* font color of non-selected tab */
        }}
        QTabBar::tab:selected {{
            background: blue;       /* background color of selected tab */
            color: white;           /* font color of selected tab */
            font-weight: bold;
        }}
        """)

    def set_background(self, widget, color):
        palette = widget.palette()
        palette.setColor(widget.backgroundRole(), QColor(color))
        widget.setAutoFillBackground(True)
        widget.setPalette(palette)

    def load_missions_button(self):
        #add load missions logic
        self.confirm_reject_label.setText("Loading the missions...")
        print("Loading the missions...")

    def start_missions_button(self):
        #add start missions logic
        self.confirm_reject_label.setText("Starting the missions...")
        print("Starting the missions...")

    def recallCougs(self):
        #add recall cougs logic
        self.confirm_reject_label.setText("Recalling the Cougs...")
        print("Recalling the Cougs...")
    
    def AbortAllMissions(self):
        #add abort all missions logic
        # print("click", s)

        dlg = AbortMissionsDialog(self)
        if dlg.exec():
            self.confirm_reject_label.setText("Aborting all missions...")
        else:
            self.confirm_reject_label.setText("Canceling abort missions command...")
        print("You pressed the abort all missions button")
    
    def make_vline(self):
        Vline = QFrame()
        Vline.setFrameShape(QFrame.Shape.VLine)
        Vline.setFrameShadow(QFrame.Shadow.Sunken)
        return Vline

    def make_hline(self):
        Hline = QFrame()
        Hline.setFrameShape(QFrame.Shape.HLine)
        Hline.setFrameShadow(QFrame.Shadow.Sunken)
        return Hline

    def set_general_page_widgets(self):
        self.general_page_layout = self.tab_dict["General"][1]

        # Create a container widget and a layout for it
        self.general_page_C0_widget = QWidget()
        self.general_page_C0_layout = QVBoxLayout()
        self.general_page_C0_widget.setLayout(self.general_page_C0_layout)
        
        self.general_page_C1_widget = QWidget()
        self.general_page_C1_layout = QVBoxLayout()
        self.general_page_C1_widget.setLayout(self.general_page_C1_layout)

        self.general_page_C2_widget = QWidget()
        self.general_page_C2_layout = QVBoxLayout()
        self.general_page_C2_widget.setLayout(self.general_page_C2_layout)

        self.general_page_C3_widget = QWidget()
        self.general_page_C3_layout = QVBoxLayout()
        self.general_page_C3_widget.setLayout(self.general_page_C3_layout)

        # Add the container widget to the main layout
        self.general_page_layout.addWidget(self.general_page_C0_widget)
        self.general_page_layout.addWidget(self.make_vline())
        self.general_page_layout.addWidget(self.general_page_C1_widget)
        self.general_page_layout.addWidget(self.make_vline())
        self.general_page_layout.addWidget(self.general_page_C2_widget)
        self.general_page_layout.addWidget(self.make_vline())
        self.general_page_layout.addWidget(self.general_page_C3_widget)

        self.set_general_page_C0_widgets()

        self.set_general_page_column_widgets(self.general_page_C1_layout, 1)
        self.set_general_page_column_widgets(self.general_page_C2_layout, 2)
        self.set_general_page_column_widgets(self.general_page_C3_layout, 3)

    def set_general_page_C0_widgets(self):
        # Create buttons
        self.Load_missions_button = QPushButton("Load Missions")
        self.Load_missions_button.clicked.connect(self.load_missions_button)

        self.Start_missions_button = QPushButton("Start Missions")
        self.Start_missions_button.clicked.connect(self.start_missions_button)

        self.Recall_cougs_button = QPushButton("Recall Cougs")
        self.Recall_cougs_button.clicked.connect(self.recallCougs)

        self.abort_all_missions = QPushButton("Abort All Missions")
        self.abort_all_missions.clicked.connect(self.AbortAllMissions)
        self.abort_all_missions.setStyleSheet("background-color: red; color: black;")

        # Create and style the label
        general_label = QLabel("General Options:")
        general_label.setFont(QFont("Arial", 17, QFont.Weight.Bold))
        general_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        # Add widgets to the layout
        self.general_page_C0_layout.addWidget(general_label, alignment=Qt.AlignmentFlag.AlignTop)
        self.general_page_C0_layout.addSpacing(100)
        self.general_page_C0_layout.addWidget(self.Load_missions_button, alignment=Qt.AlignmentFlag.AlignTop)
        self.general_page_C0_layout.addSpacing(100)

        # Add remaining buttons
        self.general_page_C0_layout.addWidget(self.Start_missions_button)
        self.general_page_C0_layout.addSpacing(100)

        self.general_page_C0_layout.addWidget(self.Recall_cougs_button)
        self.general_page_C0_layout.addSpacing(100)

        # Add spacer to push the rest of the buttons down
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.general_page_C0_layout.addItem(spacer)

        self.general_page_C0_layout.addWidget(self.abort_all_missions)
            
    def set_general_page_column_widgets(self, layout, coug_number):
        # Create and style the header label
        title_label = QLabel(f"Coug {coug_number}:")
        title_label.setFont(QFont("Arial", 17, QFont.Weight.Bold))
        title_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addSpacing(20)

        #"x" symbol -> SP_DialogNoButton
        #"check" symbol -> SP_DialogYesButton
        # "waiting" symbol -> SP_TitleBarContextHelpButton (for now, probably will change)

        #section labels
        section_titles = ["Connections", "Sensors", "Status", "Last Message"]
        for title in section_titles:
            layout.addWidget(QLabel(title, font=QFont("Arial", 15)), alignment=Qt.AlignmentFlag.AlignTop)
            layout.addSpacing(20)
            self.tab_spacing = 75

            match title:
                case "Connections": 
                    wifi_widget = self.create_icon_and_text("Wifi", self.icons_dict[self.feedback_dict["Wifi_connections"][coug_number]], self.tab_spacing)
                    wifi_widget.setObjectName(f"Wifi_connections{coug_number}")
                    layout.addWidget(wifi_widget)
                    layout.addSpacing(20)

                    radio_widget = self.create_icon_and_text("Radio", self.icons_dict[self.feedback_dict["Radio_connections"][coug_number]], self.tab_spacing)
                    radio_widget.setObjectName(f"Radio_connections{coug_number}")
                    layout.addWidget(radio_widget)
                    layout.addSpacing(20)

                    modem_widget = self.create_icon_and_text("Modem", self.icons_dict[self.feedback_dict["Modem_connections"][coug_number]], self.tab_spacing)
                    modem_widget.setObjectName(f"Modem_connections{coug_number}")
                    layout.addWidget(modem_widget)
                    layout.addSpacing(40)

                case "Sensors":

                    modem_sensor_widget = self.create_icon_and_text("Modem", self.icons_dict[self.feedback_dict["Modem_sensors"][coug_number]], self.tab_spacing)
                    modem_sensor_widget.setObjectName(f"Modem_sensors{coug_number}")
                    layout.addWidget(modem_sensor_widget)
                    layout.addSpacing(20)

                    DVL_sensor_widget = self.create_icon_and_text("DVL", self.icons_dict[self.feedback_dict["DVL_sensors"][coug_number]], self.tab_spacing)
                    DVL_sensor_widget.setObjectName(f"DVL_sensors{coug_number}")
                    layout.addWidget(DVL_sensor_widget)
                    layout.addSpacing(20)

                    GPS_sensor_widget = self.create_icon_and_text("GPS", self.icons_dict[self.feedback_dict["GPS_sensors"][coug_number]], self.tab_spacing)
                    GPS_sensor_widget.setObjectName(f"GPS_sensors{coug_number}")
                    layout.addWidget(GPS_sensor_widget)
                    layout.addSpacing(20)
                    
                    IMU_sensor_widget = self.create_icon_and_text("IMU", self.icons_dict[self.feedback_dict["IMU_sensors"][coug_number]], self.tab_spacing)
                    IMU_sensor_widget.setObjectName(f"IMU_sensors{coug_number}")
                    layout.addWidget(IMU_sensor_widget)
                    layout.addSpacing(40)

                case "Status":
                    status = self.feedback_dict["Status_messages"][coug_number]

                    status_color, status = self.get_status_message_color(status)

                    label = QLabel(f"{status}", font=QFont("Arial", 13))
                    label.setObjectName(f"Status_messages{coug_number}")
                    label.setStyleSheet(f"color: {status_color};")  # Change 'red' to any color you want (name, hex, rgb)
                    # label.setIndent(self.tab_spacing)
                    layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignTop)
                    layout.addSpacing(40)

                case "Last Message":
                    last_message = self.feedback_dict["Status_messages"][coug_number]
                    if last_message: 
                        last_mesage_label = QLabel(self.feedback_dict["Last_messages"][coug_number], font=QFont("Arial", 13), alignment=Qt.AlignmentFlag.AlignTop)
                    else:
                        last_mesage_label = QLabel("No messages have been recieved", font=QFont("Arial", 13), alignment=Qt.AlignmentFlag.AlignTop)
                        last_mesage_label.setStyleSheet(f"color: orange;")

                    last_mesage_label.setObjectName(f"Last_messages{coug_number}")
                    
                    # last_mesage_label.setIndent(self.tab_spacing)
                    layout.addWidget(last_mesage_label)
                    layout.addSpacing(40)

        # Add spacer to push content up
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

    def create_icon_and_text(self, text, icon, temp_tab_spacing):
        temp_container = QWidget()
        temp_layout = QHBoxLayout(temp_container)
        temp_layout.setContentsMargins(temp_tab_spacing, 0, 0, 0)
        temp_layout.setSpacing(20)
        icon_label = QLabel()
        icon_label.setPixmap(self.style().standardIcon(icon).pixmap(16, 16))
        icon_label.setContentsMargins(0, 0, 0, 0)
        icon_label.setFixedSize(16, 16)
        text_label = QLabel(text)
        text_label.setFont(QFont("Arial", 13))
        text_label.setContentsMargins(0, 0, 0, 0)
        temp_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        temp_layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        return temp_container

class AbortMissionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Abort Missions?")

        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Change button labels
        ok_button = self.buttonBox.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setText("Accept")

        cancel_button = self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setText("Decline")

        layout = QVBoxLayout()
        message = QLabel("Are you sure that you want to abort all missions?")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

app = QApplication(sys.argv)
window = MainWindow()
window.show()

#can control + c from the terminal
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)  # Allow Ctrl+C to exit

try:
    sys.exit(app.exec())
except KeyboardInterrupt:   #can control + c from GUI
    print("Ctrl+C detected in terminal. Closing app.")