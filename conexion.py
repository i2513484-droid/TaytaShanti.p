import os
import streamlit as st
from supabase import create_client, Client

class Conexion:
    def __init__(self):
        """Inicializa la conexión a Supabase usando Streamlit secrets"""
        try:
            self.url = st.secrets["SUPABASE_URL"]
            self.api_key = st.secrets["SUPABASE_API_KEY"]
            self._client = None
        except KeyError as e:
            raise ValueError(f"Falta la configuración en secrets.toml: {e}")
    
    def get_client(self) -> Client:
        if self._client is None:
            try:
                self._client = create_client(self.url, self.api_key)
                print("✅ Conexión a Supabase establecida")
            except Exception as e:
                raise ConnectionError(f"No se pudo conectar a Supabase: {e}")
        return self._client
    
    def test_connection(self):
        try:
            client = self.get_client()
            response = client.table('personas').select("count", count="exact").execute()
            print("✅ Conexión a Supabase verificada correctamente")
            return True
        except Exception as e:
            print(f"❌ Error en conexión: {e}")
            return False
conexion_db = Conexion()
