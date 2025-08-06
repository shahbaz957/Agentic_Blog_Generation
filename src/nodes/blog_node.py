from src.states.blogState import BlogState

class BlogNode:
    """
    A class to represent the blog Node
    """
    def __init__(self , llm ):
        self.llm = llm

    def generate_title(self , state : BlogState):
        """
        Create Title for the Blog
        """
        if "topic" in state and state['topic'] : 
            prompt ="""
                    You are an expert blog content Writer. use markdown formating. Generate a single creative blog title for the {topic}. This title should be creative and SEO friendly
                    """
            
            system_msg = prompt.format(topic = state['topic'])
            response = self.llm.invoke(system_msg)
            return {"blog" : {"title" : response.content}}
        

    def content_generation(self , state : BlogState):
        """
        Generate the Content for blog
        """
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}