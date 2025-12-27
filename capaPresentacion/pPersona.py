from capaLogica.nPersona import NPersona
import streamlit as st 

class PPersona:
    def __init__(self):
        self.__nPersona = NPersona()

        # Inicialización correcta del session_state
        st.session_state.setdefault('formularioKey', 0)
        st.session_state.setdefault('persona_seleccionada', None)
        st.session_state.setdefault('docIdentidad_seccion', '')
        st.session_state.setdefault('nombre_seccion', '')
        st.session_state.setdefault('edad_seccion', 0)
        st.session_state.setdefault('telefono_seccion', '')
        st.session_state.setdefault('correo_seccion', '')

        self.__construirInterfaz()

    def __construirInterfaz(self):
        st.title('Bienvenido a TAYTA SHANTI')
        if st.session_state.persona_seleccionada:
            p = st.session_state.persona_seleccionada
            st.session_state.docIdentidad_seccion = p['docIdentidad']
            st.session_state.nombre_seccion = p['nombre']
            st.session_state.edad_seccion = p['edad']
            st.session_state.telefono_seccion = p['telefono']
            st.session_state.correo_seccion = p['correo']

        with st.form(f'FormularioPersona{st.session_state.formularioKey}'):
            txtDocIdentidad = st.text_input(
                'Documento de identidad',
                value=st.session_state.docIdentidad_seccion
            )
            txtNombre = st.text_input(
                'Nombre',
                value=st.session_state.nombre_seccion
            )
            txtEdad = st.number_input(
                'Edad',
                min_value=0,
                max_value=150,
                value=st.session_state.edad_seccion
            )
            txtTelefono = st.text_input(
                'Teléfono',
                value=st.session_state.telefono_seccion
            )
            txtCorreo = st.text_input(
                'Correo',
                value=st.session_state.correo_seccion
            )

            btnGuardar = st.form_submit_button('Guardar', type='primary')

            if btnGuardar:
                persona = {
                    'docIdentidad': txtDocIdentidad,
                    'nombre': txtNombre,
                    'edad': txtEdad,
                    'telefono': txtTelefono,
                    'correo': txtCorreo
                }
                self.nuevaPersona(persona)

        self.mostrarPersonas()

    def mostrarPersonas(self):
        listaPersonas = self.__nPersona.mostrarPersonas()
        col1, col2 = st.columns([10, 2])

        with col1:
            tabla = st.dataframe(
                listaPersonas,
                selection_mode='single-row',
                on_select='rerun'
            )

        with col2:
            if tabla.selection.rows:
                indice = tabla.selection.rows[0]
                persona = listaPersonas[indice]

                if st.button('Editar'):
                    st.session_state.persona_seleccionada = persona
                    st.rerun()

    def nuevaPersona(self, persona: dict):
        try:
            self.__nPersona.nuevaPersona(persona)
            st.toast('Registro insertado correctamente')
            self.limpiar()
        except Exception as e:
            st.error(str(e))
            st.toast('Registro no insertado')

    def limpiar(self):
        st.session_state.formularioKey += 1
        st.session_state.persona_seleccionada = None
        st.session_state.docIdentidad_seccion = ''
        st.session_state.nombre_seccion = ''
        st.session_state.edad_seccion = 0
        st.session_state.telefono_seccion = ''
        st.session_state.correo_seccion = ''
        st.rerun()



    def limpiar(self):
        st.session_state.formularioKey += 1
        st.rerun += 1
        st.rerun
