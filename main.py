# main.py - Versión para diagnosticar
import streamlit as st
import traceback

def main():
    st.set_page_config(page_title="Debug App", layout="wide")
    st.title("🔧 Debug de la Aplicación")
    
    # Botón para probar cada capa
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Probar Importaciones"):
            try:
                from capaPresentacion.pPersona import PPersona
                st.success("✅ PPersona importado")
                
                from capaLogica.nPersona import NPersona
                st.success("✅ NPersona importado")
                
                from capaDatos.dPersona import DPersona
                st.success("✅ DPersona importado")
                
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.code(traceback.format_exc())
    
    with col2:
        if st.button("Probar Instancias"):
            try:
                from capaDatos.dPersona import DPersona
                d = DPersona()
                st.success("✅ DPersona instanciado")
                st.write("Métodos disponibles:", [m for m in dir(d) if not m.startswith('_')])
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with col3:
        if st.button("Probar Conexión BD"):
            try:
                from capaDatos.dPersona import DPersona
                d = DPersona()
                personas = d.obtener_todos()
                st.success(f"✅ Conexión OK. Personas: {len(personas) if personas else 0}")
            except Exception as e:
                st.error(f"❌ Error BD: {e}")
    
    # Separador
    st.markdown("---")
    
    # Iniciar la app real si todo está bien
    if st.button("🚀 Iniciar Aplicación Completa"):
        try:
            from capaPresentacion.pPersona import PPersona
            app = PPersona()
            app.mostrar()
        except Exception as e:
            st.error(f"❌ Error al iniciar app: {e}")
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
