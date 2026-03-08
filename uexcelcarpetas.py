import pandas as pd
import os
import glob
from pathlib import Path

def combinar_excel_carpetas(carpeta_principal, archivo_salida='combinado.xlsx'):
    """
    Combina todos los archivos Excel de todas las subcarpetas
    
    Args:
        carpeta_principal: Ruta de la carpeta principal
        archivo_salida: Nombre del archivo de salida
    """
    
    # Lista para almacenar todos los dataframes
    dataframes = []
    
    # Buscar todos los archivos .xlsx y .xls en todas las subcarpetas
    patrones = ['**/*.xlsx', '**/*.xls']
    
    for patron in patrones:
        archivos = glob.glob(os.path.join(carpeta_principal, patron), recursive=True)
        
        for archivo in archivos:
            try:
                print(f"Procesando: {archivo}")
                
                # Leer el archivo Excel
                df = pd.read_excel(archivo)
                
                # Agregar columna con el nombre del archivo de origen (opcional)
                df['archivo_origen'] = os.path.basename(archivo)
                
                # Agregar columna con la carpeta de origen (opcional)
                df['carpeta_origen'] = os.path.basename(os.path.dirname(archivo))
                
                dataframes.append(df)
                
            except Exception as e:
                print(f"Error al procesar {archivo}: {e}")
    
    # Combinar todos los dataframes
    if dataframes:
        df_combinado = pd.concat(dataframes, ignore_index=True, sort=False)
        
        # Guardar el archivo combinado
        df_combinado.to_excel(archivo_salida, index=False)
        print(f"\n✅ Archivo combinado guardado como: {archivo_salida}")
        print(f"Total de archivos procesados: {len(dataframes)}")
        print(f"Total de filas: {len(df_combinado)}")
    else:
        print("No se encontraron archivos Excel para combinar")

# Uso del programa
if __name__ == "__main__":
    carpeta = input("Ingresa la ruta de la carpeta principal: ").strip()
    
    if os.path.exists(carpeta):
        nombre_salida = input("Nombre del archivo de salida (Enter para 'combinado.xlsx'): ").strip()
        if not nombre_salida:
            nombre_salida = 'combinado.xlsx'
        
        combinar_excel_carpetas(carpeta, nombre_salida)
    else:
        print("La carpeta no existe")