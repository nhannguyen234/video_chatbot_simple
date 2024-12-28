import os
import sys

# Get the current file's directory (subfolder2)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up two directories to the 'src' folder
src_root = os.path.abspath(os.path.join(current_dir, "../../../"))

# Add 'src' folder to sys.path
sys.path.insert(0, src_root)

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document

from src.core.config import configs
from src.features.image_completion import build_image_message
from src.core.prompt import prompt_settings
from src.core.constant import TextConstant
from uuid import uuid4

import logging
import glob


embeddings = OpenAIEmbeddings(api_key=configs.OPENAI_API_KEY,
                              model=configs.EMBEDDING_MODEL,
                              dimensions=configs.DIMENSION_EMBEDDED)

def create_image_desc_db(id: str, cache_url: str=configs.FILE_VIDEO_CACHE):
    # sort frame to get the accurate timestamp
    jpg_paths = (glob.glob(os.path.join(cache_url, id, "*.jpg")))
    sorted_jpg_paths = sorted(
        jpg_paths,
        key=lambda x: int(x.split('_frame')[-1].split('.')[0])
    )   
    # check if folder id exists in cache_url
    path = os.path.join(cache_url, id)
    texts = []
    if os.path.isdir(path):
        texts = [Document(
                    metadata = {'image_name': image_path},
                    page_content = build_image_message(
                        system_prompt=prompt_settings.prompt_image_desc.format(frame_id=id_image+1),
                        message_prompt=TextConstant.message_desc,
                        image_url=image_path),
                    id = id_image)
            for id_image, image_path in enumerate(sorted_jpg_paths)]
        print(f'Number of chunking: {len(texts)}')

        # set id for each chunk
        uuids = [str(uuid4()) for _ in range(len(texts))]

        # Create vectorstore in Chroma
        vector_store = Chroma.from_documents(
            collection_name=f'{configs.COLLECTION_NAME_CHROMA}_{id}',
            documents=texts,
            embedding=embeddings,
            ids=uuids,
            persist_directory=configs.VECTOR_STORE_DB # save vectorstore locally
        )
        vector_store.persist()
    else:
        print("Error: The images don't exist")
        logging.error("The images don't exist")
        raise FileExistsError(f"The images are not found in {os.path.join(cache_url, id)}")
# create_image_desc_db('89c2361f-1023-427d-8120-c58daf153a6e')