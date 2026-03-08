import pandas as pd
import os
import glob
from pathlib import Path

print("=== PROGRAMA DE CALIFICACION DE EXAMENES === \n")

def combinar_archivos_excel(direc_entrada, arch_salida_com):
    #Combina todos los archivos Excel en uno solo
    archivos_excel = glob.glob(os.path.join(direc_entrada, "*.xlsx"))
    archivos_excel.extend(glob.glob(os.path.join(direc_entrada, "*.xls")))
    
    if not archivos_excel:
        print("ERROR. No se encontraron archivos Excel en la ruta especificada.")
        return None
    
    dataframes = []
    for archivo in archivos_excel:
        try:
            # Lee el archivo asegurando que las columnas se lean como strings
            df = pd.read_excel(archivo, dtype=str)
            df['archivo_origen'] = os.path.basename(archivo)
            dataframes.append(df)
        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")
    
    if dataframes:
        df_combinado = pd.concat(dataframes, ignore_index=True)
        
        # Limpia nombres de columnas i,e (eliminar espacios)
        df_combinado.columns = [str(col).strip() for col in df_combinado.columns]
        
        df_combinado.to_excel(arch_salida_com, index=False)
        print(f"\nArchivos combinados exitosamente en: {arch_salida_com}")
        print(f"Total de registros: {len(df_combinado)}")
        return df_combinado
    else:
        return None

def obtener_respuestas_correcta(archivo_respuestas):
    #Lee el archivo con formato vertical (pregunta | respuesta) y crea un diccionario el cual usaremos para calificar
    try:
        df_respuestas = pd.read_excel(archivo_respuestas, header=None, dtype=str)
        
        if df_respuestas.empty:
            print("ERROR: El archivo de respuestas está vacío.")
            return None
        
        print(f"\nArchivo de respuestas cargado:")
        print(f"- Dimensiones: {df_respuestas.shape[0]} filas x {df_respuestas.shape[1]} columnas")
        print(f"- Primeras 5 filas del archivo:")
        for i in range(min(5, len(df_respuestas))):
            print(f"  Fila {i+1}: Pregunta='{df_respuestas.iloc[i, 0]}', Respuesta='{df_respuestas.iloc[i, 1]}'")
        
        # Crea diccionario de respuestas correctas
        respuestas_correctas = {}
        
        for _, row in df_respuestas.iterrows():
            pregunta = str(row[0]).strip()
            respuesta = str(row[1]).strip().upper()
            respuestas_correctas[pregunta] = respuesta
        
        print(f"\nTotal de respuestas cargadas: {len(respuestas_correctas)}")
        
        # Verifica específicamente las primeras preguntas
        print("\nVerificación primeras 5 respuestas:")
        for i in range(1, 6):
            if str(i) in respuestas_correctas:
                print(f"  Pregunta {i}: {respuestas_correctas[str(i)]}")
            else:
                print(f"  Pregunta {i}: NO ENCONTRADA en el diccionario")
        
        return respuestas_correctas
        
    except Exception as e:
        print(f"Error al cargar el archivo de respuestas: {e}")#Muestra con exactitud cual es el error {e}
        return None

def verificar_archivo_respuestas(archivo_respuestas):
    #Verifica que el archivo de respuestas sea válido antes de procesarlo esto es solo por los posibles errores que pueden ocurrir al cargar el arch
    try:
        # Verifica que el archivo exista
        if not os.path.exists(archivo_respuestas):
            print(f"ERROR: El archivo {archivo_respuestas} no existe.")
            return False
        
        # Verifica que no está vacío
        if os.path.getsize(archivo_respuestas) == 0:
            print(f"ERROR: El archivo {archivo_respuestas} está vacío.")
            return False
        
        # Intenta leerlo usando la lib pandas
        df_prueba = pd.read_excel(archivo_respuestas, header=None)
        
        if df_prueba.empty:#revisa si el archivo tiene datos y tambien marca error si el archivo no tiene la estructura deseada
            print(f"ERROR: El archivo {archivo_respuestas} no contiene datos.")
            return False
        
        if df_prueba.shape[1] < 2:#verifica que el archivo respuestas tenga el siguiente formato
            print(f"ERROR: El archivo debe tener al menos 2 columnas (pregunta | respuesta)")
            return False
            
        print(f"Archivo de respuestas válido: {df_prueba.shape[0]} filas encontradas")
        return True
        
    except Exception as e:
        print(f"ERROR al verificar el archivo: {e}")
        return False

