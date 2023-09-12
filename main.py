from dotenv import load_dotenv
import os
import PyPDF2
import re
import pymysql.cursors
from datetime import datetime

# load the .env variables
load_dotenv()

PDF_FOLDER = os.getenv(f"PDF_FOLDER")

# connect with database
connection = pymysql.connect(
    host="xxx.xx.xx.xx",
    user="xxxx",
    password="xxxx",
    database="xxxx",
    cursorclass=pymysql.cursors.DictCursor,
)


def extract_information(file):
    with open(file, "rb") as f:
        pdf = PyPDF2.PdfFileReader(f)
        info = pdf.getDocumentInfo()
        pages = pdf.getNumPages()
        text = ""
        for i in range(pages):
            text += pdf.getPage(i).extract_text()
        return text


# regex patterns
cnpj_pattern = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"
razao_social_pattern = r"\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2} (.+)"
valor_pattern = r"(?<=Valor: )\d{1,3}(?:\.\d{3})*(?:,\d{2})?"
periodo_pattern = r"[A-Z][a-z]+/\d{4}"
vencimento_pattern = r"\d{2}/\d{2}/\d{4}"

for filename in os.listdir(PDF_FOLDER):
    if filename.endswith(".pdf"):
        pdf_file_obj = open(os.path.join(PDF_FOLDER, filename), "rb")
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        content = ""
        for page in pdf_reader.pages:
            content += page.extract_text()

        cnpj = re.search(cnpj_pattern, content)
        razao_social = re.search(razao_social_pattern, content)
        valor = re.search(valor_pattern, content)
        periodo = re.search(periodo_pattern, content)
        vencimento = re.search(vencimento_pattern, content)

        cnpj = re.sub(r"\.|-|/", "", cnpj.group()) if cnpj else ""
        razao_social = razao_social.group(1) if razao_social else ""
        valor = valor.group() if valor else ""
        periodo = periodo.group() if periodo else ""
        vencimento = vencimento.group() if vencimento else ""

        now = datetime.now()
        dia_envio = now.strftime("%d/%m/%Y")
        hora_envio = now.strftime("%H:%M:%S")

        with connection.cursor() as cursor:
            # SQL Injection prevention: Use placeholders (%s) instead of direct string formatting
            sql = "SELECT * FROM valor_darf_federal WHERE cnpj = %s AND periodo_apuracao = %s"
            cursor.execute(sql, (cnpj, periodo))
            result = cursor.fetchone()
            if result:
                sql = "UPDATE valor_darf_federal SET razao_social = %s, valor = %s, data_vencimento = %s, dia_envio = %s, hora_envio = %s WHERE cnpj = %s AND periodo_apuracao = %s"
                cursor.execute(
                    sql,
                    (
                        razao_social,
                        valor,
                        vencimento,
                        dia_envio,
                        hora_envio,
                        cnpj,
                        periodo,
                    ),
                )
            else:
                sql = "INSERT INTO valor_darf_federal (cnpj, razao_social, valor, periodo_apuracao, data_vencimento, dia_envio, hora_envio) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(
                    sql,
                    (
                        cnpj,
                        razao_social,
                        valor,
                        periodo,
                        vencimento,
                        dia_envio,
                        hora_envio,
                    ),
                )

        pdf_file_obj.close()

connection.commit()
connection.close()
