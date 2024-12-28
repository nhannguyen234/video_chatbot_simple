import os

class ConfigSettings:
    OPENAI_API_KEY: str = str(os.getenv('OPENAI_API_KEY'))
    EMBEDDING_MODEL: str = 'text-embedding-3-small'
    DIMENSION_EMBEDDED: int = 512 # it
    CHUNK_SIZE: int = 512
    TOP_K: int = 3
    YOUTUBE_VIDEO_CACHE: str = '/Users/macbookpro/Library/CloudStorage/OneDrive-Personal/main_games/cache_db/youtube_video' #should be absolute path
    FILE_VIDEO_CACHE: str = '/Users/macbookpro/Library/CloudStorage/OneDrive-Personal/main_games/cache_db/file_video' #should be absolute path
    COLLECTION_NAME_CHROMA: str = 'main_games'
    VECTOR_STORE_DB : str = './chroma_langchain_db'
    
configs = ConfigSettings()