import pandas as pd
import os
import glob
from pathlib import Path

print("=== PROGRAMA DE CALIFICACION DE EXAMENES === \n")

def combinar_archivos_excel(direc_entrada, arch_salida_com):
    """Combina todos los archivos Excel en uno solo."""
    archivos_excel = glob.glob(os.path.join(direc_entrada, "*.xlsx"))
    archivos_excel.extend(glob.glob(os.path.join(direc_entrada, "*.xls")))
    
    if not archivos_excel:
        print("ERROR. No se encontraron archivos Excel en la ruta especificada.")
        return None
    
    dataframes = []
    for archivo in archivos_excel:
        try:
            # Leer el archivo asegurando que las columnas se lean como strings
            df = pd.read_excel(archivo, dtype=str)
            df['archivo_origen'] = os.path.basename(archivo)
            dataframes.append(df)
        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")
    
    if dataframes:
        df_combinado = pd.concat(dataframes, ignore_index=True)
        
        # Limpiar nombres de columnas (eliminar espacios)
        df_combinado.columns = [str(col).strip() for col in df_combinado.columns]
        
        df_combinado.to_excel(arch_salida_com, index=False)
        print(f"\nArchivos combinados exitosamente en: {arch_salida_com}")
        print(f"Total de registros: {len(df_combinado)}")
        return df_combinado
    else:
        return None

def obtener_respuestas_correcta(archivo_respuestas):
    """Lee el archivo con formato vertical (pregunta | respuesta) y crea un diccionario"""
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
        
        # Crear diccionario de respuestas correctas
        respuestas_correctas = {}
        
        for _, row in df_respuestas.iterrows():
            pregunta = str(row[0]).strip()
            respuesta = str(row[1]).strip().upper()
            respuestas_correctas[pregunta] = respuesta
        
        print(f"\nTotal de respuestas cargadas: {len(respuestas_correctas)}")
        
        # Verificar específicamente las primeras preguntas
        print("\nVerificación primeras 5 respuestas:")
        for i in range(1, 6):
            if str(i) in respuestas_correctas:
                print(f"  Pregunta {i}: {respuestas_correctas[str(i)]}")
            else:
                print(f"  Pregunta {i}: NO ENCONTRADA en el diccionario")
        
        return respuestas_correctas
        
    except Exception as e:
        print(f"Error al cargar el archivo de respuestas: {e}")
        return None

def verificar_archivo_respuestas(archivo_respuestas):
    """Verifica que el archivo de respuestas sea válido antes de procesarlo"""
    try:
        # Verificar que el archivo existe
        if not os.path.exists(archivo_respuestas):
            print(f"ERROR: El archivo {archivo_respuestas} no existe.")
            return False
        
        # Verificar que no está vacío
        if os.path.getsize(archivo_respuestas) == 0:
            print(f"ERROR: El archivo {archivo_respuestas} está vacío.")
            return False
        
        # Intentar leerlo con pandas
        df_prueba = pd.read_excel(archivo_respuestas, header=None)
        
        if df_prueba.empty:
            print(f"ERROR: El archivo {archivo_respuestas} no contiene datos.")
            return False
        
        if df_prueba.shape[1] < 2:
            print(f"ERROR: El archivo debe tener al menos 2 columnas (pregunta | respuesta)")
            return False
            
        print(f"✓ Archivo de respuestas válido: {df_prueba.shape[0]} filas encontradas")
        return True
        
    except Exception as e:
        print(f"ERROR al verificar el archivo: {e}")
        return False

