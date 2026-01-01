# main.py
import streamlit as st
from capaPresentacion.pPersona import PPersona

def main():
    # Configurar página
    st.set_page_config(
        page_title="Sistema de Gestión de Personas",
        page_icon="👥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Título principal
    st.title("👥 Sistema de Gestión de Personas")
    st.markdown("---")
    
    # Inicializar y mostrar la aplicación
    try:
        app = PPersona()
        app.mostrar()
    except Exception as e:
        st.error(f"❌ Error al iniciar la aplicación: {e}")
        st.write("**Solución:**")
        st.write("1. Verifica que todos los archivos existan")
        st.write("2. Comprueba la conexión a Supabase")
        st.write("3. Asegúrate de tener los secrets configurados")

if __name__ == "__main__":
    main()
