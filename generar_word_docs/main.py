import os 
import shutil
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# Ruta de salida
OUTPUT_PATH = '.\outputs'

# Ruta fichero Excel
EXCEL_PATH = '.\input\data\people_data.xlsx'

# Ruta plantillas ficheros Word
ES_WORD_TEMPLATE_PATH = '.\input\Templates\WordTemplate_ES.docx'
EN_WORD_TEMPLATE_PATH = '.\input\Templates\WordTemplate_EN.docx'
FR_WORD_TEMPLATE_PATH = '.\input\Templates\WordTemplate_FR.docx'

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
    # Recorrer filas del dataframe
    for r_idx, r_val in df_personas.iterrows():
        # Seleccionar plantilla en funcion del idioma
        if (r_val['Idioma'] == 'ES'):
            l_tpl = ES_WORD_TEMPLATE_PATH
        elif (r_val['Idioma'] == 'EN'):
            l_tpl = EN_WORD_TEMPLATE_PATH
        elif (r_val['Idioma'] == 'FR'):
            l_tpl = FR_WORD_TEMPLATE_PATH

        # Procesar plantilla
        docx_tpl = DocxTemplate(l_tpl)

        # Añadir imagen
        img_path = IMAGE_PATH + '\\' + r_val['Imagen']
        img = InlineImage(docx_tpl, img_path, height=Mm(15))

        # Crear contexto
        context = {
            'name': r_val['Nombre'],
            'surname1': r_val['Apellido1'],
            'surname2': r_val['Apellido2'],
            'age': r_val['Edad'],
            'picture': img,
        }

        # Renderizar plantilla
        docx_tpl.render(context)

        # Guardar documento
        if (pd.notna(r_val['Apellido2'])):
            nombre_doc = 'Documento_' + r_val['Apellido1'].upper() + '_' + r_val['Apellido2'].upper() + '_' + r_val['Nombre'] + '.docx'
        else:
            nombre_doc = 'Documento_' + r_val['Apellido1'].upper() + '_' + r_val['Nombre'] + '.docx'
        docx_tpl.save(OUTPUT_PATH + '\\' + nombre_doc)


def main():
    # Eliminar y crear carpeta de salida
    EliminarCrearCarpetas(OUTPUT_PATH)
    # Leer datos de personas
    df_personas = LeerDatosPersonas(EXCEL_PATH, 'datos')
    # Crear documentos Word
    CrearWordPersonas(df_personas)

if __name__ == "__main__":
    main()