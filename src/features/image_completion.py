import numpy as np
from langchain_chroma import Chroma
from src.core.config import configs
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from src.core.prompt import prompt_settings
from src.core.constant import TextConstant
from src.core.config import configs

import base64
import logging

# LLM
llm = ChatOpenAI(api_key=configs.OPENAI_API_KEY,
                model_name="gpt-4o-mini", 
                temperature=0.2,
                top_p=1)

def build_image_message(
        system_prompt: str,
        message_prompt: str,
        image_url: str) -> str:
    if image_url.endswith('jpg'):
        with open(image_url, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        # llm execution    
        system_prompt = system_prompt
        message = [
            ("system", system_prompt),
            ("human", [
                {
                    "type": "text", 
                    "text": message_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                }
            ])
        ]
        # run llm
        response_desc = llm.invoke(message)
    else:
        logging.error("The image is only supported in jpg format")
        raise TypeError(f"The provided image is {image_url.split('.')[-1]} format, not jpg format. It should be in jpg format")
    return response_desc.content


def get_context_image_str(id: str, image_url: str):
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
    # transform image to text captioning
    image_captioning = build_image_message(
        system_prompt=prompt_settings.prompt_image_captioning,
        message_prompt=TextConstant.message_captioning,
        image_url=image_url
    )
    context_str = retriever.invoke(image_captioning)
    return context_str
