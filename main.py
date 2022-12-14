import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QLineEdit, QTableWidgetItem, \
    QDateEdit
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from forms.py.mainWindow import Ui_MainWindow
from forms.py.loginWindow import Ui_Dialog
from forms.py.UserTableWindow import Ui_UserTable
from forms.py.InsertWindow import Ui_Dialog as UI_Insert_Window
from forms.py.registrationWindow import Ui_RegistrationWindow
from PyQt5.QtCore import pyqtSlot, Qt, QTimer

import sqlite3

from db import DB

ice_hockey_bd = DB("ice-hockey_player.db")
# Form, Window = uic.loadUiType("dialog.ui")
#
# app = QApplication([])
# window = Window()
# form = Form()
# form.setupUi(window)
# window.show()
# app.exec()

# class Widget(QMainWindow):
#
#     def __init__(self):
#         super().__init__()
#         uic.loadUi("mainWindow.ui", self)


class MainWindow(QMainWindow, QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton.clicked.connect(self.open_login_form)

        self.ui.close_button.clicked.connect(self.close_window)

    def open_login_form(self):
        widget.setCurrentWidget(login_window)



    def close_window(self):
        self.hide()
        self.close()


class LoginWindow(QMainWindow, QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.password_field.setEchoMode(QLineEdit.Password)
        self.ui.logIn_button.clicked.connect(self.login_function)
        self.ui.back_to_main_window.clicked.connect(self.back_to_main_window)

    def login_function(self):
        username = self.ui.username_field.text()
        password = self.ui.password_field.text()

        if len(username) == 0 or len(password) == 0:
            self.ui.error_field.setText("Please input all fields")

        else:
            user_pass = ice_hockey_bd.get_user_password_by_username(username)
            if user_pass is None:
                self.ui.error_field.setText("User didn't find")
            else:
                if user_pass[2] == password:
                    if user_pass[3] == 'False':
                        self.ui.username_field.clear()
                        self.ui.password_field.clear()
                        self.ui.error_field.clear()
                        widget.setCurrentWidget(user_window)
                    else:
                        self.ui.username_field.clear()
                        self.ui.password_field.clear()
                        self.ui.error_field.clear()
                        widget.setCurrentWidget(admin_window)
                else:
                    self.ui.error_field.setText("Invalid username or password")

    def back_to_main_window(self):
        widget.setCurrentWidget(main_window)


class RegisterUserWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RegistrationWindow()
        self.ui.setupUi(self)
        self.ui.password1_field.setEchoMode(QLineEdit.Password)
        self.ui.password2_field.setEchoMode(QLineEdit.Password)
        self.ui.register_user_button.clicked.connect(self.register_function)
        self.ui.back_to_main_window.clicked.connect(self.back_to_main_window)

    def register_function(self):

        username = self.ui.username_field.text()
        password1 = self.ui.password1_field.text()
        password2 = self.ui.password2_field.text()
        is_superuser = self.ui.check_is_superuser.isChecked()

        if len(username) == 0 or len(password1) == 0 or len(password2) == 0:
            self.ui.error_field.setText("Please input all fields")
        else:
            if password2 != password1:
                self.ui.error_field.setText("Passwords don't match")
            elif password2 == password1:
                ice_hockey_bd.add_new_user(username, password1, bool(is_superuser))
                self.ui.username_field.clear()
                self.ui.password1_field.clear()
                self.ui.password2_field.clear()
                self.ui.error_field.clear()
                widget.setCurrentWidget(admin_window)

    def back_to_main_window(self):
        widget.setCurrentWidget(admin_window)


class UserTableWindow(QDialog):
    def __init__(self):
        super(UserTableWindow, self).__init__()
        loadUi("UserTableWindow.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.top_fife_player_button.clicked.connect(self.get_top_fife_player)
        self.player_list_button.clicked.connect(self.get_player_list_button)
        self.logout_button.clicked.connect(self.logout)
        self.sorting_button.clicked.connect(self.click_sorting_button)
        self.find_player_field.returnPressed.connect(self.get_find_player)
        #self.tableWidget.doubleClicked.connect(self.current_row)

        self.load_data()

    def get_find_player(self):
        self.tableWidget.setRowCount(0)
        player_name = self.find_player_field.text()
        player = ice_hockey_bd.get_player_by_name(player_name)
        self.find_player_field.clear()
        self.tableWidget.setRowCount(1)
        if player is not None:
            self.tableWidget.setItem(0, 0, QTableWidgetItem(player[0]))
            self.tableWidget.setItem(0, 1, QTableWidgetItem(player[1]))
            self.tableWidget.setItem(0, 2, QTableWidgetItem(str(player[2])))
            self.tableWidget.setItem(0, 3, QTableWidgetItem(str(player[3])))
            self.tableWidget.setItem(0, 4, QTableWidgetItem(str(player[4])))
            self.tableWidget.setItem(0, 5, QTableWidgetItem(str(player[5])))
            self.tableWidget.setItem(0, 6, QTableWidgetItem(str(player[6])))

    def click_sorting_button(self):

        self.tableWidget.setRowCount(0)
        param_sorting = self.comboBox.currentText()
        sorted_list_player = ice_hockey_bd.get_sorting_player_list(param_sorting)
        print(sorted_list_player)
        tablerow = 0
        self.tableWidget.setRowCount(len(sorted_list_player))
        print()
        print("sorting list")
        for player in sorted_list_player:
            print(player)
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(player[0]))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(player[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(str(player[2])))
            self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(str(player[3])))
            self.tableWidget.setItem(tablerow, 4, QTableWidgetItem(str(player[4])))
            self.tableWidget.setItem(tablerow, 5, QTableWidgetItem(str(player[5])))
            self.tableWidget.setItem(tablerow, 6, QTableWidgetItem(str(player[6])))
            tablerow += 1
    def get_top_fife_player(self):
        self.tableWidget.setRowCount(0)
        top_fife_players = ice_hockey_bd.get_top_fife_players()
        tablerow = 0
        self.tableWidget.setRowCount(5)
        for player in top_fife_players:
            print(player)
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(player[0]))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(player[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(str(player[2])))
            self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(str(player[3])))
            self.tableWidget.setItem(tablerow, 4, QTableWidgetItem(str(player[4])))
            self.tableWidget.setItem(tablerow, 5, QTableWidgetItem(str(player[5])))
            self.tableWidget.setItem(tablerow, 6, QTableWidgetItem(str(player[6])))
            tablerow += 1

    def load_data(self):
        players_information = ice_hockey_bd.get_information_about_players()
        tablerow = 0
        self.tableWidget.setRowCount(len(players_information))
        for player in players_information:
            print(player)
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(player[0]))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(player[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(str(player[2])))
            self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(str(player[3])))
            self.tableWidget.setItem(tablerow, 4, QTableWidgetItem(str(player[4])))
            self.tableWidget.setItem(tablerow, 5, QTableWidgetItem(str(player[5])))
            self.tableWidget.setItem(tablerow, 6, QTableWidgetItem(str(player[6])))
            tablerow += 1

    def get_player_list_button(self):
        players_information = ice_hockey_bd.get_information_about_players()
        tablerow = 0
        self.tableWidget.setRowCount(len(players_information))
        for player in players_information:
            print(player)
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(player[0]))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(player[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(str(player[2])))
            self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(str(player[3])))
            self.tableWidget.setItem(tablerow, 4, QTableWidgetItem(str(player[4])))
            self.tableWidget.setItem(tablerow, 5, QTableWidgetItem(str(player[5])))
            self.tableWidget.setItem(tablerow, 6, QTableWidgetItem(str(player[6])))
            tablerow += 1

    def logout(self):
        widget.setCurrentWidget(main_window)


