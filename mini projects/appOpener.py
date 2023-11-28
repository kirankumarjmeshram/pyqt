import subprocess
import winreg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        # Get the list of all applications
        apps = self.get_apps()

        # Create a button for each application
        for app in apps:
            btn = QPushButton(app, self)
            btn.clicked.connect(lambda _, app=app: self.open_app(app))
            vbox.addWidget(btn)

        self.setLayout(vbox)
        self.setWindowTitle('App Launcher')
        self.show()

    def get_apps(self):
        # This function gets the list of all installed applications from the Windows Registry
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)

        aKey = winreg.OpenKey(aReg, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall")
        count_subkey = winreg.QueryInfoKey(aKey)[0]

        software_list = []
        for i in range(count_subkey):
            software = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, software)
            try:
                display_name = winreg.QueryValueEx(asubkey, "DisplayName")[0]
                software_list.append(display_name)
            except EnvironmentError:
                continue

        winreg.CloseKey(aKey)

        return software_list

    def open_app(self, app):
        # This command opens an application in the background
        # You need to replace this with the actual command to open the application
        subprocess.Popen(app)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
