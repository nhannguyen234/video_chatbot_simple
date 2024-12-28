import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from src.core.config import configs
from src.core.prompt import prompt_settings
from src.features.text_completion import build_text_message, get_context_str
from src.features.image_completion import get_context_image_str
from src.utils.helper_functions import extract_images_from_video, check_chroma_exists
from src.features.chroma.create_vectorstore import create_image_desc_db

import logging


def completion_with_retrieval(
        id: str,
        question: str,
        image_url: str = '',
        video_url: str = '',
        history: dict = {}) -> str:
    
    if question == '':
        raise Exception('Please ask the chatbot')

    context_str = get_context_str(id, question)
    # LLM
    llm = ChatOpenAI(api_key=configs.OPENAI_API_KEY,
                    model_name="gpt-4o-mini", 
                    temperature=0.2,
                    top_p=1)

    # Post-processing
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    system_prompt = PromptTemplate(input_variables=['context'], template=prompt_settings.prompt_rag)
    if check_chroma_exists(id):
        if image_url != '':
            context_str = get_context_image_str(id=id, image_url=image_url)
        print(f'The context_str {context_str}')
        message = build_text_message(
            id=id,
            system_prompt=system_prompt.format(context=format_docs(context_str)),
            question=question,
            history=history
        )
    else:
        if video_url != '':
            extract_images_from_video(id=id, path_link=video_url)
            create_image_desc_db(id=id)
        else:
            logging.error("Video should be provided and store to database, it can be youtube url or mp4 file")
            raise Exception("Video should be provided and store to database, it can be youtube url or mp4 file")
    # print(message)

    # run llm
    response = llm.invoke(message)

    # save history message
    new_conversation = {
        'message_id': id,
        'message':[
            {'role':'human', 'content':question},
            {'role':'ai', 'content': response.content}
    ]}
    save_history_conversation(id, './history.json', new_conversation)

    return response.content

def save_history_conversation(id:str, path:str, new_data:dict):
    try:
        with open(path, "r") as json_file:
            existing_data = json.load(json_file)  # Load existing data as a dictionary
    except FileNotFoundError:
        existing_data = [{
            'message_id': id,
            'message':[]
        }]

    # Update the existing dictionary with the new data
    for id_, data in enumerate(existing_data):
        if new_data['message_id'] == data['message_id']:
            existing_data[id_]['message'].extend(new_data['message'])

    # Write the updated dictionary back to the JSON file
    with open(path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)
        print("New data has been added to the JSON file.")