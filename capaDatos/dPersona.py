from conexion import ConexionDB

class DPersona: 
    def __init__(self):
        self.__db = ConexionDB().conexionSupabase()
        self.__nombreTabla = 'Usuario'
    
    def __ejecutarConsultas(self, consulta, tipoConsulta = None):
        try:
            if tipoConsulta == 'SELECT':            
                resultado = consulta.execute().data 
                return resultado 
            else:
                resultado = consulta.execute()
                return resultado
        except Exception as e:
            return f'Error:{e}'

    def mostrarPersonas(self):
        consulta = self.__db.table(self.__nombreTabla).select('*')
        return self.__ejecutarConsultas(consulta, 'SELECT')

    def nuevaPersona(self, persona: dict):
        print(persona)
        consulta = self.__db.table(self.__nombreTabla).insert(persona)
        return self.__ejecutarConsultas(consulta)
    
    def actualizarPersona(self):
        pass 

    def eliminarPersona(self):
        pass 

