import os
import re
from pypdf import PdfReader

PASTA_RAIZ = r"C:\Caminho\Para\Sua\Pasta"

def extrair_nome_funcionario(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        if len(reader.pages) == 0:
            return None
            
        texto = reader.pages[0].extract_text()
        
        match = re.search(r"Nome do Funcion.*?rio:\s*(.*?)\s*CPF do Funcion.*?rio", texto, re.IGNORECASE)
        if match:
            return match.group(1).strip()
            
        match = re.search(r"(?:Dados do Funcion.*?rio|Favorecido|Trabalhador)\s*[\s\S]*?Nome\s*:\s*([^\n]+)", texto, re.IGNORECASE)
        if match:
            nome = match.group(1).strip()
            return re.split(r'\s*CPF', nome, flags=re.IGNORECASE)[0].strip()
            
        match = re.search(r"(?:Dados do Funcion.*?rio|Favorecido)\s*[\s\S]*?Nome\s*\n\s*([A-ZÀ-Ÿa-zÀ-ÿ\s]+)", texto)
        if match:
            nome = match.group(1).strip().split('\n')[0].strip()
            if not nome.lower().startswith("do funcion"):
                return nome
                
        match = re.search(r"Dados do Receb.*?or\s*Nome\s*(.*?)\s*(?:Chave|CPF/CNPJ|Institui)", texto, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).replace('\n', ' ').strip()
            
    except Exception as e:
        print(f"Erro ao ler {os.path.basename(pdf_path)}: {e}")
    return None

def processar_todas_as_pastas():
    for raiz, pastas, arquivos in os.walk(PASTA_RAIZ):
        nome_subpasta = os.path.basename(raiz)
        
        for arquivo in arquivos:
            if arquivo.lower().endswith('.pdf') and (
                arquivo.startswith('GerarPDF') or 
                arquivo.lower().startswith('comprovante') or 
                'do Funcion' in arquivo
            ):
                caminho_completo = os.path.join(raiz, arquivo)
                nome_funcionario = extrair_nome_funcionario(caminho_completo)
                
                if nome_funcionario:
                    nome_limpo = re.sub(r'[\\/*?:"<>|]', "", nome_funcionario)
                    novo_nome = f"{nome_subpasta} - {nome_limpo}.pdf"
                    novo_caminho = os.path.join(raiz, novo_nome)
                    
                    novo_caminho_win = "\\\\?\\" + os.path.abspath(novo_caminho)
                    caminho_completo_win = "\\\\?\\" + os.path.abspath(caminho_completo)
                    
                    contador = 1
                    while os.path.exists(novo_caminho_win):
                        novo_nome = f"{nome_subpasta} - {nome_limpo} ({contador}).pdf"
                        novo_caminho = os.path.join(raiz, novo_nome)
                        novo_caminho_win = "\\\\?\\" + os.path.abspath(novo_caminho)
                        contador += 1
                    
                    os.rename(caminho_completo_win, novo_caminho_win)
                    print(f"✓ Sucesso [{nome_subpasta}]: {arquivo} -> {novo_nome}")
                else:
                    print(f"⚠ Não foi possível identificar o nome em: {arquivo}")

if __name__ == "__main__":
    processar_todas_as_pastas()