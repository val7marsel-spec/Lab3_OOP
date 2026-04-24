import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, 
                            QSpinBox, QSlider, QApplication, QGroupBox)
from PyQt5.QtCore import Qt

from model import TripleModel


class TripleView(QMainWindow):
    """Представление для отображения и редактирования трех чисел"""
    
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.model.add_observer(self)
        
        self.update_counter = 0
        
        self.setWindowTitle("MVC - Контроль чисел [A ≤ B ≤ C]")
        self.setGeometry(100, 100, 800, 300)
        
        self.init_ui()
        self.update_display()
    
    def init_ui(self):
        """Создание интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Создаем три группы для A, B, C
        for letter in ['A', 'B', 'C']:
            group = self.create_control_group(letter)
            main_layout.addWidget(group)
    
    def create_control_group(self, letter):
        """Создает группу контролов для одной буквы"""
        group = QGroupBox(f"Число {letter}")
        layout = QVBoxLayout()
        
        # Label
        label = QLabel(f"Значение {letter}:")
        layout.addWidget(label)
        
        # Line Edit (текстовое поле)
        line_edit = QLineEdit()
        line_edit.setObjectName(f"line_{letter}")
        layout.addWidget(line_edit)
        
        # Spin Box
        spin_box = QSpinBox()
        spin_box.setObjectName(f"spin_{letter}")
        spin_box.setRange(0, 100)
        layout.addWidget(spin_box)
        
        # Slider (ползунок)
        slider = QSlider(Qt.Horizontal)
        slider.setObjectName(f"slider_{letter}")
        slider.setRange(0, 100)
        layout.addWidget(slider)
        
        # Текущее значение (для отладки)
        value_label = QLabel(f"Текущее: 0")
        value_label.setObjectName(f"value_{letter}")
        layout.addWidget(value_label)
        
        group.setLayout(layout)
        
        # Сохраняем ссылки на виджеты
        setattr(self, f"line_{letter}", line_edit)
        setattr(self, f"spin_{letter}", spin_box)
        setattr(self, f"slider_{letter}", slider)
        setattr(self, f"value_{letter}", value_label)
        
        # Подключаем сигналы
        line_edit.textChanged.connect(lambda text, l=letter: self.on_text_changed(l, text))
        spin_box.valueChanged.connect(lambda value, l=letter: self.on_spin_changed(l, value))
        slider.valueChanged.connect(lambda value, l=letter: self.on_slider_changed(l, value))
        
        return group
    
    def on_text_changed(self, letter, text):
        """Обработка изменения текстового поля"""
        if letter == 'A':
            self.model.set_a(text)
        elif letter == 'B':
            self.model.set_b(text)
        else:  # C
            self.model.set_c(text)
    
    def on_spin_changed(self, letter, value):
        """Обработка изменения спин-бокса"""
        if letter == 'A':
            self.model.set_a(value)
        elif letter == 'B':
            self.model.set_b(value)
        else:
            self.model.set_c(value)
    
    def on_slider_changed(self, letter, value):
        """Обработка изменения слайдера"""
        if letter == 'A':
            self.model.set_a(value)
        elif letter == 'B':
            self.model.set_b(value)
        else:
            self.model.set_c(value)
    
    def on_model_changed(self, a, b, c):
        """Вызывается моделью при изменении (только одно уведомление)"""
        self.update_counter += 1
        print(f"Обновление #{self.update_counter}: A={a}, B={b}, C={c}")
        self.update_display(a, b, c)
    
    def update_display(self, a=None, b=None, c=None):
        """Обновление всех контролов"""
        if a is None or b is None or c is None:
            a, b, c = self.model.get_values()
        
        # Блокируем сигналы, чтобы избежать рекурсии
        for letter, value in [('A', a), ('B', b), ('C', c)]:
            line = getattr(self, f"line_{letter}")
            spin = getattr(self, f"spin_{letter}")
            slider = getattr(self, f"slider_{letter}")
            label = getattr(self, f"value_{letter}")
            
            line.blockSignals(True)
            spin.blockSignals(True)
            slider.blockSignals(True)
            
            line.setText(str(value))
            spin.setValue(value)
            slider.setValue(value)
            label.setText(f"Текущее: {value}")
            
            line.blockSignals(False)
            spin.blockSignals(False)
            slider.blockSignals(False)
    
    def closeEvent(self, event):
        """При закрытии окна сохраняем данные"""
        self.model.save()
        event.accept()


def main():
    app = QApplication(sys.argv)
    model = TripleModel()
    view = TripleView(model)
    view.show()
    
    print("Приложение запущено. Модель загружена и отправила 1 уведомление.")
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()