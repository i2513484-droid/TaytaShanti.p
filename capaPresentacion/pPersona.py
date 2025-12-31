from capaLogica.nPersona import NPersona
import streamlit as st 

class PPersona:
    def __init__(self):
        self.__nPersona = NPersona()
        self.__inicializar_session_state()
        self.__construirInterfaz()

    def __inicializar_session_state(self):
        """Inicializa las variables de sesión"""
        if 'persona_seleccionada' not in st.session_state:
            st.session_state.persona_seleccionada = None
        if 'doc_original' not in st.session_state:
            st.session_state.doc_original = ''

    def __construirInterfaz(self):
        st.title('TAYTA SHANTI - Gestión de Personas')
        
        # Formulario
        self.__mostrar_formulario()
        
        # Lista de personas
        self.__mostrar_lista_personas()

    def __mostrar_formulario(self):
        """Muestra el formulario para registrar o editar personas"""
        st.header("📝 Formulario de Persona")
        
        # Valores por defecto
        doc = ''
        nombre = ''
        edad = 0
        telefono = ''
        correo = ''
        
        # Si estamos editando, cargar datos
        if st.session_state.persona_seleccionada:
            persona = st.session_state.persona_seleccionada
            doc = persona.get('docidentidad', persona.get('docIdentidad', ''))
            nombre = persona.get('Nombre', '')
            edad = persona.get('Edad', 0)
            telefono = persona.get('Telefono', '')
            correo = persona.get('Correo', '')
        
        # Campos del formulario
        with st.form("form_persona"):
            txtDoc = st.text_input("Documento de Identidad", value=doc, 
                                  disabled=bool(st.session_state.persona_seleccionada))
            txtNombre = st.text_input("Nombre", value=nombre)
            txtEdad = st.number_input("Edad", min_value=0, max_value=150, value=edad)
            txtTelefono = st.text_input("Teléfono", value=telefono)
            txtCorreo = st.text_input("Correo", value=correo)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.session_state.persona_seleccionada:
                    btn_actualizar = st.form_submit_button("🔄 Actualizar", type="primary")
                else:
                    btn_guardar = st.form_submit_button("💾 Guardar", type="primary")
            
            with col2:
                if st.session_state.persona_seleccionada:
                    btn_cancelar = st.form_submit_button("❌ Cancelar")
                else:
                    btn_limpiar = st.form_submit_button("🧹 Limpiar")
        
        # Manejar acciones del formulario
        if st.session_state.persona_seleccionada and btn_actualizar:
            nueva_persona = {
                'docIdentidad': txtDoc,
                'Nombre': txtNombre,
                'Edad': txtEdad,
                'Telefono': txtTelefono,
                'Correo': txtCorreo
            }
            # Llamar al método con 2 argumentos
            self.__actualizar_persona(nueva_persona, st.session_state.doc_original)
            
        elif not st.session_state.persona_seleccionada and btn_guardar:
            persona = {
                'docIdentidad': txtDoc,
                'Nombre': txtNombre,
                'Edad': txtEdad,
                'Telefono': txtTelefono,
                'Correo': txtCorreo
            }
            self.__nueva_persona(persona)
            
        elif (st.session_state.persona_seleccionada and btn_cancelar) or (not st.session_state.persona_seleccionada and btn_limpiar):
            self.__limpiar_formulario()

    def __mostrar_lista_personas(self):
        """Muestra la lista de personas registradas"""
        st.header("👥 Personas Registradas")
        
        try:
            personas = self.__nPersona.mostrarPersonas()
            
            if personas:
                for i, persona in enumerate(personas):
                    col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 2, 1, 2, 3, 1, 1])
                    
                    with col1:
                        st.write(f"**{persona.get('Nombre', '')}**")
                    with col2:
                        st.write(persona.get('docidentidad', persona.get('docIdentidad', '')))
                    with col3:
                        st.write(persona.get('Edad', ''))
                    with col4:
                        st.write(persona.get('Telefono', ''))
                    with col5:
                        st.write(persona.get('Correo', ''))
                    with col6:
                        if st.button("✏️", key=f"editar_{i}"):
                            st.session_state.persona_seleccionada = persona
                            st.session_state.doc_original = persona.get('docidentidad', persona.get('docIdentidad', ''))
                            st.rerun()
                    with col7:
                        if st.button("🗑️", key=f"eliminar_{i}"):
                            doc = persona.get('docidentidad', persona.get('docIdentidad', ''))
                            self.__eliminar_persona(doc)
                st.info(f"Total: {len(personas)} personas")
            else:
                st.info("No hay personas registradas")
                
        except Exception as e:
            st.error(f"Error: {e}")

    def __nueva_persona(self, persona: dict):
        """Registra una nueva persona"""
        try:
            self.__nPersona.nuevaPersona(persona)
            st.success("Persona registrada correctamente")
            self.__limpiar_formulario()
        except Exception as e:
            st.error(f"Error: {e}")

    def __actualizar_persona(self, persona: dict, doc_original: str):
        """Actualiza una persona existente"""
        try:
            # LLAMADA CORRECTA - 2 argumentos
            self.__nPersona.actualizarPersonas(persona, doc_original)
            st.success("Persona actualizada correctamente")
            self.__limpiar_formulario()
        except Exception as e:
            st.error(f"Error: {e}")

    def __eliminar_persona(self, doc: str):
        """Elimina una persona"""
        try:
            self.__nPersona.eliminarPersona(doc)
            st.success("Persona eliminada correctamente")
            self.__limpiar_formulario()
        except Exception as e:
            st.error(f"Error: {e}")

    def __limpiar_formulario(self):
        """Limpia el formulario"""
        st.session_state.persona_seleccionada = None
        st.session_state.doc_original = ''
        st.rerun()
