# datos_app/views.py
import io
import base64
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Usar backend no-GUI para evitar warnings en Django
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import arff
from django.shortcuts import render

def get_graph_as_base64():
    """Convierte el gráfico de Matplotlib en una cadena Base64."""
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png') 
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')

# ==============================================================================
# 2. Funciones de Lectura y Particionado
# ==============================================================================
def load_kdd_dataset(data_path):
    """Lectura de dataset KDD desde archivo ARFF."""
    
    # Leer el archivo manualmente para obtener atributos y datos
    attributes = []
    data_section_started = False
    data_lines = []
    
    with open(data_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            
            # Ignorar líneas vacías y comentarios
            if not line or line.startswith('%'):
                continue
            
            # Detectar sección de datos
            if line.upper().startswith('@DATA'):
                data_section_started = True
                continue
            
            # Procesar atributos
            if line.upper().startswith('@ATTRIBUTE') and not data_section_started:
                # Extraer nombre del atributo
                parts = line.split(None, 2)  # Split en máximo 3 partes
                if len(parts) >= 2:
                    attr_name = parts[1].strip("'\"")  # Remover comillas
                    attributes.append(attr_name)
            
            # Procesar datos
            elif data_section_started:
                data_lines.append(line)
    
    # Parsear líneas de datos
    data = []
    for line in data_lines:
        if line:
            # Dividir por comas, pero respetando comillas
            values = []
            current = ''
            in_quotes = False
            
            for char in line:
                if char == '"':
                    in_quotes = not in_quotes
                elif char == ',' and not in_quotes:
                    # Limpiar comillas y espacios
                    val = current.strip().strip("'\"")
                    values.append(val)
                    current = ''
                    continue
                current += char
            
            if current:
                val = current.strip().strip("'\"")
                values.append(val)
            
            if values:
                data.append(values)
    
    # Crear DataFrame
    df = pd.DataFrame(data, columns=attributes)
    
    return df

def train_val_test_split(df, rstate=42, shuffle=True, stratify=None):
    """Función para particionado completo (60/20/20)"""
    # Nota: Se ignora el parámetro stratify para evitar errores con valores de bytes
    train_set, test_val_set = train_test_split(
        df, test_size=0.4, random_state=rstate, shuffle=shuffle, stratify=None
    )
    
    val_set, test_set = train_test_split(
        test_val_set, test_size=0.5, random_state=rstate, shuffle=shuffle, stratify=None
    )
    
    return train_set, val_set, test_set

# datos_app/views.py

# ... (código de imports y funciones auxiliares load_kdd_dataset y train_val_test_split)

def mostrar_datos(request):
    
    # RUTA ABSOLUTA (Verificada por el usuario)
    data_file_path = "/home/pred/Documentos/lenguajes_y_automatas/entorno_pesado/datasets/datasets/NSL-KDD/KDDTrain+.arff"
    datos_cargados = False
    graficas = {}
    logs = []
    df = pd.DataFrame()
    
    try:
       
        # 1. Carga del Dataset (usando SciPy)
        df = load_kdd_dataset(data_file_path)
        logs.append(f"Dataset cargado correctamente con SciPy: {len(df)} registros.")
        datos_cargados = True

        # 2. Particionado 60/20/20
        # === CORRECCIÓN CLAVE: SIN ESTRATIFICACIÓN ===
        # Se elimina stratify='protocol_type' para evitar el error de valor 'icmp'
        train_set, val_set, test_set = train_val_test_split(df) 
        # =============================================
        
        logs.append(f"     Particionado 60/20/20 completado:")
        logs.append(f"   - Training Set: {len(train_set)} ({len(train_set)/len(df)*100:.2f}%)")
        logs.append(f"   - Validation Set: {len(val_set)} ({len(val_set)/len(df)*100:.2f}%)")
        logs.append(f"   - Test Set: {len(test_set)} ({len(test_set)/len(df)*100:.2f}%)")

        # 3. Generación y Captura de Gráficas
        sets_a_graficar = {
            "Original": df,
            "Training": train_set,
            "Validation": val_set,
            "Test": test_set
        }

        for name, data_set in sets_a_graficar.items():
            plt.figure(figsize=(6, 4))
            # La columna 'protocol_type' se usa aquí para graficar, lo cual es seguro.
            data_set["protocol_type"].hist() 
            plt.title(f"{name} Set - Distribución de 'protocol_type'")
            plt.xlabel("protocol_type")
            plt.ylabel("Frecuencia")
            
            graficas[name] = get_graph_as_base64()
            plt.close()
            
    except FileNotFoundError as e:
        logs.append(f" ERROR CRÍTICO: Archivo no encontrado. Verifique la ruta y el nombre.")
        logs.append(f"Detalle: {e}")
    except KeyError as e:
        logs.append(f" ERROR: Columna no encontrada. Verifique que 'protocol_type' exista en el dataset. Error: {e}")
    except Exception as e:
        logs.append(f" ERROR INESPERADO: Error de datos o de ejecución. Error: {e}")


    contexto = {
        'titulo': "Despliegue de Análisis y Particionado KDD",
        'datos_cargados': datos_cargados,
        'logs': logs,
        'graficas': graficas,
        'df_head_html': df.head().to_html(classes='table table-bordered') if datos_cargados else None
    }
    
    return render(request, 'datos_app/datos.html', contexto)