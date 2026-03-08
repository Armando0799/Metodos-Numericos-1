import pandas as pd
import os
import glob
from pathlib import Path
#este es el que funciona correctamente
print("=== PROGRAMA DE CALIFICACION DE EXAMENES === \n")

def combinar_archivos_excel(direc_entrada, arch_salida_com):
    #Combina todos los archivos Excel en uno solo
    # Busca los archivos .xlsx y .xls, excluyendo archivos temporales (~$)
    archivos_excel = [f for f in glob.glob(os.path.join(direc_entrada, "*.xlsx")) 
                      if not os.path.basename(f).startswith('~$')]
    archivos_excel.extend([f for f in glob.glob(os.path.join(direc_entrada, "*.xls")) 
                          if not os.path.basename(f).startswith('~$')])
    
    if not archivos_excel:
        print("ERROR. No se encontraron archivos Excel en la ruta especificada.")
        return None
    
    print(f"Archivos encontrados: {len(archivos_excel)}")
    
    dataframes = []
    for archivo in archivos_excel:
        try:
            print(f"\nProcesando: {os.path.basename(archivo)}")
            
            #IMPORTANTE: Lee el archivo para inspeccionar su estructura, es la parte que me costo uno y la mitad
            df_raw = pd.read_excel(archivo, header=None, dtype=str)
            
            # Busca la fila que contiene los encabezados correctos
            header_row = None
            for i in range(min(10, len(df_raw))):  #Revisa las primeras 10 filas
                row_values = df_raw.iloc[i].astype(str).tolist()
                # Busca si alguna celda contiene "Nombre completo", ya que normalmente es la que contiene el encabezado
                if any('Nombre completo' in str(val) for val in row_values):
                    header_row = i
                    print(f" => Encabezados encontrados en fila {i+1}")
                    break
            
            if header_row is not None:
                # Usa la fila encontrada como encabezado
                df = pd.read_excel(archivo, header=header_row, dtype=str)
            else:
                # Si no encuentra, usa la fila 2 como intento, fila 2 en python = fila 3 en excel
                print("No se encontró 'Nombre completo', usando fila 3 como encabezado")
                df = pd.read_excel(archivo, header=2, dtype=str)
            
            # Elimina las filas completamente vacías, esto no me funciona totalmete bien ya que deja varias filas vacias
            # pero es porque al final de la fila siempre lleva un nombre que proviene de la direccion de procedencia
            df = df.dropna(how='all')
            
            # Elimina las columnas completamente vacías, por si llegará a haber y evitar que se rompa el programa
            df = df.dropna(axis=1, how='all')
            
            # Limpia los nombres de columnas
            df.columns = [str(col).strip() for col in df.columns]
            
            # Identifica las columnas de respuestas (P1, P2, etc. O columnas con letras como en el caso de los archivos que tienen)
            print(f" => Columnas encontradas: {list(df.columns)[:10]}...")
            
            df['archivo_origen'] = os.path.basename(archivo)
            dataframes.append(df)
            print(f" / Registros en este archivo: {len(df)}")
            
        except Exception as e:
            print(f" Error al procesar {archivo}: {e}")
    
    if dataframes:
        df_combinado = pd.concat(dataframes, ignore_index=True)
        
        # Limpia nombres de columnas (eliminar espacios)
        df_combinado.columns = [str(col).strip() for col in df_combinado.columns]
        
        # Guarda el archivo combinado
        df_combinado.to_excel(arch_salida_com, index=False)
        print(f"\n Archivos combinados exitosamente en: {arch_salida_com}")
        print(f" Total de registros: {len(df_combinado)}")
        print(f" Columnas finales: {list(df_combinado.columns)}")
        return df_combinado
    else:
        return None

def identificar_columnas_respuestas(df):
    # Identifica automáticamente las columnas que contienen respuestas
    columnas_respuestas = []
    
    # Busca las columnas que empiezan con 'P' seguido de número (ej: P1, P2)
    for col in df.columns:
        col_str = str(col).strip()
        if col_str.startswith('P') and col_str[1:].isdigit():
            columnas_respuestas.append(col_str)
    
    # Si no encuentra con P, busca columnas que sean letras individuales ()
    if not columnas_respuestas:
        letras = ['a', 'b', 'c', 'd', 'e', 'A', 'B', 'C', 'D', 'E']
        for col in df.columns:
            col_str = str(col).strip()
            # Si la columna es una letra individual
            if col_str in letras or (len(col_str) == 1 and col_str.isalpha()):
                columnas_respuestas.append(col_str)
    
    return columnas_respuestas

