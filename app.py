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

# Estilos CSS personalizados
st.markdown("""
<style>
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 25px;
    }
    .kpi-card {
        border-radius: 8px;
        padding: 15px 20px;
        flex: 1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Fondos de las tarjetas */
    .kpi-card.total { background-color: #1E293B; border-left: 5px solid #60A5FA; }
    .kpi-card.propia { background-color: #3B82F6; } /* Azul de Inversión Propia */
    .kpi-card.ecovida { background-color: #10B981; } /* Verde de EcoVida */
    
    /* Textos base */
    .kpi-card h4 {
        font-size: 0.9rem;
        margin-bottom: 5px;
        font-weight: 600;
        text-transform: uppercase;
    }
    .kpi-card .usd {
        color: #FFFFFF;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
    }
    .kpi-card .bs {
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 5px;
    }
    .kpi-card .subtext {
        font-size: 0.8rem;
        margin-top: 8px;
    }

    /* Colores específicos de textos para la tarjeta Total (Fondo oscuro) */
    .kpi-card.total h4 { color: #94A3B8; }
    .kpi-card.total .bs { color: #CBD5E1; }
    .kpi-card.total .subtext { color: #64748B; }

    /* Colores específicos de textos para las tarjetas de colores */
    .kpi-card.propia h4, .kpi-card.ecovida h4 { color: #F8FAFC; opacity: 0.9; }
    .kpi-card.propia .bs, .kpi-card.ecovida .bs { color: #F1F5F9; }
    .kpi-card.propia .subtext, .kpi-card.ecovida .subtext { color: #E2E8F0; opacity: 0.85; }
</style>
""", unsafe_allow_html=True)

# Datos precargados (Fallback por si no se sube un archivo Excel)
DATOS_PRE