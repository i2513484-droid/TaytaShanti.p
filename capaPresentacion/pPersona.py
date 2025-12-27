from capaLogica.nPersona import NPersona
import streamlit as st 

class PPersona:
    def __init__(self):
        self.__nPersona = NPersona()
        # Inicializar todas las variables de sesión con nombres consistentes
        if 'formularioKey' not in st.session_state:
            st.session_state.formularioKey = 0
        if 'persona_seleccionada' not in st.session_state:
            st.session_state.persona_seleccionada = None  # Usar None en lugar de ''
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
        self.__construirInterfaz()

    def __construirInterfaz(self):
        st.title('Bienvenido a TAYTA SHANTI')
        
        # Verificar si hay una persona seleccionada (usando None como valor por defecto)
        if st.session_state.persona_seleccionada is not None:
            # Actualizar valores de sesión desde la persona seleccionada
            persona = st.session_state.persona_seleccionada
            st.session_state.docIdentidad_sesion = persona.get('docIdentidad', persona.get('Documento de identidad', ''))
            st.session_state.nombre_sesion = persona.get('Nombre', '')
            st.session_state.edad_sesion = persona.get('Edad', 0)
            st.session_state.telefono_sesion = persona.get('Telefono', '')
            st.session_state.correo_sesion = persona.get('Correo', '')
        
        with st.form(f'FormularioPersona{st.session_state.formularioKey}'):
            txtDocIdentidad = st.text_input('Documento de identidad', value=st.session_state.docIdentidad_sesion)
            txtNombre = st.text_input('Nombre', value=st.session_state.nombre_sesion)
            txtEdad = st.number_input('Edad', min_value=0, max_value=150, value=st.session_state.edad_sesion)
            txtTelefono = st.text_input('Telefono', value=st.session_state.telefono_sesion)
            txtCorreo = st.text_input('Correo', value=st.session_state.correo_sesion)
            
            # Botón de envío dentro del formulario
            if st.session_state.persona_seleccionada is not None:
                btnActualizar = st.form_submit_button('Actualizar', type='primary')
                if btnActualizar:
                    # Aquí deberías agregar la lógica para actualizar
                    nueva_persona = {
                        'docIdentidad': txtDocIdentidad,
                        'Nombre': txtNombre,
                        'Edad': txtEdad,
                        'Telefono': txtTelefono,
                        'Correo': txtCorreo
                    }
                    # self.actualizarPersona(nueva_persona)  # Descomentar cuando implementes
                    self.limpiar()
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
        
        self.mostrarPersonas()

    def mostrarPersonas(self):
        try:
            listaPersonas = self.__nPersona.mostrarPersonas()
            
            if listaPersonas is not None and len(listaPersonas) > 0:
                col1, col2 = st.columns([10, 2])
                
                with col1:
                    # Mostrar el dataframe
                    st.write("Lista de Personas:")
                    st.dataframe(listaPersonas)
                    
                with col2:
                    # Para selección simple, usamos selectbox en lugar de dataframe selection
                    if hasattr(listaPersonas, 'iloc'):  # Es un DataFrame de pandas
                        nombres = listaPersonas['Nombre'].tolist()
                    else:  # Es una lista de diccionarios
                        nombres = [p.get('Nombre', f"Persona {i}") for i, p in enumerate(listaPersonas)]
                    
                    seleccion = st.selectbox("Seleccionar persona", options=[""] + nombres)
                    
                    if seleccion != "":
                        # Encontrar la persona seleccionada
                        if hasattr(listaPersonas, 'iloc'):  # DataFrame
                            idx = nombres.index(seleccion)
                            persona_seleccionada = listaPersonas.iloc[idx].to_dict()
                        else:  # Lista de diccionarios
                            idx = nombres.index(seleccion)
                            persona_seleccionada = listaPersonas[idx]
                        
                        btnEditar = st.button('Editar')
                        
                        if btnEditar:
                            st.session_state.persona_seleccionada = persona_seleccionada
                            st.rerun()
            else:
                st.info("No hay personas registradas aún.")
                
        except Exception as e:
            st.error(f"Error al mostrar personas: {e}")

    def nuevaPersona(self, persona: dict):
        try:
            self.__nPersona.nuevaPersona(persona)
            st.toast('Registro insertado correctamente', icon='✅')
            self.limpiar()
        except Exception as e:
            st.error(f"Error: {e}")
            st.toast('Registro no insertado', icon='❌')

    def limpiar(self):
        # Incrementar la clave del formulario para limpiarlo
        st.session_state.formularioKey += 1
        
        # Limpiar todas las variables de sesión relacionadas con el formulario
        st.session_state.persona_seleccionada = None
        st.session_state.docIdentidad_sesion = ''
        st.session_state.nombre_sesion = ''
        st.session_state.edad_sesion = 0
        st.session_state.telefono_sesion = ''
        st.session_state.correo_sesion = ''
        
        # Recargar la página
        st.rerun()
