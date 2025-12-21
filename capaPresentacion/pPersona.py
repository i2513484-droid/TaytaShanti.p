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
        if 'edad_seccion' not in st.session_state:
            st.session_state.Edad_seccion = ''
        if 'telefono_seccion' not in st.session_state:
            st.session_state.Telefono_seccion = ''
        if 'correo_seccion'not in st.session_state:
            st.session_state.Correo_seccion = ''
        self.__construirInterfaz()

    def __construirInterfaz(self):
        st.title('Bienvenido a TAYTA SHANTI')
        if st.session_state.persona_Seleccionada !='':
            st.session_state.docIdentdidad_sesion = st.session_state.persona_seleccionada['docIdentidad']
            st.session_state.nombre_sesion = st.session_state.persona_seleccionada ['nombre']
            st.session_state.edad_sesion = st.session_state.persona_seleccionada['edad']
            st.session_state.telefono_seccion = st.session_state.persona_selecionada['telefono']
            st.session_state.correo.seccion = st.session_state.persona_seleccionada['correo']
        with st.form(f'FormularioPersona{st.session_state.formularioKey}'):
            txtDocIdentidad = st.text_input('Documento de identidad', value =st.session_state.docIdentidad_seccion)
            txtNombre = st.text_input('Nombre', value=st.session_state.Nombre_seccion)
            txtEdad = st.number_input('Edad', min_value=0, max_value=150, value=st.session_state.edad_seccion)
            txtTelefono = st.text_input('Telefono', value=st.session_state.telefono_seccion)
            txtCorreo = st.text_input('Correo', value=st.session_state.correo_seccion)
            if st.session_state.persona_seleccionada != '':
                btnActualizar = st.form_submit_button('Actualizar', type = 'primary')
            else:
                btnGuardar = st.form_submit_button('Guardar', type = 'primary')
           
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
            personaSeleccionada = st.dataframe(listaPersonas, selection_mode = 'single-row', on_select='rerun')

        with col2:
            if personaSeleccionada.selection.rows:
                indice_persona = personaSeleccionada.selection.rows[0]
                personaSeleccionadaIndice = listaPersonas[indice_persona]
                btnEditar = st.button('Editar')

                if btnEditar:
                   st.session_state.persona_Seleccionada = personaSeleccionadaIndice
                   st.rerun()

                    
    def nuevaPersona(self, persona: dict):
         try:
            self.__nPersona.nuevaPersona(persona)
            st.toast('Registro insertado correctamente', duration='short')
            self.limpiar()
         except Exception as e:
             st.error(e)
             st.toast('Registro no insertado', duration='short')


    def limpiar(self):
        st.session_state.formularioKey += 1
        st.rerun


    def limpiar(self):
        st.session_state.formularioKey += 1
        st.rerun
