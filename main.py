import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from cinetrack import Ui_MainWindow
from database import init_db, insert_movie, init_recommendation_data, get_recommendation_based_on_history
from history_window import HistoryWindow

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CineTrack - Welcome")
        self.setFixedSize(1200, 600)
        self.setStyleSheet("background-color: #fff8e1; color: #4e342e;")

        layout = QVBoxLayout()

        logo = QLabel()
        pixmap = QPixmap("logo.png").scaled(400, 400, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(QtCore.Qt.AlignCenter)

        label = QLabel("Welcome to CineTrack")
        label.setStyleSheet("font-size: 28px; font-weight: bold;")
        label.setAlignment(QtCore.Qt.AlignCenter)

        btnStart = QPushButton("Start")
        btnStart.setFixedSize(200, 50)
        btnStart.setStyleSheet("""
            QPushButton {
                background-color: #f9a825;
                color: #4e342e;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #f57f17;
            }
        """)
        btnStart.clicked.connect(self.open_main)

        layout.addWidget(logo)
        layout.addWidget(label)
        layout.addWidget(btnStart, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(layout)

    def open_main(self):
        self.mainWindow = MainApp()
        self.mainWindow.show()
        self.close()

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setStyleSheet("""
            QWidget {
                background-color: #fff8e1;
                color: #4e342e;
                font-size: 20px;
                font-family: Segoe UI, sans-serif;
            }
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #f9a825;
                color: #4e342e;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #f57f17;
            }
            QLineEdit, QComboBox, QTextEdit, QSpinBox {
                background-color: #fff;
                padding: 6px;
                border-radius: 6px;
                font-size: 20px;
                border: 2px solid #f9a825; /* warna kuning terang */
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QSpinBox:focus {
                border: 2px solid #4e342e; /* coklat gelap saat fokus */
            }
        """)


        self.poster_path = ""

        self.ui.btnUploadPoster.clicked.connect(self.upload_poster)
        self.ui.btnSaveMovie.clicked.connect(self.save_movie)
        self.ui.btnRecommend.clicked.connect(self.show_recommendation)

        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.show_about)
        self.ui.actionOpenHistory.triggered.connect(self.open_history)
        self.ui.actionExportCSV.triggered.connect(self.export_csv)
        self.ui.actionDeleteAll.triggered.connect(self.delete_all)

    def upload_poster(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Poster", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.poster_path = path
            pixmap = QPixmap(path).scaled(100, 150)
            self.ui.posterPreview.setPixmap(pixmap)

    def save_movie(self):
        title = self.ui.inputTitle.text()
        genre = self.ui.inputGenre.currentText()
        rating = self.ui.inputRating.value()
        status = self.ui.inputStatus.currentText()
        notes = self.ui.inputNotes.toPlainText()

        if not title.strip():
            QMessageBox.warning(self, "Error", "Title is required.")
            return

        insert_movie(title, genre, rating, status, notes, self.poster_path)
        QMessageBox.information(self, "Saved", "Movie saved successfully!")
        self.ui.inputTitle.clear()
        self.ui.inputNotes.clear()
        self.ui.posterPreview.clear()
        self.poster_path = ""

    def show_about(self):
        QMessageBox.information(self, "About", "CineTrack\n\nCineTrack aplikasi manajemen watchlist film yang memudahkan pengguna mencatat, menyimpan, dan mendapatkan rekomendasi film berdasarkan preferensi genre mereka.\n\nCreated by Cindy Aulia Rahmani (F1D022116)")

    def open_history(self):
        self.historyWindow = HistoryWindow()
        self.historyWindow.show()

    def export_csv(self):
        self.open_history()
        self.historyWindow.export_csv()

    def delete_all(self):
        self.open_history()
        self.historyWindow.clear_all()

    def show_recommendation(self):
        recommendation = get_recommendation_based_on_history()
        if recommendation:
            QMessageBox.information(self, "Recommendation", recommendation)
        else:
            QMessageBox.warning(self, "Not enough data", "You need to save at least 5 movies to get a recommendation.")

if __name__ == "__main__":
    init_db()
    init_recommendation_data()  

    app = QApplication(sys.argv)
    splash = WelcomeScreen()
    splash.show()
    sys.exit(app.exec_())
