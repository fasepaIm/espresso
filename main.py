import sys
import sqlite3

from PyQt5 import uic  # Импортируем uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загружаем дизайн
        self.con = sqlite3.connect('coffee.db')
        self.write_to_table()

    def write_to_table(self):
        cur = self.con.cursor()
        result = cur.execute(f"""SELECT * FROM info_about_coffee
                             ORDER BY ID""").fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        header = self.tableWidget.horizontalHeader()
        title = ['ID', 'sorts_name', 'degree_of_roast', 'type_of_coffee',
                 'flavor_description', 'price_rub', 'packing_volume_g']
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.result = []
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for i in range(1, len(title)):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
