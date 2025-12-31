from capaDatos.dPersona import DPersona

class NPersona:
    def __init__(self):
        self.__dPersona = DPersona()

    def nuevaPersona(self, persona: dict):
        """Registra una nueva persona"""
        try:
            # Validar datos
            self.__validar_persona(persona)
            
            # Verificar si ya existe
            docidentidad = persona.get('docIdentidad', '')
            if self.__dPersona.buscar_por_docidentidad(docidentidad):
                raise Exception(f"Ya existe una persona con documento {docidentidad}")
            
            # Insertar en la base de datos
            if self.__dPersona.insertar(persona):
                return True
            else:
                raise Exception("No se pudo insertar la persona en la base de datos")
            
        except Exception as e:
            raise Exception(f"Error al registrar persona: {e}")

    def mostrarPersonas(self):
        """Obtiene todas las personas"""
        try:
            return self.__dPersona.mostrar()
        except Exception as e:
            raise Exception(f"Error al obtener personas: {e}")

    def actualizarPersonas(self, persona: dict, docidentidad_original: str):
        """Actualiza una persona existente"""
        try:
            # Validar datos
            self.__validar_persona(persona)
            
            # Verificar si el nuevo documento ya existe (si cambió)
            nuevo_docidentidad = persona.get('docIdentidad', '')
            if nuevo_docidentidad != docidentidad_original:
                if self.__dPersona.buscar_por_docidentidad(nuevo_docidentidad):
                    raise Exception(f"Ya existe una persona con documento {nuevo_docidentidad}")
            
            # Actualizar en la base de datos
            if self.__dPersona.actualizar(persona, docidentidad_original):
                return True
            else:
                raise Exception("No se pudo actualizar la persona en la base de datos")
            
        except Exception as e:
            raise Exception(f"Error al actualizar persona: {e}")

    def eliminarPersona(self, docidentidad: str):
        """Elimina una persona por documento de identidad"""
        try:
            if not docidentidad:
                raise Exception("Documento de identidad es requerido")
            
            if self.__dPersona.eliminar(docidentidad):
                return True
            else:
                raise Exception("No se pudo eliminar la persona de la base de datos")
            
        except Exception as e:
            raise Exception(f"Error al eliminar persona: {e}")

    def __validar_persona(self, persona: dict):
        """Valida los datos de una persona"""
        # Verificar campos obligatorios
        campos_obligatorios = ['docIdentidad', 'Nombre', 'Edad']
        for campo in campos_obligatorios:
            if campo not in persona or not str(persona[campo]).strip():
                raise Exception(f"Campo '{campo}' es requerido")
        
        # Validar documento de identidad
        docidentidad = str(persona['docIdentidad']).strip()
        if not docidentidad.isdigit():
            raise Exception("Documento de identidad debe contener solo números")
        
        # Validar edad
        edad = persona['Edad']
        if not isinstance(edad, int) or edad < 0 or edad > 150:
            raise Exception("Edad debe ser un número entre 0 y 150")
        
        # Validar teléfono (opcional)
        telefono = persona.get('Telefono', '')
        if telefono and not str(telefono).strip().isdigit():
            raise Exception("Teléfono debe contener solo números")
        
        # Validar correo (opcional)
        correo = persona.get('Correo', '')
        if correo and '@' not in correo:
            raise Exception("Correo electrónico no válido")
