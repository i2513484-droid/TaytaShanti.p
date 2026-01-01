# conexion.py
import os
from supabase import create_client, Client

class ConexionDB:
    def __init__(self):
        # En Streamlit Cloud, usa st.secrets en lugar de .env
        try:
            import streamlit as st
            self.url = st.secrets["SUPABASE_URL"]
            self.api_key = st.secrets["SUPABASE_API_KEY"]
        except:
            # Fallback para desarrollo local
            from dotenv import load_dotenv
            load_dotenv()
            self.url = os.getenv('SUPABASE_URL')
            self.api_key = os.getenv('SUPABASE_API_KEY')
        
    def get_conexion(self) -> Client:
        """Obtiene la conexión a Supabase"""
        if not hasattr(self, '_client') or self._client is None:
            self._client = create_client(self.url, self.api_key)
        return self._client
    
    def test_conexion(self):
        """Prueba la conexión"""
        try:
            client = self.get_conexion()
            # Realiza una consulta simple para verificar
            result = client.table('personas').select("*").limit(1).execute()
            return True, "Conexión exitosa"
        except Exception as e:
            return False, f"Error de conexión: {e}"

# Instancia global para reutilizar la conexión
conexion = ConexionDB()
