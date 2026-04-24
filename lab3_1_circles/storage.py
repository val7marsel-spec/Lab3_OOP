class Storage:
    """Контейнер для хранения кругов"""
    
    def __init__(self):
        self.objects = []      # список всех кругов
        self.current_index = -1
    
    def add(self, obj):
        """Добавляет круг"""
        self.objects.append(obj)
        print(f"[Добавлен] Круг в ({obj.x}, {obj.y}), всего: {len(self.objects)}")
    
    def remove(self, obj):
        """
        Удаляет конкретный объект из контейнера
        Важно: удаляет по ссылке на объект
        """
        if obj in self.objects:
            self.objects.remove(obj)
            print(f"[Удален] Круг, осталось: {len(self.objects)}")
            return True
        return False
    
    def remove_at(self, index):
        """Удаляет объект по индексу"""
        if 0 <= index < len(self.objects):
            deleted = self.objects.pop(index)
            print(f"[Удален] Круг по индексу {index}, осталось: {len(self.objects)}")
            return deleted
        return None
    
    def get_all(self):
        """Возвращает список всех кругов"""
        return self.objects
    
    def get_object(self):
        """Возвращает текущий объект (для итерации)"""
        if 0 <= self.current_index < len(self.objects):
            return self.objects[self.current_index]
        return None
    
    def first(self):
        """Переход к первому объекту"""
        self.current_index = 0 if self.objects else -1
    
    def next(self):
        """Переход к следующему объекту"""
        if self.current_index < len(self.objects) - 1:
            self.current_index += 1
        else:
            self.current_index = -1
    
    def eol(self):
        """Проверка конца списка"""
        return self.current_index == -1
    
    def clear(self):
        """Полная очистка контейнера"""
        count = len(self.objects)
        self.objects.clear()
        print(f"[Очистка] Удалено {count} объектов")
        self.current_index = -1
    
    def count(self):
        return len(self.objects)