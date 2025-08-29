import os
from search import search_prompt
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_postgres import PGVector
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
for k in ("OPENAI_EMBEDDING_MODEL","OPENAI_API_KEY","PG_VECTOR_COLLECTION_NAME", "DATABASE_URL"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")
    
def main():
    template = getTemplateChain()
    store = getEmbeddingsStored()

    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
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
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
    
    return store

if __name__ == "__main__":
    main()