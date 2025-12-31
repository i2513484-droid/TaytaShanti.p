import pandas as pd
from conexion import Conexion

class DPersona:
    def __init__(self):
        self.__conexion = Conexion()
        self.__nombre_tabla = "personas"
        self.__crear_tabla()

    def __crear_tabla(self):
        try:
            query = f'''
            CREATE TABLE IF NOT EXISTS {self.__nombre_tabla} (
                docidentidad TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                edad INTEGER NOT NULL,
                telefono TEXT,
                correo TEXT
            )
            '''
            self.__conexion.conectar()
            self.__conexion.ejecutar(query)
            self.__conexion.desconectar()
        except Exception as e:
            print(f"Error al crear tabla: {e}")

    def insertar(self, persona: dict):
        try:
            query = f'''
            INSERT INTO {self.__nombre_tabla} (docidentidad, nombre, edad, telefono, correo)
            VALUES (?, ?, ?, ?, ?)
            '''
            parametros = (
                persona.get('docIdentidad', ''), 
                persona.get('Nombre', ''),
                persona.get('Edad', 0),
                persona.get('Telefono', ''),
                persona.get('Correo', '')
            )
            
            self.__conexion.conectar()
            resultado = self.__conexion.ejecutar(query, parametros)
            self.__conexion.desconectar()
            return resultado > 0
        except Exception as e:
            print(f"Error al insertar persona: {e}")
            return False

    def mostrar(self):
        try:
            query = f"SELECT * FROM {self.__nombre_tabla}"
            self.__conexion.conectar()
            resultado = self.__conexion.consultar(query)
            self.__conexion.desconectar()
            
            if resultado:
                columnas = ['docidentidad', 'Nombre', 'Edad', 'Telefono', 'Correo']
                personas = []
                for fila in resultado:
                    persona_dict = {
                        'docidentidad': fila[0],
                        'Nombre': fila[1],
                        'Edad': fila[2],
                        'Telefono': fila[3],
                        'Correo': fila[4]
                    }
                    personas.append(persona_dict)
                return personas
            return []
        except Exception as e:
            print(f"Error al mostrar personas: {e}")
            return []

    def actualizar(self, persona: dict, docidentidad_original: str):
        try:
            query = f'''
            UPDATE {self.__nombre_tabla} 
            SET docidentidad = ?, nombre = ?, edad = ?, telefono = ?, correo = ?
            WHERE docidentidad = ?
            '''
            parametros = (
                persona.get('docIdentidad', ''),
                persona.get('Nombre', ''),
                persona.get('Edad', 0),
                persona.get('Telefono', ''),
                persona.get('Correo', ''),
                docidentidad_original
            )
            
            self.__conexion.conectar()
            resultado = self.__conexion.ejecutar(query, parametros)
            self.__conexion.desconectar()
            return resultado > 0
        except Exception as e:
            print(f"Error al actualizar persona: {e}")
            return False

    def eliminar(self, docidentidad: str):
        try:
            query = f"DELETE FROM {self.__nombre_tabla} WHERE docidentidad = ?"
            parametros = (docidentidad,)
            
            self.__conexion.conectar()
            resultado = self.__conexion.ejecutar(query, parametros)
            self.__conexion.desconectar()
            return resultado > 0
        except Exception as e:
            print(f"Error al eliminar persona: {e}")
            return False

    def buscar_por_docidentidad(self, docidentidad: str):
        try:
            query = f"SELECT * FROM {self.__nombre_tabla} WHERE docidentidad = ?"
            parametros = (docidentidad,)
            
            self.__conexion.conectar()
            resultado = self.__conexion.consultar(query, parametros)
            self.__conexion.desconectar()
            
            if resultado:
                fila = resultado[0]
                return {
                    'docidentidad': fila[0],
                    'Nombre': fila[1],
                    'Edad': fila[2],
                    'Telefono': fila[3],
                    'Correo': fila[4]
                }
            return None
        except Exception as e:
            print(f"Error al buscar persona: {e}")
            return None
