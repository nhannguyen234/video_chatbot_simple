### Prerequisites: 
python>=3.11

### Instruction and Information:
- Install dependencies packages by using `pip install -r requirements.txt`
- Create vector store and save locally in folder `chroma_langchain_db` if there are more documents by running `python create_vectorstore.py`
- Update your OPENAI API KEY in `.env` with variable `OPENAI_API_KEY = "your-key"`
- The history chat is stored in `history.json`
- Change frame step to reduce the huge image extraction data by modifying the value of `STEP_FRAME` in config.
- Run programatically `python main.py`. Then go to Swagger UI to test your question by the link `http://127.0.0.1:8000/docs` or using curl command: 

`curl -X POST "http://127.0.0.1:8000/app" -H "Content-Type: application/json" -d '{
    "id": "89c2361f-1023-427d-8120-c58daf153a6e",
    "question": "What is the timestamp of this image?",
    "image_url": ".cache_db/file_video/89c2361f-1023-427d-8120-c58daf153a6e/YouTube Rewind 2019 For the Record | #YouTubeRewind_frame23.jpg",
    "video_url": ""
}'`

### Limitation:
- Not yet handle log with good structure.
- Not yet implement hybrid search.
- Not yet self-refection RAG (halluciation, irrelevant question to documents).
- Not yet handle validation input.
- The timestamp is unstable due to LLM generation.
- Similar images will be resembled before embedding to the vectorstore in the next step.
- Image retrieval is not implemented.
- **Voice multimodal data** will be on the next step development, it will enhance the chunk content of the video stored in vectordatabase due to its global content.
- Cache_db is used in local, it should be replaced by a microservice (Redis, etc).
- History chat will be stored in MongoDB or PostgresQL.