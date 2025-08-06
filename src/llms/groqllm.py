from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv
class GroqLLM:
    def __init__(self):
        load_dotenv()
        

    def get_llm(self):
        try:
            os.environ['GROQ_API_KEY'] = self.groq_api_key = os.getenv("GROQ_API_KEY")
            model = ChatGroq(api_key=self.groq_api_key , model = 'llama-3.3-70b-versatile')
            return model
        except Exception as e:
            print("ERROR has Occured in Get_LLM : " , e)