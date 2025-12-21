from capaLogica.nPersona import NPersona
import streamlit as st 

class PPersona:
    def __init__(self):
        self.__nPersona = NPersona()
        if 'formularioKey' not in st.session_state:
            st.session_state.formularioKey = 0
        self.__construirInterfaz()

    def __construirInterfaz(self):
        st.title('Bienvenido a TAYTA SHANTI')
        with st.form(f'FormularioPersona{st.session_state.formularioKey}'):
            txtDocIdentidad = st.text_input("Documento de identidad")
            txtNombre = st.text_input("Nombre")
            txtEdad = st.number_input("Edad", min_value=0, max_value=150)
            txtTelefono = st.text_input("Telefono")
            txtCorreo = st.text_input("Correo")
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
        listaPersona = self.__nPersona.mostrarPersonas()
        st.dataframe(listaPersona)
    
    def nuevaPersona(self, persona: dict):
        self.__nPersona.nuevaPersona(persona)
        st.toast('Registro insertado correctamente', duration='short')
        self.limpiar()

    def limpiar(self):
        st.session_state.formularioKey += 1
        st.rerun