class AdminTableWindow(QDialog):
    def __init__(self):
        super(AdminTableWindow, self).__init__()
        loadUi("AdminTableWindow.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.add_player_button.clicked.connect(self.click_add_player_button)
        self.logout_button.clicked.connect(self.logout)
        self.load_data()

        self.tableWidget.doubleClicked.connect(self.get_double_click_item)
        self.tableWidget.itemChanged.connect(self.get_change_item)
        self.tableWidget.itemClicked.connect(self.get_clicked_item)
        self.update_table_button.clicked.connect(self.get_player_list_button)
        self.delete_player_button.clicked.connect(self.delete_player)
        self.register_button.clicked.connect(self.open_register_form)
        self.delete_account_window_button.clicked.connect(self.open_delete_user_form)
        #self.delete_player_button.clicked.connect(self.delete_player_button)

        self.double_click_item = ()
        self.double_click_player_name = ''
        self.change_item = ()
        self.clicked_item_to_delete = ''

    def load_data(self):
        players_information = ice_hockey_bd.get_information_about_players()
        tablerow = 0
        self.tableWidget.setRowCount(len(players_information))
        for player in players_information:
            print(player)
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(player[0]))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(player[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(str(player[2])))
            self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(str(player[3])))
            self.tableWidget.setItem(tablerow, 4, QTableWidgetItem(str(player[4])))
            self.tableWidget.setItem(tablerow, 5, QTableWidgetItem(str(player[5])))
            self.tableWidget.setItem(tablerow, 6, QTableWidgetItem(str(player[6])))
            tablerow += 1

    def open_delete_user_form(self):
        widget.setCurrentWidget(delete_user_window)

    def click_add_player_button(self):
        widget.setCurrentWidget(add_player_window)

    def get_double_click_item(self, item):
        print(10)
        row, column = item.row(), item.column()
        self.double_click_item = (row, column)
        self.double_click_player_name = self.tableWidget.item(row, 0).text()

    def open_register_form(self):

        widget.setCurrentWidget(register_window)

    def get_change_item(self, item):
        row, column = item.row(), item.column()
        self.change_item = (row, column)

        changed_information = item.text()
        changed_database_field = self.tableWidget.horizontalHeaderItem(column).text()
        print(changed_database_field)
        if self.double_click_item == self.change_item:
            ice_hockey_bd.update_player(player_name=self.double_click_player_name,
                                        change_field=changed_database_field.lower(),
                                        change_information=changed_information)

    def get_player_list_button(self):
        players_information = ice_hockey_bd.get_information_about_players()
        tablerow = 0
        self.tableWidget.setRowCount(len(players_information))
        for player in players_information:
            print(player)
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(player[0]))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(player[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(str(player[2])))
            self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(str(player[3])))
            self.tableWidget.setItem(tablerow, 4, QTableWidgetItem(str(player[4])))
            self.tableWidget.setItem(tablerow, 5, QTableWidgetItem(str(player[5])))
            self.tableWidget.setItem(tablerow, 6, QTableWidgetItem(str(player[6])))
            tablerow += 1

    def get_clicked_item(self, item):
        player_name = self.tableWidget.item(item.row(), 0).text()
        self.clicked_item_to_delete = player_name

    def delete_player(self):
        player_name = self.clicked_item_to_delete
        ice_hockey_bd.delete_player(player_name)

    def logout(self):
        widget.setCurrentWidget(main_window)


class AddPlayerWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = UI_Insert_Window()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #self.ui.birthday_field.setEchoMode(QDateEdit.calendar)
        self.ui.insert_button.clicked.connect(self.add_player)
        self.ui.back_to_admin_window.clicked.connect(self.back_to_admin_window)

    def add_player(self):
        player_name = self.ui.name_field.text()
        player_birthday = self.ui.birthday_field.text()
        add_player_id = ice_hockey_bd.add_new_player(player_name, player_birthday).lastrowid

        statistic_player_game = self.ui.game_field.text()
        statistic_player_goal = self.ui.goal_field.text()
        statistic_player_assists = self.ui.assist_field.text()
        statistic_player_penalty_minutes = self.ui.penalty_minutes_field.text()
        ice_hockey_bd.add_player_statistic(add_player_id, statistic_player_game,
                                           statistic_player_goal, statistic_player_assists,
                                           statistic_player_penalty_minutes)
        self.ui.name_field.clear()
        self.ui.birthday_field.clear()
        self.ui.game_field.clear()
        self.ui.goal_field.clear()
        self.ui.assist_field.clear()
        self.ui.penalty_minutes_field.clear()

        widget.setCurrentWidget(admin_window)

    def back_to_admin_window(self):
        widget.setCurrentWidget(admin_window)


class DeleteUserTableWindow(QDialog):
    def __init__(self):
        super(DeleteUserTableWindow, self).__init__()
        loadUi("DeleteUserTableWindow.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.back_to_admin_window_button.clicked.connect(self.back_to_admin_window)
        self.delete_user_button.clicked.connect(self.delete_user)
        self.tableWidget.itemClicked.connect(self.get_clicked_item)
        self.update_table_button.clicked.connect(self.get_player_list_button)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 220)
        self.load_data()

        self.clicked_item_to_delete = ''

    def load_data(self):
        users = ice_hockey_bd.get_information_about_users()
        tablerow = 0
        self.tableWidget.setRowCount(len(users))
        for user in users:
            print(user)
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(str(user[0])))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(user[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(user[2]))
            tablerow += 1

    def get_player_list_button(self):
        self.tableWidget.setRowCount(0)
        users = ice_hockey_bd.get_information_about_users()
        tablerow = 0
        self.tableWidget.setRowCount(len(users))
        for user in users:
            print(user)
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(str(user[0])))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(user[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(user[2]))
            tablerow += 1

    def get_clicked_item(self, item):
        user_id = self.tableWidget.item(item.row(), 0).text()
        print(user_id)
        self.clicked_item_to_delete = user_id

    def delete_user(self):
        user_id = self.clicked_item_to_delete
        ice_hockey_bd.delete_user(user_id)

    def back_to_admin_window(self):
        widget.setCurrentWidget(admin_window)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    main_window = MainWindow()
    login_window = LoginWindow()
    register_window = RegisterUserWindow()
    user_window = UserTableWindow()
    admin_window = AdminTableWindow()
    add_player_window = AddPlayerWindow()
    delete_user_window = DeleteUserTableWindow()

    widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    widget.setFixedHeight(500)
    widget.setFixedWidth(750)

    widget.addWidget(main_window)
    widget.addWidget(login_window)
    widget.addWidget(register_window)
    widget.addWidget(user_window)
    widget.addWidget(admin_window)
    widget.addWidget(add_player_window)
    widget.addWidget(delete_user_window)

    widget.setCurrentWidget(main_window)
    widget.show()

    sys.exit(app.exec_())
