from capaLogica.nPersona import NPersona
import streamlit as st 

class PPersona:
    def __init__(self):
        self.__nPersona = NPersona()
        if 'formularioKey' not in st.session_state:
            st.session_state.formularioKey = 0
        if 'persona_seleccionada' not in st.session_state:
            st.session_state.persona_seleccionada = None  
        if 'docIdentidad_sesion' not in st.session_state:
            st.session_state.docIdentidad_sesion = ''
        if 'nombre_sesion' not in st.session_state:
            st.session_state.nombre_sesion = ''
        if 'edad_sesion' not in st.session_state:
            st.session_state.edad_sesion = 0
        if 'telefono_sesion' not in st.session_state:
            st.session_state.telefono_sesion = ''
        if 'correo_sesion' not in st.session_state:
            st.session_state.correo_sesion = ''
        if 'accion' not in st.session_state:
            st.session_state.accion = 'guardar'
        self.__construirInterfaz()

    def __construirInterfaz(self):
        st.title('Bienvenido a TAYTA SHANTI')

        # Si hay una persona seleccionada para editar, cargar sus datos
        if st.session_state.persona_seleccionada is not None:
            persona = st.session_state.persona_seleccionada
            
            # Aquí está el problema: en mostrarPersonas() obtienes los datos con minúscula 'docidentidad'
            # pero en nuevaPersona usas 'docIdentidad'. Necesitamos manejar ambos casos.
            st.session_state.docIdentidad_sesion = persona.get('docIdentidad', 
                                                               persona.get('docidentidad', ''))
            st.session_state.nombre_sesion = persona.get('Nombre', '')
            st.session_state.edad_sesion = persona.get('Edad', 0)
            st.session_state.telefono_sesion = persona.get('Telefono', '')
            st.session_state.correo_sesion = persona.get('Correo', '')
            st.session_state.accion = 'actualizar'
        
        with st.form(f'FormularioPersona{st.session_state.formularioKey}'):
            txtDocIdentidad = st.text_input('Documento de identidad', 
                                            value=st.session_state.docIdentidad_sesion,
                                            disabled=(st.session_state.accion == 'actualizar'))
            txtNombre = st.text_input('Nombre', value=st.session_state.nombre_sesion)
            txtEdad = st.number_input('Edad', min_value=0, max_value=150, 
                                     value=st.session_state.edad_sesion)
            txtTelefono = st.text_input('Telefono', value=st.session_state.telefono_sesion)
            txtCorreo = st.text_input('Correo', value=st.session_state.correo_sesion)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.session_state.accion == 'actualizar':
                    btnActualizar = st.form_submit_button('Actualizar', type='primary')
                    if btnActualizar:
                        nueva_persona = {
                            'docIdentidad': txtDocIdentidad,
                            'Nombre': txtNombre,
                            'Edad': txtEdad,
                            'Telefono': txtTelefono,
                            'Correo': txtCorreo
                        }
                        # Obtener el docIdentidad original para la actualización
                        doc_original = st.session_state.persona_seleccionada.get('docIdentidad', 
                                                                                st.session_state.persona_seleccionada.get('docidentidad', ''))
                        self.actualizarPersona(nueva_persona, doc_original)
                else:
                    btnGuardar = st.form_submit_button('Guardar', type='primary')
                    if btnGuardar:
                        persona = {
                            'docIdentidad': txtDocIdentidad,
                            'Nombre': txtNombre,
                            'Edad': txtEdad,
                            'Telefono': txtTelefono,
                            'Correo': txtCorreo
                        }
                        self.nuevaPersona(persona)
            
            with col2:
                if st.session_state.accion == 'actualizar':
                    btnCancelar = st.form_submit_button('Cancelar')
                    if btnCancelar:
                        self.limpiar()
        
        self.mostrarPersonas()

    def mostrarPersonas(self):
        try:
            listaPersonas = self.__nPersona.mostrarPersonas()
            
            if listaPersonas is not None and len(listaPersonas) > 0:
                col1, col2 = st.columns([10, 2])
                
                with col1:
                    st.write("Lista de Personas:")
                    st.dataframe(listaPersonas)
                    
                with col2:
                    if hasattr(listaPersonas, 'iloc'):
                        nombres = listaPersonas['Nombre'].tolist()
                        docs = listaPersonas['docidentidad'].tolist() if 'docidentidad' in listaPersonas.columns else listaPersonas['docIdentidad'].tolist()
                    else:
                        nombres = [p.get('Nombre', f"Persona {i}") for i, p in enumerate(listaPersonas)]
                        docs = [p.get('docIdentidad', p.get('docidentidad', f"ID_{i}")) for i, p in enumerate(listaPersonas)]
                    
                    # Crear opciones con nombre y documento
                    opciones = [""] + [f"{nombre} ({doc})" for nombre, doc in zip(nombres, docs)]
                    
                    seleccion = st.selectbox("Seleccionar persona", options=opciones)
                    
                    if seleccion != "":
                        # Extraer el índice de la selección
                        idx = opciones.index(seleccion) - 1
                        
                        if hasattr(listaPersonas, 'iloc'): 
                            persona_seleccionada = listaPersonas.iloc[idx].to_dict()
                        else:
                            persona_seleccionada = listaPersonas[idx]
                        
                        col_editar, col_eliminar = st.columns(2)
                        
                        with col_editar:
                            btnEditar = st.button('✏️ Editar', key=f'editar_{idx}')
                            
                        with col_eliminar:
                            btnEliminar = st.button('🗑️ Eliminar', key=f'eliminar_{idx}')
                        
                        if btnEditar:
                            st.session_state.persona_seleccionada = persona_seleccionada
                            st.rerun()
                            
                        if btnEliminar:
                            # Obtener el documento de identidad
                            doc_identidad = persona_seleccionada.get('docIdentidad', 
                                                                     persona_seleccionada.get('docidentidad', ''))
                            if doc_identidad:
                                if self.eliminarPersona(doc_identidad):
                                    st.success(f"Persona eliminada correctamente")
                                    st.rerun()
            else:
                st.info("No hay personas registradas aún.")
                
        except Exception as e:
            st.error(f"Error al mostrar personas: {e}")

    def nuevaPersona(self, persona: dict):
        try:
            self.__nPersona.nuevaPersona(persona)
            st.toast('Registro insertado correctamente', duration='short')
            self.limpiar()
        except Exception as e:
            st.error(f"Error: {e}")
            st.toast('Registro no insertado', duration='short')

    def actualizarPersona(self, persona: dict, docIdentidad_original: str):
        try:
            self.__nPersona.actualizarPersonas(persona, docIdentidad_original)
            st.toast('Registro actualizado correctamente', duration='short')
            self.limpiar()
        except Exception as e:
            st.error(f"Error: {e}")
            st.toast('Registro no actualizado', duration='short')

    def eliminarPersona(self, docIdentidad: str):
        try:
            resultado = self.__nPersona.eliminarPersona(docIdentidad)
            if resultado:
                st.toast('Registro eliminado correctamente', duration='short')
                self.limpiar()
                return True
            else:
                st.error("No se pudo eliminar la persona")
                return False
        except Exception as e:
            st.error(f"Error al eliminar: {e}")
            return False

    def limpiar(self):
        st.session_state.formularioKey += 1
        st.session_state.persona_seleccionada = None
        st.session_state.docIdentidad_sesion = ''
        st.session_state.nombre_sesion = ''
        st.session_state.edad_sesion = 0
        st.session_state.telefono_sesion = ''
        st.session_state.correo_sesion = ''
        st.session_state.accion = 'guardar'
        
        # Recargar la página
        st.rerun()
