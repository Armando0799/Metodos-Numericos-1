import pandas as pd
import os
import glob
from pathlib import Path

print("=== PROGRAMA DE CALIFICACION DE EXAMENES === \n")

def combinar_archivos_excel(direc_entrada, arch_salida_com):
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
        df_combinado.to_excel(arch_salida_com, index=False)
        print(f"\nArchivos combinados exitosamente en: {arch_salida_com}")
        print(f"Total de registros: {len(df_combinado)}")
        return df_combinado
    else:
        return None

"""def combinar_archivos_excel(direc_entrada, arch_salida_com):
    #En esta funcion se conbinan o unen todos los archivos excel en uno solo.
    archivos_excel = glob.glob(os.path.join(direc_entrada, "*.xlsx"))#aqui buscamos todos los archivos excel con esa terminacion
    archivos_excel.extend(glob.glob(os.path.join(direc_entrada, "*.xls")))#aqui es en caso que la version de excel sea la viejita
    if not archivos_excel:
        print("ERRROR. No se encontraron archivos Excel en la ruta especificada.")
        return None
    
    dataframe = []#en esta lista guardamos los dataframe de todos los archivos excel
    for archivo in archivos_excel:
        try:
            df = pd.read_excel(archivo)
            df['archivo_origen'] = os.path.basename(archivo)#esto puede ser opcional ya que solo es para saber de que archivo proviene
            dataframe.append(df)
        except Exception as e: #aca en caso de que el programa falle en un excel capturamos el error pero seguimos con los demas excel
            print(f"Error al procesar {archivo}: {e}")
    if dataframe:
        df_combinado = pd.concat(dataframe, ignore_index=True) #combina todos los dataframe
        df_combinado.to_excel(arch_salida_com, index=False)#guarda el archivo combinado
        print(f"\n Archivos combinados exitosamente en: {arch_salida_com}")
        print(f"Total de registros: {len(df_combinado)}")
        return df_combinado
    else:
        return None"""
    
def obtener_respuestas_correcta(archivo_respuestas):
    #Lee el archivo con formato vertical (pregunta | respuesta) y crea un diccionario
    try:
        df_respuestas = pd.read_excel(archivo_respuestas, header=None)  # Sin encabezados
        
        # Verificar que el DataFrame no esté vacío
        if df_respuestas.empty:
            print("ERROR: El archivo de respuestas está vacío.")
            return None
        
        print(f"\nArchivo de respuestas cargado:")
        print(f"- Dimensiones: {df_respuestas.shape[0]} filas x {df_respuestas.shape[1]} columnas")
        
        # Crear diccionario de respuestas correctas
        respuestas_correctas = {}
        
        # Asumiendo que la primera columna es el número de pregunta y la segunda la respuesta
        for _, row in df_respuestas.iterrows():
            pregunta = str(row[0]).strip()  # Número de pregunta (1, 2, 3, ...)
            respuesta = str(row[1]).strip().upper()  # Respuesta (A, B, C, D)
            respuestas_correctas[pregunta] = respuesta
        
        print("\nRespuestas correctas cargadas:")
        for pregunta in range(1, 21):  # Mostrar las primeras 20 preguntas
            if str(pregunta) in respuestas_correctas:
                print(f"  Pregunta {pregunta}: {respuestas_correctas[str(pregunta)]}")
        
        print(f"\nTotal de respuestas cargadas: {len(respuestas_correctas)}")
        return respuestas_correctas
        
    except Exception as e:
        print(f"Error al cargar el archivo de respuestas: {e}")
        return None

"""def obtener_respuestas_correcta(archivo_respuestas): #aqui lee el archivo para obtener las respuestas
    try:
        df_respuestas = pd.read_excel(archivo_respuestas)
        respuestas_correctas = df_respuestas.iloc[0].to_dict()#tomamos la 1º fila como respuestas
        #creo que aca tengo un error porque no funciona como quiero, falta revisar y arreglar
        print("Respuestas correctas cargadas exitosamente.")
        return respuestas_correctas
    except Exception as e:
        print(f"Error al cargar el archivo de respuestas: {e}")
        return None"""

