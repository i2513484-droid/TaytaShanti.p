# capaPresentacion/pPersona.py
import streamlit as st
from capaLogica.nPersona import NPersona

class PPersona:
    def __init__(self):
        self.nPersona = NPersona()
    
    def mostrar(self):
        """Muestra la interfaz principal de gestión de personas"""
        st.title("👥 Gestión de Personas")
        
        # Menú de opciones
        opcion = st.sidebar.selectbox(
            "Seleccione una opción:",
            ["📋 Ver Personas", "➕ Agregar Persona", "✏️ Editar Persona", "🗑️ Eliminar Persona"]
        )
        
        if opcion == "📋 Ver Personas":
            self._mostrar_personas()
        elif opcion == "➕ Agregar Persona":
            self._agregar_persona()
        elif opcion == "✏️ Editar Persona":
            self._editar_persona()
        elif opcion == "🗑️ Eliminar Persona":
            self._eliminar_persona()
    
    def _mostrar_personas(self):
        """Muestra todas las personas en una tabla"""
        st.header("📋 Lista de Personas")
        
        try:
            personas = self.nPersona.obtener_todas_personas()
            
            if personas:
                # Mostrar en tabla
                st.dataframe(personas, use_container_width=True)
                
                # Mostrar métricas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Personas", len(personas))
            else:
                st.info("No hay personas registradas aún.")
                
        except Exception as e:
            st.error(f"Error al obtener personas: {e}")
    
    def _agregar_persona(self):
        """Formulario para agregar nueva persona"""
        st.header("➕ Agregar Nueva Persona")
        
        with st.form("form_agregar"):
            col1, col2 = st.columns(2)
            
            with col1:
                doc_identidad = st.text_input("Documento de Identidad*")
                nombre = st.text_input("Nombre*")
                apellido = st.text_input("Apellido*")
                
            with col2:
                email = st.text_input("Email")
                telefono = st.text_input("Teléfono")
                edad = st.number_input("Edad", min_value=0, max_value=120, value=0)
            
            # Campos adicionales
            direccion = st.text_area("Dirección")
            
            submitted = st.form_submit_button("💾 Guardar Persona")
            
            if submitted:
                if not doc_identidad or not nombre or not apellido:
                    st.error("Los campos marcados con * son obligatorios")
                    return
                
                try:
                    datos_persona = {
                        'docIdentidad': doc_identidad,
                        'nombre': nombre,
                        'apellido': apellido,
                        'email': email if email else None,
                        'telefono': telefono if telefono else None,
                        'edad': edad if edad > 0 else None,
                        'direccion': direccion if direccion else None
                    }
                    
                    resultado = self.nPersona.crear_persona(datos_persona)
                    st.success(f"✅ Persona creada exitosamente: {resultado['nombre']} {resultado['apellido']}")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error al crear persona: {e}")
    
    def _editar_persona(self):
        """Formulario para editar persona existente"""
        st.header("✏️ Editar Persona")
        
        try:
            # Obtener personas para seleccionar
            personas = self.nPersona.obtener_todas_personas()
            
            if not personas:
                st.info("No hay personas para editar.")
                return
            
            # Selector de persona
            opciones = [f"{p['docIdentidad']} - {p['nombre']} {p['apellido']}" for p in personas]
            seleccion = st.selectbox("Seleccione una persona:", opciones)
            
            if seleccion:
                doc_identidad = seleccion.split(" - ")[0]
                persona = self.nPersona.obtener_persona(doc_identidad)
                
                if persona:
                    with st.form("form_editar"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            nombre = st.text_input("Nombre*", value=persona.get('nombre', ''))
                            apellido = st.text_input("Apellido*", value=persona.get('apellido', ''))
                            
                        with col2:
                            email = st.text_input("Email", value=persona.get('email', ''))
                            telefono = st.text_input("Teléfono", value=persona.get('telefono', ''))
                        
                        edad = st.number_input("Edad", 
                                             min_value=0, 
                                             max_value=120, 
                                             value=persona.get('edad', 0))
                        direccion = st.text_area("Dirección", value=persona.get('direccion', ''))
                        
                        submitted = st.form_submit_button("💾 Actualizar Persona")
                        
                        if submitted:
                            if not nombre or not apellido:
                                st.error("Nombre y apellido son obligatorios")
                                return
                            
                            datos_actualizados = {
                                'nombre': nombre,
                                'apellido': apellido,
                                'email': email if email else None,
                                'telefono': telefono if telefono else None,
                                'edad': edad if edad > 0 else None,
                                'direccion': direccion if direccion else None
                            }
                            
                            try:
                                resultado = self.nPersona.actualizar_personas(datos_actualizados, doc_identidad)
                                st.success(f"✅ Persona actualizada exitosamente")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error al actualizar: {e}")
                
        except Exception as e:
            st.error(f"Error: {e}")
    
    def _eliminar_persona(self):
        """Interfaz para eliminar persona"""
        st.header("🗑️ Eliminar Persona")
        st.warning("⚠️ Esta acción no se puede deshacer")
        
        try:
            personas = self.nPersona.obtener_todas_personas()
            
            if not personas:
                st.info("No hay personas para eliminar.")
                return
            
            # Selector de persona
            opciones = [f"{p['docIdentidad']} - {p['nombre']} {p['apellido']}" for p in personas]
            seleccion = st.selectbox("Seleccione una persona para eliminar:", opciones)
            
            if seleccion:
                doc_identidad = seleccion.split(" - ")[0]
                persona = self.nPersona.obtener_persona(doc_identidad)
                
                if persona and st.button("🗑️ Confirmar Eliminación", type="primary"):
                    try:
                        self.nPersona.eliminar_persona(doc_identidad)
                        st.success(f"✅ Persona eliminada exitosamente")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error al eliminar: {e}")
                        
        except Exception as e:
            st.error(f"Error: {e}")
