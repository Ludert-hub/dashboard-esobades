# -*- coding: utf-8 -*-
"""
DASHBOARD FINANCIERO LOCAL - REPARACIONES GENERALES EN INSTALACIONES DE ESOBADES
Versión Corregida (Manejo de saltos de línea y errores robusto).
"""

import os
import sys
import traceback
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    plt = None

DATOS_PRECARGADOS = [
  {
    "id": 1,
    "fecha": "27-08-2026",
    "concepto": "MANGO CENTER",
    "bs": 1935167.0,
    "usd": 2445.4923,
    "tasa": 791.32,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 2,
    "fecha": "27-08-2026",
    "concepto": "FLETE",
    "bs": 56000.0,
    "usd": 70.7678,
    "tasa": 791.32,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 3,
    "fecha": "27-08-2026",
    "concepto": "CEMENTO",
    "bs": 33968.28,
    "usd": 42.9261,
    "tasa": 791.32,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 4,
    "fecha": "27-08-2026",
    "concepto": "PEINILLA-HOJAS-CARTUCHOS",
    "bs": 18991.68,
    "usd": 24.0,
    "tasa": 791.32,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 5,
    "fecha": "27-08-2026",
    "concepto": "ferreteria global center",
    "bs": 279005.18,
    "usd": 352.582,
    "tasa": 791.32,
    "origen": "ECOVIDA"
  },
  {
    "id": 6,
    "fecha": "27-08-2026",
    "concepto": "GLOBAL CENTER",
    "bs": 70164.92,
    "usd": 88.6682,
    "tasa": 791.32,
    "origen": "ECOVIDA"
  },
  {
    "id": 7,
    "fecha": "27-08-2026",
    "concepto": "CEMENTO",
    "bs": 33968.28,
    "usd": 42.9261,
    "tasa": 791.32,
    "origen": "ECOVIDA"
  },
  {
    "id": 8,
    "fecha": "27-08-2026",
    "concepto": "FLETE DE DRYWALL",
    "bs": 11869.8,
    "usd": 15.0,
    "tasa": 791.32,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 9,
    "fecha": "27-08-2026",
    "concepto": "DRYWALL C/PERFILES",
    "bs": 70261.9,
    "usd": 88.7908,
    "tasa": 791.32,
    "origen": "ECOVIDA"
  },
  {
    "id": 10,
    "fecha": "27-08-2026",
    "concepto": "LLANA-SEGUETA-OTROS",
    "bs": 9495.84,
    "usd": 12.0,
    "tasa": 791.32,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 11,
    "fecha": "27-08-2026",
    "concepto": "TOBO DE ALBA",
    "bs": 6330.56,
    "usd": 8.0,
    "tasa": 791.32,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 12,
    "fecha": "27-08-2026",
    "concepto": "AGUA - HIELO",
    "bs": 10928.12,
    "usd": 13.81,
    "tasa": 791.32,
    "origen": "ECOVIDA"
  },
  {
    "id": 13,
    "fecha": "29-08-2026",
    "concepto": "electricista",
    "bs": 197917.5,
    "usd": 250.0,
    "tasa": 791.67,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 14,
    "fecha": "29-08-2026",
    "concepto": "nominas",
    "bs": 303470.8611,
    "usd": 383.33,
    "tasa": 791.67,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 15,
    "fecha": "29-08-2026",
    "concepto": "lamparas",
    "bs": 53959.56,
    "usd": 68.1592,
    "tasa": 791.67,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 16,
    "fecha": "29-08-2026",
    "concepto": "ferreteria el llano",
    "bs": 453839.47,
    "usd": 573.2685,
    "tasa": 791.67,
    "origen": "ECOVIDA"
  },
  {
    "id": 17,
    "fecha": "29-08-2026",
    "concepto": "cabezal guadaña",
    "bs": 15900.0,
    "usd": 20.0841,
    "tasa": 791.67,
    "origen": "ECOVIDA"
  },
  {
    "id": 18,
    "fecha": "29-08-2026",
    "concepto": "tarslado de andamios",
    "bs": 15833.4,
    "usd": 20.0,
    "tasa": 791.67,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 19,
    "fecha": "29-08-2026",
    "concepto": "botellon de agua y hielo",
    "bs": 11875.05,
    "usd": 15.0,
    "tasa": 791.67,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 20,
    "fecha": "29-08-2026",
    "concepto": "clavitos de drywall",
    "bs": 791.67,
    "usd": 1.0,
    "tasa": 791.67,
    "origen": "ECOVIDA"
  },
  {
    "id": 21,
    "fecha": "29-08-2026",
    "concepto": "hielo",
    "bs": 1583.34,
    "usd": 2.0,
    "tasa": 791.67,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 22,
    "fecha": "29-08-2026",
    "concepto": "tornillos drywall negros",
    "bs": 5541.69,
    "usd": 7.0,
    "tasa": 791.67,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 23,
    "fecha": "29-08-2026",
    "concepto": "gasolina",
    "bs": 15833.4,
    "usd": 20.0,
    "tasa": 791.67,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 24,
    "fecha": "29-08-2026",
    "concepto": "mango center",
    "bs": 311476.57,
    "usd": 393.4424,
    "tasa": 791.67,
    "origen": "ECOVIDA"
  },
  {
    "id": 25,
    "fecha": "29-08-2026",
    "concepto": "cemento",
    "bs": 9398.51,
    "usd": 11.8718,
    "tasa": 791.67,
    "origen": "ECOVIDA"
  },
  {
    "id": 26,
    "fecha": "29-08-2026",
    "concepto": "pico de solplete",
    "bs": 20892.17,
    "usd": 26.39,
    "tasa": 791.67,
    "origen": "ECOVIDA"
  },
  {
    "id": 27,
    "fecha": "29-08-2026",
    "concepto": "pico de solplete",
    "bs": 28468.45,
    "usd": 35.96,
    "tasa": 791.67,
    "origen": "ECOVIDA"
  },
  {
    "id": 28,
    "fecha": "29-08-2026",
    "concepto": "pintura montana",
    "bs": 29291.79,
    "usd": 37.0,
    "tasa": 791.67,
    "origen": "ECOVIDA"
  },
  {
    "id": 29,
    "fecha": "29-08-2026",
    "concepto": "mobiliario de Oficina Valencia",
    "bs": 1862007.84,
    "usd": 2352.0,
    "tasa": 791.67,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 30,
    "fecha": "29-08-2026",
    "concepto": "implementos de seguridad",
    "bs": 336459.75,
    "usd": 425.0,
    "tasa": 791.67,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 31,
    "fecha": "31-08-2026",
    "concepto": "HIELO",
    "bs": 1430.0,
    "usd": 1.7988,
    "tasa": 794.99,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 32,
    "fecha": "31-08-2026",
    "concepto": "AGUA Y THINNER",
    "bs": 12115.0,
    "usd": 15.2392,
    "tasa": 794.99,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 33,
    "fecha": "31-08-2026",
    "concepto": "GRAFIADO ADELANTO",
    "bs": 227826.0,
    "usd": 286.5772,
    "tasa": 794.99,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 34,
    "fecha": "31-08-2026",
    "concepto": "PROTECTOR DE AIRE ACOND.",
    "bs": 198747.5,
    "usd": 250.0,
    "tasa": 794.99,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 35,
    "fecha": "31-08-2026",
    "concepto": "GRAPAS",
    "bs": 3577.455,
    "usd": 4.5,
    "tasa": 794.99,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 36,
    "fecha": "31-08-2026",
    "concepto": "BREACKERS",
    "bs": 7623.78,
    "usd": 9.5898,
    "tasa": 794.99,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 37,
    "fecha": "31-08-2026",
    "concepto": "NIVEL, CLAVOS, ACEITE 2 TIEMPOS",
    "bs": 30621.92,
    "usd": 38.5186,
    "tasa": 794.99,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 38,
    "fecha": "31-08-2026",
    "concepto": "CONEXIONES ELECTRICAS",
    "bs": 3452.0,
    "usd": 4.3422,
    "tasa": 794.99,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 39,
    "fecha": "31-08-2026",
    "concepto": "TORNILLOS GARRAPATEROS",
    "bs": 3179.0,
    "usd": 3.9988,
    "tasa": 794.99,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 40,
    "fecha": "31-08-2026",
    "concepto": "PEINILLA",
    "bs": 12719.84,
    "usd": 16.0,
    "tasa": 794.99,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 41,
    "fecha": "01-09-2026",
    "concepto": "CASA PRO FILTRO Y GUANTES Y ESCALER",
    "bs": 223542.34,
    "usd": 279.4279,
    "tasa": 800.0,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 42,
    "fecha": "01-09-2026",
    "concepto": "GLOBAL CENTER  CANDADOS",
    "bs": 58303.92,
    "usd": 72.8799,
    "tasa": 800.0,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 43,
    "fecha": "01-09-2026",
    "concepto": "CASA DEL ELECTRODO",
    "bs": 34338.41,
    "usd": 42.923,
    "tasa": 800.0,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 44,
    "fecha": "01-09-2026",
    "concepto": "CASA DEL ELECTRODO",
    "bs": 120406.75,
    "usd": 150.5084,
    "tasa": 800.0,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 45,
    "fecha": "01-09-2026",
    "concepto": "HIELO Y AGUA",
    "bs": 2150.0,
    "usd": 2.6875,
    "tasa": 800.0,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 46,
    "fecha": "01-09-2026",
    "concepto": "VASOS Y REEFRESCO",
    "bs": 3470.0,
    "usd": 4.3375,
    "tasa": 800.0,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 47,
    "fecha": "01-09-2026",
    "concepto": "CANDADOS COMISI",
    "bs": 15.0,
    "usd": 0.0187,
    "tasa": 800.0,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 48,
    "fecha": "01-09-2026",
    "concepto": "IMPRESIÓN JUAN CARLOS",
    "bs": 7200.0,
    "usd": 9.0,
    "tasa": 800.0,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 49,
    "fecha": "01-09-2026",
    "concepto": "GUADAÑA",
    "bs": 15168.0,
    "usd": 18.96,
    "tasa": 800.0,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 50,
    "fecha": "01-09-2026",
    "concepto": "traslado de tanque metalico",
    "bs": 120228.0,
    "usd": 150.0,
    "tasa": 801.52,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 51,
    "fecha": "02-09-2026",
    "concepto": "CEMENTO -DISCO-LIJA-LIMPOTEX",
    "bs": 19659.68,
    "usd": 24.5384,
    "tasa": 801.18,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 52,
    "fecha": "02-09-2026",
    "concepto": "FERRETERIA ALONDRA",
    "bs": 11961.47,
    "usd": 14.9298,
    "tasa": 801.18,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 53,
    "fecha": "02-09-2026",
    "concepto": "CERRADURA",
    "bs": 19899.25,
    "usd": 24.8374,
    "tasa": 801.18,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 54,
    "fecha": "02-09-2026",
    "concepto": "TORNILLOS",
    "bs": 2163.16,
    "usd": 2.7,
    "tasa": 801.18,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 55,
    "fecha": "03-09-2026",
    "concepto": "VIDRIOS",
    "bs": 67581.6,
    "usd": 83.9617,
    "tasa": 804.91,
    "origen": "ECOVIDA"
  },
  {
    "id": 56,
    "fecha": "03-09-2026",
    "concepto": "PASTA FROFESIONAL",
    "bs": 11184.28,
    "usd": 13.8951,
    "tasa": 804.91,
    "origen": "ECOVIDA"
  },
  {
    "id": 57,
    "fecha": "03-09-2026",
    "concepto": "AGUA Y HIELO",
    "bs": 3717.26,
    "usd": 4.6182,
    "tasa": 804.91,
    "origen": "ECOVIDA"
  },
  {
    "id": 58,
    "fecha": "03-09-2026",
    "concepto": "TUBOS pvc",
    "bs": 96588.17,
    "usd": 119.9987,
    "tasa": 804.91,
    "origen": "ECOVIDA"
  },
  {
    "id": 59,
    "fecha": "03-09-2026",
    "concepto": "CANALERO",
    "bs": 140206.0,
    "usd": 174.1884,
    "tasa": 804.91,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 60,
    "fecha": "03-09-2026",
    "concepto": "MANGO CENTER",
    "bs": 33096.19,
    "usd": 41.1179,
    "tasa": 804.91,
    "origen": "ECOVIDA"
  },
  {
    "id": 61,
    "fecha": "03-09-2026",
    "concepto": "Combustible",
    "bs": 112687.4,
    "usd": 140.0,
    "tasa": 804.91,
    "origen": "ECOVIDA"
  },
  {
    "id": 62,
    "fecha": "03-09-2026",
    "concepto": "ESCOBA Y BOLSAS",
    "bs": 9433.24,
    "usd": 11.6836,
    "tasa": 807.39,
    "origen": "ECOVIDA"
  },
  {
    "id": 63,
    "fecha": "03-09-2026",
    "concepto": "PVC Y LUCES",
    "bs": 100641.16,
    "usd": 124.65,
    "tasa": 807.39,
    "origen": "ECOVIDA"
  },
  {
    "id": 64,
    "fecha": "03-09-2026",
    "concepto": "PERSIANA",
    "bs": 65398.59,
    "usd": 81.0,
    "tasa": 807.39,
    "origen": "ECOVIDA"
  },
  {
    "id": 65,
    "fecha": "03-09-2026",
    "concepto": "MANGO CENTER ARO",
    "bs": 743113.27,
    "usd": 920.3895,
    "tasa": 807.39,
    "origen": "ECOVIDA"
  },
  {
    "id": 66,
    "fecha": "03-09-2026",
    "concepto": "TIRROS",
    "bs": 4353.17,
    "usd": 5.3917,
    "tasa": 807.39,
    "origen": "ECOVIDA"
  },
  {
    "id": 67,
    "fecha": "03-09-2026",
    "concepto": "LLAVES LAVAMANOS",
    "bs": 12016.22,
    "usd": 14.8828,
    "tasa": 807.39,
    "origen": "ECOVIDA"
  },
  {
    "id": 68,
    "fecha": "03-09-2026",
    "concepto": "PUERTAS",
    "bs": 201847.5,
    "usd": 250.0,
    "tasa": 807.39,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 69,
    "fecha": "03-09-2026",
    "concepto": "DRYWALL",
    "bs": 177625.8,
    "usd": 220.0,
    "tasa": 807.39,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 70,
    "fecha": "03-09-2026",
    "concepto": "HERRERO ADELANTO",
    "bs": 40369.5,
    "usd": 50.0,
    "tasa": 807.39,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 71,
    "fecha": "03-09-2026",
    "concepto": "HERRERIA",
    "bs": 11312.0,
    "usd": 14.0106,
    "tasa": 807.39,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 73,
    "fecha": "03-09-2026",
    "concepto": "deuda ecovida",
    "bs": 16088.0,
    "usd": 20.0,
    "tasa": 804.4,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 74,
    "fecha": "03-09-2026",
    "concepto": "prestamo eudes casa",
    "bs": 40220.0,
    "usd": 50.0,
    "tasa": 804.4,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 75,
    "fecha": "03-09-2026",
    "concepto": "deuda ecovida",
    "bs": 11312.0,
    "usd": 14.0627,
    "tasa": 804.4,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 76,
    "fecha": "03-09-2026",
    "concepto": "discos de corte",
    "bs": 10000.0,
    "usd": 12.3894,
    "tasa": 807.14,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 77,
    "fecha": "03-09-2026",
    "concepto": "hielo",
    "bs": 1400.0,
    "usd": 1.7345,
    "tasa": 807.14,
    "origen": "ECOVIDA"
  },
  {
    "id": 78,
    "fecha": "03-09-2026",
    "concepto": "gasolina",
    "bs": 33781.0,
    "usd": 41.8527,
    "tasa": 807.14,
    "origen": "ECOVIDA"
  },
  {
    "id": 79,
    "fecha": "03-09-2026",
    "concepto": "hielo, disco corte, botellon",
    "bs": 21438.0,
    "usd": 26.5604,
    "tasa": 807.14,
    "origen": "ECOVIDA"
  },
  {
    "id": 80,
    "fecha": "07-09-2026",
    "concepto": "COPIAS LICITACION",
    "bs": 58685.0,
    "usd": 72.1176,
    "tasa": 813.74,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 81,
    "fecha": "07-09-2026",
    "concepto": "PUERTA DE MADERA",
    "bs": 12210.0,
    "usd": 15.0048,
    "tasa": 813.74,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 82,
    "fecha": "07-09-2026",
    "concepto": "GRAFIADO EDF 1",
    "bs": 53707.0,
    "usd": 66.0002,
    "tasa": 813.74,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 83,
    "fecha": "07-09-2026",
    "concepto": "ADELANTO DE NOMINA",
    "bs": 25000.0,
    "usd": 30.7223,
    "tasa": 813.74,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 84,
    "fecha": "08-09-2026",
    "concepto": "CEMENTO 2",
    "bs": 19552.7,
    "usd": 24.0002,
    "tasa": 814.69,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 85,
    "fecha": "08-09-2026",
    "concepto": "ESMALTE VERDE 3",
    "bs": 90440.36,
    "usd": 111.012,
    "tasa": 814.69,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 86,
    "fecha": "08-09-2026",
    "concepto": "MANILLA DE PUERTA",
    "bs": 15080.0,
    "usd": 18.5101,
    "tasa": 814.69,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 87,
    "fecha": "08-09-2026",
    "concepto": "IMPRESIÓN LICITACION AG",
    "bs": 42560.0,
    "usd": 52.2407,
    "tasa": 814.69,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 88,
    "fecha": "08-09-2026",
    "concepto": "NOMINA AYUDANTE",
    "bs": 38754.54,
    "usd": 47.5697,
    "tasa": 814.69,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 89,
    "fecha": "08-09-2026",
    "concepto": "COMPUADORA   268 USDT",
    "bs": 262004.304,
    "usd": 321.6,
    "tasa": 814.69,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 90,
    "fecha": "08-09-2026",
    "concepto": "PORTATIL    RIZEN 7    USDT",
    "bs": 400827.48,
    "usd": 492.0,
    "tasa": 814.69,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 91,
    "fecha": "09-09-2026",
    "concepto": "HIPERMERCADO AGROPECUARIO",
    "bs": 8818.69,
    "usd": 10.7532,
    "tasa": 820.1,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 92,
    "fecha": "09-09-2026",
    "concepto": "MANGO CENTER",
    "bs": 70619.03,
    "usd": 86.1103,
    "tasa": 820.1,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 93,
    "fecha": "09-09-2026",
    "concepto": "TUBO DE HIERRO",
    "bs": 37000.0,
    "usd": 45.1164,
    "tasa": 820.1,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 94,
    "fecha": "09-09-2026",
    "concepto": "AGUA Y HIELO",
    "bs": 2600.0,
    "usd": 3.1703,
    "tasa": 820.1,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 95,
    "fecha": "09-09-2026",
    "concepto": "FERRETERIA LOPEZ",
    "bs": 65000.0,
    "usd": 79.2586,
    "tasa": 820.1,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 96,
    "fecha": "10-09-2026",
    "concepto": "CERRADURA DE EMPOTRAR",
    "bs": 16473.99,
    "usd": 19.8,
    "tasa": 832.02,
    "origen": "ECOVIDA"
  },
  {
    "id": 97,
    "fecha": "11-09-2026",
    "concepto": "NOMINA",
    "bs": 454840.3734,
    "usd": 546.67,
    "tasa": 832.02,
    "origen": "ECOVIDA"
  },
  {
    "id": 98,
    "fecha": "11-09-2026",
    "concepto": "LLAVE DE CHORRO",
    "bs": 5349.91,
    "usd": 6.43,
    "tasa": 832.02,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 99,
    "fecha": "11-09-2026",
    "concepto": "HIELO",
    "bs": 1498.48,
    "usd": 1.801,
    "tasa": 832.02,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 100,
    "fecha": "12-09-2026",
    "concepto": "ESTUCO GLOBAL CENTER",
    "bs": 21063.28,
    "usd": 25.3158,
    "tasa": 832.02,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 101,
    "fecha": "12-09-2026",
    "concepto": "AGUA, HIELO",
    "bs": 3678.0,
    "usd": 4.4206,
    "tasa": 832.02,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 102,
    "fecha": "14-09-2026",
    "concepto": "GRAFIADO",
    "bs": 204000.0,
    "usd": 244.0,
    "tasa": 836.07,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 103,
    "fecha": "15-09-2026",
    "concepto": "MANGO CENTER",
    "bs": 83543.15,
    "usd": 98.6913,
    "tasa": 846.51,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 104,
    "fecha": "15-09-2026",
    "concepto": "REPUESTO GUADAÑA",
    "bs": 8325.0,
    "usd": 9.8345,
    "tasa": 846.51,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 105,
    "fecha": "16-09-2026",
    "concepto": "mango center 14-09-2026",
    "bs": 411989.94,
    "usd": 489.183,
    "tasa": 842.2,
    "origen": "ECOVIDA"
  },
  {
    "id": 106,
    "fecha": "16-09-2026",
    "concepto": "mango center 16-09-2026",
    "bs": 114537.87,
    "usd": 135.306,
    "tasa": 846.51,
    "origen": "ECOVIDA"
  },
  {
    "id": 107,
    "fecha": "16-09-2026",
    "concepto": "mango center 17-09-2026",
    "bs": 27385.4,
    "usd": 32.3509,
    "tasa": 846.51,
    "origen": "ECOVIDA"
  },
  {
    "id": 108,
    "fecha": "16-09-2026",
    "concepto": "global center 17-9-2026",
    "bs": 57236.72,
    "usd": 67.6149,
    "tasa": 846.51,
    "origen": "ECOVIDA"
  },
  {
    "id": 109,
    "fecha": "16-09-2026",
    "concepto": "montana  17-9-2026",
    "bs": 59320.78,
    "usd": 70.0,
    "tasa": 847.44,
    "origen": "ECOVIDA"
  },
  {
    "id": 110,
    "fecha": "16-09-2026",
    "concepto": "grafiado",
    "bs": 413550.72,
    "usd": 488.0,
    "tasa": 847.44,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 111,
    "fecha": "16-09-2026",
    "concepto": "herrero",
    "bs": 110167.2,
    "usd": 130.0,
    "tasa": 847.44,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 112,
    "fecha": "16-09-2026",
    "concepto": "hielo",
    "bs": 1500.0,
    "usd": 1.77,
    "tasa": 847.44,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 113,
    "fecha": "16-09-2026",
    "concepto": "agua potable",
    "bs": 2542.32,
    "usd": 3.0,
    "tasa": 847.44,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 114,
    "fecha": "16-09-2026",
    "concepto": "limpieza instalaciones",
    "bs": 25423.2,
    "usd": 30.0,
    "tasa": 847.44,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 115,
    "fecha": "19-09-2026",
    "concepto": "cerradura",
    "bs": 8800.0,
    "usd": 10.9838,
    "tasa": 801.18,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 116,
    "fecha": "19-09-2026",
    "concepto": "hoja de guadaña",
    "bs": 6552.09,
    "usd": 8.178,
    "tasa": 801.18,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 117,
    "fecha": "19-09-2026",
    "concepto": "agua hielo",
    "bs": 3500.0,
    "usd": 4.1197,
    "tasa": 849.57,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 118,
    "fecha": "25-09-2026",
    "concepto": "hielo",
    "bs": 2000.0,
    "usd": 2.3374,
    "tasa": 855.66,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 119,
    "fecha": "25-09-2026",
    "concepto": "tirros",
    "bs": 5161.35,
    "usd": 6.032,
    "tasa": 855.66,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 120,
    "fecha": "25-09-2026",
    "concepto": "CANALERO",
    "bs": 149740.5,
    "usd": 175.0,
    "tasa": 855.66,
    "origen": "ECOVIDA"
  },
  {
    "id": 121,
    "fecha": "25-09-2026",
    "concepto": "ANDAMIOS",
    "bs": 154018.8,
    "usd": 180.0,
    "tasa": 855.66,
    "origen": "ECOVIDA"
  },
  {
    "id": 122,
    "fecha": "25-09-2026",
    "concepto": "NOMINA",
    "bs": 500561.1,
    "usd": 585.0,
    "tasa": 855.66,
    "origen": "ECOVIDA"
  },
  {
    "id": 123,
    "fecha": "26-09-2026",
    "concepto": "ARRANQUE DE GUADAÑA",
    "bs": 14546.22,
    "usd": 17.0,
    "tasa": 855.66,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 124,
    "fecha": "26-09-2026",
    "concepto": "HIELO",
    "bs": 1542.61,
    "usd": 1.8028,
    "tasa": 855.66,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 125,
    "fecha": "28-09-2026",
    "concepto": "MANGO CENTER",
    "bs": 84615.49,
    "usd": 98.7334,
    "tasa": 857.01,
    "origen": "ECOVIDA"
  },
  {
    "id": 126,
    "fecha": "28-09-2026",
    "concepto": "HIELO",
    "bs": 3000.0,
    "usd": 3.5005,
    "tasa": 857.01,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 127,
    "fecha": "29-09-2026",
    "concepto": "impresora",
    "bs": 201604.15,
    "usd": 235.0,
    "tasa": 857.89,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 128,
    "fecha": "29-09-2026",
    "concepto": "hielo",
    "bs": 6000.0,
    "usd": 6.9939,
    "tasa": 857.89,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 129,
    "fecha": "29-09-2026",
    "concepto": "limpieza general",
    "bs": 26000.0,
    "usd": 30.3069,
    "tasa": 857.89,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 130,
    "fecha": "29-09-2026",
    "concepto": "gasolina del camion",
    "bs": 60052.0,
    "usd": 69.9997,
    "tasa": 857.89,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 131,
    "fecha": "29-09-2026",
    "concepto": "mango center",
    "bs": 175859.04,
    "usd": 204.9902,
    "tasa": 857.89,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 132,
    "fecha": "29-09-2026",
    "concepto": "brochas",
    "bs": 3668.92,
    "usd": 4.2767,
    "tasa": 857.89,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 133,
    "fecha": "30-09-2026",
    "concepto": "mango center",
    "bs": 49998.45,
    "usd": 58.2013,
    "tasa": 859.06,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 134,
    "fecha": "30-09-2026",
    "concepto": "aceite dos tiempos",
    "bs": 7741.62,
    "usd": 9.0117,
    "tasa": 859.06,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 135,
    "fecha": "30-09-2026",
    "concepto": "MECHAS",
    "bs": 6925.77,
    "usd": 8.062,
    "tasa": 859.06,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 136,
    "fecha": "30-09-2026",
    "concepto": "HIELO",
    "bs": 1700.0,
    "usd": 1.9789,
    "tasa": 859.06,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 137,
    "fecha": "30-09-2026",
    "concepto": "ALMUERZO",
    "bs": 10500.0,
    "usd": 12.2227,
    "tasa": 859.06,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 138,
    "fecha": "01-10-2026",
    "concepto": "desayuno",
    "bs": 7647.0,
    "usd": 8.89,
    "tasa": 860.18,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 139,
    "fecha": "01-10-2026",
    "concepto": "agua y hielo",
    "bs": 3986.25,
    "usd": 4.6342,
    "tasa": 860.18,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 140,
    "fecha": "01-10-2026",
    "concepto": "casa pro cortadora",
    "bs": 78098.5,
    "usd": 90.7932,
    "tasa": 860.18,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 141,
    "fecha": "01-10-2026",
    "concepto": "cassa pro flotante",
    "bs": 9459.22,
    "usd": 10.9968,
    "tasa": 860.18,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 142,
    "fecha": "01-10-2026",
    "concepto": "Combustible",
    "bs": 112687.4,
    "usd": 140.0,
    "tasa": 804.91,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 143,
    "fecha": "02-10-2026",
    "concepto": "MANGO CENTER",
    "bs": 378856.27,
    "usd": 437.1957,
    "tasa": 866.56,
    "origen": "ECOVIDA"
  },
  {
    "id": 144,
    "fecha": "02-10-2026",
    "concepto": "AGUA Y HIELO",
    "bs": 3000.0,
    "usd": 3.462,
    "tasa": 866.56,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 145,
    "fecha": "03-10-2026",
    "concepto": "NOMINA",
    "bs": 506937.6,
    "usd": 585.0,
    "tasa": 866.56,
    "origen": "ECOVIDA"
  },
  {
    "id": 146,
    "fecha": "03-10-2026",
    "concepto": "GAS",
    "bs": 13000.0,
    "usd": 15.0018,
    "tasa": 866.56,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 147,
    "fecha": "03-10-2026",
    "concepto": "HIELO",
    "bs": 1568.47,
    "usd": 1.81,
    "tasa": 866.56,
    "origen": "ECOVIDA"
  },
  {
    "id": 148,
    "fecha": "03-10-2026",
    "concepto": "global center soplete punta",
    "bs": 24279.16,
    "usd": 28.0179,
    "tasa": 866.56,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 149,
    "fecha": "05-10-2026",
    "concepto": "PUNTAS PARA SOPLETE",
    "bs": 22289.64,
    "usd": 25.58,
    "tasa": 871.37,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 150,
    "fecha": "05-10-2026",
    "concepto": "SEÑORA YOHANA FIESTA",
    "bs": 26000.0,
    "usd": 29.8381,
    "tasa": 871.37,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 151,
    "fecha": "05-10-2026",
    "concepto": "HIELO AGUA",
    "bs": 2000.0,
    "usd": 2.2952,
    "tasa": 871.37,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 152,
    "fecha": "05-10-2026",
    "concepto": "GOTERO",
    "bs": 8800.0,
    "usd": 10.099,
    "tasa": 871.37,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 153,
    "fecha": "05-10-2026",
    "concepto": "TORNILLOS",
    "bs": 4360.0,
    "usd": 5.0036,
    "tasa": 871.37,
    "origen": "INVERSIÓN PROPIA"
  },
  {
    "id": 154,
    "fecha": "06-10-2026",
    "concepto": "MANGO CENTER",
    "bs": 816585.74,
    "usd": 934.4476,
    "tasa": 873.87,
    "origen": "ECOVIDA"
  },
  {
    "id": 155,
    "fecha": "06-10-2026",
    "concepto": "CANALERO",
    "bs": 419457.6,
    "usd": 480.0,
    "tasa": 873.87,
    "origen": "ECOVIDA"
  }
]

class DashboardESOBADESApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard Financiero • Reparaciones Generales ESOBADES")
        self.root.geometry("1450x880")
        self.root.minsize(1200, 750)
        self.root.configure(bg="#0F172A")

        self.datos_completos = list(DATOS_PRECARGADOS)
        self.datos_filtrados = list(self.datos_completos)
        
        self.filtro_origen = tk.StringVar(value="TODOS")
        self.busqueda_var = tk.StringVar()

        self._configurar_estilos()
        self._construir_interfaz()
        
        # Intentar cargar Excel local
        self._intentar_cargar_excel_local()
        
        self.actualizar_todo()

    def _configurar_estilos(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Treeview", background="#1E293B", foreground="#F8FAFC", fieldbackground="#1E293B", rowheight=29, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#0F172A", foreground="#60A5FA", font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", "#3B82F6")], foreground=[("selected", "#FFFFFF")])

    def _intentar_cargar_excel_local(self):
        archivos_posibles = [
            "Relacion_Gastos_ESOBADES_Actualizado_4.xlsx",
            "Relacion_Gastos_ESOBADES_Actualizado_3.xlsx",
            "Relacion_Gastos_ESOBADES_Actualizado.xlsx",
            "Relacion_Gastos_ESOBADES.xlsx"
        ]
        cargado = False
        for nombre in archivos_posibles:
            if os.path.exists(nombre) and pd is not None:
                exito = self.cargar_desde_ruta(nombre, silencioso=True)
                if exito:
                    cargado = True
                    break
        
        if not cargado and not self.datos_completos:
            messagebox.showwarning("Atención", "No se encontró el archivo Excel de la relación de gastos en esta carpeta.\nPor favor, usa el botón 'Cargar / Actualizar Excel' para seleccionarlo manualmente.")

    def cargar_desde_ruta(self, filepath, silencioso=False):
        if pd is None:
            if not silencioso:
                messagebox.showerror("Librería faltante", "Instala pandas y openpyxl: pip install pandas openpyxl")
            return False

        try:
            xls = pd.ExcelFile(filepath)
            df = pd.read_excel(filepath, sheet_name=xls.sheet_names[0])
            
            # Limpiar nombres de columnas
            df.columns = df.columns.astype(str).str.strip().str.upper()

            # Buscar columnas clave (flexibilidad en nombres)
            col_fecha = next((c for c in df.columns if 'FECHA' in c), 'FECHA')
            col_concepto = next((c for c in df.columns if 'CONCEPTO' in c), 'CONCEPTO')
            col_bs = next((c for c in df.columns if 'BOLIVARES' in c or 'BS' in c), 'MONTO EN BOLIVARES')
            col_usd = next((c for c in df.columns if 'DOLARES' in c or 'USD' in c or 'DIVISAS' in c), 'MONTO EN DOLARES')
            col_origen = next((c for c in df.columns if 'ORIGEN' in c or 'FONDO' in c), 'ORIGEN DE LOS FONDOS')

            # Validar que existan
            faltantes = [c for c, name in [(col_fecha, 'Fecha'), (col_concepto, 'Concepto'), (col_bs, 'Monto Bs'), (col_usd, 'Monto USD'), (col_origen, 'Origen')] if c not in df.columns]
            if faltantes:
                if not silencioso:
                    messagebox.showerror("Error de Formato", f"El Excel no tiene las columnas esperadas. Faltan o cambiaron de nombre.")
                return False

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
                    continue # Solo estos dos origenes

                fecha = str(row[col_fecha]).strip()
                if fecha.lower() == 'nan':
                    fecha = "SIN FECHA"
                concepto = str(row[col_concepto]).strip() if pd.notna(row[col_concepto]) else "SIN CONCEPTO"
                if concepto.lower() == 'nan':
                    concepto = "SIN CONCEPTO"
                
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

            self.datos_completos = nuevos
            self.actualizar_todo()
            if not silencioso:
                messagebox.showinfo("Archivo Cargado", f"Se cargaron {len(nuevos)} registros válidos exitosamente.\nArchivo: {os.path.basename(filepath)}")
            return True

        except Exception as e:
            if not silencioso:
                error_trace = traceback.format_exc()
                messagebox.showerror("Error al cargar Excel", f"Ocurrió un error leyendo el archivo:\n{str(e)}\n\n{error_trace}")
            return False

    def seleccionar_archivo_excel(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar Relación de Gastos Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls")]
        )
        if ruta:
            self.cargar_desde_ruta(ruta, silencioso=False)

    def _construir_interfaz(self):
        header = tk.Frame(self.root, bg="#0F172A", padx=18, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="CONTROL FINANCIERO DE OBRAS • ESOBADES", bg="#0F172A", fg="#34D399", font=("Segoe UI", 9, "bold")).pack(anchor="w")

        top_row = tk.Frame(header, bg="#0F172A")
        top_row.pack(fill="x", pady=(2, 0))
        tk.Label(top_row, text="REPARACIONES GENERALES EN INSTALACIONES DE ESOBADES", bg="#0F172A", fg="#FFFFFF", font=("Segoe UI", 16, "bold")).pack(side="left")
        tk.Button(top_row, text="📂 Cargar / Actualizar Excel (.xlsx)", command=self.seleccionar_archivo_excel, bg="#3B82F6", fg="#FFFFFF", activebackground="#2563EB", font=("Segoe UI", 10, "bold"), relief="flat", padx=14, pady=6, cursor="hand2").pack(side="right")

        kpi_frame = tk.Frame(self.root, bg="#0F172A", padx=18, pady=6)
        kpi_frame.pack(fill="x")
        for i in range(3):
            kpi_frame.columnconfigure(i, weight=1)

        self.card_total = self._crear_tarjeta_kpi(kpi_frame, 0, "TOTAL GENERAL DE OBRA", "#60A5FA")
        self.card_propia = self._crear_tarjeta_kpi(kpi_frame, 1, "INVERSIÓN PROPIA (Azul Claro)", "#3B82F6")
        self.card_ecovida = self._crear_tarjeta_kpi(kpi_frame, 2, "ECOVIDA (Verde)", "#10B981")

        main_pane = tk.PanedWindow(self.root, orient="horizontal", bg="#334155", sashwidth=6, bd=0)
        main_pane.pack(fill="both", expand=True, padx=18, pady=8)

        left_panel = tk.Frame(main_pane, bg="#1E293B", padx=10, pady=10)
        main_pane.add(left_panel, width=640)

        chart_top_bar = tk.Frame(left_panel, bg="#1E293B")
        chart_top_bar.pack(fill="x", pady=(0, 6))
        tk.Label(chart_top_bar, text="📊 Visualización Gráfica", bg="#1E293B", fg="#F8FAFC", font=("Segoe UI", 11, "bold")).pack(side="left")

        self.canvas_frame = tk.Frame(left_panel, bg="#1E293B")
        self.canvas_frame.pack(fill="both", expand=True)

        if plt is not None:
            self.fig, self.axes = plt.subplots(2, 2, figsize=(6.5, 5.8), dpi=100, facecolor="#1E293B")
            self.fig.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.38, wspace=0.28)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            tk.Label(self.canvas_frame, text="Instala matplotlib:\npip install matplotlib", bg="#1E293B", fg="#F87171").pack(expand=True)

        right_panel = tk.Frame(main_pane, bg="#1E293B", padx=12, pady=10)
        main_pane.add(right_panel, width=720)

        nav_bar = tk.Frame(right_panel, bg="#1E293B")
        nav_bar.pack(fill="x", pady=(0, 8))
        tk.Label(nav_bar, text="Mostrar Gastos:", bg="#1E293B", fg="#34D399", font=("Segoe UI", 10, "bold")).pack(side="left")
        
        tk.Button(nav_bar, text="Ambos Orígenes", command=lambda: self.seleccionar_filtro_origen("TODOS"), bg="#334155", fg="#FFFFFF", relief="flat", padx=10, pady=3, cursor="hand2").pack(side="left", padx=6)
        tk.Button(nav_bar, text="Solo Inversión Propia", command=lambda: self.seleccionar_filtro_origen("INVERSIÓN PROPIA"), bg="#3B82F6", fg="#FFFFFF", relief="flat", padx=10, pady=3, cursor="hand2").pack(side="left", padx=6)
        tk.Button(nav_bar, text="Solo EcoVida", command=lambda: self.seleccionar_filtro_origen("ECOVIDA"), bg="#10B981", fg="#FFFFFF", relief="flat", padx=10, pady=3, cursor="hand2").pack(side="left", padx=6)

        search_bar = tk.Frame(right_panel, bg="#1E293B")
        search_bar.pack(fill="x", pady=(0, 8))
        tk.Label(search_bar, text="Buscar Concepto / Fecha:", bg="#1E293B", fg="#CBD5E1", font=("Segoe UI", 9, "bold")).pack(side="left")
        ent_busqueda = tk.Entry(search_bar, textvariable=self.busqueda_var, bg="#0F172A", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Segoe UI", 10), relief="flat", width=26)
        ent_busqueda.pack(side="left", padx=6, ipady=3)
        self.busqueda_var.trace_add("write", lambda *args: self.filtrar_tabla())
        tk.Button(search_bar, text="Limpiar Búsqueda", command=self._limpiar_filtros, bg="#334155", fg="#F8FAFC", relief="flat", padx=8, pady=2, cursor="hand2").pack(side="left", padx=4)

        table_container = tk.Frame(right_panel, bg="#1E293B")
        table_container.pack(fill="both", expand=True)

        columnas = ("id", "fecha", "concepto", "bs", "usd", "origen")
        self.tree = ttk.Treeview(table_container, columns=columnas, show="headings", selectmode="browse")
        self.tree.heading("id", text="#")
        self.tree.heading("fecha", text="FECHA")
        self.tree.heading("concepto", text="CONCEPTO / ACTIVIDAD DE GASTO")
        self.tree.heading("bs", text="MONTO (Bs.)")
        self.tree.heading("usd", text="MONTO ($ USD)")
        self.tree.heading("origen", text="ORIGEN DE FONDOS")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("fecha", width=85, anchor="center")
        self.tree.column("concepto", width=220, anchor="w")
        self.tree.column("bs", width=110, anchor="e")
        self.tree.column("usd", width=95, anchor="e")
        self.tree.column("origen", width=125, anchor="center")

        scrollbar_y = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.mostrar_detalle_renglon)
        self.tree.bind("<Double-1>", self.abrir_popup_detalle)

        self.detail_frame = tk.LabelFrame(right_panel, text=" 🔍 INSPECTOR DE PARTIDA SELECCIONADA ", bg="#0F172A", fg="#60A5FA", font=("Segoe UI", 10, "bold"), padx=12, pady=8, bd=1, relief="solid")
        self.detail_frame.pack(fill="x", pady=(8, 0))

        self.lbl_det_concepto = tk.Label(self.detail_frame, text="Selecciona o navega entre los gastos...", bg="#0F172A", fg="#FFFFFF", font=("Segoe UI", 11, "bold"), anchor="w")
        self.lbl_det_concepto.pack(fill="x", pady=(0, 4))

        grid_det = tk.Frame(self.detail_frame, bg="#0F172A")
        grid_det.pack(fill="x")
        for c in range(3):
            grid_det.columnconfigure(c, weight=1)

        self.lbl_det_col1 = tk.Label(grid_det, text="Fecha: --\nRenglón #: --\nOrigen: --", bg="#0F172A", fg="#CBD5E1", font=("Segoe UI", 10), justify="left", anchor="w")
        self.lbl_det_col1.grid(row=0, column=0, sticky="w")
        self.lbl_det_col2 = tk.Label(grid_det, text="Monto Bs.: --\nMonto USD: --\nTasa: --", bg="#0F172A", fg="#34D399", font=("Segoe UI", 10, "bold"), justify="left", anchor="w")
        self.lbl_det_col2.grid(row=0, column=1, sticky="w")
        self.lbl_det_col3 = tk.Label(grid_det, text="% Origen: --\n% Obra: --\nESOBADES", bg="#0F172A", fg="#60A5FA", font=("Segoe UI", 10), justify="left", anchor="w")
        self.lbl_det_col3.grid(row=0, column=2, sticky="w")

    def _crear_tarjeta_kpi(self, parent, col_idx, titulo, color_borde):
        card = tk.Frame(parent, bg="#1E293B", padx=12, pady=8, highlightbackground=color_borde, highlightthickness=2)
        card.grid(row=0, column=col_idx, sticky="nsew", padx=4)

        lbl_tit = tk.Label(card, text=titulo, bg="#1E293B", fg=color_borde, font=("Segoe UI", 9, "bold"))
        lbl_tit.pack(anchor="w")

        lbl_usd = tk.Label(card, text="$ 0.00", bg="#1E293B", fg="#FFFFFF", font=("Segoe UI", 14, "bold"))
        lbl_usd.pack(anchor="w", pady=(2, 0))

        lbl_bs = tk.Label(card, text="Bs. 0.00", bg="#1E293B", fg="#CBD5E1", font=("Segoe UI", 10, "bold"))
        lbl_bs.pack(anchor="w")

        lbl_sub = tk.Label(card, text="0 partidas", bg="#1E293B", fg="#94A3B8", font=("Segoe UI", 9))
        lbl_sub.pack(anchor="w", pady=(1, 0))

        return {"usd": lbl_usd, "bs": lbl_bs, "sub": lbl_sub}

    def seleccionar_filtro_origen(self, origen):
        self.filtro_origen.set(origen)
        self.filtrar_tabla()

    def _limpiar_filtros(self):
        self.filtro_origen.set("TODOS")
        self.busqueda_var.set("")
        self.filtrar_tabla()

    def actualizar_todo(self):
        if not self.datos_completos:
            self.card_total["usd"].config(text="$ 0.00")
            self.card_total["bs"].config(text="Bs. 0.00")
            self.card_total["sub"].config(text="0 partidas")
            self.card_propia["usd"].config(text="$ 0.00")
            self.card_propia["bs"].config(text="Bs. 0.00")
            self.card_propia["sub"].config(text="0 partidas")
            self.card_ecovida["usd"].config(text="$ 0.00")
            self.card_ecovida["bs"].config(text="Bs. 0.00")
            self.card_ecovida["sub"].config(text="0 partidas")
            if plt is not None:
                for ax in self.axes.flat:
                    ax.clear()
                self.canvas.draw()
            return

        tot_bs = sum(r["bs"] for r in self.datos_completos)
        tot_usd = sum(r["usd"] for r in self.datos_completos)
        cant_tot = len(self.datos_completos)

        prop_rows = [r for r in self.datos_completos if r["origen"] == "INVERSIÓN PROPIA"]
        eco_rows = [r for r in self.datos_completos if r["origen"] == "ECOVIDA"]

        prop_bs = sum(r["bs"] for r in prop_rows)
        prop_usd = sum(r["usd"] for r in prop_rows)
        eco_bs = sum(r["bs"] for r in eco_rows)
        eco_usd = sum(r["usd"] for r in eco_rows)

        self.card_total["usd"].config(text=f"$ {tot_usd:,.2f} USD")
        self.card_total["bs"].config(text=f"Bs. {tot_bs:,.2f}")
        self.card_total["sub"].config(text=f"{cant_tot} partidas válidas (100%)")

        pct_prop_usd = (prop_usd / tot_usd * 100) if tot_usd else 0
        self.card_propia["usd"].config(text=f"$ {prop_usd:,.2f} USD")
        self.card_propia["bs"].config(text=f"Bs. {prop_bs:,.2f}")
        self.card_propia["sub"].config(text=f"{len(prop_rows)} partidas ({pct_prop_usd:.1f}% USD)")

        pct_eco_usd = (eco_usd / tot_usd * 100) if tot_usd else 0
        self.card_ecovida["usd"].config(text=f"$ {eco_usd:,.2f} USD")
        self.card_ecovida["bs"].config(text=f"Bs. {eco_bs:,.2f}")
        self.card_ecovida["sub"].config(text=f"{len(eco_rows)} partidas ({pct_eco_usd:.1f}% USD)")

        self._dibujar_graficos(prop_bs, eco_bs, prop_usd, eco_usd)
        self.filtrar_tabla()

    def _dibujar_graficos(self, prop_bs, eco_bs, prop_usd, eco_usd):
        if plt is None:
            return

        for ax in self.axes.flat:
            ax.clear()

        labels = ["INVERSIÓN PROPIA", "ECOVIDA"]
        colores = ["#3B82F6", "#10B981"]
        bs_vals = [prop_bs / 1e6, eco_bs / 1e6]
        bs_exact = [prop_bs, eco_bs]
        usd_vals = [prop_usd, eco_usd]

        tot_bs_2 = prop_bs + eco_bs
        tot_usd_2 = prop_usd + eco_usd

        # 1. Barras Bs
        ax1 = self.axes[0, 0]
        ax1.set_facecolor("#0F172A")
        bars1 = ax1.bar(labels, bs_vals, color=colores, width=0.48, edgecolor="#F8FAFC", linewidth=1)
        ax1.set_title("Gastos en Bolívares (Millones Bs.)", color="#F8FAFC", fontsize=9.5, fontweight="bold", pad=6)
        ax1.tick_params(colors="#CBD5E1", labelsize=8)
        ax1.set_ylim(0, max(bs_vals) * 1.32 if max(bs_vals) > 0 else 1)
        ax1.grid(axis="y", linestyle="--", alpha=0.25, color="#94A3B8")
        for bar, exact in zip(bars1, bs_exact):
            h = bar.get_height()
            pct = (exact / tot_bs_2 * 100) if tot_bs_2 else 0
            ax1.annotate(f"Bs. {exact:,.1f}\n({pct:.1f}%)", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", color="#FFFFFF", fontsize=7.5, fontweight="bold")

        # 2. Barras USD
        ax2 = self.axes[0, 1]
        ax2.set_facecolor("#0F172A")
        bars2 = ax2.bar(labels, usd_vals, color=colores, width=0.48, edgecolor="#F8FAFC", linewidth=1)
        ax2.set_title("Gastos en Dólares ($ USD)", color="#F8FAFC", fontsize=9.5, fontweight="bold", pad=6)
        ax2.tick_params(colors="#CBD5E1", labelsize=8)
        ax2.set_ylim(0, max(usd_vals) * 1.32 if max(usd_vals) > 0 else 1)
        ax2.grid(axis="y", linestyle="--", alpha=0.25, color="#94A3B8")
        for bar, exact in zip(bars2, usd_vals):
            h = bar.get_height()
            pct = (exact / tot_usd_2 * 100) if tot_usd_2 else 0
            ax2.annotate(f"$ {exact:,.1f}\n({pct:.1f}%)", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", color="#FFFFFF", fontsize=7.5, fontweight="bold")

        # 3. Torta Bs
        ax3 = self.axes[1, 0]
        ax3.set_facecolor("#1E293B")
        if tot_bs_2 > 0:
            ax3.pie(bs_exact, labels=labels, autopct="%1.1f%%", startangle=140, colors=colores, pctdistance=0.72, explode=(0.03, 0.03), textprops=dict(color="#F8FAFC", fontsize=8, fontweight="bold"), wedgeprops=dict(edgecolor="#1E293B", linewidth=2))
            c1 = plt.Circle((0, 0), 0.46, fc="#1E293B")
            ax3.add_artist(c1)
            ax3.text(0, 0, f"Bs.\n{tot_bs_2/1e6:,.2f}M", ha="center", va="center", color="#F8FAFC", fontsize=7.5, fontweight="bold")
        ax3.set_title("Participación Bs. (Torta)", color="#F8FAFC", fontsize=9.5, fontweight="bold")

        # 4. Torta USD
        ax4 = self.axes[1, 1]
        ax4.set_facecolor("#1E293B")
        if tot_usd_2 > 0:
            ax4.pie(usd_vals, labels=labels, autopct="%1.1f%%", startangle=140, colors=colores, pctdistance=0.72, explode=(0.03, 0.03), textprops=dict(color="#F8FAFC", fontsize=8, fontweight="bold"), wedgeprops=dict(edgecolor="#1E293B", linewidth=2))
            c2 = plt.Circle((0, 0), 0.46, fc="#1E293B")
            ax4.add_artist(c2)
            ax4.text(0, 0, f"$ USD\n{tot_usd_2:,.1f}", ha="center", va="center", color="#F8FAFC", fontsize=7.5, fontweight="bold")
        ax4.set_title("Participación USD (Torta)", color="#F8FAFC", fontsize=9.5, fontweight="bold")

        self.canvas.draw()

    def filtrar_tabla(self):
        origen_sel = self.filtro_origen.get()
        query = self.busqueda_var.get().strip().lower()

        self.datos_filtrados = []
        for r in self.datos_completos:
            if origen_sel != "TODOS" and r["origen"] != origen_sel:
                continue
            if query and (query not in r["concepto"].lower() and query not in r["fecha"].lower() and query not in str(r["id"])):
                continue
            self.datos_filtrados.append(r)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for r in self.datos_filtrados:
            self.tree.insert("", "end", iid=str(r["id"]), values=(r["id"], r["fecha"], r["concepto"], f"Bs. {r['bs']:,.2f}", f"$ {r['usd']:,.2f}", r["origen"]))

    def _obtener_registro_seleccionado(self):
        sel = self.tree.selection()
        if not sel:
            return None
        rec_id = int(sel[0])
        for r in self.datos_completos:
            if r["id"] == rec_id:
                return r
        return None

    def mostrar_detalle_renglon(self, event=None):
        r = self._obtener_registro_seleccionado()
        if not r:
            return

        tot_usd = sum(x["usd"] for x in self.datos_completos)
        tot_origen_usd = sum(x["usd"] for x in self.datos_completos if x["origen"] == r["origen"])

        pct_obra = (r["usd"] / tot_usd * 100) if tot_usd > 0 else 0.0
        pct_origen = (r["usd"] / tot_origen_usd * 100) if tot_origen_usd > 0 else 0.0

        self.lbl_det_concepto.config(text=f"📌 CONCEPTO: {r['concepto'].upper()}")
        self.lbl_det_col1.config(text=f"• Renglón #: {r['id']}\n• Fecha: {r['fecha']}\n• Origen: {r['origen']}")
        self.lbl_det_col2.config(text=f"• Monto Bs.: Bs. {r['bs']:,.2f}\n• Monto USD: $ {r['usd']:,.2f}\n• Tasa: Bs. {r['tasa']:,.2f} / USD")
        self.lbl_det_col3.config(text=f"• % Origen: {pct_origen:.1f}%\n• % Obra: {pct_obra:.1f}%\n• ESOBADES")

    def abrir_popup_detalle(self, event=None):
        r = self._obtener_registro_seleccionado()
        if not r:
            return

        tot_usd = sum(x["usd"] for x in self.datos_completos)
        tot_bs = sum(x["bs"] for x in self.datos_completos)
        tot_origen_usd = sum(x["usd"] for x in self.datos_completos if x["origen"] == r["origen"])
        tot_origen_bs = sum(x["bs"] for x in self.datos_completos if x["origen"] == r["origen"])

        pct_obra_usd = (r["usd"] / tot_usd * 100) if tot_usd > 0 else 0.0
        pct_origen_usd = (r["usd"] / tot_origen_usd * 100) if tot_origen_usd > 0 else 0.0
        pct_obra_bs = (r["bs"] / tot_bs * 100) if tot_bs > 0 else 0.0
        pct_origen_bs = (r["bs"] / tot_origen_bs * 100) if tot_origen_bs > 0 else 0.0

        win = tk.Toplevel(self.root)
        win.title(f"Expediente de Partida #{r['id']} - {r['concepto']}")
        win.geometry("520x380")
        win.configure(bg="#0F172A", padx=20, pady=20)
        win.resizable(False, False)

        tk.Label(win, text="EXPEDIENTE DETALLADO DE PARTIDA", bg="#0F172A", fg="#34D399", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(win, text=r["concepto"].upper(), bg="#0F172A", fg="#FFFFFF", font=("Segoe UI", 14, "bold"), wraplength=480, justify="left").pack(anchor="w", pady=(4, 12))

        card = tk.Frame(win, bg="#1E293B", padx=16, pady=14, highlightbackground="#60A5FA", highlightthickness=1)
        card.pack(fill="both", expand=True)

        lineas = [
            ("Renglón / Fila en Archivo:", f"# {r['id']}"),
            ("Obra Asociada:", "REPARACIONES GENERALES EN INSTALACIONES DE ESOBADES"),
            ("Fecha de Operación:", r["fecha"]),
            ("Origen de los Fondos:", r["origen"]),
            ("Monto en Bolívares:", f"Bs. {r['bs']:,.2f}"),
            ("Monto en Dólares:", f"$ {r['usd']:,.2f} USD"),
            ("Tasa Implícita (Bs./USD):", f"Bs. {r['tasa']:,.2f}"),
            ("Incidencia en su Origen:", f"{pct_origen_bs:.1f}% (Bs.)  |  {pct_origen_usd:.1f}% (USD)"),
            ("Incidencia en Total Obra:", f"{pct_obra_bs:.1f}% (Bs.)  |  {pct_obra_usd:.1f}% (USD)")
        ]

        for idx_l, (k, v) in enumerate(lineas):
            row_f = tk.Frame(card, bg="#1E293B")
            row_f.pack(fill="x", pady=2)
            tk.Label(row_f, text=k, bg="#1E293B", fg="#94A3B8", font=("Segoe UI", 9, "bold")).pack(side="left")
            tk.Label(row_f, text=v, bg="#1E293B", fg="#F8FAFC", font=("Segoe UI", 9, "bold")).pack(side="right")

        tk.Button(win, text="Cerrar Ficha", command=win.destroy, bg="#3B82F6", fg="#FFFFFF", font=("Segoe UI", 10, "bold"), relief="flat", padx=16, pady=6, cursor="hand2").pack(pady=(12, 0))

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = DashboardESOBADESApp(root)
        root.mainloop()
    except Exception as e:
        error_trace = traceback.format_exc()
        messagebox.showerror("Error Critico", f"Ocurrió un error fatal al iniciar la aplicación:\n{str(e)}\n\n{error_trace}")
