import os
import glob
import logging
import cv2 as cv
from langchain_community.vectorstores import Chroma
from pytubefix import YouTube
from pytubefix.cli import on_progress 

from src.core.config import configs

def get_documents_from_folder_path(folder_path: str) -> list:
    documents = []
    for path in glob.glob(os.path.join(folder_path,'*.txt')):
        documents.append(path)
    return documents

def check_chroma_exists(id: str) -> bool:
    collection_name = f"{configs.COLLECTION_NAME_CHROMA}_{id}"
    # Initialize Chroma
    vectorstore = Chroma(
        collection_name=collection_name,
        persist_directory=configs.VECTOR_STORE_DB)
    # Check if the collection exists
    try:
        # Check if the collection contains data
        data = vectorstore.get()
        if data and 'ids' in data and len(data['ids']) > 0:
            logging.info(f"The collection '{collection_name}' contain data.")
            return True
        else:
            logging.error(f"The collection '{collection_name}' is empty.")
            return False
    except Exception as e:
        logging.error(f"Error accessing collection '{collection_name}': {e}")
        return False

def extract_images_from_mp4(id: str, file_path: str) -> None:
    if file_path.endswith('mp4'):
        filename = os.path.basename(file_path).split('.mp4')[0]
        vidcap = cv.VideoCapture(file_path)
        # get fps
        fps = vidcap.get(cv.CAP_PROP_FPS)
        logging.info(f"Frame per second is {fps}")
        success, _ = vidcap.read()

        #create folder if not exist
        saved_path = os.path.join(configs.FILE_VIDEO_CACHE, id)
        if not os.path.exists(saved_path):
            os.mkdir(saved_path)
        # --> will replace to save in cache service
        while success:
            frame_id = int(round(vidcap.get(1))) # get current frame
            success, image = vidcap.read()
            if frame_id % int(fps) == 0 and frame_id != 0:
                cv.imwrite(os.path.join(saved_path, filename + "_frame%d.jpg") % frame_id/int(fps), image)
        vidcap.release()
        logging.info("Extract images from video complete")
    else:
        raise TypeError('It only supports mp4 format. Please give the right format string')

def extract_images_from_video(id: str, path_link: str) -> None:
    if path_link.startswith('http'):
        try: # object creation using Youtube
            yt = YouTube(path_link, 
                        use_oauth=True, 
                        on_progress_callback = on_progress)
        except:
            logging.error("Youtube connection error")
            raise Exception
        mp4_streams = yt.streams.filter(progressive=True, 
                                        file_extension='mp4')

        #get the video with highest resolution
        d_video = mp4_streams[-1]

        #create folder if not exist
        saved_path = os.path.join(configs.YOUTUBE_VIDEO_CACHE, id)
        if not os.path.exists(saved_path):
            os.mkdir(saved_path)
        # --> will replace to save in cache service
        # download video
        try:
            d_video.download(output_path=saved_path)
            logging.info("Video download successfully")
        except:
            logging.error("Video download fail!!!")
            raise Exception
        for file in glob.glob(os.path.join(saved_path,'*.mp4')):
            extract_images_from_mp4(id=id, 
                                    file_path=file)
    elif path_link.endswith('mp4'):
        extract_images_from_mp4(id=id, file_path=path_link)
    else:
       raise TypeError('It only supports mp4 format or youtube link. Please give the right format string')