def obtener_respuestas_correcta(archivo_respuestas):
    # Lee el archivo con formato vertical (pregunta | respuesta)
    try:
        df_respuestas = pd.read_excel(archivo_respuestas, header=None, dtype=str)
        
        if df_respuestas.empty:
            print("ERROR: El archivo de respuestas está vacío.")
            return None
        
        print(f"\n Archivo de respuestas cargado:")
        print(f" Dimensiones: {df_respuestas.shape[0]} filas x {df_respuestas.shape[1]} columnas")
        
        # Crea diccionario de respuestas correctas
        respuestas_correctas = {}
        
        for _, row in df_respuestas.iterrows():
            pregunta = str(row[0]).strip()
            respuesta = str(row[1]).strip().upper()
            respuestas_correctas[pregunta] = respuesta
        
        print(f" Total de respuestas cargadas: {len(respuestas_correctas)}")
        
        # Verifica las primeras respuestas
        print("\n Verificación primeras 5 respuestas:")
        for i in range(1, 6):
            if str(i) in respuestas_correctas:
                print(f" Pregunta {i}: {respuestas_correctas[str(i)]}")
            else:
                print(f" Pregunta {i}: NO ENCONTRADA")
        
        return respuestas_correctas
        
    except Exception as e:
        print(f"Error al cargar el archivo de respuestas: {e}")
        return None

def verificar_archivo_respuestas(archivo_respuestas):
    # Verifica que el archivo de respuestas sea válido
    try:
        if not os.path.exists(archivo_respuestas):
            print(f"ERROR: El archivo {archivo_respuestas} no existe.")
            return False
        
        if os.path.getsize(archivo_respuestas) == 0:
            print(f"ERROR: El archivo {archivo_respuestas} está vacío.")
            return False
        
        df_prueba = pd.read_excel(archivo_respuestas, header=None)
        
        if df_prueba.empty:
            print(f"ERROR: El archivo {archivo_respuestas} no contiene datos.")
            return False
        
        if df_prueba.shape[1] < 2:
            print(f"ERROR: El archivo debe tener al menos 2 columnas (pregunta | respuesta)")
            return False
            
        print(f"Archivo de respuestas válido: {df_prueba.shape[0]} filas encontradas")
        return True
        
    except Exception as e:
        print(f"ERROR al verificar el archivo: {e}")
        return False

def calificar_examenes(df_examenes, respuestas_correctas):
    # Califica los exámenes comparando respuestas
    print("\n=== INICIANDO CALIFICACIÓN ===")
    
    if df_examenes is None or df_examenes.empty:
        print("ERROR: El DataFrame de exámenes está vacío")
        return None
    
    print(f"Dimensiones del DataFrame: {df_examenes.shape}")
    print(f"Columnas disponibles: {list(df_examenes.columns)}")
    
    # IDENTIFICA LAS COLUMNAS DE RESPUESTAS AUTOMÁTICAMENTE
    columnas_respuestas = identificar_columnas_respuestas(df_examenes)
    
    if not columnas_respuestas:
        print("\n ERROR: No se encontraron columnas de respuestas")
        return None
    
    print(f"\n Columnas de respuestas identificadas: {columnas_respuestas}")
    print(f" Total de preguntas a calificar: {len(columnas_respuestas)}")
    
    # IDENTIFICA LA COLUMNA DE NOMBRE
    columna_nombre = None
    posibles_nombres = ['Nombre completo', 'NOMBRES', 'Nombre', 'ALUMNO', 'ESTUDIANTE']
    for col in df_examenes.columns:
        col_str = str(col).strip()
        if any(nombre in col_str for nombre in posibles_nombres):
            columna_nombre = col
            print(f" Columna de nombres encontrada: '{columna_nombre}'")
            break
    
    if not columna_nombre:
        print(" No se encontró columna de nombres, se usarán índices")
    
    calificaciones = []
    
    # Procesa TODOS los estudiantes
    print("\n=== PROCESANDO ESTUDIANTES ===")
    
    for index, row in df_examenes.iterrows():
        try:
            aciertos = 0
            total_preguntas = len(columnas_respuestas)
            
            # Obtiene nombres del estudiante
            if columna_nombre and pd.notna(row[columna_nombre]):
                nombre_estudiante = str(row[columna_nombre]).strip()
            else:
                nombre_estudiante = f"Estudiante_{index+1}"
            
            # Califica cada respuesta
            respuestas_estudiante = []
            for i, col in enumerate(columnas_respuestas, 1):
                # Obtenie respuestas del alumno
                if pd.notna(row[col]):
                    respuesta_est = str(row[col]).strip().upper()
                else:
                    respuesta_est = ""
                
                respuestas_estudiante.append(respuesta_est)
                
                # Compara con respuesta correcta (usando el número de pregunta como clave)
                pregunta_key = str(i)
                if pregunta_key in respuestas_correctas:
                    respuesta_correcta = respuestas_correctas[pregunta_key]
                    if respuesta_est and respuesta_est == respuesta_correcta:
                        aciertos += 1
            
            # Calcula calificación
            calificacion = (aciertos / total_preguntas) * 100 if total_preguntas > 0 else 0
            
            # Crea registro
            registro = {
                'nombre': nombre_estudiante,
                'aciertos': aciertos,
                'total_preguntas': total_preguntas,
                'calificacion': round(calificacion, 2)
            }
            
            calificaciones.append(registro)
            
            # Muestra el progreso (primeros 5 estudiante, nos sirve para encontrar errores, en caso de ternerlos)
            if index < 5:
                print(f"  {index+1}. {nombre_estudiante[:30]}: {aciertos}/{total_preguntas} = {calificacion:.1f}%")
                
        except Exception as e:
            print(f" Error al procesar fila {index}: {e}")
            continue
    
    if not calificaciones:
        print(" ERROR: No se pudo calificar ningún estudiante")
        return None
    
    print(f"\n Total estudiantes calificados: {len(calificaciones)}")
    return pd.DataFrame(calificaciones)

