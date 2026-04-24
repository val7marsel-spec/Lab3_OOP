import json
import os

class TripleModel:
    """Модель для хранения трех чисел с бизнес-правилами"""
    
    CONFIG_FILE = "triple_model.json"
    
    def __init__(self):
        self._a = 0
        self._b = 50
        self._c = 100
        self._observers = []
        self.load()  # загружаем сохраненные значения
    
    def add_observer(self, observer):
        """Подписка на уведомления"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer):
        """Отписка"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self):
        """Уведомление всех подписчиков (только одно уведомление)"""
        for observer in self._observers:
            observer.on_model_changed(self._a, self._b, self._c)
    
    def _enforce_rules(self, old_a, old_b, old_c):
        """Применяет бизнес-правила"""
        # Обеспечиваем A <= B <= C
        if self._a > self._b:
            self._b = self._a
        if self._b > self._c:
            self._c = self._b
        
        # Проверяем границы 0-100
        self._a = max(0, min(100, self._a))
        self._b = max(0, min(100, self._b))
        self._c = max(0, min(100, self._c))
        
        # Уведомляем, только если что-то изменилось
        if old_a != self._a or old_b != self._b or old_c != self._c:
            self._notify_observers()
            self.save()
    
    def set_a(self, value):
        """Установка A (разрешающее поведение)"""
        old_a, old_b, old_c = self._a, self._b, self._c
        
        try:
            val = int(value)
            if 0 <= val <= 100:
                self._a = val
        except:
            pass
        
        self._enforce_rules(old_a, old_b, old_c)
    
    def set_b(self, value):
        """Установка B (запрещающее поведение)"""
        old_a, old_b, old_c = self._a, self._b, self._c
        
        try:
            val = int(value)
            if 0 <= val <= 100 and self._a <= val <= self._c:
                self._b = val
                self._enforce_rules(old_a, old_b, old_c)
            else:
                # Запрещающее поведение - просто не меняем
                # Но все равно уведомляем с текущими значениями (обновить UI)
                if old_b != self._b:
                    self._notify_observers()
        except:
            pass
    
    def set_c(self, value):
        """Установка C (разрешающее поведение)"""
        old_a, old_b, old_c = self._a, self._b, self._c
        
        try:
            val = int(value)
            if 0 <= val <= 100:
                self._c = val
        except:
            pass
        
        self._enforce_rules(old_a, old_b, old_c)
    
    def get_values(self):
        """Возвращает текущие значения"""
        return (self._a, self._b, self._c)
    
    def save(self):
        """Сохранение в файл"""
        data = {
            "a": self._a,
            "b": self._b,
            "c": self._c
        }
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(data, f)
        except:
            pass
    
    def load(self):
        """Загрузка из файла"""
        try:
            with open(self.CONFIG_FILE, 'r') as f:
                data = json.load(f)
                self._a = data.get("a", 0)
                self._b = data.get("b", 50)
                self._c = data.get("c", 100)
                self._enforce_rules(self._a, self._b, self._c)
        except:
            pass