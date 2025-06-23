from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QMessageBox
import csv
from database import get_all_movies, delete_all_movies

class HistoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie History")
        self.resize(1200, 600)

        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.exportBtn = QPushButton("Export to CSV")
        self.deleteSelectedBtn = QPushButton("Delete Selected")
        self.refreshBtn = QPushButton("Refresh")


        self.layout.addWidget(self.table)
        self.layout.addWidget(self.exportBtn)
        self.layout.addWidget(self.deleteSelectedBtn)
        self.layout.addWidget(self.refreshBtn)

        self.setLayout(self.layout)

        self.exportBtn.clicked.connect(self.export_csv)
        self.deleteSelectedBtn.clicked.connect(self.delete_selected)
        self.refreshBtn.clicked.connect(self.load_data)

        self.setStyleSheet("""
            QWidget {
                background-color: #fff8e1;
                color: #4e342e;
            }
            QTableWidget {
                background-color: #ffffff;
                color: #4e342e;
                gridline-color: #ccc;
                font-size: 18px;
            }
            QHeaderView::section {
                background-color: #f9a825;
                color: #4e342e;
                font-weight: bold;
                padding: 4px;
            }
            QPushButton {
                background-color: #f9a825;
                color: #4e342e;
                border-radius: 6px;
                font-weight: bold;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #f57f17;
            }
        """)

        self.load_data()

    def load_data(self):
        data = get_all_movies()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Genre", "Rating", "Status", "Notes", "Poster"])
        for row_idx, row_data in enumerate(data):
            for col_idx, item in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if path:
            data = get_all_movies()
            with open(path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Title", "Genre", "Rating", "Status", "Notes", "Poster"])
                writer.writerows(data)
            QMessageBox.information(self, "Success", "Data exported successfully.")

    def delete_selected(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Warning", "Please select a movie to delete.")
            return

        row = selected[0].row()
        movie_id = self.table.item(row, 0).text()

        reply = QMessageBox.question(self, "Confirm", f"Delete movie ID {movie_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            from database import delete_movie_by_id
            delete_movie_by_id(movie_id)
            self.load_data()

