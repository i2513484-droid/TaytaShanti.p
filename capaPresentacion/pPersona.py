from capaLogica.nPersona import NPersona
import streamlit as st 

class PPersona:
    def __init__(self):
        self.__nPersona = NPersona()
        if 'formularioKey' not in st.session_state:
            st.session_state.formularioKey = 0
        if 'persona_Seleccionada' not in st.session_state:
            st.session_state.persona_Seleccionada = ''
        if 'docIdentidad_seccion' not in st.session_state:
            st.session_state.docIdentidad_seccion = ''
        if 'nombre_seccion' not in st.session_state:
            st.session_state.Nombre_seccion = ''
        if 'edad:_seccion' not in st.session_state:
            st.session_state.Edad_seccion = ''
        if 'telefono_seccion' not in st.session_state:
            st.session_state.Telefono_seccion = ''
        if 'correo_seccion' not in st.session_state:
            st.session_state.Correo_seccion = ''
        self.__construirInterfaz()

    def __construirInterfaz(self):
        st.title('Bienvenido a TAYTA SHANTI')
        
        # Corregir nombres de variables de sesión
        if st.session_state.persona_Seleccionada != '':
            st.session_state.docIdentidad_seccion = st.session_state.persona_Seleccionada['docIdentidad']
            st.session_state.Nombre_seccion = st.session_state.persona_Seleccionada['Nombre']
            st.session_state.Edad_seccion = st.session_state.persona_Seleccionada['Edad']
            st.session_state.Telefono_seccion = st.session_state.persona_Seleccionada['Telefono']
            st.session_state.Correo_seccion = st.session_state.persona_Seleccionada['Correo']
        
        with st.form(f'FormularioPersona{st.session_state.formularioKey}'):
            txtDocIdentidad = st.text_input('Documento de identidad', value=st.session_state.docIdentidad_seccion)
            txtNombre = st.text_input('Nombre', value=st.session_state.Nombre_seccion)
            txtEdad = st.number_input('Edad', min_value=0, max_value=150, value=st.session_state.Edad_seccion if 'Edad_seccion' in st.session_state else 0)
            txtTelefono = st.text_input('Telefono', value=st.session_state.Telefono_seccion)
            txtCorreo = st.text_input('Correo', value=st.session_state.Correo_seccion)
            
            # Botón de envío dentro del formulario
            if st.session_state.persona_Seleccionada != '':
                btnActualizar = st.form_submit_button('Actualizar', type='primary')
                if btnActualizar:
                    # Aquí deberías agregar la lógica para actualizar
                    pass
            else:
                btnGuardar = st.form_submit_button('Guardar', type='primary')
                if btnGuardar:
                    persona = {
                        'Documento de identidad': txtDocIdentidad,
                        'Nombre': txtNombre,
                        'Edad': txtEdad,
                        'Telefono': txtTelefono,
                        'Correo': txtCorreo
                    }
                    self.nuevaPersona(persona)
        
        self.mostrarPersonas()

    def mostrarPersonas(self):
        listaPersonas = self.__nPersona.mostrarPersonas()
        col1, col2 = st.columns([10, 2])
        with col1:
            # Corregir el uso de dataframe selection
            selection = st.dataframe(listaPersonas, selection_mode='single-row')
            
        with col2:
            if selection and hasattr(selection, 'selection') and selection.selection.rows:
                indice_persona = selection.selection.rows[0]
                personaSeleccionadaIndice = listaPersonas.iloc[indice_persona] if hasattr(listaPersonas, 'iloc') else listaPersonas[indice_persona]
                btnEditar = st.button('Editar')
                
                if btnEditar:
                    st.session_state.persona_Seleccionada = personaSeleccionadaIndice.to_dict() if hasattr(personaSeleccionadaIndice, 'to_dict') else dict(personaSeleccionadaIndice)
                    st.rerun()
                    
    def nuevaPersona(self, persona: dict):
        try:
            self.__nPersona.nuevaPersona(persona)
            st.toast('Registro insertado correctamente', icon='✅')
            self.limpiar()
        except Exception as e:
            st.error(e)
            st.toast('Registro no insertado', icon='❌')

    def limpiar(self):
        st.session_state.formularioKey += 1
        # Limpiar las variables de sesión
        st.session_state.persona_Seleccionada = ''
        st.session_state.docIdentidad_seccion = ''
        st.session_state.Nombre_seccion = ''
        st.session_state.Edad_seccion = ''
        st.session_state.Telefono_seccion = ''
        st.session_state.Correo_seccion = ''
        st.rerun()
        st.session_state.telefono_seccion = ''
        st.session_state.correo_seccion = ''
        st.rerun()