def calificar_examenes(df_examenes, respuestas_correctas):
    """Califica los exámenes comparando las respuestas de los alumnos con las correctas"""
    print("\n=== INICIANDO CALIFICACIÓN ===")
    
    # Verificar que df_examenes no esté vacío
    if df_examenes is None or df_examenes.empty:
        print("ERROR: El DataFrame de exámenes está vacío o es nulo")
        return None
    
    # Mostrar información del DataFrame
    print(f"Dimensiones del DataFrame: {df_examenes.shape}")
    print(f"Columnas disponibles: {list(df_examenes.columns)}")
    
    # Identificar columnas de respuestas (números del 1 al 20)
    columnas_respuestas = []
    for i in range(1, 21):
        col_name = str(i)
        if col_name in df_examenes.columns:
            columnas_respuestas.append(col_name)
    
    if not columnas_respuestas:
        print("\nERROR CRÍTICO: No se encontraron columnas de respuestas (1-20)")
        return None
    
    print(f"\nColumnas de respuestas encontradas: {columnas_respuestas}")
    print(f"Total de preguntas a calificar: {len(columnas_respuestas)}")
    
    # DEPURACIÓN: Mostrar las respuestas correctas
    print("\n=== DEPURACIÓN: RESPUESTAS CORRECTAS ===")
    for i in range(1, 6):  # Mostrar primeras 5
        if str(i) in respuestas_correctas:
            print(f"Pregunta {i}: {respuestas_correctas[str(i)]}")
    
    calificaciones = []
    
    # Tomar SOLO EL PRIMER ESTUDIANTE para depurar (Mateo Hernández)
    primer_estudiante = df_examenes.iloc[0]
    nombre_estudiante = primer_estudiante['NOMBRES'] if 'NOMBRES' in df_examenes.columns else "Estudiante_1"
    
    print(f"\n=== DEPURACIÓN: PRIMER ESTUDIANTE ({nombre_estudiante}) ===")
    
    aciertos = 0
    total_preguntas = len(columnas_respuestas)
    
    for i, col in enumerate(columnas_respuestas, 1):
        # Obtener respuesta del alumno
        if pd.notna(primer_estudiante[col]):
            respuesta_est = str(primer_estudiante[col]).strip().upper()
        else:
            respuesta_est = ""
        
        # Obtener respuesta correcta
        pregunta_key = str(i)
        if pregunta_key in respuestas_correctas:
            respuesta_correcta = respuestas_correctas[pregunta_key]
            
            # Mostrar comparación
            coincide = "✓" if respuesta_est == respuesta_correcta else "✗"
            print(f"P{i}: Alumno='{respuesta_est}' vs Correcta='{respuesta_correcta}' {coincide}")
            
            if respuesta_est == respuesta_correcta:
                aciertos += 1
        else:
            print(f"P{i}: ADVERTENCIA - No hay respuesta correcta para pregunta {pregunta_key}")
    
    print(f"\nTotal aciertos primer estudiante: {aciertos}/{total_preguntas}")
    
    # Ahora procesar TODOS los estudiantes
    print("\n=== PROCESANDO TODOS LOS ESTUDIANTES ===")
    
    for index, row in df_examenes.iterrows():
        try:
            aciertos = 0
            total_preguntas = len(columnas_respuestas)
            
            # Obtener nombre del estudiante
            nombre_estudiante = f"Estudiante_{index+1}"
            if 'NOMBRES' in df_examenes.columns:
                nombre_estudiante = row['NOMBRES'] if pd.notna(row['NOMBRES']) else f"Estudiante_{index+1}"
            
            # Calificar cada respuesta
            for i, col in enumerate(columnas_respuestas, 1):
                # Obtener respuesta del alumno
                if pd.notna(row[col]):
                    respuesta_est = str(row[col]).strip().upper()
                else:
                    respuesta_est = ""
                
                # Comparar con respuesta correcta
                pregunta_key = str(i)
                if pregunta_key in respuestas_correctas:
                    respuesta_correcta = respuestas_correctas[pregunta_key]
                    if respuesta_est == respuesta_correcta:
                        aciertos += 1
            
            calificacion = (aciertos / total_preguntas) * 100 if total_preguntas > 0 else 0
            
            # Crear registro
            registro = {
                'nombre': nombre_estudiante,
                'aciertos': aciertos,
                'total_preguntas': total_preguntas,
                'calificaciones': round(calificacion, 2)
            }
            
            calificaciones.append(registro)
            
            # Mostrar progreso (solo primeros 3 para depuración)
            if index < 3:
                print(f"{nombre_estudiante}: {aciertos}/{total_preguntas} = {calificacion}%")
                
        except Exception as e:
            print(f"Error al procesar estudiante en fila {index}: {e}")
            continue
    
    if not calificaciones:
        print("ERROR: No se pudo calificar ningún estudiante")
        return None
    
    return pd.DataFrame(calificaciones)

# ==== AQUI INICIA EL PROGRAMA PRINCIPAL ====
print("INICIANDO EL PROCESO DE CALIFICACION")
print("=" * 50)

# Directorio de exámenes
directorio_examenes = input("\nIngrese la ruta del directorio con los archivos de examenes: ")

if not os.path.exists(directorio_examenes):
    print("El directorio no existe. Usando el directorio actual.")
    directorio_examenes = "."

archivo_combinado = "examenes_combinados.xlsx"

