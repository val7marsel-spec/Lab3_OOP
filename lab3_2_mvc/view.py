import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, 
                            QSpinBox, QSlider, QApplication, QGroupBox)
from PyQt5.QtCore import Qt

from model import TripleModel


class TripleView(QMainWindow):
    
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.model.add_observer(self)
        
        self.update_counter = 0
        self._updating = False 
        
        self.setWindowTitle("MVC - Контроль чисел [A ≤ B ≤ C]")
        self.setGeometry(100, 100, 850, 350)
        
        self.init_ui()
        self.update_display()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        for letter in ['A', 'B', 'C']:
            group = self.create_control_group(letter)
            main_layout.addWidget(group)
        
        bottom_layout = QVBoxLayout()
        self.notif_label = QLabel("Уведомлений модели: 0")
        self.notif_label.setStyleSheet("font-size: 14pt; font-weight: bold; margin: 10px;")
        self.notif_label.setAlignment(Qt.AlignCenter)
        bottom_layout.addWidget(self.notif_label)
        
        main_widget = central_widget.layout()
        main_widget.addLayout(bottom_layout)
    
    def create_control_group(self, letter):
        group = QGroupBox(f"Число {letter}")
        layout = QVBoxLayout()
        
        label = QLabel(f"Значение {letter}:")
        layout.addWidget(label)
        
        line_edit = QLineEdit()
        line_edit.setObjectName(f"line_{letter}")
        layout.addWidget(line_edit)
        
        spin_box = QSpinBox()
        spin_box.setObjectName(f"spin_{letter}")
        spin_box.setRange(0, 100)
        layout.addWidget(spin_box)
        
        slider = QSlider(Qt.Horizontal)
        slider.setObjectName(f"slider_{letter}")
        slider.setRange(0, 100)
        layout.addWidget(slider)
        
        group.setLayout(layout)
        
        setattr(self, f"line_{letter}", line_edit)
        setattr(self, f"spin_{letter}", spin_box)
        setattr(self, f"slider_{letter}", slider)
        
        line_edit.editingFinished.connect(lambda l=letter: self.on_editing_finished(l))
        spin_box.valueChanged.connect(lambda value, l=letter: self.on_spin_changed(l, value))
        slider.sliderReleased.connect(lambda l=letter: self.on_slider_released(l))
        slider.valueChanged.connect(lambda value, l=letter: self.on_slider_value_changed(l, value))
        
        return group
    
    def on_editing_finished(self, letter):
        if self._updating:
            return
        
        line = getattr(self, f"line_{letter}")
        try:
            val = int(line.text())
            if letter == 'A':
                self.model.set_a(val)
            elif letter == 'B':
                self.model.set_b(val)
            else:
                self.model.set_c(val)
        except ValueError:
            self.update_display()
    
    def on_spin_changed(self, letter, value):
        if self._updating:
            return
        
        if letter == 'A':
            self.model.set_a(value)
        elif letter == 'B':
            self.model.set_b(value)
        else:
            self.model.set_c(value)
    
    def on_slider_value_changed(self, letter, value):
        if self._updating:
            return
        
        line = getattr(self, f"line_{letter}")
        spin = getattr(self, f"spin_{letter}")
        
        line.blockSignals(True)
        spin.blockSignals(True)
        line.setText(str(value))
        spin.setValue(value)
        line.blockSignals(False)
        spin.blockSignals(False)
    
    def on_slider_released(self, letter):
        if self._updating:
            return
        
        slider = getattr(self, f"slider_{letter}")
        value = slider.value()
        
        if letter == 'A':
            self.model.set_a(value)
        elif letter == 'B':
            self.model.set_b(value)
        else:
            self.model.set_c(value)
    
    def on_model_changed(self, a, b, c):
        self.update_counter += 1
        print(f"Обновление #{self.update_counter}: A={a}, B={b}, C={c}")
        self.update_display(a, b, c)
        
        self.notif_label.setText(f"Уведомлений модели: {self.update_counter}")
    
    def update_display(self, a=None, b=None, c=None):
        if a is None or b is None or c is None:
            a, b, c = self.model.get_values()
        
        self._updating = True
        
        for letter, value in [('A', a), ('B', b), ('C', c)]:
            line = getattr(self, f"line_{letter}")
            spin = getattr(self, f"spin_{letter}")
            slider = getattr(self, f"slider_{letter}")
            
            line.blockSignals(True)
            spin.blockSignals(True)
            slider.blockSignals(True)
            
            line.setText(str(value))
            spin.setValue(value)
            slider.setValue(value)
            
            line.blockSignals(False)
            spin.blockSignals(False)
            slider.blockSignals(False)
        
        self._updating = False
    
    def closeEvent(self, event):
        self.model.save()
        event.accept()


def main():
    app = QApplication(sys.argv)
    model = TripleModel()
    view = TripleView(model)
    view.show()
    
    print("=" * 50)
    print("MVC приложение запущено")
    print("Правило: A <= B <= C")
    print("=" * 50)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()