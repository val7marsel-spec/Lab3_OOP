"""
Лабораторная работа 3.2 - MVC
Приложение для управления тремя числами A, B, C с правилом A <= B <= C
"""

import sys
import io

# Настройка кодировки для Windows консоли
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from PyQt5.QtWidgets import QApplication
from model import TripleModel
from view import TripleView


def main():
    """Точка входа в приложение"""
    
    # Создаем приложение Qt
    app = QApplication(sys.argv)
    
    # Создаем модель (данные и бизнес-логика)
    model = TripleModel()
    
    # Создаем представление (GUI) и передаем ему модель
    # View автоматически подпишется на уведомления модели
    view = TripleView(model)
    
    # Показываем окно
    view.show()
    
    # Выводим в консоль информацию для отладки (без спецсимволов)
    print("=" * 50)
    print("MVC приложение запущено")
    print("Правило: A <= B <= C")
    print("Поведение:")
    print("  - A и C: разрешающее (B подстраивается)")
    print("  - B: запрещающее (не меняется при нарушении)")
    print("  - Сохранение между запусками: ДА")
    print("=" * 50)
    print("\nЗначения загружены из файла (если есть)")
    print("Ожидается только 1 уведомление модели при старте\n")
    
    # Запускаем цикл обработки событий
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()