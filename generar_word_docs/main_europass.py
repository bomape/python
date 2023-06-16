import os 
import shutil
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# Ruta de salida
OUTPUT_PATH = '.\outputs\cv_europass'

# Ruta fichero Excel
EXCEL_PATH = '.\input\data\people_data.xlsx'

# Ruta plantillas ficheros Word
CV_EURO_TEMPLATE_PATH = '.\input\Templates\CVEuropassTemplate.docx'

# Ruta de imagenes
IMAGE_PATH = '.\input\images'

# Funcion para eliminar y crear carpetas
def EliminarCrearCarpetas(path):
    # Verificar si la carpeta existe y eliminarla
    if (os.path.exists(path)):
        shutil.rmtree(path)

    # Crear carpeta
    os.mkdir(path)

def LeerDatosPersonas(path, worksheet):
    excel_df = pd.read_excel(path, sheet_name=worksheet)
    return excel_df

def CrearWordPersonas(df_personas):
    l_tpl = CV_EURO_TEMPLATE_PATH
    # Recorrer filas del dataframe
    for r_idx, r_val in df_personas.iterrows():

        # Procesar plantilla
        docx_tpl = DocxTemplate(l_tpl)

        # Añadir imagen
        img_path = IMAGE_PATH + '\\' + r_val['Imagen']
        img = InlineImage(docx_tpl, img_path, height=Mm(30))

        # Crear contexto
        context = {
            'name': r_val['Nombre'],
            'surname1': r_val['Apellido1'],
            'surname2': r_val['Apellido2'],
            'date_of_birth': r_val['Fecha de nacimiento'],
            'nationality': r_val['Nacionalidad'],
            'genre': r_val['Género'],
            'telephone_number': r_val['Número de teléfono'],
            'email': r_val['Dirección de correo electrónico'],
            'web_linkedin': r_val['Web de LinkedIn'],
            'adress': r_val['Dirección'],
            'postcode': r_val['Código postal'],
            'city': r_val['Ciudad'],
            'country': r_val['País'],
            'extract': r_val['Extracto'],
            'work_experience_title': r_val['Profesión'],
            'work_experience_extract': r_val['Experiencia'],
            'education_training': r_val['Educación'],
            'driving_licence': r_val['Permiso conducir'],
            'image': img,
        }

        # Renderizar plantilla
        docx_tpl.render(context)

        # Guardar documento
        if (pd.notna(r_val['Apellido2'])):
            nombre_doc = 'CVEuro_' + r_val['Apellido1'].upper() + '_' + r_val['Apellido2'].upper() + '_' + r_val['Nombre'] + '.docx'
        else:
            nombre_doc = 'CVEuro_' + r_val['Apellido1'].upper() + '_' + r_val['Nombre'] + '.docx'
        docx_tpl.save(OUTPUT_PATH + '\\' + nombre_doc)


def main():
    # Eliminar y crear carpeta de salida
    EliminarCrearCarpetas(OUTPUT_PATH)
    # Leer datos de personas
    df_personas = LeerDatosPersonas(EXCEL_PATH, 'datos_europass')
    # Crear documentos Word
    CrearWordPersonas(df_personas)

if __name__ == "__main__":
    main()