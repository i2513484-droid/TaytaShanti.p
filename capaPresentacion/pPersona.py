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
        datos_formulario = {}
        if st.session_state.persona_seleccionada is not None:
            persona = st.session_state.persona_seleccionada
            datos_formulario = {
                'docIdentidad': persona.get('docIdentidad', persona.get('docidentidad', '')),
                'Nombre': persona.get('Nombre', ''),
                'Edad': persona.get('Edad', 0),
                'Telefono': persona.get('Telefono', ''),
                'Correo': persona.get('Correo', '')
            }
            st.session_state.modo_edicion = True
        else:
            datos_formulario = {
                'docIdentidad': '',
                'Nombre': '',
                'Edad': 0,
                'Telefono': '',
                'Correo': ''
            }
            st.session_state.modo_edicion = False
        
        with st.form(f'FormularioPersona{st.session_state.formularioKey}'):
            col1, col2 = st.columns(2)
            
            with col1:
                txtDocIdentidad = st.text_input(
                    'Documento de identidad *', 
                    value=datos_formulario['docIdentidad'],
                    disabled=st.session_state.modo_edicion,
                    help="Número de documento (solo números)"
                )
                txtNombre = st.text_input(
                    'Nombre completo *', 
                    value=datos_formulario['Nombre'],
                    help="Nombre y apellidos"
                )
                txtEdad = st.number_input(
                    'Edad *', 
                    min_value=0, 
                    max_value=150, 
                    value=datos_formulario['Edad'],
                    help="Edad entre 0 y 150 años"
                )
            
            with col2:
                txtTelefono = st.text_input(
                    'Teléfono', 
                    value=datos_formulario['Telefono'],
                    help="Número de teléfono (opcional)"
                )
                txtCorreo = st.text_input(
                    'Correo electrónico', 
                    value=datos_formulario['Correo'],
                    help="Correo electrónico (opcional)"
                )
            
            st.markdown("* Campos obligatorios")
            
            # Botones del formulario
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.session_state.modo_edicion:
                    btnActualizar = st.form_submit_button('🔄 Actualizar', type='primary')
                else:
                    btnGuardar = st.form_submit_button('💾 Guardar', type='primary')
            
            with col_btn2:
                if st.session_state.modo_edicion:
                    btnCancelar = st.form_submit_button('❌ Cancelar')
                else:
                    btnLimpiar = st.form_submit_button('🧹 Limpiar')
            
            # Acciones del formulario
            if st.session_state.modo_edicion and btnActualizar:
                nueva_persona = {
                    'docIdentidad': txtDocIdentidad,
                    'Nombre': txtNombre,
                    'Edad': txtEdad,
                    'Telefono': txtTelefono,
                    'Correo': txtCorreo
                }
                # Obtener el docIdentidad original
                persona_original = st.session_state.persona_seleccionada
                doc_original = persona_original.get('docIdentidad', persona_original.get('docidentidad', ''))
                
                try:
                    self.__nPersona.actualizarPersonas(nueva_persona, doc_original)
                    st.success('✅ Registro actualizado correctamente')
                    self.__limpiar_formulario()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                
            elif not st.session_state.modo_edicion and btnGuardar:
                persona = {
                    'docIdentidad': txtDocIdentidad,
                    'Nombre': txtNombre,
                    'Edad': txtEdad,
                    'Telefono': txtTelefono,
                    'Correo': txtCorreo
                }
                try:
                    self.__nPersona.nuevaPersona(persona)
                    st.success('✅ Registro insertado correctamente')
                    self.__limpiar_formulario()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                
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
                    with st.container():
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
                            if st.button('✏️', key=f'editar_{i}'):
                                st.session_state.persona_seleccionada = persona
                                st.rerun()
                        
                        with col7:
                            if st.button('🗑️', key=f'eliminar_{i}'):
                                doc_identidad = persona.get('docidentidad', persona.get('docIdentidad', ''))
                                if doc_identidad:
                                    try:
                                        self.__nPersona.eliminarPersona(doc_identidad)
                                        st.success(f"✅ Persona eliminada correctamente")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Error: {e}")
                
                st.markdown("---")
                st.info(f"Total de personas registradas: {len(listaPersonas)}")
            else:
                st.info("📭 No hay personas registradas aún. ¡Registra la primera!")
                
        except Exception as e:
            st.error(f"❌ Error al mostrar personas: {e}")

    def __limpiar_formulario(self):
        """Limpia el formulario y las variables de sesión"""
        st.session_state.formularioKey += 1
        st.session_state.persona_seleccionada = None
        st.session_state.modo_edicion = False
        st.rerun()
