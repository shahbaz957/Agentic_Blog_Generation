import uvicorn
from fastapi import FastAPI , Request
from src.graph.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM
from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/blogs")
async def create_blogs(request: Request):
    try:
        data = await request.json()
        topic = data.get("topic", "")
        print("Topic received:", topic)

        groqllm = GroqLLM()
        llm = groqllm.get_llm()
        graph_builder = GraphBuilder(llm)

        if topic:
            graph = graph_builder.setup_graph(usecase="topic")
            state = graph.invoke({"topic": topic})
        else:
            state = {"error": "No topic provided"}

        return {"data": state}
    except Exception as e:
        print("Error in backend:", e)
        return {"data": {"error": str(e)}}

if __name__ == "__main__":
    uvicorn.run("app:app" , host="0.0.0.0" , port = 8000 , reload=True)