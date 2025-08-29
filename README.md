# Desafio MBA Engenharia de Software com IA - Full Cycle

Projeto consiste em um assistente básico com o intuito de responder perguntas com base num pdf que pode ser inserido na raíz do projeto.

## Configuração do Ambiente

Para configurar o ambiente e instalar as dependências do projeto, siga os passos abaixo:

1. **Criar e ativar um ambiente virtual (`venv`):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Instalar as dependências:**

   **Opção A - A partir do `requirements.txt`:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar as variáveis de ambiente:**

   - Duplique o arquivo `.env.example` e renomeie para `.env`
   - Abra o arquivo `.env` e substitua os valores pelas suas chaves de API reais.

## Instruções para rodar o projeto:

1. **Insira um pdf na raíz do projeto:**

 Por padrão o nome é `document.pdf` mas pode ser alterado mudando a variável de ambiente `PDF_PATH` :

2. **Subir o banco de dados via docker:**

     ```bash 
    docker compose up -d
     ```

3. **Usar o comando abaixo para ingestão do documento no pgVector:**

    ```bash 
    python src/ingest.py
    ```

4. **Iniciar o chat:**

    ```bash
    python src/chat.py
    ```


Após isso será possível inserir perguntas referentes ao documento.