# Combinar archivos de exámenes
print("\n--- COMBINANDO ARCHIVOS DE EXAMENES ---")
df_combinado = combinar_archivos_excel(directorio_examenes, archivo_combinado)

if df_combinado is None:
    print("No se pudieron combinar los archivos. Saliendo...")
    exit()

print(f"\nArchivo combinado creado: {archivo_combinado}")
print(f"Total de registros combinados: {len(df_combinado)}")

# === VERIFICACIÓN DEL ARCHIVO COMBINADO ===
print("\n=== VERIFICACIÓN DEL ARCHIVO COMBINADO ===")
print(f"Dimensiones: {df_combinado.shape}")
print(f"Columnas: {list(df_combinado.columns)}")
print("\nPrimeras 3 filas:")
print(df_combinado.head(3))
print("\nNombres de columnas que son números:")
numeros = [col for col in df_combinado.columns if str(col).strip().isdigit()]
print(numeros)

# === CARGAR RESPUESTAS CORRECTAS ===
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

# === VERIFICACIÓN DE RESPUESTAS CORRECTAS ===
print("\n=== VERIFICACIÓN DE RESPUESTAS CORRECTAS ===")
print("Ejemplo de respuestas correctas (primeras 5):")
for i in range(1, 6):
    if str(i) in respuestas_correctas:
        print(f"  Pregunta {i}: {respuestas_correctas[str(i)]}")

# === CALIFICAR EXÁMENES ===
print("\n" + "=" * 50)
print("INICIA CALIFICACION DE EXAMENES")
print("=" * 50)

df_resultados = calificar_examenes(df_combinado, respuestas_correctas)

# VERIFICACIÓN CRÍTICA
if df_resultados is None:
    print("\n" + "=" * 50)
    print("ERROR: No se pudo generar la tabla de resultados")
    print("Posibles causas:")
    print("1. El archivo combinado no tiene el formato esperado")
    print("2. Las columnas de respuestas no se encontraron (deben llamarse 1,2,3,...)")
    print("3. Hay un error en los datos")
    print("\nInformación de depuración:")
    print(f"- Tipo de df_combinado: {type(df_combinado)}")
    if df_combinado is not None:
        print(f"- Columnas en df_combinado: {list(df_combinado.columns)}")
        print(f"- Primeras filas:\n{df_combinado.head()}")
    exit()

# Ordenar resultados
df_resultados = df_resultados.sort_values('calificaciones', ascending=False)

# === GUARDAR RESULTADOS ===
print("\n--- GUARDAR RESULTADOS ---")
archivo_resultados = input("Ingrese el nombre del archivo para guardar los resultados (ej: resultados.xlsx): ").strip()

if not archivo_resultados:
    archivo_resultados = "resultados_calificaciones.xlsx"
elif not archivo_resultados.endswith('.xlsx'):
    archivo_resultados += '.xlsx'

# Guardar resultados
df_resultados.to_excel(archivo_resultados, index=False)

# Mostrar resumen
print(f"\n{'=' * 50}")
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 50)
print(f"Resultados guardados en: {archivo_resultados}")
print(f"Total de estudiantes calificados: {len(df_resultados)}")

print(f"\nRESUMEN DE CALIFICACIONES:")
print(f"=> Calificación más alta: {df_resultados['calificaciones'].max()}")
print(f"=> Calificación más baja: {df_resultados['calificaciones'].min()}")
print(f"=> Calificación promedio: {df_resultados['calificaciones'].mean():.2f}")

# Mostrar top 5 estudiantes
print(f"\nTOP 5 MEJORES ESTUDIANTES:")
top_5 = df_resultados.head(5)
for i, (_, row) in enumerate(top_5.iterrows(), 1):
    print(f"{i}. {row['nombre']}: {row['calificaciones']}% ({row['aciertos']}/{row['total_preguntas']})")

# Mostrar estudiantes con calificación baja (opcional)
print(f"\nESTUDIANTES CON CALIFICACIÓN BAJA (< 60%):")
bajos = df_resultados[df_resultados['calificaciones'] < 60]
if not bajos.empty:
    for i, (_, row) in enumerate(bajos.iterrows(), 1):
        print(f"{i}. {row['nombre']}: {row['calificaciones']}% ({row['aciertos']}/{row['total_preguntas']})")
else:
    print("No hay estudiantes con calificación baja")

print("\n¡PROGRAMA FINALIZADO!")