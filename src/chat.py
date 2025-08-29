import os
from search import search_prompt
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chat_models import init_chat_model
from langchain_postgres import PGVector
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
for k in ("LLM_API_KEY","PG_VECTOR_COLLECTION_NAME", "DATABASE_URL"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")
    
def main():
    template = getTemplateChain()
    store = getEmbeddingsStored()

    llm = init_chat_model(model="gemini-2.5-flash-lite", model_provider="google_genai", temperature=0, google_api_key=os.getenv("LLM_API_KEY"))
    pipeline = template | llm | StrOutputParser()

    print("Faça sua pergunta: (ou 'sair' para encerrar):")
    while True:
        query = input('> ')
        if query.strip().lower() in ("sair", "exit", "quit"): 
            print("Encerrando o chat.")
            break
        result = executeChain(store, pipeline, query)
        print(result)

def executeChain(store, pipeline, query):
    results = store.similarity_search_with_score(query, k=10)
    context = "\n".join([doc.page_content for doc, _ in results])
    result = pipeline.invoke({"contexto": context, "pergunta": query})
    return result

def getTemplateChain():
    chain = search_prompt()
    if not chain:
        raise RuntimeError(f"Não foi possível iniciar o chat. Verifique os erros de inicialização.")

    template = PromptTemplate(
        input_variables=["contexto", "pergunta"],
        template=chain
    )
    
    return template

def getEmbeddingsStored():
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", google_api_key=os.getenv("LLM_API_KEY"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
    
    return store

if __name__ == "__main__":
    main()