"""
def calificar_examenes(df_examenes, respuestas_correctas):
    columnas_respuestas = [] #guarda las columnas con las respuetas 
    print("\n Columnas disponibles en el archivo combinado: ")

    for i, col in enumerate(df_examenes.columns):
        print(f"{i+1}. {col}")
    print("\n Identifique las columnas que contienen las respuestas de los examenes.")
    print("Ingrese los numeros de las columnas separados por comas, (ej: 1,2,3,4):")

    while True:
        try:
            seleccion = input("Seleccion: ").strip()#aqui quitamos los posibles espacios
            if not seleccion:#por si el usuario no ingresa nada entoces
                print("Por favor ingrese al menos un numero de la columna.")
                continue
            indices = [int(x.strip())-1 for x in seleccion.split(',')]
            columnas_respuestas = [df_examenes.columns[i] for i in indices]
            if len(columnas_respuestas)>= 1:
                break
            else:
                print("Debe seleccionar al menos una columna.")
        except ValueError:
            print("ERROR: Ingrese solo numeros separados por comas (,).")
        except IndexError:
            print("ERROR: Algunos numeros estan fuera del rango de las columnas disponibles.")
        except Exception as e:
            print(f"Error inesperado: {e}")
    calificaciones = []

    for index, row in df_examenes.iterrows():
        aciertos = 0
        total_preguntas = len(columnas_respuestas)
        respuestas_estudiantes = {}
        for col in columnas_respuestas:
            respuestas_est = row[col]
            respuestas_estudiantes[col] = respuestas_est
            if col in respuestas_correctas and str(respuestas_est).strip().lower() == str(respuestas_correctas[col]).strip().lower():
                aciertos += 1 #aqui comparamos con las respuestas
        calificacion = (aciertos/total_preguntas)*100 if total_preguntas > 0 else 0
        #ponemos un nombre por defecto por si no en la columna no ecuentra nombre
        nombre_estudiante = f"Estudiantes_{index+1}"
        posibles_columnas_nombre = ['nombre', 'Nombre', 'NOMBRE', 'estudiante', 'Estudiante', 'alumno', 'Alumno', 'name', 'Name']

        for col_nombre in posibles_columnas_nombre:
            if col_nombre in df_examenes.columns:
                nombre_estudiante = row[col_nombre]
                break
        #aqui creamos el registro de los estudiantes ya calificados
        registro = {
            'nombre': nombre_estudiante,
            'aciertos': aciertos,
            'total_preguntas':total_preguntas,
            'calificaciones': round(calificacion, 2)
        }
        #aqui agregamos las respuestas al registro
        for col, resp in respuestas_correctas.items():
            registro[f'respuestas_{col}'] = resp
        
        calificaciones.append(registro)
    return pd.DataFrame(calificaciones)
    """
def calificar_examenes(df_examenes, respuestas_correctas):
    print("\n=== INICIANDO CALIFICACIÓN ===")
    
    # Mostrar información del DataFrame
    print(f"Dimensiones del DataFrame: {df_examenes.shape}")
    print(f"Columnas disponibles: {list(df_examenes.columns)}")
    
    # Verificar que df_examenes no esté vacío
    if df_examenes is None or df_examenes.empty:
        print("ERROR: El DataFrame de exámenes está vacío o es nulo")
        return None
    
    # Identificar columnas de respuestas (números del 1 al 20)
    columnas_respuestas = []
    for i in range(1, 21):
        col_name = str(i)
        if col_name in df_examenes.columns:
            columnas_respuestas.append(col_name)
        else:
            print(f"ADVERTENCIA: No se encontró la columna '{col_name}'")
    
    # Verificar que encontramos columnas
    if not columnas_respuestas:
        print("ERROR CRÍTICO: No se encontraron columnas de respuestas (1-20)")
        print("Posibles causas:")
        print("- Los nombres de las columnas no son números (revisa tu archivo Excel)")
        print("- El archivo combinado no tiene el formato esperado")
        return None
    
    print(f"Columnas de respuestas encontradas: {columnas_respuestas}")
    print(f"Total de preguntas a calificar: {len(columnas_respuestas)}")
    
    calificaciones = []
    
    for index, row in df_examenes.iterrows():
        try:
            aciertos = 0
            total_preguntas = len(columnas_respuestas)
            
            # Obtener nombre del estudiante
            nombre_estudiante = f"Estudiante_{index+1}"
            if 'NOMBRES' in df_examenes.columns:
                nombre_estudiante = row['NOMBRES'] if pd.notna(row['NOMBRES']) else f"Estudiante_{index+1}"
            
            # Calificar cada respuesta
            respuestas_estudiante = {}
            for i, col in enumerate(columnas_respuestas, 1):
                # Obtener respuesta del alumno
                if pd.notna(row[col]):
                    respuesta_est = str(row[col]).strip().upper()
                else:
                    respuesta_est = ""
                
                respuestas_estudiante[f"p{i}"] = respuesta_est
                
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
            
            # Mostrar progreso cada 10 estudiantes
            if (index + 1) % 10 == 0:
                print(f"Procesados {index + 1} estudiantes...")
                
        except Exception as e:
            print(f"Error al procesar estudiante en fila {index}: {e}")
            continue
    
    if not calificaciones:
        print("ERROR: No se pudo calificar ningún estudiante")
        return None
    
    print(f"Calificación completada. Total estudiantes calificados: {len(calificaciones)}")
    return pd.DataFrame(calificaciones)