def calificar_examenes(df_examenes, respuestas_correctas):
    #funciion que califica los exámenes comparando las respuestas de los alumnos con las correctas
    print("\n=== INICIANDO CALIFICACIÓN ===")
    
    # Verifica que df_examenes no esté vacío
    if df_examenes is None or df_examenes.empty:
        print("ERROR: El DataFrame de exámenes está vacío o es nulo")
        return None
    
    # Muestra información del DataFrame
    print(f"Dimensiones del DataFrame: {df_examenes.shape}")
    print(f"Columnas disponibles: {list(df_examenes.columns)}")
    
    # Identifica columnas de respuestas (números del 1 al 20)esto puede variar dependiendo el total de respuestas
    columnas_respuestas = []
    for i in range(1, 11):#aca ajustamos dependiendo de nuestras necesidades
        col_name = str(i)
        if col_name in df_examenes.columns:
            columnas_respuestas.append(col_name)
    
    if not columnas_respuestas:
        print("\nERROR CRÍTICO: No se encontraron columnas de respuestas (1-20)")
        return None
    
    print(f"\nColumnas de respuestas encontradas: {columnas_respuestas}")
    print(f"Total de preguntas a calificar: {len(columnas_respuestas)}")
    
    # muestrar las respuestas correctas, esto para verificar que se allá cargado bien en caso necesario se puede quitar
    print("\n=== RESPUESTAS CORRECTAS ===")
    for i in range(1, 6):  # muestra las primeras 5
        if str(i) in respuestas_correctas:
            print(f"Pregunta {i}: {respuestas_correctas[str(i)]}")
    
    calificaciones = []
    
    # Toma SOLO EL PRIMER ESTUDIANTE para obs que se alla cargado bien, puede ser opcional solo lo ocupe para ver mis errores
    primer_estudiante = df_examenes.iloc[0]
    nombre_estudiante = primer_estudiante['NOMBRES'] if 'NOMBRES' in df_examenes.columns else "Estudiante_1"
    
    print(f"\n=== PRIMER ESTUDIANTE ({nombre_estudiante}) ===")
    
    aciertos = 0
    total_preguntas = len(columnas_respuestas)
    
    for i, col in enumerate(columnas_respuestas, 1):
        # Obtiene respuestas del alumno
        if pd.notna(primer_estudiante[col]):
            respuesta_est = str(primer_estudiante[col]).strip().upper()
        else:
            respuesta_est = ""
        
        # Obtiene respuestas correctas
        pregunta_key = str(i)
        if pregunta_key in respuestas_correctas:
            respuesta_correcta = respuestas_correctas[pregunta_key]
            
            # Muestra comparación
            coincide = "/" if respuesta_est == respuesta_correcta else "x"
            print(f"P{i}: Alumno='{respuesta_est}' vs Correcta='{respuesta_correcta}' {coincide}")
            
            if respuesta_est == respuesta_correcta:
                aciertos += 1
        else:
            print(f"P{i}: ADVERTENCIA - No hay respuesta correcta para pregunta {pregunta_key}")
    
    print(f"\nTotal aciertos primer estudiante: {aciertos}/{total_preguntas}")
    
    # procesar a todos los estudiantes para obtner nombres 
    print("\n=== PROCESANDO TODOS LOS ESTUDIANTES ===")
    
    for index, row in df_examenes.iterrows():
        try:
            aciertos = 0
            total_preguntas = len(columnas_respuestas)
            
            # Obtenie el nombre de los estudiantes
            nombre_estudiante = f"Estudiante_{index+1}"
            if 'NOMBRES' in df_examenes.columns:
                nombre_estudiante = row['NOMBRES'] if pd.notna(row['NOMBRES']) else f"Estudiante_{index+1}"
            
            # Califica cada respuesta
            for i, col in enumerate(columnas_respuestas, 1):
                # Obtenie respuesta del alumno, inciso a inciso
                if pd.notna(row[col]):
                    respuesta_est = str(row[col]).strip().upper()
                else:
                    respuesta_est = ""
                
                # Compara con las respuestas correctas
                pregunta_key = str(i)
                if pregunta_key in respuestas_correctas:
                    respuesta_correcta = respuestas_correctas[pregunta_key]
                    if respuesta_est == respuesta_correcta:
                        aciertos += 1
            
            calificacion = (aciertos / total_preguntas) * 100 if total_preguntas > 0 else 0
            
            # Crea registro
            registro = {
                'nombre': nombre_estudiante,
                'aciertos': aciertos,
                'total_preguntas': total_preguntas,
                'calificaciones': round(calificacion, 2)
            }
            
            calificaciones.append(registro)
            
            # Muestra progreso (solo primeros 3 para obs que valla bien, en caso de error podemos detectar el error)
            if index < 3:
                print(f"{nombre_estudiante}: {aciertos}/{total_preguntas} = {calificacion}%")
                
        except Exception as e:#imprime la causa del error y continua con el programa
            print(f"Error al procesar estudiante en fila {index}: {e}")
            continue
    
    if not calificaciones:
        print("ERROR: No se pudo calificar ningún estudiante")
        return None
    
    return pd.DataFrame(calificaciones)

