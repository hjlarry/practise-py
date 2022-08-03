import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from login import Ui_MainWindow


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # 添加登录按钮信号和槽
        self.submit_btn.clicked.connect(self.display)

    def display(self):
        username = self.username_input.toPlainText()
        password = self.password_input.toPlainText()
        self.display_area.setText("登录成功!\n" + "用户名是: " + username + ",密码是： " + password)


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())