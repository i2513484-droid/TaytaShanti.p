from capaLogica.nPersona import NPersona
import streamlit as st 

class PPersona:
    def __init__(self):
        self.__nPersona = NPersona()
        self.__inicializar_session_state()
        self.__construirInterfaz()

    def __inicializar_session_state(self):
        """Inicializa las variables de sesión"""
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
        if 'modo_edicion' not in st.session_state:
            st.session_state.modo_edicion = False

    def __construirInterfaz(self):
        st.title('Bienvenido a TAYTA SHANTI')
        st.markdown("---")
        
        # Formulario para registrar/editar personas
        self.__mostrar_formulario()
        
        # Lista de personas registradas
        self.__mostrar_lista_personas()

    def __mostrar_formulario(self):
        """Muestra el formulario para registrar o editar personas"""
        st.header("📝 Registrar/Editar Persona")
        
        # Si hay una persona seleccionada para editar, cargar sus datos
        if st.session_state.persona_seleccionada is not None:
            persona = st.session_state.persona_seleccionada
            
            # Manejar diferentes nombres de campo para docidentidad
            docidentidad = persona.get('docIdentidad', persona.get('docidentidad', ''))
            st.session_state.docIdentidad_sesion = docidentidad
            st.session_state.nombre_sesion = persona.get('Nombre', '')
            st.session_state.edad_sesion = persona.get('Edad', 0)
            st.session_state.telefono_sesion = persona.get('Telefono', '')
            st.session_state.correo_sesion = persona.get('Correo', '')
            st.session_state.modo_edicion = True
        else:
            st.session_state.modo_edicion = False
        
        with st.form(f'FormularioPersona{st.session_state.formularioKey}', clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                txtDocIdentidad = st.text_input(
                    'Documento de identidad *', 
                    value=st.session_state.docIdentidad_sesion,
                    disabled=st.session_state.modo_edicion,
                    help="Número de documento (solo números)"
                )
                txtNombre = st.text_input(
                    'Nombre completo *', 
                    value=st.session_state.nombre_sesion,
                    help="Nombre y apellidos"
                )
                txtEdad = st.number_input(
                    'Edad *', 
                    min_value=0, 
                    max_value=150, 
                    value=st.session_state.edad_sesion,
                    help="Edad entre 0 y 150 años"
                )
            
            with col2:
                txtTelefono = st.text_input(
                    'Teléfono', 
                    value=st.session_state.telefono_sesion,
                    help="Número de teléfono (opcional)"
                )
                txtCorreo = st.text_input(
                    'Correo electrónico', 
                    value=st.session_state.correo_sesion,
                    help="Correo electrónico (opcional)"
                )
            
            st.markdown("* Campos obligatorios")
            
            # Botones del formulario
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
            
            with col_btn1:
                if st.session_state.modo_edicion:
                    btnActualizar = st.form_submit_button('🔄 Actualizar', type='primary', use_container_width=True)
                else:
                    btnGuardar = st.form_submit_button('💾 Guardar', type='primary', use_container_width=True)
            
            with col_btn2:
                if st.session_state.modo_edicion:
                    btnCancelar = st.form_submit_button('❌ Cancelar', use_container_width=True)
                else:
                    btnLimpiar = st.form_submit_button('🧹 Limpiar', use_container_width=True)
            
            # Acciones del formulario
            if st.session_state.modo_edicion and btnActualizar:
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
                self.__actualizar_persona(nueva_persona, doc_original)
                
            elif not st.session_state.modo_edicion and btnGuardar:
                persona = {
                    'docIdentidad': txtDocIdentidad,
                    'Nombre': txtNombre,
                    'Edad': txtEdad,
                    'Telefono': txtTelefono,
                    'Correo': txtCorreo
                }
                self.__nueva_persona(persona)
                
            elif (st.session_state.modo_edicion and btnCancelar) or (not st.session_state.modo_edicion and btnLimpiar):
                self.__limpiar_formulario()

    def __mostrar_lista_personas(self):
        """Muestra la lista de personas registradas"""
        st.markdown("---")
        st.header("👥 Personas Registradas")
        
        try:
            listaPersonas = self.__nPersona.mostrarPersonas()
            
            if listaPersonas and len(listaPersonas) > 0:
                # Crear tabla con opciones de acción
                for i, persona in enumerate(listaPersonas):
                    col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 3, 2, 3, 3, 1, 1])
                    
                    with col1:
                        st.write(f"**{persona.get('Nombre', 'N/A')}**")
                    
                    with col2:
                        st.write(persona.get('docidentidad', persona.get('docIdentidad', 'N/A')))
                    
                    with col3:
                        st.write(persona.get('Edad', 'N/A'))
                    
                    with col4:
                        st.write(persona.get('Telefono', 'N/A'))
                    
                    with col5:
                        st.write(persona.get('Correo', 'N/A'))
                    
                    with col6:
                        if st.button('✏️', key=f'editar_{i}', help="Editar"):
                            st.session_state.persona_seleccionada = persona
                            st.rerun()
                    
                    with col7:
                        if st.button('🗑️', key=f'eliminar_{i}', help="Eliminar"):
                            doc_identidad = persona.get('docidentidad', persona.get('docIdentidad', ''))
                            if doc_identidad:
                                if self.__eliminar_persona(doc_identidad):
                                    st.success(f"✅ Persona eliminada correctamente")
                                    st.rerun()
                
                st.markdown("---")
                st.info(f"Total de personas registradas: {len(listaPersonas)}")
            else:
                st.info("📭 No hay personas registradas aún. ¡Registra la primera!")
                
        except Exception as e:
            st.error(f"❌ Error al mostrar personas: {e}")

    def __nueva_persona(self, persona: dict):
        """Registra una nueva persona"""
        try:
            self.__nPersona.nuevaPersona(persona)
            st.success('✅ Registro insertado correctamente')
            self.__limpiar_formulario()
        except Exception as e:
            st.error(f"❌ Error: {e}")

    def __actualizar_persona(self, persona: dict, docIdentidad_original: str):
        """Actualiza una persona existente"""
        try:
            self.__nPersona.actualizarPersonas(persona, docIdentidad_original)
            st.success('✅ Registro actualizado correctamente')
            self.__limpiar_formulario()
        except Exception as e:
            st.error(f"❌ Error: {e}")

    def __eliminar_persona(self, docIdentidad: str):
        """Elimina una persona"""
        try:
            if st.session_state.get('confirmar_eliminar', False):
                resultado = self.__nPersona.eliminarPersona(docIdentidad)
                if resultado:
                    st.session_state.confirmar_eliminar = False
                    return True
                else:
                    st.error("⚠️ No se pudo eliminar la persona")
                    return False
            else:
                # Pedir confirmación
                if st.button("✅ Confirmar eliminación", key="confirmar_elim"):
                    st.session_state.confirmar_eliminar = True
                    st.rerun()
                return False
        except Exception as e:
            st.error(f"❌ Error al eliminar: {e}")
            return False

    def __limpiar_formulario(self):
        """Limpia el formulario y las variables de sesión"""
        st.session_state.formularioKey += 1
        st.session_state.persona_seleccionada = None
        st.session_state.docIdentidad_sesion = ''
        st.session_state.nombre_sesion = ''
        st.session_state.edad_sesion = 0
        st.session_state.telefono_sesion = ''
        st.session_state.correo_sesion = ''
        st.session_state.modo_edicion = False
        st.rerun()
