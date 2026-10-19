# -*- coding: utf-8 -*-
"""
DASHBOARD FINANCIERO WEB - REPARACIONES GENERALES EN INSTALACIONES DE ESOBADES
Versión para Streamlit (Cloud)
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

# Configuración de página
st.set_page_config(
    page_title="Dashboard Financiero • ESOBADES",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para los colores Azul Claro y Verde
st.markdown("""
<style>
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 25px;
    }
    .kpi-card {
        background-color: #1E293B;
        border-radius: 8px;
        padding: 15px 20px;
        flex: 1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid;
    }
    .kpi-card h4 {
        color: #94A3B8;
        font-size: 0.9rem;
        margin-bottom: 5px;
        font-weight: 600;
        text-transform: uppercase;
    }
    .kpi-card.total { border-color: #60A5FA; }
    .kpi-card.propia { border-color: #3B82F6; }
    .kpi-card.ecovida { border-color: #10B981; }
    
    .kpi-card .usd {
        color: #FFFFFF;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
    }
    .kpi-card .bs {
        color: #CBD5E1;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 5px;
    }
    .kpi-card .subtext {
        color: #64748B;
        font-size: 0.8rem;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Datos precargados (Fallback por si no se sube un archivo Excel)
DATOS_PRECARGADOS = [
  {"id": 1, "fecha": "27-08-2026", "concepto": "MANGO CENTER", "bs": 1935167.0, "usd": 2445.4923, "tasa": 791.32, "origen": "INVERSIÓN PROPIA"},
  {"id": 2, "fecha": "27-08-2026", "concepto": "FLETE", "bs": 56000.0, "usd": 70.7678, "tasa": 791.32, "origen": "INVERSIÓN PROPIA"},
  {"id": 3, "fecha": "27-08-2026", "concepto": "CEMENTO", "bs": 33968.28, "usd": 42.9261, "tasa": 791.32, "origen": "INVERSIÓN PROPIA"},
  {"id": 4, "fecha": "27-08-2026", "concepto": "PEINILLA-HOJAS-CARTUCHOS", "bs": 18991.68, "usd": 24.0, "tasa": 791.32, "origen": "INVERSIÓN PROPIA"},
  {"id": 5, "fecha": "27-08-2026", "concepto": "ferreteria global center", "bs": 279005.18, "usd": 352.582, "tasa": 791.32, "origen": "ECOVIDA"},
  {"id": 6, "fecha": "27-08-2026", "concepto": "GLOBAL CENTER", "bs": 70164.92, "usd": 88.6682, "tasa": 791.32, "origen": "ECOVIDA"},
  {"id": 7, "fecha": "27-08-2026", "concepto": "CEMENTO", "bs": 33968.28, "usd": 42.9261, "tasa": 791.32, "origen": "ECOVIDA"},
  {"id": 8, "fecha": "27-08-2026", "concepto": "FLETE DE DRYWALL", "bs": 11869.8, "usd": 15.0, "tasa": 791.32, "origen": "INVERSIÓN PROPIA"},
  {"id": 9, "fecha": "27-08-2026", "concepto": "DRYWALL C/PERFILES", "bs": 70261.9, "usd": 88.7908, "tasa": 791.32, "origen": "ECOVIDA"},
  {"id": 10, "fecha": "27-08-2026", "concepto": "LLANA-SEGUETA-OTROS", "bs": 9495.84, "usd": 12.0, "tasa": 791.32, "origen": "INVERSIÓN PROPIA"},
  {"id": 11, "fecha": "27-08-2026", "concepto": "TOBO DE ALBA", "bs": 6330.56, "usd": 8.0, "tasa": 791.32, "origen": "INVERSIÓN PROPIA"},
  {"id": 12, "fecha": "27-08-2026", "concepto": "AGUA - HIELO", "bs": 10928.12, "usd": 13.81, "tasa": 791.32, "origen": "ECOVIDA"},
  {"id": 13, "fecha": "29-08-2026", "concepto": "electricista", "bs": 197917.5, "usd": 250.0, "tasa": 791.67, "origen": "INVERSIÓN PROPIA"},
  {"id": 14, "fecha": "29-08-2026", "concepto": "nominas", "bs": 303470.8611, "usd": 383.33, "tasa": 791.67, "origen": "INVERSIÓN PROPIA"},
  {"id": 15, "fecha": "29-08-2026", "concepto": "lamparas", "bs": 53959.56, "usd": 68.1592, "tasa": 791.67, "origen": "INVERSIÓN PROPIA"},
  {"id": 16, "fecha": "29-08-2026", "concepto": "ferreteria el llano", "bs": 453839.47, "usd": 573.2685, "tasa": 791.67, "origen": "ECOVIDA"},
  {"id": 17, "fecha": "29-08-2026", "concepto": "cabezal guadaña", "bs": 15900.0, "usd": 20.0841, "tasa": 791.67, "origen": "ECOVIDA"},
  {"id": 18, "fecha": "29-08-2026", "concepto": "tarslado de andamios", "bs": 15833.4, "usd": 20.0, "tasa": 791.67, "origen": "INVERSIÓN PROPIA"},
  {"id": 19, "fecha": "29-08-2026", "concepto": "botellon de agua y hielo", "bs": 11875.05, "usd": 15.0, "tasa": 791.67, "origen": "INVERSIÓN PROPIA"},
  {"id": 20, "fecha": "29-08-2026", "concepto": "clavitos de drywall", "bs": 791.67, "usd": 1.0, "tasa": 791.67, "origen": "ECOVIDA"},
  {"id": 21, "fecha": "29-08-2026", "concepto": "hielo", "bs": 1583.34, "usd": 2.0, "tasa": 791.67, "origen": "INVERSIÓN PROPIA"},
  {"id": 22, "fecha": "29-08-2026", "concepto": "tornillos drywall negros", "bs": 5541.69, "usd": 7.0, "tasa": 791.67, "origen": "INVERSIÓN PROPIA"},
  {"id": 23, "fecha": "29-08-2026", "concepto": "gasolina", "bs": 15833.4, "usd": 20.0, "tasa": 791.67, "origen": "INVERSIÓN PROPIA"},
  {"id": 24, "fecha": "29-08-2026", "concepto": "mango center", "bs": 311476.57, "usd": 393.4424, "tasa": 791.67, "origen": "ECOVIDA"},
  {"id": 25, "fecha": "29-08-2026", "concepto": "cemento", "bs": 9398.51, "usd": 11.8718, "tasa": 791.67, "origen": "ECOVIDA"},
  {"id": 26, "fecha": "29-08-2026", "concepto": "pico de solplete", "bs": 20892.17, "usd": 26.39, "tasa": 791.67, "origen": "ECOVIDA"},
  {"id": 27, "fecha": "29-08-2026", "concepto": "pico de solplete", "bs": 28468.45, "usd": 35.96, "tasa": 791.67, "origen": "ECOVIDA"},
  {"id": 28, "fecha": "29-08-2026", "concepto": "pintura montana", "bs": 29291.79, "usd": 37.0, "tasa": 791.67, "origen": "ECOVIDA"},
  {"id": 29, "fecha": "29-08-2026", "concepto": "mobiliario de Oficina Valencia", "bs": 1862007.84, "usd": 2352.0, "tasa": 791.67, "origen": "INVERSIÓN PROPIA"},
  {"id": 30, "fecha": "29-08-2026", "concepto": "implementos de seguridad", "bs": 336459.75, "usd": 425.0, "tasa": 791.67, "origen": "INVERSIÓN PROPIA"},
  {"id": 31, "fecha": "31-08-2026", "concepto": "HIELO", "bs": 1430.0, "usd": 1.7988, "tasa": 794.99, "origen": "INVERSIÓN PROPIA"},
  {"id": 32, "fecha": "31-08-2026", "concepto": "AGUA Y THINNER", "bs": 12115.0, "usd": 15.2392, "tasa": 794.99, "origen": "INVERSIÓN PROPIA"},
  {"id": 33, "fecha": "31-08-2026", "concepto": "GRAFIADO ADELANTO", "bs": 227826.0, "usd": 286.5772, "tasa": 794.99, "origen": "INVERSIÓN PROPIA"},
  {"id": 34, "fecha": "31-08-2026", "concepto": "PROTECTOR DE AIRE ACOND.", "bs": 198747.5, "usd": 250.0, "tasa": 794.99, "origen": "INVERSIÓN PROPIA"},
  {"id": 35, "fecha": "31-08-2026", "concepto": "GRAPAS", "bs": 3577.455, "usd": 4.5, "tasa": 794.99, "origen": "INVERSIÓN PROPIA"},
  {"id": 36, "fecha": "31-08-2026", "concepto": "BREACKERS", "bs": 7623.78, "usd": 9.5898, "tasa": 794.99, "origen": "INVERSIÓN PROPIA"},
  {"id": 37, "fecha": "31-08-2026", "concepto": "NIVEL, CLAVOS, ACEITE 2 TIEMPOS", "bs": 30621.92, "usd": 38.5186, "tasa": 794.99, "origen": "INVERSIÓN PROPIA"},
  {"id": 38, "fecha": "31-08-2026", "concepto": "CONEXIONES ELECTRICAS", "bs": 3452.0, "usd": 4.3422, "tasa": 794.99, "origen": "INVERSIÓN PROPIA"},
  {"id": 39, "fecha": "31-08-2026", "concepto": "TORNILLOS GARRAPATEROS", "bs": 3179.0, "usd": 3.9988, "tasa": 794.99, "origen": "INVERSIÓN PROPIA"},
  {"id": 40, "fecha": "31-08-2026", "concepto": "PEINILLA", "bs": 12719.84, "usd": 16.0, "tasa": 794.99, "origen": "INVERSIÓN PROPIA"},
  {"id": 41, "fecha": "01-09-2026", "concepto": "CASA PRO FILTRO Y GUANTES Y ESCALER", "bs": 223542.34, "usd": 279.4279, "tasa": 800.0, "origen": "INVERSIÓN PROPIA"},
  {"id": 42, "fecha": "01-09-2026", "concepto": "GLOBAL CENTER  CANDADOS", "bs": 58303.92, "usd": 72.8799, "tasa": 800.0, "origen": "INVERSIÓN PROPIA"},
  {"id": 43, "fecha": "01-09-2026", "concepto": "CASA DEL ELECTRODO", "bs": 34338.41, "usd": 42.923, "tasa": 800.0, "origen": "INVERSIÓN PROPIA"},
  {"id": 44, "fecha": "01-09-2026", "concepto": "CASA DEL ELECTRODO", "bs": 120406.75, "usd": 150.5084, "tasa": 800.0, "origen": "INVERSIÓN PROPIA"},
  {"id": 45, "fecha": "01-09-2026", "concepto": "HIELO Y AGUA", "bs": 2150.0, "usd": 2.6875, "tasa": 800.0, "origen": "INVERSIÓN PROPIA"},
  {"id": 46, "fecha": "01-09-2026", "concepto": "VASOS Y REEFRESCO", "bs": 3470.0, "usd": 4.3375, "tasa": 800.0, "origen": "INVERSIÓN PROPIA"},
  {"id": 47, "fecha": "01-09-2026", "concepto": "CANDADOS COMISI", "bs": 15.0, "usd": 0.0187, "tasa": 800.0, "origen": "INVERSIÓN PROPIA"},
  {"id": 48, "fecha": "01-09-2026", "concepto": "IMPRESIÓN JUAN CARLOS", "bs": 7200.0, "usd": 9.0, "tasa": 800.0, "origen": "INVERSIÓN PROPIA"},
  {"id": 49, "fecha": "01-09-2026", "concepto": "GUADAÑA", "bs": 15168.0, "usd": 18.96, "tasa": 800.0, "origen": "INVERSIÓN PROPIA"},
  {"id": 50, "fecha": "01-09-2026", "concepto": "traslado de tanque metalico", "bs": 120228.0, "usd": 150.0, "tasa": 801.52, "origen": "INVERSIÓN PROPIA"},
  {"id": 51, "fecha": "02-09-2026", "concepto": "CEMENTO -DISCO-LIJA-LIMPOTEX", "bs": 19659.68, "usd": 24.5384, "tasa": 801.18, "origen": "INVERSIÓN PROPIA"},
  {"id": 52, "fecha": "02-09-2026", "concepto": "FERRETERIA ALONDRA", "bs": 11961.47, "usd": 14.9298, "tasa": 801.18, "origen": "INVERSIÓN PROPIA"},
  {"id": 53, "fecha": "02-09-2026", "concepto": "CERRADURA", "bs": 19899.25, "usd": 24.8374, "tasa": 801.18, "origen": "INVERSIÓN PROPIA"},
  {"id": 54, "fecha": "02-09-2026", "concepto": "TORNILLOS", "bs": 2163.16, "usd": 2.7, "tasa": 801.18, "origen": "INVERSIÓN PROPIA"},
  {"id": 55, "fecha": "03-09-2026", "concepto": "VIDRIOS", "bs": 67581.6, "usd": 83.9617, "tasa": 804.91, "origen": "ECOVIDA"},
  {"id": 56, "fecha": "03-09-2026", "concepto": "PASTA FROFESIONAL", "bs": 11184.28, "usd": 13.8951, "tasa": 804.91, "origen": "ECOVIDA"},
  {"id": 57, "fecha": "03-09-2026", "concepto": "AGUA Y HIELO", "bs": 3717.26, "usd": 4.6182, "tasa": 804.91, "origen": "ECOVIDA"},
  {"id": 58, "fecha": "03-09-2026", "concepto": "TUBOS pvc", "bs": 96588.17, "usd": 119.9987, "tasa": 804.91, "origen": "ECOVIDA"},
  {"id": 59, "fecha": "03-09-2026", "concepto": "CANALERO", "bs": 140206.0, "usd": 174.1884, "tasa": 804.91, "origen": "INVERSIÓN PROPIA"},
  {"id": 60, "fecha": "03-09-2026", "concepto": "MANGO CENTER", "bs": 33096.19, "usd": 41.1179, "tasa": 804.91, "origen": "ECOVIDA"},
  {"id": 61, "fecha": "03-09-2026", "concepto": "Combustible", "bs": 112687.4, "usd": 140.0, "tasa": 804.91, "origen": "ECOVIDA"},
  {"id": 62, "fecha": "03-09-2026", "concepto": "ESCOBA Y BOLSAS", "bs": 9433.24, "usd": 11.6836, "tasa": 807.39, "origen": "ECOVIDA"},
  {"id": 63, "fecha": "03-09-2026", "concepto": "PVC Y LUCES", "bs": 100641.16, "usd": 124.65, "tasa": 807.39, "origen": "ECOVIDA"},
  {"id": 64, "fecha": "03-09-2026", "concepto": "PERSIANA", "bs": 65398.59, "usd": 81.0, "tasa": 807.39, "origen": "ECOVIDA"},
  {"id": 65, "fecha": "03-09-2026", "concepto": "MANGO CENTER ARO", "bs": 743113.27, "usd": 920.3895, "tasa": 807.39, "origen": "ECOVIDA"},
  {"id": 66, "fecha": "03-09-2026", "concepto": "TIRROS", "bs": 4353.17, "usd": 5.3917, "tasa": 807.39, "origen": "ECOVIDA"},
  {"id": 67, "fecha": "03-09-2026", "concepto": "LLAVES LAVAMANOS", "bs": 12016.22, "usd": 14.8828, "tasa": 807.39, "origen": "ECOVIDA"},
  {"id": 68, "fecha": "03-09-2026", "concepto": "PUERTAS", "bs": 201847.5, "usd": 250.0, "tasa": 807.39, "origen": "INVERSIÓN PROPIA"},
  {"id": 69, "fecha": "03-09-2026", "concepto": "DRYWALL", "bs": 177625.8, "usd": 220.0, "tasa": 807.39, "origen": "INVERSIÓN PROPIA"},
  {"id": 70, "fecha": "03-09-2026", "concepto": "HERRERO ADELANTO", "bs": 40369.5, "usd": 50.0, "tasa": 807.39, "origen": "INVERSIÓN PROPIA"},
  {"id": 71, "fecha": "03-09-2026", "concepto": "HERRERIA", "bs": 11312.0, "usd": 14.0106, "tasa": 807.39, "origen": "INVERSIÓN PROPIA"},
  {"id": 73, "fecha": "03-09-2026", "concepto": "deuda ecovida", "bs": 16088.0, "usd": 20.0, "tasa": 804.4, "origen": "INVERSIÓN PROPIA"},
  {"id": 74, "fecha": "03-09-2026", "concepto": "prestamo eudes casa", "bs": 40220.0, "usd": 50.0, "tasa": 804.4, "origen": "INVERSIÓN PROPIA"},
  {"id": 75, "fecha": "03-09-2026", "concepto": "deuda ecovida", "bs": 11312.0, "usd": 14.0627, "tasa": 804.4, "origen": "INVERSIÓN PROPIA"},
  {"id": 76, "fecha": "03-09-2026", "concepto": "discos de corte", "bs": 10000.0, "usd": 12.3894, "tasa": 807.14, "origen": "INVERSIÓN PROPIA"},
  {"id": 77, "fecha": "03-09-2026", "concepto": "hielo", "bs": 1400.0, "usd": 1.7345, "tasa": 807.14, "origen": "ECOVIDA"},
  {"id": 78, "fecha": "03-09-2026", "concepto": "gasolina", "bs": 33781.0, "usd": 41.8527, "tasa": 807.14, "origen": "ECOVIDA"},
  {"id": 79, "fecha": "03-09-2026", "concepto": "hielo, disco corte, botellon", "bs": 21438.0, "usd": 26.5604, "tasa": 807.14, "origen": "ECOVIDA"},
  {"id": 80, "fecha": "07-09-2026", "concepto": "COPIAS LICITACION", "bs": 58685.0, "usd": 72.1176, "tasa": 813.74, "origen": "INVERSIÓN PROPIA"},
  {"id": 81, "fecha": "07-09-2026", "concepto": "PUERTA DE MADERA", "bs": 12210.0, "usd": 15.0048, "tasa": 813.74, "origen": "INVERSIÓN PROPIA"},
  {"id": 82, "fecha": "07-09-2026", "concepto": "GRAFIADO EDF 1", "bs": 53707.0, "usd": 66.0002, "tasa": 813.74, "origen": "INVERSIÓN PROPIA"},
  {"id": 83, "fecha": "07-09-2026", "concepto": "ADELANTO DE NOMINA", "bs": 25000.0, "usd": 30.7223, "tasa": 813.74, "origen": "INVERSIÓN PROPIA"},
  {"id": 84, "fecha": "08-09-2026", "concepto": "CEMENTO 2", "bs": 19552.7, "usd": 24.0002, "tasa": 814.69, "origen": "INVERSIÓN PROPIA"},
  {"id": 85, "fecha": "08-09-2026", "concepto": "ESMALTE VERDE 3", "bs": 90440.36, "usd": 111.012, "tasa": 814.69, "origen": "INVERSIÓN PROPIA"},
  {"id": 86, "fecha": "08-09-2026", "concepto": "MANILLA DE PUERTA", "bs": 15080.0, "usd": 18.5101, "tasa": 814.69, "origen": "INVERSIÓN PROPIA"},
  {"id": 87, "fecha": "08-09-2026", "concepto": "IMPRESIÓN LICITACION AG", "bs": 42560.0, "usd": 52.2407, "tasa": 814.69, "origen": "INVERSIÓN PROPIA"},
  {"id": 88, "fecha": "08-09-2026", "concepto": "NOMINA AYUDANTE", "bs": 38754.54, "usd": 47.5697, "tasa": 814.69, "origen": "INVERSIÓN PROPIA"},
  {"id": 89, "fecha": "08-09-2026", "concepto": "COMPUADORA   268 USDT", "bs": 262004.304, "usd": 321.6, "tasa": 814.69, "origen": "INVERSIÓN PROPIA"},
  {"id": 90, "fecha": "08-09-2026", "concepto": "PORTATIL    RIZEN 7    USDT", "bs": 400827.48, "usd": 492.0, "tasa": 814.69, "origen": "INVERSIÓN PROPIA"},
  {"id": 91, "fecha": "09-09-2026", "concepto": "HIPERMERCADO AGROPECUARIO", "bs": 8818.69, "usd": 10.7532, "tasa": 820.1, "origen": "INVERSIÓN PROPIA"},
  {"id": 92, "fecha": "09-09-2026", "concepto": "MANGO CENTER", "bs": 70619.03, "usd": 86.1103, "tasa": 820.1, "origen": "INVERSIÓN PROPIA"},
  {"id": 93, "fecha": "09-09-2026", "concepto": "TUBO DE HIERRO", "bs": 37000.0, "usd": 45.1164, "tasa": 820.1, "origen": "INVERSIÓN PROPIA"},
  {"id": 94, "fecha": "09-09-2026", "concepto": "AGUA Y HIELO", "bs": 2600.0, "usd": 3.1703, "tasa": 820.1, "origen": "INVERSIÓN PROPIA"},
  {"id": 95, "fecha": "09-09-2026", "concepto": "FERRETERIA LOPEZ", "bs": 65000.0, "usd": 79.2586, "tasa": 820.1, "origen": "INVERSIÓN PROPIA"},
  {"id": 96, "fecha": "10-09-2026", "concepto": "CERRADURA DE EMPOTRAR", "bs": 16473.99, "usd": 19.8, "tasa": 832.02, "origen": "ECOVIDA"},
  {"id": 97, "fecha": "11-09-2026", "concepto": "NOMINA", "bs": 454840.3734, "usd": 546.67, "tasa": 832.02, "origen": "ECOVIDA"},
  {"id": 98, "fecha": "11-09-2026", "concepto": "LLAVE DE CHORRO", "bs": 5349.91, "usd": 6.43, "tasa": 832.02, "origen": "INVERSIÓN PROPIA"},
  {"id": 99, "fecha": "11-09-2026", "concepto": "HIELO", "bs": 1498.48, "usd": 1.801, "tasa": 832.02, "origen": "INVERSIÓN PROPIA"},
  {"id": 100, "fecha": "12-09-2026", "concepto": "ESTUCO GLOBAL CENTER", "bs": 21063.28, "usd": 25.3158, "tasa": 832.02, "origen": "INVERSIÓN PROPIA"},
  {"id": 101, "fecha": "12-09-2026", "concepto": "AGUA, HIELO", "bs": 3678.0, "usd": 4.4206, "tasa": 832.02, "origen": "INVERSIÓN PROPIA"},
  {"id": 102, "fecha": "14-09-2026", "concepto": "GRAFIADO", "bs": 204000.0, "usd": 244.0, "tasa": 836.07, "origen": "INVERSIÓN PROPIA"},
  {"id": 103, "fecha": "15-09-2026", "concepto": "MANGO CENTER", "bs": 83543.15, "usd": 98.6913, "tasa": 846.51, "origen": "INVERSIÓN PROPIA"},
  {"id": 104, "fecha": "15-09-2026", "concepto": "REPUESTO GUADAÑA", "bs": 8325.0, "usd": 9.8345, "tasa": 846.51, "origen": "INVERSIÓN PROPIA"},
  {"id": 105, "fecha": "16-09-2026", "concepto": "mango center 14-09-2026", "bs": 411989.94, "usd": 489.183, "tasa": 842.2, "origen": "ECOVIDA"},
  {"id": 106, "fecha": "16-09-2026", "concepto": "mango center 16-09-2026", "bs": 114537.87, "usd": 135.306, "tasa": 846.51, "origen": "ECOVIDA"},
  {"id": 107, "fecha": "16-09-2026", "concepto": "mango center 17-09-2026", "bs": 27385.4, "usd": 32.3509, "tasa": 846.51, "origen": "ECOVIDA"},
  {"id": 108, "fecha": "16-09-2026", "concepto": "global center 17-9-2026", "bs": 57236.72, "usd": 67.6149, "tasa": 846.51, "origen": "ECOVIDA"},
  {"id": 109, "fecha": "16-09-2026", "concepto": "montana  17-9-2026", "bs": 59320.78, "usd": 70.0, "tasa": 847.44, "origen": "ECOVIDA"},
  {"id": 110, "fecha": "16-09-2026", "concepto": "grafiado", "bs": 413550.72, "usd": 488.0, "tasa": 847.44, "origen": "INVERSIÓN PROPIA"},
  {"id": 111, "fecha": "16-09-2026", "concepto": "herrero", "bs": 110167.2, "usd": 130.0, "tasa": 847.44, "origen": "INVERSIÓN PROPIA"},
  {"id": 112, "fecha": "16-09-2026", "concepto": "hielo", "bs": 1500.0, "usd": 1.77, "tasa": 847.44, "origen": "INVERSIÓN PROPIA"},
  {"id": 113, "fecha": "16-09-2026", "concepto": "agua potable", "bs": 2542.32, "usd": 3.0, "tasa": 847.44, "origen": "INVERSIÓN PROPIA"},
  {"id": 114, "fecha": "16-09-2026", "concepto": "limpieza instalaciones", "bs": 25423.2, "usd": 30.0, "tasa": 847.44, "origen": "INVERSIÓN PROPIA"},
  {"id": 115, "fecha": "19-09-2026", "concepto": "cerradura", "bs": 8800.0, "usd": 10.9838, "tasa": 801.18, "origen": "INVERSIÓN PROPIA"},
  {"id": 116, "fecha": "19-09-2026", "concepto": "hoja de guadaña", "bs": 6552.09, "usd": 8.178, "tasa": 801.18, "origen": "INVERSIÓN PROPIA"},
  {"id": 117, "fecha": "19-09-2026", "concepto": "agua hielo", "bs": 3500.0, "usd": 4.1197, "tasa": 849.57, "origen": "INVERSIÓN PROPIA"},
  {"id": 118, "fecha": "25-09-2026", "concepto": "hielo", "bs": 2000.0, "usd": 2.3374, "tasa": 855.66, "origen": "INVERSIÓN PROPIA"},
  {"id": 119, "fecha": "25-09-2026", "concepto": "tirros", "bs": 5161.35, "usd": 6.032, "tasa": 855.66, "origen": "INVERSIÓN PROPIA"},
  {"id": 120, "fecha": "25-09-2026", "concepto": "CANALERO", "bs": 149740.5, "usd": 175.0, "tasa": 855.66, "origen": "ECOVIDA"},
  {"id": 121, "fecha": "25-09-2026", "concepto": "ANDAMIOS", "bs": 154018.8, "usd": 180.0, "tasa": 855.66, "origen": "ECOVIDA"},
  {"id": 122, "fecha": "25-09-2026", "concepto": "NOMINA", "bs": 500561.1, "usd": 585.0, "tasa": 855.66, "origen": "ECOVIDA"},
  {"id": 123, "fecha": "26-09-2026", "concepto": "ARRANQUE DE GUADAÑA", "bs": 14546.22, "usd": 17.0, "tasa": 855.66, "origen": "INVERSIÓN PROPIA"},
  {"id": 124, "fecha": "26-09-2026", "concepto": "HIELO", "bs": 1542.61, "usd": 1.8028, "tasa": 855.66, "origen": "INVERSIÓN PROPIA"},
  {"id": 125, "fecha": "28-09-2026", "concepto": "MANGO CENTER", "bs": 84615.49, "usd": 98.7334, "tasa": 857.01, "origen": "ECOVIDA"},
  {"id": 126, "fecha": "28-09-2026", "concepto": "HIELO", "bs": 3000.0, "usd": 3.5005, "tasa": 857.01, "origen": "INVERSIÓN PROPIA"},
  {"id": 127, "fecha": "29-09-2026", "concepto": "impresora", "bs": 201604.15, "usd": 235.0, "tasa": 857.89, "origen": "INVERSIÓN PROPIA"},
  {"id": 128, "fecha": "29-09-2026", "concepto": "hielo", "bs": 6000.0, "usd": 6.9939, "tasa": 857.89, "origen": "INVERSIÓN PROPIA"},
  {"id": 129, "fecha": "29-09-2026", "concepto": "limpieza general", "bs": 26000.0, "usd": 30.3069, "tasa": 857.89, "origen": "INVERSIÓN PROPIA"},
  {"id": 130, "fecha": "29-09-2026", "concepto": "gasolina del camion", "bs": 60052.0, "usd": 69.9997, "tasa": 857.89, "origen": "INVERSIÓN PROPIA"},
  {"id": 131, "fecha": "29-09-2026", "concepto": "mango center", "bs": 175859.04, "usd": 204.9902, "tasa": 857.89, "origen": "INVERSIÓN PROPIA"},
  {"id": 132, "fecha": "29-09-2026", "concepto": "brochas", "bs": 3668.92, "usd": 4.2767, "tasa": 857.89, "origen": "INVERSIÓN PROPIA"},
  {"id": 133, "fecha": "30-09-2026", "concepto": "mango center", "bs": 49998.45, "usd": 58.2013, "tasa": 859.06, "origen": "INVERSIÓN PROPIA"},
  {"id": 134, "fecha": "30-09-2026", "concepto": "aceite dos tiempos", "bs": 7741.62, "usd": 9.0117, "tasa": 859.06, "origen": "INVERSIÓN PROPIA"},
  {"id": 135, "fecha": "30-09-2026", "concepto": "MECHAS", "bs": 6925.77, "usd": 8.062, "tasa": 859.06, "origen": "INVERSIÓN PROPIA"},
  {"id": 136, "fecha": "30-09-2026", "concepto": "HIELO", "bs": 1700.0, "usd": 1.9789, "tasa": 859.06, "origen": "INVERSIÓN PROPIA"},
  {"id": 137, "fecha": "30-09-2026", "concepto": "ALMUERZO", "bs": 10500.0, "usd": 12.2227, "tasa": 859.06, "origen": "INVERSIÓN PROPIA"},
  {"id": 138, "fecha": "01-10-2026", "concepto": "desayuno", "bs": 7647.0, "usd": 8.89, "tasa": 860.18, "origen": "INVERSIÓN PROPIA"},
  {"id": 139, "fecha": "01-10-2026", "concepto": "agua y hielo", "bs": 3986.25, "usd": 4.6342, "tasa": 860.18, "origen": "INVERSIÓN PROPIA"},
  {"id": 140, "fecha": "01-10-2026", "concepto": "casa pro cortadora", "bs": 78098.5, "usd": 90.7932, "tasa": 860.18, "origen": "INVERSIÓN PROPIA"},
  {"id": 141, "fecha": "01-10-2026", "concepto": "cassa pro flotante", "bs": 9459.22, "usd": 10.9968, "tasa": 860.18, "origen": "INVERSIÓN PROPIA"},
  {"id": 142, "fecha": "01-10-2026", "concepto": "Combustible", "bs": 112687.4, "usd": 140.0, "tasa": 804.91, "origen": "INVERSIÓN PROPIA"},
  {"id": 143, "fecha": "02-10-2026", "concepto": "MANGO CENTER", "bs": 378856.27, "usd": 437.1957, "tasa": 866.56, "origen": "ECOVIDA"},
  {"id": 144, "fecha": "02-10-2026", "concepto": "AGUA Y HIELO", "bs": 3000.0, "usd": 3.462, "tasa": 866.56, "origen": "INVERSIÓN PROPIA"},
  {"id": 145, "fecha": "03-10-2026", "concepto": "NOMINA", "bs": 506937.6, "usd": 585.0, "tasa": 866.56, "origen": "ECOVIDA"},
  {"id": 146, "fecha": "03-10-2026", "concepto": "GAS", "bs": 13000.0, "usd": 15.0018, "tasa": 866.56, "origen": "INVERSIÓN PROPIA"},
  {"id": 147, "fecha": "03-10-2026", "concepto": "HIELO", "bs": 1568.47, "usd": 1.81, "tasa": 866.56, "origen": "ECOVIDA"},
  {"id": 148, "fecha": "03-10-2026", "concepto": "global center soplete punta", "bs": 24279.16, "usd": 28.0179, "tasa": 866.56, "origen": "INVERSIÓN PROPIA"},
  {"id": 149, "fecha": "05-10-2026", "concepto": "PUNTAS PARA SOPLETE", "bs": 22289.64, "usd": 25.58, "tasa": 871.37, "origen": "INVERSIÓN PROPIA"},
  {"id": 150, "fecha": "05-10-2026", "concepto": "SEÑORA YOHANA FIESTA", "bs": 26000.0, "usd": 29.8381, "tasa": 871.37, "origen": "INVERSIÓN PROPIA"},
  {"id": 151, "fecha": "05-10-2026", "concepto": "HIELO AGUA", "bs": 2000.0, "usd": 2.2952, "tasa": 871.37, "origen": "INVERSIÓN PROPIA"},
  {"id": 152, "fecha": "05-10-2026", "concepto": "GOTERO", "bs": 8800.0, "usd": 10.099, "tasa": 871.37, "origen": "INVERSIÓN PROPIA"},
  {"id": 153, "fecha": "05-10-2026", "concepto": "TORNILLOS", "bs": 4360.0, "usd": 5.0036, "tasa": 871.37, "origen": "INVERSIÓN PROPIA"},
  {"id": 154, "fecha": "06-10-2026", "concepto": "MANGO CENTER", "bs": 816585.74, "usd": 934.4476, "tasa": 873.87, "origen": "ECOVIDA"},
  {"id": 155, "fecha": "06-10-2026", "concepto": "CANALERO", "bs": 419457.6, "usd": 480.0, "tasa": 873.87, "origen": "ECOVIDA"}
]

# Inicializar sesión de Streamlit para los datos
if 'datos' not in st.session_state:
    st.session_state['datos'] = pd.DataFrame(DATOS_PRECARGADOS)

# Función para procesar y cargar archivo subido
def cargar_excel(uploaded_file):
    try:
        xls = pd.ExcelFile(uploaded_file)
        df = pd.read_excel(uploaded_file, sheet_name=xls.sheet_names[0])
        
        df.columns = df.columns.astype(str).str.strip().str.upper()

        col_fecha = next((c for c in df.columns if 'FECHA' in c), 'FECHA')
        col_concepto = next((c for c in df.columns if 'CONCEPTO' in c), 'CONCEPTO')
        col_bs = next((c for c in df.columns if 'BOLIVARES' in c or 'BS' in c), 'MONTO EN BOLIVARES')
        col_usd = next((c for c in df.columns if 'DOLARES' in c or 'USD' in c or 'DIVISAS' in c), 'MONTO EN DOLARES')
        col_origen = next((c for c in df.columns if 'ORIGEN' in c or 'FONDO' in c), 'ORIGEN DE LOS FONDOS')

        df_clean = df[df[col_fecha].astype(str).str.upper() != 'TOTAL'].copy()
        df_clean[col_origen] = df_clean[col_origen].astype(str).str.strip().str.upper()
        df_clean[col_bs] = pd.to_numeric(df_clean[col_bs], errors='coerce')
        df_clean[col_usd] = pd.to_numeric(df_clean[col_usd], errors='coerce')
        
        df_valid = df_clean[~(df_clean[col_bs].isna() & df_clean[col_usd].isna())].copy()

        nuevos = []
        for idx, row in df_valid.iterrows():
            origen_raw = str(row[col_origen]).strip().upper()
            if "PROPIA" in origen_raw:
                origen = "INVERSIÓN PROPIA"
            elif "ECOVIDA" in origen_raw:
                origen = "ECOVIDA"
            else:
                continue 

            fecha = str(row[col_fecha]).strip()
            concepto = str(row[col_concepto]).strip() if pd.notna(row[col_concepto]) else "SIN CONCEPTO"
            bs = float(row[col_bs]) if pd.notna(row[col_bs]) else 0.0
            usd = float(row[col_usd]) if pd.notna(row[col_usd]) else 0.0
            tasa = (bs / usd) if usd > 0 else 0.0
            
            nuevos.append({
                "id": int(idx) + 1,
                "fecha": fecha,
                "concepto": concepto,
                "bs": round(bs, 4),
                "usd": round(usd, 4),
                "tasa": round(tasa, 2),
                "origen": origen
            })
        
        if nuevos:
            st.session_state['datos'] = pd.DataFrame(nuevos)
            st.success(f"✅ Archivo procesado correctamente. {len(nuevos)} partidas cargadas.")
        else:
            st.warning("El archivo está vacío o no tiene formatos válidos.")
            
    except Exception as e:
        st.error(f"Error al leer el archivo Excel: {e}")

# ================== INTERFAZ WEB ==================

st.markdown("<h2 style='color: #34D399; font-size: 1.2rem; margin-bottom: -15px;'>CONTROL FINANCIERO DE OBRAS • ESOBADES</h2>", unsafe_allow_html=True)
st.title("REPARACIONES GENERALES EN INSTALACIONES DE ESOBADES")

# Panel lateral: Carga y Filtros
with st.sidebar:
    st.markdown("### ⚙️ Panel de Control")
    st.markdown("---")
    
    archivo_subido = st.file_uploader("📂 Cargar Excel Actualizado", type=["xlsx", "xls"])
    if archivo_subido is not None:
        if st.button("Procesar Archivo"):
            cargar_excel(archivo_subido)
            
    st.markdown("---")
    st.markdown("### 🔍 Filtros")
    filtro_origen = st.radio(
        "Mostrar Gastos por Origen:",
        ("Ambos Orígenes", "Solo Inversión Propia", "Solo EcoVida")
    )
    
    busqueda_texto = st.text_input("Buscar Concepto o Fecha:")

# Filtrar Datos
df = st.session_state['datos'].copy()

if filtro_origen == "Solo Inversión Propia":
    df = df[df["origen"] == "INVERSIÓN PROPIA"]
elif filtro_origen == "Solo EcoVida":
    df = df[df["origen"] == "ECOVIDA"]

if busqueda_texto:
    busqueda_texto = busqueda_texto.lower()
    df = df[df["concepto"].str.lower().str.contains(busqueda_texto) | df["fecha"].str.lower().str.contains(busqueda_texto)]

# Calcular Totales KPI (Sobre todos los datos precargados, sin filtrar)
df_all = st.session_state['datos']
tot_bs = df_all["bs"].sum()
tot_usd = df_all["usd"].sum()
cant_tot = len(df_all)

df_prop = df_all[df_all["origen"] == "INVERSIÓN PROPIA"]
prop_bs = df_prop["bs"].sum()
prop_usd = df_prop["usd"].sum()
pct_prop_usd = (prop_usd / tot_usd * 100) if tot_usd > 0 else 0

df_eco = df_all[df_all["origen"] == "ECOVIDA"]
eco_bs = df_eco["bs"].sum()
eco_usd = df_eco["usd"].sum()
pct_eco_usd = (eco_usd / tot_usd * 100) if tot_usd > 0 else 0

# Mostrar Tarjetas KPI en HTML (Stremalit native columns padding is limited)
st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card total">
        <h4>TOTAL GENERAL DE OBRA</h4>
        <p class="usd">$ {tot_usd:,.2f}</p>
        <p class="bs">Bs. {tot_bs:,.2f}</p>
        <p class="subtext">{cant_tot} partidas válidas (100%)</p>
    </div>
    <div class="kpi-card propia">
        <h4>INVERSIÓN PROPIA (Azul Claro)</h4>
        <p class="usd">$ {prop_usd:,.2f}</p>
        <p class="bs">Bs. {prop_bs:,.2f}</p>
        <p class="subtext">{len(df_prop)} partidas ({pct_prop_usd:.1f}% USD)</p>
    </div>
    <div class="kpi-card ecovida">
        <h4>ECOVIDA (Verde)</h4>
        <p class="usd">$ {eco_usd:,.2f}</p>
        <p class="bs">Bs. {eco_bs:,.2f}</p>
        <p class="subtext">{len(df_eco)} partidas ({pct_eco_usd:.1f}% USD)</p>
    </div>
</div>
""", unsafe_allow_html=True)


# Sección Principal (Gráficos y Tabla)
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 📊 Visualización Gráfica")
    
    # Preparar datos de gráficos
    labels = ["INVERSIÓN PROPIA", "ECOVIDA"]
    colores = ["#3B82F6", "#10B981"]
    bs_vals = [prop_bs / 1e6, eco_bs / 1e6]
    usd_vals = [prop_usd, eco_usd]

    fig, axes = plt.subplots(2, 2, figsize=(6, 6), facecolor='#0F172A')
    fig.subplots_adjust(hspace=0.4, wspace=0.3)
    
    # Barras Bs
    ax1 = axes[0,0]
    ax1.set_facecolor('#0F172A')
    bars1 = ax1.bar(labels, bs_vals, color=colores, edgecolor="#F8FAFC", linewidth=1)
    ax1.set_title("Millones de Bs.", color="#F8FAFC", fontsize=10)
    ax1.tick_params(colors="#CBD5E1", labelsize=8)
    for spine in ax1.spines.values(): spine.set_color('#334155')
    
    # Barras USD
    ax2 = axes[0,1]
    ax2.set_facecolor('#0F172A')
    bars2 = ax2.bar(labels, usd_vals, color=colores, edgecolor="#F8FAFC", linewidth=1)
    ax2.set_title("Dólares ($ USD)", color="#F8FAFC", fontsize=10)
    ax2.tick_params(colors="#CBD5E1", labelsize=8)
    for spine in ax2.spines.values(): spine.set_color('#334155')

    # Torta Bs
    ax3 = axes[1,0]
    ax3.set_facecolor('#0F172A')
    if (prop_bs + eco_bs) > 0:
        ax3.pie([prop_bs, eco_bs], labels=["", ""], autopct="%1.1f%%", startangle=140, colors=colores, textprops=dict(color="#F8FAFC", fontsize=8, fontweight="bold"), wedgeprops=dict(edgecolor="#0F172A", linewidth=2))
        c1 = plt.Circle((0, 0), 0.5, fc="#0F172A")
        ax3.add_artist(c1)
        ax3.text(0, 0, f"Bs.\n{(prop_bs+eco_bs)/1e6:,.1f}M", ha="center", va="center", color="#F8FAFC", fontsize=8, fontweight="bold")
    ax3.set_title("Participación (Bs.)", color="#F8FAFC", fontsize=10)

    # Torta USD
    ax4 = axes[1,1]
    ax4.set_facecolor('#0F172A')
    if (prop_usd + eco_usd) > 0:
        ax4.pie(usd_vals, labels=["", ""], autopct="%1.1f%%", startangle=140, colors=colores, textprops=dict(color="#F8FAFC", fontsize=8, fontweight="bold"), wedgeprops=dict(edgecolor="#0F172A", linewidth=2))
        c2 = plt.Circle((0, 0), 0.5, fc="#0F172A")
        ax4.add_artist(c2)
        ax4.text(0, 0, f"$ USD\n{(prop_usd+eco_usd):,.0f}", ha="center", va="center", color="#F8FAFC", fontsize=8, fontweight="bold")
    ax4.set_title("Participación (USD)", color="#F8FAFC", fontsize=10)

    st.pyplot(fig, transparent=True)


with col2:
    st.markdown("### 📋 Navegador de Gastos")
    
    # Formatear el DataFrame para visualización
    df_show = df.copy()
    df_show = df_show.rename(columns={
        "id": "#", "fecha": "FECHA", "concepto": "CONCEPTO", 
        "bs": "Bs.", "usd": "$ USD", "origen": "ORIGEN"
    })
    
    # Format currency
    df_show["Bs."] = df_show["Bs."].apply(lambda x: f"Bs. {x:,.2f}")
    df_show["$ USD"] = df_show["$ USD"].apply(lambda x: f"$ {x:,.2f}")
    df_show["tasa"] = df_show["tasa"].apply(lambda x: f"{x:,.2f}")
    
    # Render interactive dataframe
    st.dataframe(
        df_show[["#", "FECHA", "CONCEPTO", "Bs.", "$ USD", "ORIGEN"]],
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    st.info("💡 En la versión web (Streamlit), puedes usar la lupa ubicada en la esquina superior derecha de la tabla para buscar renglones específicos rápidamente, o hacer clic en los encabezados para ordenar montos de mayor a menor.")
