import time

class Programador:
    
    __dias_semana_validos = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    def __init__(self, dispositivo):
        if not (hasattr(dispositivo, 'encender') and hasattr(dispositivo, 'apagar')):
            raise TypeError("El dispositivo no tiene los métodos 'encender' o 'apagar' requeridos.")
            
        self.__dispositivo = dispositivo
        self.__horario = {}

    @classmethod
    def get_dias_semana_validos(cls):
        return cls.__dias_semana_validos

    @classmethod
    def get_hora_actual(cls):
        now = time.localtime()
        try:
            dia_str = cls.__dias_semana_validos[now.tm_wday]
        except IndexError:
            dia_str = "Desconocido"
        hora_formateada = f"{now.tm_hour:02}:{now.tm_min:02}:{now.tm_sec:02}"
        return f"{dia_str} {hora_formateada}"

    def __validar_dia(self, dia_semana):
        return dia_semana in self.__dias_semana_validos

    def comienzo(self, dia_semana, hora):
        if not self.__validar_dia(dia_semana):
            print(f"Error: '{dia_semana}' no es un día válido.")
            return
        if dia_semana not in self.__horario:
            self.__horario[dia_semana] = {}
        self.__horario[dia_semana][hora] = "encender"
        print(f"Programado ENCENDIDO para {dia_semana} a las {hora}")

    def fin(self, dia_semana, hora):
        if not self.__validar_dia(dia_semana):
            print(f"Error: '{dia_semana}' no es un día válido.")
            return
        if dia_semana not in self.__horario:
            self.__horario[dia_semana] = {}
        self.__horario[dia_semana][hora] = "apagar"
        print(f"Programado APAGADO para {dia_semana} a las {hora}")

    def borrar(self, dia_semana, hora):
        if dia_semana in self.__horario and hora in self.__horario[dia_semana]:
            accion = self.__horario[dia_semana].pop(hora)
            print(f"Borrada programación de '{accion}' para {dia_semana} a las {hora}")
        else:
            print(f"Error: No hay nada programado para {dia_semana} a las {hora}")
            
    def get_horario(self):
        return self.__horario
        
    def verificar_estado(self):
        now = time.localtime()
        dia_actual = self.__dias_semana_validos[now.tm_wday]
        hora_actual = f"{now.tm_hour:02}:{now.tm_min:02}" 
        
        if dia_actual in self.__horario:
            if hora_actual in self.__horario[dia_actual]:
                accion = self.__horario[dia_actual][hora_actual]
                
                if accion == "encender":
                    self.__dispositivo.encender()
                elif accion == "apagar":
                    self.__dispositivo.apagar()