# ==== AQUI INICIA EL PROGRAMA PRINCIPAL ====
print("INICIANDO EL PROCESO DE CALIFICACION")
print("=" * 50)

# pedimos al usiario que ingrese el directorio de exámenes i,e hacer pwd en para obtner la ruta del los archivos
# obligatoriamente deben de estar todos los excel en una misma carpeta a exepcion del excel de las respuestas
directorio_examenes = input("\nIngrese la ruta del directorio con los archivos de examenes: ")

if not os.path.exists(directorio_examenes):#Verificamos si existe la ruta dada
    print("El directorio no existe. Usando el directorio actual.")
    directorio_examenes = "."

archivo_combinado = "examenes_combinados.xlsx"

# aqui combinamos los archivos de exámenes
print("\n--- COMBINANDO ARCHIVOS DE EXAMENES ---")
df_combinado = combinar_archivos_excel(directorio_examenes, archivo_combinado)

if df_combinado is None:
    print("No se pudieron combinar los archivos. Saliendo...")
    exit()

print(f"\nArchivo combinado creado: {archivo_combinado}")
print(f"Total de registros combinados: {len(df_combinado)}")

# VERIFICACIÓN DEL ARCHIVO COMBINADO (esto es para verificar que la carga valla bien, puede ser opcional)
print("\n=== VERIFICACIÓN DEL ARCHIVO COMBINADO ===")
print(f"Dimensiones: {df_combinado.shape}")
print(f"Columnas: {list(df_combinado.columns)}")
print("\nPrimeras 3 filas:")
print(df_combinado.head(3))
print("\nNombres de columnas que son números:")
numeros = [col for col in df_combinado.columns if str(col).strip().isdigit()]
print(numeros)

# === CARGA RESPUESTAS CORRECTAS ===
print("\n" + "=" * 50)
print("INICIANDO CARGA DE LAS RESPUESTAS CORRECTAS")
print("=" * 50)

archivo_respuestas = input("\nIngrese la ruta del archivo excel con las respuestas correctas: ").strip()

while not os.path.exists(archivo_respuestas) or not verificar_archivo_respuestas(archivo_respuestas):
    print("\nEl archivo no es válido. Intente de nuevo.")
    archivo_respuestas = input("Ingrese la ruta del archivo excel con las respuestas correctas: ").strip()

respuestas_correctas = obtener_respuestas_correcta(archivo_respuestas)

if respuestas_correctas is None:
    print("No se pudieron cargar las respuestas correctas. Saliendo...")
    exit()

print(f"\nRespuestas correctas cargadas: {len(respuestas_correctas)} preguntas")

# VERIFICACIÓN DE RESPUESTAS CORRECTAS
print("\n=== VERIFICACIÓN DE RESPUESTAS CORRECTAS ===")
print("Ejemplo de respuestas correctas (primeras 5):")
for i in range(1, 6):
    if str(i) in respuestas_correctas:
        print(f"  Pregunta {i}: {respuestas_correctas[str(i)]}")

# === CALIFICA LOS EXÁMENES ===
print("\n" + "=" * 50)
print("INICIA CALIFICACION DE EXAMENES")
print("=" * 50)

df_resultados = calificar_examenes(df_combinado, respuestas_correctas)

# Ordena los resultados
df_resultados = df_resultados.sort_values('calificaciones', ascending=False)

# === GUARDA LOS RESULTADOS ===
print("\n--- GUARDANDO RESULTADOS ---")
archivo_resultados = input("Ingrese el nombre del archivo para guardar los resultados (ej: resultados.xlsx): ").strip()

if not archivo_resultados:
    archivo_resultados = "resultados_calificaciones.xlsx"
elif not archivo_resultados.endswith('.xlsx'):
    archivo_resultados += '.xlsx'

# Guarda los resultados
df_resultados.to_excel(archivo_resultados, index=False)

# Muestra el resumen final
print(f"\n{'=' * 50}")
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 50)
print(f"Resultados guardados en: {archivo_resultados}")
print(f"Total de estudiantes calificados: {len(df_resultados)}")

print(f"\nRESUMEN DE CALIFICACIONES:")
print(f"=> Calificación más alta: {df_resultados['calificaciones'].max()}")
print(f"=> Calificación más baja: {df_resultados['calificaciones'].min()}")
print(f"=> Calificación promedio: {df_resultados['calificaciones'].mean():.2f}")

print("\n¡PROGRAMA FINALIZADO!")