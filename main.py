import sys
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt

# Load the UI file
qtcreator_file = os.path.join(os.path.dirname(__file__), "design.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class DesignWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DesignWindow, self).__init__()
        self.setupUi(self)
        
        self.apply_modern_theme()
        
        # Internal state
        self.img_bgr = None
        
        # Connect signals to slots
        self.btn_browse.clicked.connect(self.get_image)
        self.DisplayRedChan.clicked.connect(self.showRedChannel)
        self.DisplayGreenChan.clicked.connect(self.showGreenChannel)
        self.DisplayBlueChan.clicked.connect(self.showBlueChannel)
        self.DisplayColorHist.clicked.connect(self.show_HistColor)
        self.DisplayGrayImg.clicked.connect(self.show_UpdatedImgGray)
        self.DisplayGrayHist.clicked.connect(self.show_HistGray)
        
        # Creative Filters
        self.btn_edge.clicked.connect(self.applyEdgeDetection)
        self.btn_blur.clicked.connect(self.applyBlur)
        self.btn_negative.clicked.connect(self.applyNegative)
        self.btn_sepia.clicked.connect(self.applySepia)
        
    def apply_modern_theme(self):
        # A sleek dark theme for a "Creative App" feel
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #e0e0e0;
                font-weight: bold;
            }
            QGroupBox {
                border: 2px solid #3d3d3d;
                border-radius: 8px;
                margin-top: 20px;
                color: #4da6ff;
                font-size: 14px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #0d47a1;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #002171;
            }
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
                background-color: #333333;
            }
            QTabBar::tab {
                background: #1e1e1e;
                color: #a0a0a0;
                padding: 10px 20px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #333333;
                color: #ffffff;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
        """)

    def show_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Erreur")
        msg.setInformativeText(message)
        msg.setWindowTitle("Erreur")
        msg.exec_()
        
    def convert_cv_qt(self, cv_image):
        """Convertit une image OpenCV au format QPixmap"""
        if len(cv_image.shape) == 3:
            h, w, ch = cv_image.shape
            bytes_per_line = ch * w
            cv_image_Qt_format = QtGui.QImage(cv_image.data, w, h, bytes_per_line, QtGui.QImage.Format_BGR888)
        else:
            h, w = cv_image.shape
            bytes_per_line = w
            cv_image_Qt_format = QtGui.QImage(cv_image.data, w, h, bytes_per_line, QtGui.QImage.Format_Grayscale8)
        
        return QPixmap.fromImage(cv_image_Qt_format)

    def set_scaled_pixmap(self, label, pixmap):
        # Scale pixmap preserving aspect ratio to avoid squishing
        if not pixmap.isNull():
            # Adjust scaling slightly inside the layout so it looks good visually
            scaled_pixmap = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled_pixmap)

    def showDimensions(self):
        if self.img_bgr is not None:
            if len(self.img_bgr.shape) == 3:
                h, w, ch = self.img_bgr.shape
                self.lbl_dimensions.setText(f"{w}x{h} ({ch} canaux)")
            else:
                h, w = self.img_bgr.shape
                self.lbl_dimensions.setText(f"{w}x{h} (Gris)")

    def get_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner une image", "", 
            "Images (*.png *.xpm *.jpg *.jpeg *.bmp);;Tous les fichiers (*)", 
            options=options
        )
        
        if file_path:
            # Handle special characters (like accents) in file paths
            try:
                img_array = np.fromfile(file_path, np.uint8)
                self.img_bgr = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            except Exception as e:
                self.img_bgr = None
                
            if self.img_bgr is None:
                self.show_error(f"Impossible de charger l'image.\nChemin: {file_path}")
                return
            
            pixmap = self.convert_cv_qt(self.img_bgr)
            self.set_scaled_pixmap(self.OriginalImg, pixmap)
            self.showDimensions()
            
            # Clear previous images
            self.RedChannel.setText("Rouge")
            self.GreenChannel.setText("Vert")
            self.BlueChannel.setText("Bleu")
            self.ColorHist.setText("Histogramme Couleur")
            self.GrayImg.setText("Image Niveaux de Gris")
            self.GrayHist.setText("Histogramme Gris")
            self.CreativeImg.setText("Veuillez choisir un effet à gauche.")
            
    def showRedChannel(self):
        if self.img_bgr is not None:
            r_img = np.zeros_like(self.img_bgr)
            r_img[:,:,2] = self.img_bgr[:,:,2]
            pixmap = self.convert_cv_qt(r_img)
            self.set_scaled_pixmap(self.RedChannel, pixmap)
            
    def showGreenChannel(self):
        if self.img_bgr is not None:
            g_img = np.zeros_like(self.img_bgr)
            g_img[:,:,1] = self.img_bgr[:,:,1]
            pixmap = self.convert_cv_qt(g_img)
            self.set_scaled_pixmap(self.GreenChannel, pixmap)

    def showBlueChannel(self):
        if self.img_bgr is not None:
            b_img = np.zeros_like(self.img_bgr)
            b_img[:,:,0] = self.img_bgr[:,:,0]
            pixmap = self.convert_cv_qt(b_img)
            self.set_scaled_pixmap(self.BlueChannel, pixmap)
            
    def show_HistColor(self):
        if self.img_bgr is not None:
            # Set matplotlib dark background to match theme
            plt.style.use('dark_background')
            plt.figure(figsize=(6,4), facecolor='#333333')
            ax = plt.axes()
            ax.set_facecolor('#333333')
            
            colors = ('b', 'g', 'r')
            for i, col in enumerate(colors):
                hist = cv2.calcHist([self.img_bgr], [i], None, [256], [0, 256])
                plt.plot(hist, color=col, linewidth=2)
            
            plt.title('Histogramme Spectrographique RVB', color='#e0e0e0')
            plt.xlim([0,256])
            
            hist_path = os.path.join(os.path.dirname(__file__), 'Color_Histogram.png')
            plt.savefig(hist_path, bbox_inches='tight')
            plt.close()
            
            pixmap = QPixmap(hist_path)
            self.set_scaled_pixmap(self.ColorHist, pixmap)

    def getContrast(self):
        try:
            return float(self.Contrast.text())
        except ValueError:
            self.show_error("Veuillez entrer une valeur numérique valide pour le contraste.")
            return 1.0

    def getBrightness(self):
        try:
            return float(self.Brightness.text())
        except ValueError:
            self.show_error("Veuillez entrer une valeur numérique valide pour la brillance.")
            return 0.0

    def show_UpdatedImgGray(self):
        if self.img_bgr is not None:
            alpha = self.getContrast()
            beta = self.getBrightness()
            
            img_updated = cv2.convertScaleAbs(self.img_bgr, alpha=alpha, beta=beta)
            img_gray = cv2.cvtColor(img_updated, cv2.COLOR_BGR2GRAY)
            self.img_gray = img_gray
            
            pixmap = self.convert_cv_qt(img_gray)
            self.set_scaled_pixmap(self.GrayImg, pixmap)

    def calc_HistGray(self):
        if hasattr(self, 'img_gray'):
            hist_gray = cv2.calcHist([self.img_gray], [0], None, [256], [0, 256])
            return hist_gray
        return None

    def show_HistGray(self):
        hist = self.calc_HistGray()
        if hist is not None:
            plt.style.use('dark_background')
            plt.figure(figsize=(6,4), facecolor='#333333')
            ax = plt.axes()
            ax.set_facecolor('#333333')
            
            plt.plot(hist, color='cyan', linewidth=2)
            plt.title("Répartition Luminance (Gris)", color='#e0e0e0')
            plt.xlim([0,256])
            
            hist_path = os.path.join(os.path.dirname(__file__), 'Gray_Histogram.png')
            plt.savefig(hist_path, bbox_inches='tight')
            plt.close()
            
            pixmap = QPixmap(hist_path)
            self.set_scaled_pixmap(self.GrayHist, pixmap)

    # --- CREATIVE FILTERS ---
    
    def applyEdgeDetection(self):
        if self.img_bgr is not None:
            # Canny Edge Detection
            edges = cv2.Canny(self.img_bgr, 100, 200)
            # Create a localized glowing neon effect representation
            edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            # Add some colors to edges to make it "neon"
            edges_bgr[:,:,0] = edges # Blue neon
            edges_bgr[:,:,1] = edges * 0.5 # Purple-ish
            edges_bgr[:,:,2] = edges * 0.8
            
            pixmap = self.convert_cv_qt(edges_bgr)
            self.set_scaled_pixmap(self.CreativeImg, pixmap)
            
    def applyBlur(self):
        if self.img_bgr is not None:
            # Heavy Gaussian Blur for an artistic effect
            blur = cv2.GaussianBlur(self.img_bgr, (25, 25), 0)
            pixmap = self.convert_cv_qt(blur)
            self.set_scaled_pixmap(self.CreativeImg, pixmap)
            
    def applyNegative(self):
        if self.img_bgr is not None:
            # Invert colors
            neg = cv2.bitwise_not(self.img_bgr)
            pixmap = self.convert_cv_qt(neg)
            self.set_scaled_pixmap(self.CreativeImg, pixmap)
            
    def applySepia(self):
        if self.img_bgr is not None:
            # Sepia matrix transformation
            kernel = np.array([[0.272, 0.534, 0.393],
                               [0.349, 0.686, 0.769],
                               [0.393, 0.769, 0.189]])
            sepia = cv2.transform(self.img_bgr, kernel)
            # Normalize to avoid extreme overflow
            sepia = np.clip(sepia, 0, 255).astype(np.uint8)
            pixmap = self.convert_cv_qt(sepia)
            self.set_scaled_pixmap(self.CreativeImg, pixmap)

    # Overriding resizeEvent to keep image aspect ratios responsive to window resize
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Redraw visible stuff to apply scaling gracefully bounds if we wanted.
        # scaledContents = True in ui file generally handles this fine when Ignored size policy is set.
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DesignWindow()
    window.show()
    sys.exit(app.exec_())
