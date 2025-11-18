import arff
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt # ¡Nueva Importación!

# ==============================================================================
# 1.- Lectura del Dataset
# ==============================================================================

def load_kdd_dataset(data_path):
    """Lectura de dataset KDD"""
    with open(data_path, "r")as train_set:
        dataset = arff.load(train_set)
        atributes = [attr[0] for attr in dataset["attributes"]]
        return pd.DataFrame(dataset["data"], columns=atributes)

# NOTA IMPORTANTE: Asegúrate de cambiar esta ruta al archivo ARFF en tu sistema.
data_file_path = "/home/pred/Documentos/lenguajes y automatas/entorno pesado/datasets/datasets/NSL-KDD/KDDTrain+.arff"
try:
    df = load_kdd_dataset(data_file_path)
    print(f"Dataset cargado correctamente desde: {data_file_path}")
    print("\nInformación inicial del DataFrame:")
    df.info()
except FileNotFoundError:
    print(f"ERROR: Archivo no encontrado en la ruta: {data_file_path}")
    print("Por favor, actualiza la variable 'data_file_path' con la ruta correcta a 'KDDTrain+.arff'.")
    # Salir si el archivo no se puede cargar, ya que el resto del script fallará.
    exit()

# ==============================================================================
# 2.- División del Dataset (Ejemplo Básico)
# ==============================================================================

# separar el dataset 60% train set, 40% test set
train_set, test_set = train_test_split(df, test_size=0.4, random_state=42)

print("\nInformación del Training Set (después de 60/40 split):")
train_set.info()

# Separar el Dataset de pruebas 50% validacion set, 50% test set
# Esto convierte el 40% inicial de 'test_set' en un 20% para 'val_set' y 20% para 'test_set'
val_set, test_set = train_test_split(test_set, test_size=0.5, random_state=42)

print("\nResumen de longitudes de los conjuntos (split 60/20/20 aleatorio):")
print("Longitud del Training Set:", len(train_set))
print("Longitud del Validacion Set:", len(val_set))
print("Longitud del Test Set:", len(test_set))


# ==============================================================================
# 3.- Particionado Aleatorio y Stratified Sampling
# ==============================================================================

# Si shuffle es igual a False, el Dataset no se mezclará antes del particionado.
# Se toman las primeras filas para el train set y las siguientes para el test set.
print("\nEjecutando split sin shuffle (shuffle=False):")
train_set_no_shuffle, test_set_no_shuffle = train_test_split(df, test_size=0.4, random_state=42, shuffle=False)
print("Longitud del Training Set (no shuffle):", len(train_set_no_shuffle))

# Stratified Sampling: Asegura que la proporción de los valores de una columna
# (en este caso 'protocol_type') sea la misma en los conjuntos resultantes.
print("\nEjecutando split con Stratified Sampling:")
train_set_stratify, test_set_stratify = train_test_split(df, test_size=0.4, random_state=42, stratify=df['protocol_type'])
print("Longitud del Training Set (stratify):", len(train_set_stratify))

# ==============================================================================
# 4.- Generación de una función de particionado completo (60/20/20)
# ==============================================================================

# Construcción de una función que realice el particionado completo
def train_val_test_split(df, rstate=42, shuffle=True, stratify=None):
    # Nota: Se ignora el parámetro stratify para evitar errores con valores de bytes
    # División 1: 60% train, 40% test+val
    train_set, test_val_set = train_test_split(
        df, test_size=0.4, random_state=rstate, shuffle=shuffle, stratify=None
    )
    
    # División 2: del 40% restante, se divide 50% para val y 50% para test (20% y 20% del total)
    val_set, test_set = train_test_split(
        test_val_set, test_size=0.5, random_state=rstate, shuffle=shuffle, stratify=None
    )
    
    return train_set, val_set, test_set

print("\nLongitud total del DataSet:", len(df))

# CORRECCIÓN: Se elimina stratify='protocol_type' para evitar errores con valores ICMP
# El stratified sampling puede causar problemas si los valores en la columna no son válidos
train_set, val_set, test_set = train_val_test_split(df)

print("\nResumen de longitudes de los conjuntos (usando train_val_test_split):")
print("Longitud del Training Set:", len(train_set))
print("Longitud del Validation Set:", len(val_set))
print("Longitud del Test Set:", len(test_set))


# ==============================================================================
# 5.- Comparación de Stratified Sampling
# ==============================================================================

print("\nMostrando Histograma de 'protocol_type' para el DataSet Original, Train, Val y Test:")
print("Cierre cada ventana de gráfico para ver la siguiente.")

# Gráfico 1: DataSet Original
df["protocol_type"].hist()
plt.title("DataSet Original - Distribución de 'protocol_type'")
plt.xlabel("protocol_type")
plt.ylabel("Frecuencia")
plt.show() # Se muestra el primer gráfico 

# Gráfico 2: Training Set
train_set["protocol_type"].hist()
plt.title("Training Set - Distribución de 'protocol_type'")
plt.xlabel("protocol_type")
plt.ylabel("Frecuencia")
plt.show()

# Gráfico 3: Validation Set
val_set["protocol_type"].hist()
plt.title("Validation Set - Distribución de 'protocol_type'")
plt.xlabel("protocol_type")
plt.ylabel("Frecuencia")
plt.show()

# Gráfico 4: Test Set
test_set["protocol_type"].hist()
plt.title("Test Set - Distribución de 'protocol_type'")
plt.xlabel("protocol_type")
plt.ylabel("Frecuencia")
plt.show()