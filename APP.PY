import streamlit as st
import pandas as pd
import pvlib
from pvlib import pvsystem, iotools, location, modelchain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
import plotly.graph_objects as go
from fpdf import FPDF
import io

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="CESAR CM Solar Design", layout="wide", page_icon="☀️")

# --- FUNCIONES DE REPORTE (PDF Y EXCEL) ---
def generar_pdf(nombre_sitio, panel, inversor, num_paneles, energia, ahorro, lat, lon):
    """Genera el reporte PDF para el cliente."""
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'CESAR CM INGENIERIA Y DISENO PROFESIONAL', 0, 1, 'C')
            self.line(10, 20, 200, 20)
            self.ln(10)

    pdf = PDF()
    pdf.add_page()
    
    # Cuerpo del reporte
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Reporte de Generacion: {nombre_sitio}", ln=True)
    
    pdf.set_font("Arial", '', 11)
    pdf.ln(5)
    pdf.cell(0, 8, f"Ubicacion: Lat {lat}, Lon {lon}", ln=True)
    pdf.cell(0, 8, f"Panel: {panel}", ln=True)
    pdf.cell(0, 8, f"Inversor: {inversor}", ln=True)
    pdf.cell(0, 8, f"Configuracion: {num_paneles} paneles en serie", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 100, 0) # Verde
    pdf.cell(0, 10, f"Energia Anual Estimada: {energia/1000:.2f} MWh/ano", ln=True)
    pdf.cell(0, 10, f"Ahorro Estimado: $ {ahorro:,.0f} COP", ln=True)
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, "Calculo realizado bajo estandares de ingenieria (NREL/PVLib).", 0, 1, 'C')
    
    # Retornamos los bytes del PDF
    return pdf.output(dest='S').encode('latin-1', 'replace')

def generar_excel(dataframe):
    """Genera el archivo Excel para ingeniería."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        dataframe.to_excel(writer, sheet_name='Simulacion_Horaria')
    return output.getvalue()

# --- FUNCIONES DE CACHÉ (OPTIMIZACIÓN) ---
@st.cache_data
def cargar_bases_datos():
    modulos = pvsystem.retrieve_sam('CECMod')
    inversores = pvsystem.retrieve_sam('CECInverter')
    return modulos, inversores

@st.cache_data
def obtener_clima(lat, lon, anio):
    try:
        data, metadata = iotools.get_power(
            latitude=lat, longitude=lon,
            start=pd.Timestamp(f'{anio}-01-01'),
            end=pd.Timestamp(f'{anio}-12-31'),
            user_community='SSE', timeout=45
        )
        return data
    except Exception:
        return None

# --- INTERFAZ GRÁFICA ---
st.title("☀️ CESAR CM INGENIERÍA Y DISEÑO PROFESIONAL")
st.markdown("Software de Simulación Fotovoltaica de Alta Precisión")
st.markdown("---")

# Carga de datos inicial
try:
    with st.spinner('Inicializando motores de cálculo...'):
        db_paneles, db_inversores = cargar_bases_datos()
except Exception as e:
    st.error("Error cargando bases de datos. Verifique su conexión a internet.")
    st.stop()

# BARRA LATERAL
st.sidebar.header("📍 Configuración")
nombre_sitio = st.sidebar.text_input("Nombre del Proyecto", "Planta Sede Principal")
lat = st.sidebar.number_input("Latitud", value=4.6097, format="%.4f")
lon = st.sidebar.number_input("Longitud", value=-74.0817, format="%.4f")
alt = st.sidebar.number_input("Altitud (msnm)", value=2600)

st.sidebar.markdown("---")
st.sidebar.header("⚡ Equipos")

# Filtros de búsqueda
filtro_p = st.sidebar.text_input("Buscar Panel (Marca)", "Jinko")
opciones_p = [m for m in db_paneles.columns if filtro_p.lower() in m.lower()]
panel_elegido = st.sidebar.selectbox("Modelo de Panel", options=opciones_p)

filtro_i = st.sidebar.text_input("Buscar Inversor (Marca)", "Fronius")
opciones_i = [i for i in db_inversores.columns if filtro_i.lower() in i.lower()]
inv_elegido = st.sidebar.selectbox("Modelo de Inversor", options=opciones_i)

num_paneles = st.sidebar.slider("Paneles por String", 1, 30, 10)
tarifa = st.sidebar.number_input("Tarifa ($/kWh)", value=850)

# BOTÓN DE CÁLCULO
if st.sidebar.button("CALCULAR PROYECTO", type="primary"):
    
    # 1. Mapa
    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
    
    # 2. Clima
    with st.spinner('Descargando datos satelitales NASA POWER...'):
        clima = obtener_clima(lat, lon, 2020)
        
    if clima is not None:
        # 3. Simulación
        loc = location.Location(lat, lon, altitude=alt, name=nombre_sitio)
        mount = pvsystem.FixedMount(surface_tilt=lat, surface_azimuth=180)
        
        sistema = pvsystem.PVSystem(
            mounts=[mount],
            module_parameters=db_paneles[panel_elegido],
            inverter_parameters=db_inversores[inv_elegido],
            temperature_model_parameters=TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass'],
            modules_per_string=num_paneles,
            strings_per_inverter=1
        )
        
        mc = modelchain.ModelChain(sistema, loc, aoi_model='physical', spectral_model='no_loss')
        mc.run_model(clima)
        
        # 4. Resultados
        energia_anual = mc.results.ac.sum() / 1000 # kWh
        ahorro = energia_anual * tarifa
        potencia_pico = (num_paneles * db_paneles[panel_elegido]['STC']) / 1000 # kWp
        
        # KPIs
        st.subheader("📊 Resultados Ejecutivos")
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Energía Año 1", f"{energia_anual/1000:.2f} MWh")
        kpi2.metric("Ahorro Estimado", f"$ {ahorro:,.0f} COP")
        kpi3.metric("Potencia Instalada", f"{potencia_pico:.2f} kWp")
        
        # Gráfica
        st.subheader("📈 Perfil de Generación Diaria (Promedio)")
        diario = mc.results.ac.groupby(mc.results.ac.index.hour).mean()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=diario.index, y=diario.values, fill='tozeroy', line=dict(color='orange'), name='Potencia'))
        fig.update_layout(xaxis_title="Hora", yaxis_title="Potencia (W)")
        st.plotly_chart(fig, use_container_width=True)
        
        # --- ZONA DE DESCARGAS (INTEGRADA) ---
        st.markdown("---")
        st.subheader("📥 Descargar Entregables")
        col_pdf, col_xls = st.columns(2)
        
        # Generar PDF en memoria
        pdf_bytes = generar_pdf(nombre_sitio, panel_elegido, inv_elegido, num_paneles, energia_anual, ahorro, lat, lon)
        col_pdf.download_button(
            label="📄 Reporte PDF (Cliente)",
            data=pdf_bytes,
            file_name=f"Reporte_{nombre_sitio}.pdf",
            mime="application/pdf"
        )
        
        # Generar Excel en memoria
        xls_bytes = generar_excel(mc.results.ac)
        col_xls.download_button(
            label="📊 Datos Excel (Ingeniería)",
            data=xls_bytes,
            file_name=f"Datos_{nombre_sitio}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    else:
        st.error("No se pudo conectar con la base de datos climática. Intente de nuevo.")
else:
    st.info("👈 Configure los parámetros en el menú izquierdo y presione CALCULAR PROYECTO.")
