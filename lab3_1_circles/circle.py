from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt

class Circle:
    """Класс круга"""
    
    RADIUS = 20
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.selected = False
    
    def draw(self, painter):
        """Рисует круг"""
        if self.selected:
            painter.setBrush(QBrush(Qt.red))      # Выделенный - красный
            painter.setPen(QPen(Qt.black, 2))     # Толстая рамка
        else:
            painter.setBrush(QBrush(Qt.blue))     # Обычный - синий
            painter.setPen(QPen(Qt.black, 1))     # Тонкая рамка
        
        painter.drawEllipse(self.x - Circle.RADIUS, 
                           self.y - Circle.RADIUS,
                           Circle.RADIUS * 2, 
                           Circle.RADIUS * 2)
    
    def contains(self, px, py):
        """Проверяет попадание точки в круг"""
        dx = px - self.x
        dy = py - self.y
        return (dx * dx + dy * dy) <= (Circle.RADIUS * Circle.RADIUS)
    
    def set_selected(self, selected):
        """Устанавливает флаг выделения"""
        self.selected = selected
    
    def is_selected(self):
        return self.selected