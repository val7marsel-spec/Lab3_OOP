import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QLineEdit, QSpinBox,
                            QSlider, QGroupBox)
from PyQt5.QtCore import Qt

from model import TripleModel


class MainWindow(QMainWindow):
    
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.model.add_observer(self)
        
        self.setupUi()
        self.connectWidgets()
        self.updateAllFromModel()
        
        self.setWindowTitle("MVC - Контроль чисел [A ≤ B ≤ C]")
        self.resize(800, 500)
        self.setMinimumSize(600, 400)
    
    def setupUi(self):
        central = QWidget(self)
        mainLayout = QVBoxLayout(central)
        
        self.rows = []
        names = ["A", "B", "C"]
        
        for i, name in enumerate(names):
            rowLayout = QHBoxLayout()
            
            label = QLabel(name, self)
            label.setMinimumWidth(30)
            
            line = QLineEdit(self)
            line.setMinimumSize(120, 40)
            line.setStyleSheet("font-size: 16pt;")
            
            spin = QSpinBox(self)
            spin.setRange(0, 100)
            spin.setMinimumSize(100, 40)
            spin.setStyleSheet("font-size: 16pt;")
            
            slider = QSlider(Qt.Horizontal, self)
            slider.setRange(0, 100)
            slider.setMinimumSize(300, 40)
            slider.setStyleSheet("height: 40px;")
            
            rowLayout.addWidget(label)
            rowLayout.addWidget(line, 2)
            rowLayout.addWidget(spin, 1)
            rowLayout.addWidget(slider, 3)
            
            mainLayout.addLayout(rowLayout)
            
            self.rows.append({
                'label': label,
                'line': line,
                'spin': spin,
                'slider': slider
            })
        
        self.lblNotifCount = QLabel(self)
        self.lblNotifCount.setStyleSheet("font-size: 14pt;")
        mainLayout.addWidget(self.lblNotifCount)
        
        self.setCentralWidget(central)
    
    def connectWidgets(self):
        for i, row in enumerate(self.rows):
            row['line'].editingFinished.connect(self.updateFromLineEdit)
            row['spin'].valueChanged.connect(self.updateFromSpinBox)
            row['slider'].valueChanged.connect(self.updateFromSlider)
    
    def updateFromLineEdit(self):
        for i, row in enumerate(self.rows):
            if self.sender() == row['line']:
                try:
                    val = int(row['line'].text())
                    
                    if i == 0:  
                        self.model.setA(val)
                    elif i == 1:  
                        minVal = self.model.getA()
                        maxVal = self.model.getC()
                        if val < minVal:
                            val = minVal
                        if val > maxVal:
                            val = maxVal
                        row['line'].setText(str(val))
                        self.model.setB(val)
                    else:  # C
                        self.model.setC(val)
                except:
                    pass
                break
    
    def updateFromSpinBox(self, val):
        for i, row in enumerate(self.rows):
            if self.sender() == row['spin']:
                if i == 0:  
                    self.model.setA(val)
                elif i == 1: 
                    minVal = self.model.getA()
                    maxVal = self.model.getC()
                    if val < minVal:
                        val = minVal
                    if val > maxVal:
                        val = maxVal
                    row['spin'].setValue(val)
                    self.model.setB(val)
                else: 
                    self.model.setC(val)
                break
    
    def updateFromSlider(self, val):
        for i, row in enumerate(self.rows):
            if self.sender() == row['slider']:
                if i == 0: 
                    self.model.setA(val)
                elif i == 1:
                    minVal = self.model.getA()
                    maxVal = self.model.getC()
                    if val < minVal:
                        val = minVal
                    elif val > maxVal:
                        val = maxVal
                    row['slider'].setValue(val)
                    self.model.setB(val)
                else:  # C
                    self.model.setC(val)
                break
    
    def on_model_changed(self, a, b, c):
        self.updateAllFromModel(a, b, c)
    
    def updateAllFromModel(self, a=None, b=None, c=None):
        if a is None or b is None or c is None:
            a = self.model.getA()
            b = self.model.getB()
            c = self.model.getC()
        
        vals = [a, b, c]
        
        for i, row in enumerate(self.rows):
            row['line'].blockSignals(True)
            row['spin'].blockSignals(True)
            row['slider'].blockSignals(True)
            
            row['line'].setText(str(vals[i]))
            row['spin'].setValue(vals[i])
            row['slider'].setValue(vals[i])
            
            row['line'].blockSignals(False)
            row['spin'].blockSignals(False)
            row['slider'].blockSignals(False)
        
        self.lblNotifCount.setText(
            f"        A <= B <= C       \n\n\nModel notifications: {self.model.notification_count()}"
        )
        
        print(f"Обновление: A={a}, B={b}, C={c}, уведомлений={self.model.notification_count()}")
    
    def closeEvent(self, event):
        if self.model:
            self.model.save()
        event.accept()


def main():
    app = QApplication(sys.argv)
    
    model = TripleModel()
    window = MainWindow(model)
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()