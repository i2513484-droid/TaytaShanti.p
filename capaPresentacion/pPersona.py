from capaLogica.nPersona import NPersona
import streamlit as st 

class PPersona:
    def __init__(self):
        self.__nPersona = NPersona()
        
        # Inicialización de estados (Nombres normalizados en minúsculas para evitar errores)
        if 'formularioKey' not in st.session_state:
            st.session_state.formularioKey = 0
        if 'persona_Seleccionada' not in st.session_state:
            st.session_state.persona_Seleccionada = None
            
        # Variables de campos del formulario
        campos = ['docIdentidad', 'nombre', 'edad', 'telefono', 'correo']
        for campo in campos:
            key = f'{campo}_seccion'
            if key not in st.session_state:
                st.session_state[key] = 0 if campo == 'edad' else ''
        
        self.__construirInterfaz()

    def __construirInterfaz(self):
        st.title('Bienvenido a TAYTA SHANTI')
        
        # Cargar datos si hay una persona seleccionada para editar
        if st.session_state.persona_Seleccionada is not None:
            p = st.session_state.persona_Seleccionada
            # Usamos .get() por seguridad si las llaves varían entre Mayúsculas/Minúsculas
            st.session_state.docIdentidad_seccion = p.get('docIdentidad', '')
            st.session_state.nombre_seccion = p.get('Nombre', '')
            st.session_state.edad_seccion = p.get('Edad', 0)
            st.session_state.telefono_seccion = p.get('Telefono', '')
            st.session_state.correo_seccion = p.get('Correo', '')

        # FORMULARIO
        with st.form(key=f'FormularioPersona{st.session_state.formularioKey}'):
            txtDocIdentidad = st.text_input('Documento de identidad', value=st.session_state.docIdentidad_seccion)
            txtNombre = st.text_input('Nombre', value=st.session_state.nombre_seccion)
            txtEdad = st.number_input('Edad', min_value=0, max_value=150, value=int(st.session_state.edad_seccion))
            txtTelefono = st.text_input('Telefono', value=st.session_state.telefono_seccion)
            txtCorreo = st.text_input('Correo', value=st.session_state.correo_seccion)
            
            # SOLUCIÓN AL ERROR DE LA IMAGEN:
            # El botón de envío debe definirse claramente para cualquier flujo
            etiqueta = 'Actualizar' if st.session_state.persona_Seleccionada else 'Guardar'
            btnAccion = st.form_submit_button(etiqueta, type='primary')
            
            if btnAccion:
                persona_dic = {
                    'docIdentidad': txtDocIdentidad,
                    'Nombre': txtNombre,
                    'Edad': txtEdad,
                    'Telefono': txtTelefono,
                    'Correo': txtCorreo
                }
                
                if st.session_state.persona_Seleccionada:
                    # Aquí llamarías a self.actualizarPersona(persona_dic)
                    st.success("Lógica de actualización")
                else:
                    self.nuevaPersona(persona_dic)

        self.mostrarPersonas()

    def mostrarPersonas(self):
        listaPersonas = self.__nPersona.mostrarPersonas()
        col1, col2 = st.columns([10, 2])
        
        with col1:
            # Captura de selección en el dataframe
            event = st.dataframe(listaPersonas, selection_mode='single-row', on_select='rerun')

        with col2:
            if event.selection.rows:
                idx = event.selection.rows[0]
                # Manejo si listaPersonas es DataFrame o Lista
                persona_data = listaPersonas.iloc[idx].to_dict() if hasattr(listaPersonas, 'iloc') else listaPersonas[idx]
                
                if st.button('Editar'):
                    st.session_state.persona_Seleccionada = persona_data
                    st.rerun()
            
            if st.button('Limpiar'):
                self.limpiar()

    def nuevaPersona(self, persona: dict):
        try:
            self.__nPersona.nuevaPersona(persona)
            st.toast('Registro insertado correctamente')
            self.limpiar()
        except Exception as e:
            st.error(f"Error: {e}")

    def limpiar(self):
        st.session_state.formularioKey += 1
        st.session_state.persona_Seleccionada = None
        # Resetear variables de sesión de los campos
        st.session_state.docIdentidad_seccion = ''
        st.session_state.nombre_seccion = ''
        st.session_state.edad_seccion = 0
        st.session_state.telefono_seccion = ''
        st.session_state.correo_seccion = ''
        st.rerun()
