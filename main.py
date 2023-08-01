import os
import re
import PyPDF2
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

PDF_FOLDER = os.getenv('PDF_FOLDER')

# connection with you database
conn = mysql.connector.connect(
    host='xxx.xx.xx.xx',
    user='xxxxx',
    password='xxxxx',
    database='xxxxx'
)

def extract_information(file):
    with open(file, 'rb') as f:
        pdf = PyPDF2.PdfFileReader(f)
        info = pdf.getDocumentInfo()
        pages = pdf.getNumPages()
        text = ""
        for i in range(pages):
            text += pdf.getPage(i).extract_text()
        return text

# extract the values of darfs
def extract_and_store(file, conn):
    text = extract_information(file)
    try:
        cnpj = re.search('\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}', text).group(0)
    except:
        print("Erro ao extrair CNPJ")
        cnpj = ""
    try:
        razao_social = re.search('(?<=\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\s).*(?=\nPeríodo de Apuração)', text).group(0)
    except:
        print("Erro ao extrair razão social")
        razao_social = ""
    try:
        valor = re.search('Valor: (\d+,\d{2})', text).group(1)
    except:
        print("Erro ao extrair valor")
        valor = ""
    try:
        periodo_apuracao = re.search('(?i)(janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\/\d{4}', text).group(0)
    except:
        print("Erro ao extrair período de apuração")
        periodo_apuracao = ""
    try:
        data_vencimento = re.search('\d{2}\/\d{2}\/\d{4}', text).group(0)
    except:
        print("Erro ao extrair data de vencimento")
        data_vencimento = ""
    data_envio = datetime.now().strftime('%Y-%m-%d')
    hora_envio = datetime.now().strftime('%H:%M:%S')

    conn.cursor().execute('INSERT INTO valor_darf_federal VALUES (%s, %s, %s, %s, %s, %s, %s)', (cnpj, razao_social, valor, periodo_apuracao, data_vencimento, data_envio, hora_envio))
    conn.commit()

for file in os.listdir(PDF_FOLDER):
    if file.endswith('.pdf'):
        extract_and_store(os.path.join(PDF_FOLDER, file), conn)

# close connection
conn.close()
