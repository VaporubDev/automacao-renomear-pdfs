# 📁 Automação de Leitura e Renomeação de Comprovantes em PDF com Python

> **Projeto de automação de processos (RPA / Python) para organização e padronização automatizada de comprovantes bancários em lote.**

---

## 📌 1. Problema de Negócio

No fluxo do Setor Pessoal/RH, o sistema bancário exportava centenas de comprovantes de pagamento (Adiantamento, Salário, Transporte, Alimentação, Rescisões) com nomes de arquivos genéricos gerados automaticamente, como `GerarPDF_19022026144405.pdf`.

### O gargalo do processo manual:
1. **Abertura Individual:** Abrir o PDF no visualizador.
2. **Busca Visual:** Localizar o campo "Dados do Funcionário" ou "Favorecido".
3. **Renomeação:** Copiar o nome do colaborador e renomear o arquivo no Windows Explorer mantendo o padrão da subpasta/mês.

Esse processo consumia horas de trabalho braçal e estava sujeito a erros humanos de digitação e padronização.

---

## 💡 2. A Solução Automatizada

Foi criado um script em **Python** que varre recursivamente toda a estrutura de pastas do setor, faz a extração de texto dos PDFs utilizando a biblioteca `pypdf`, identifica o nome do recebedor/favorecido através de **Expressões Regulares (Regex)** e renomeia o arquivo no padrão exigido em poucos segundos.

---

## 🛠️ 3. Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Manipulação de PDF:** `pypdf` (`PdfReader`)
* **Expressões Regulares:** `re`
* **Manipulação de Sistema de Arquivos:** `os` / `os.path`

---

## ⚙️ 4. Casos de Borda e Desafios Técnicos Superados

* **Múltiplos Layouts de PDF:** Implementação de regras em cascata no Regex para cobrir variações de layouts (comprovantes bancários com campo inline, nomes em linhas subsequentes e comprovantes de transferências PIX).
* **Tratamento de Encoding/Acentuação:** Adequação de padrões tolerantes a falhas (`Funcion.*?rio`) para ler documentos onde a acentuação do PDF estava corrompida na extração do texto.
* **Prevenção contra Sobrescrita:** Lógica de checagem de duplicatas com atribuição de sufixo numérico `(1)`, `(2)` caso o arquivo renomeado já exista na pasta.
* **Suporte a Caminhos Longos no Windows (`MAX_PATH`):** Utilização do prefixo estendido `\\\\?\\` para evitar limitações de 260 caracteres do sistema de arquivos ao manipular diretórios aninhados.
* **Resiliência a Erros:** Blocos de tratamento de exceção (`try/except`) para ignorar PDFs corrompidos/vazios sem interromper a execução do lote.

---

## 🚀 5. Como Utilizar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/VaporubDev/automacao-renomear-pdfs.git
   cd automacao-renomear-pdfs
   ```

2. **Instale a biblioteca necessária:**
   ```bash
   pip install pypdf
   ```

3. **Execute o script:**
   (Altere a variável PASTA_RAIZ no arquivo renomear.py para o caminho desejado e execute)
