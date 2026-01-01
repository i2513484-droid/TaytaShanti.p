# conexion.py (en la RAIZ del proyecto)
import streamlit as st
from supabase import create_client, Client

class ConexionDB:
    """
    Clase para manejar la conexión a Supabase.
    Usa patrón singleton para una sola instancia.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConexionDB, cls).__new__(cls)
            cls._instance._inicializar()
        return cls._instance
    
    def _inicializar(self):
        """Inicializa las credenciales desde Streamlit secrets"""
        try:
            # Para producción (Streamlit Cloud)
            self.url = st.secrets.get("SUPABASE_URL")
            self.api_key = st.secrets.get("SUPABASE_API_KEY")
            
            if not self.url or not self.api_key:
                raise ValueError("Credenciales de Supabase no encontradas en secrets")
                
            self._client = None
            print("✅ Configuración de Supabase cargada desde secrets")
            
        except Exception as e:
            # Fallback para desarrollo local
            try:
                from dotenv import load_dotenv
                import os
                load_dotenv()
                
                self.url = os.getenv('SUPABASE_URL')
                self.api_key = os.getenv('SUPABASE_API_KEY')
                
                if not self.url or not self.api_key:
                    raise ValueError("Credenciales no encontradas en .env")
                    
                self._client = None
                print("✅ Configuración de Supabase cargada desde .env")
                
            except:
                raise ValueError(f"No se pudieron cargar las credenciales: {e}")
    
    def get_client(self) -> Client:
        """Obtiene el cliente de Supabase (crea la conexión si no existe)"""
        if self._client is None:
            try:
                self._client = create_client(self.url, self.api_key)
                print("✅ Conexión a Supabase establecida")
            except Exception as e:
                raise ConnectionError(f"Error al conectar con Supabase: {e}")
        return self._client
    
    def test_connection(self):
        """Prueba la conexión a Supabase"""
        try:
            client = self.get_client()
            # Consulta simple para verificar conexión
            response = client.table('personas').select("count", count="exact").limit(1).execute()
            print(f"✅ Conexión exitosa. Tabla 'personas' accesible")
            return True
        except Exception as e:
            print(f"❌ Error en conexión: {e}")
            return False

# Instancia global para importar en otros archivos
conexion_db = ConexionDB()