# ==== AQUI INICIA EL PROGRAMA PRINCIPAL i,e inbocamos las funciones====
print("INICIANDO EL PROCESO DE CALIFICACION")
print("="*50)
directorio_examenes = input("\nIngrese la ruta del directorio con los archivos de examenes: ")

if not os.path.exists(directorio_examenes):
    print("El direcctorio no existe. Usando el directorio actual.")
    directorio_examenes = "."
archivo_combinado = "examenes_combinados.xlsx"
#iniciamos combinando todos los archivos excel
print("--- COMBINANDO ARCHIVOS DE EXEMENES ---")
df_combinado = combinar_archivos_excel(directorio_examenes, archivo_combinado)

if df_combinado is None:
    print("No se pudieron combinar los archivos...")
    exit()

print(f"\n Archivo combinado creado: {archivo_combinado}")
print(f"\n Total de registros combinados: {len(df_combinado)} \n")

print("==== INCIANDO CARGA DE LAS RESPUESTAS CORRECTAS ====")
archivo_respuestas = input("Ingrese la ruta del archivo erxcel con las respuestas correctas (debe de terminar con .xlsx o .xls)").strip()

while not os.path.exists(archivo_respuestas):
    print("El archivo no existe o no se pudo encontrar. Intente de nuevo.")
    archivo_respuestas = input("Ingrese la ruta del archivo erxcel con las respuestas correctas (debe de terminar con .xlsx o .xls) ").strip()

respuestas_correctas = obtener_respuestas_correcta(archivo_respuestas)
if respuestas_correctas is None:
    print("No se pudieron cargar las respuestas correctas....")
    exit()
print(f"Respuestas corectas cargadas: {len(respuestas_correctas)} preguntas ")

print("==== INICIA CALIFICACION DE EXAMENES ====")
df_resultados = calificar_examenes(df_combinado, respuestas_correctas)
df_resultados = df_resultados.sort_values('calificaciones', ascending=False)

print("--- GUARDAR RESULTADOS ---")
archivo_resultados = input("Ingrese el nombre del archivo para guardar los resultados (ej: resultados.xlsx): ").strip()

if not archivo_resultados:
    archivo_resultados = "resultados_calificaciones.xlsx"
elif not archivo_resultados.endswith('.xlsx'):
    archivo_resultados += '.xlsx'

df_resultados.to_excel(archivo_resultados, index=False)
print(f"\n{'='*50}")
print(f"PROCESO COMPLETADO EXITOSAMENTE")
print("="*50)
print(f"Resultados guardados en : {archivo_resultados}")
print(f"Total de estudiantes calificados: {len(df_resultados)}")
print(f"\nRESUMEN DE CALIFICACIONES: ")
print(f"=> Calificacion mas alta: {df_resultados['calificaciones'].max()}")
print(f"=> Calificacion mas baja: {df_resultados['calificaciones'].min()}")
print(f"=> Calificacion promedio: {df_resultados['calificaciones'].mean():.2f}")