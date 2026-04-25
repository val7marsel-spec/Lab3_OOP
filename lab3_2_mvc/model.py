import json
import os

class TripleModel:
    
    def __init__(self):
        self._a = 0
        self._b = 50
        self._c = 100
        self._observers = []
        self._notifications = 0 
        self.load()
    
    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify(self):
        self._notifications += 1
        for observer in self._observers:
            observer.on_model_changed(self._a, self._b, self._c)
    
    def notification_count(self):
        return self._notifications
    
    def setA(self, val):
        if val < 0:
            val = 0
        if val > 100:
            val = 100
        
        self._a = val
        
        if self._b < self._a:
            self._b = self._a
        
        if self._c < self._a:
            self._c = self._a
        
        self._notify()
    
    def setB(self, val):
        if val < self._a or val > self._c:
            return
        
        if self._b == val:
            return
        
        self._b = val
        self._notify()
    
    def setC(self, val):
        if val < 0:
            val = 0
        if val > 100:
            val = 100
        
        self._c = val
        
        if self._b > self._c:
            self._b = self._c
        
        if self._a > self._c:
            self._a = self._c
        
        self._notify()
    
    def getA(self):
        return self._a
    
    def getB(self):
        return self._b
    
    def getC(self):
        return self._c
    
    def save(self):
        data = {
            "A": self._a,
            "B": self._b,
            "C": self._c
        }
        try:
            with open("triple_model.json", 'w') as f:
                json.dump(data, f)
        except:
            pass
    
    def load(self):
        try:
            with open("triple_model.json", 'r') as f:
                data = json.load(f)
                a = data.get("A", 0)
                b = data.get("B", 50)
                c = data.get("C", 100)
                
                if a < 0: a = 0
                if a > 100: a = 100
                if b < 0: b = 0
                if b > 100: b = 100
                if c < 0: c = 0
                if c > 100: c = 100
                
                if a > c:
                    c = a
                
                if b < a: b = a
                if b > c: b = c
                
                changed = (self._a != a) or (self._b != b) or (self._c != c)
                
                self._a = a
                self._b = b
                self._c = c
                
                if changed:
                    self._notify()
        except:
            pass