# === PROGRAMA PRINCIPAL ===
print("=" * 60)
print("INICIANDO EL PROCESO DE CALIFICACION")
print("=" * 60)

# Solicita el directorio de exámenes
directorio_examenes = input("\n Ingrese la ruta del directorio con los archivos de examenes: ")

if not os.path.exists(directorio_examenes):
    print(" El directorio no existe. Usando el directorio actual.")
    directorio_examenes = "."

archivo_combinado = "examenes_combinados.xlsx"

# Combinar archivos de exámenes
print("\n--- COMBINANDO ARCHIVOS DE EXAMENES ---")
df_combinado = combinar_archivos_excel(directorio_examenes, archivo_combinado)

if df_combinado is None:
    print(" No se pudieron combinar los archivos. Saliendo...")
    exit()

# VERIFICACIÓN DEL ARCHIVO COMBINADO
print("\n=== VERIFICACIÓN DEL ARCHIVO COMBINADO ===")
print(f" Dimensiones: {df_combinado.shape}")
print(f" Columnas disponibles: {list(df_combinado.columns)}")

# Mostra las primeras filas para verificar estructura
print("\n Primeros 3 registros:")
print(df_combinado.head(3))

# Identifica las columnas de respuestas
columnas_respuestas_encontradas = identificar_columnas_respuestas(df_combinado)
print(f"\n Columnas de respuestas identificadas: {columnas_respuestas_encontradas}")

# CARGA RESPUESTAS CORRECTAS
print("\n" + "=" * 60)
print("CARGANDO RESPUESTAS CORRECTAS")
print("=" * 60)

archivo_respuestas = input("\n Ingrese la ruta del archivo excel con las respuestas correctas: ").strip()

while not os.path.exists(archivo_respuestas) or not verificar_archivo_respuestas(archivo_respuestas):
    print("\n El archivo no es válido. Intente de nuevo.")
    archivo_respuestas = input(" Ingrese la ruta del archivo excel con las respuestas correctas: ").strip()

respuestas_correctas = obtener_respuestas_correcta(archivo_respuestas)

if respuestas_correctas is None:
    print(" No se pudieron cargar las respuestas correctas. Saliendo...")
    exit()

# CALIFICA EXÁMENES
print("\n" + "=" * 60)
print("CALIFICANDO EXAMENES")
print("=" * 60)

df_resultados = calificar_examenes(df_combinado, respuestas_correctas)

if df_resultados is None or df_resultados.empty:
    print(" No se obtuvieron resultados. Saliendo...")
    exit()

# Ordenar resultados
df_resultados = df_resultados.sort_values('calificacion', ascending=False)

# GUARDA RESULTADOS
print("\n--- GUARDANDO RESULTADOS ---")
archivo_resultados = input(" Ingrese el nombre del archivo para guardar los resultados: ").strip()

if not archivo_resultados:
    archivo_resultados = "resultados_calificaciones.xlsx"
elif not archivo_resultados.endswith('.xlsx'):
    archivo_resultados += '.xlsx'

# Guarda resultados en archivo excel
df_resultados.to_excel(archivo_resultados, index=False)

# Muestra resumen final
print(f"\n{'=' * 60}")
print(" PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 60)
print(f" Resultados guardados en: {archivo_resultados}")
print(f" Total de estudiantes calificados: {len(df_resultados)}")
print(f"\n RESUMEN DE CALIFICACIONES:")
print(f" Calificación más alta: {df_resultados['calificacion'].max()}%")
print(f" Calificación más baja: {df_resultados['calificacion'].min()}%")
print(f" Calificación promedio: {df_resultados['calificacion'].mean():.2f}%")
print("\n¡PROGRAMA FINALIZADO!")