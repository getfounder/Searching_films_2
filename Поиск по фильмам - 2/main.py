import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton
from design import Ui_Form

DATA_BASE = 'films_db.sqlite'
DATA_NAMES = ["year", "title", "duration"]


def filtration(db_name, year, title, duration):
    data_base = sqlite3.connect(db_name)
    sql = data_base.cursor()

    query = f"SELECT * FROM films"

    data = [year, title, duration]

    flag = False

    for x in data:
        if x != '' and not flag:
            flag = True
            query += f" WHERE {DATA_NAMES[data.index(x)]} {x}"
        elif x != '':
            query += f" AND {DATA_NAMES[data.index(x)]} {x}"

    result = sql.execute(query).fetchall()

    return result


class MyWidget(Ui_Form, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.editing_table)
        self.editing_table()

    def editing_table(self):
        year = self.lineEdit.text()
        title = self.lineEdit_2.text()
        duration = self.lineEdit_3.text()

        data = filtration(DATA_BASE, year, title, duration)
        title = ['ID фильма', 'Название фильма', 'Год выпуска', 'Жанр', 'Продолжительность']

        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)

        self.tableWidget.setRowCount(0)

        count = 0

        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            count += 1
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

        self.label_4.setText(f"Найдено записей: {count}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
