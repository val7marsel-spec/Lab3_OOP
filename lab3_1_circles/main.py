import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, 
                            QStatusBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

from circle import Circle
from storage import Storage


class DrawingArea(QWidget):
    """Область для рисования и управления кругами"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.storage = Storage()
        self.selected_objects = []
        self.setMinimumSize(800, 600)
        self.setMouseTracking(True)
    
    def paintEvent(self, event):
        """Отрисовка всех кругов"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        for circle in self.storage.get_all():
            circle.draw(painter)
    
    def mousePressEvent(self, event):
        """
        ЕДИНЫЙ обработчик кликов мыши
        Здесь происходит И создание, И выделение кругов
        """
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            
            # Ищем круг, по которому кликнули
            clicked_circle = None
            for circle in reversed(self.storage.get_all()):
                if circle.contains(pos.x(), pos.y()):
                    clicked_circle = circle
                    break
            
            if clicked_circle:
                # КЛИК ПО КРУГУ - выделение
                if event.modifiers() == Qt.ControlModifier:
                    # Ctrl + клик: добавляем/убираем выделение
                    if clicked_circle not in self.selected_objects:
                        self.selected_objects.append(clicked_circle)
                        clicked_circle.set_selected(True)
                        print(f"[Selected] Circle, total selected: {len(self.selected_objects)}")
                    else:
                        self.selected_objects.remove(clicked_circle)
                        clicked_circle.set_selected(False)
                        print(f"[Deselected] Circle, selected: {len(self.selected_objects)}")
                else:
                    # Обычный клик: выделяем только этот круг
                    for c in self.selected_objects:
                        c.set_selected(False)
                    self.selected_objects.clear()
                    self.selected_objects.append(clicked_circle)
                    clicked_circle.set_selected(True)
                    print(f"[Selected] Only one circle")
            else:
                # КЛИК ПО ПУСТОМУ МЕСТУ - создаем новый круг
                new_circle = Circle(pos.x(), pos.y())
                self.storage.add(new_circle)
                print(f"[Created] New circle at ({pos.x()}, {pos.y()})")
                
                # Снимаем все выделения при создании нового круга
                for c in self.selected_objects:
                    c.set_selected(False)
                self.selected_objects.clear()
            
            self.update()  # перерисовываем
    
    def delete_selected(self):
        """Удаление выделенных кругов"""
        print(f"\n[Delete] Selected objects: {len(self.selected_objects)}")
        
        for circle in self.selected_objects.copy():
            self.storage.remove(circle)
        
        self.selected_objects.clear()
        self.update()
        print(f"[Delete] Done. Circles left: {self.storage.count()}\n")


class MainWindow(QMainWindow):
    """Главное окно"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Circles - Lab 3.1")
        self.setGeometry(100, 100, 900, 700)
        
        self.drawing_area = DrawingArea()
        self.setCentralWidget(self.drawing_area)
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Click on empty space - create circle | Click on circle - select | Ctrl+click - add to selection | Delete - remove selected")
    
    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        if event.key() == Qt.Key_Delete:
            print("[Key] DELETE pressed")
            self.drawing_area.delete_selected()
        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    print("\n" + "="*60)
    print("INSTRUCTIONS:")
    print("  Click on empty space -> create circle")
    print("  Click on circle -> select it")
    print("  Ctrl + click on circle -> add to selection")
    print("  DELETE -> remove selected circles")
    print("="*60 + "\n")
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()