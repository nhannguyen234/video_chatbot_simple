from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from src.core.config import configs

def get_context_str(id: str, question: str):
    embeddings = OpenAIEmbeddings(api_key=configs.OPENAI_API_KEY,
                                model=configs.EMBEDDING_MODEL,
                                dimensions=configs.DIMENSION_EMBEDDED)
    # load vector_store
    vector_store = Chroma(collection_name=f'{configs.COLLECTION_NAME_CHROMA}_{id}',
                          persist_directory=configs.VECTOR_STORE_DB, 
                          embedding_function=embeddings)
    retriever = vector_store.as_retriever(
                search_type='mmr', #Use MMR for avoiding redundancy
                search_kwargs={"k": configs.TOP_K})
    context_str = retriever.invoke(question)
    return context_str

def build_text_message(
        id: str,
        system_prompt: str, 
        question: str,
        history: list = []) -> list[tuple[str, str]]:
    message = [("system", system_prompt)]

    if history:
        message.extend(
            (msg['role'], msg['content'])
            for message_ in history 
            if message_['message_id']==id
            for msg in message_['message']
        )
    
    if question:
        message.append(("human", question))
    
    return message