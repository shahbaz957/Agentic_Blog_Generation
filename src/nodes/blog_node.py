from src.states.blogState import BlogState , Blog
from langchain_core.messages import HumanMessage , SystemMessage , AIMessage
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
        
    def translation(self , state : BlogState):
        """
        Translate the content to the specified Language.
        """
        translation_prompt = """
                            Translate the following content into {current_language}.
                            - Maintain the original tone , style and formatting.
                            - Adapt cultural references and idioms to be appropriate for {current_language}
                            Return ONLY a JSON object with the fields:
                            - title: string
                            - content: string


                            ORIGINAL CONTENT : 
                            {blog_content}
                            """
        
        blog_content = state['blog']['content']
        message = [
            HumanMessage(content=translation_prompt.format(current_language = state['current_language'] , blog_content = blog_content))
        ]
        translation_content = self.llm.with_structured_output(Blog).invoke(message)
        return {'blog' : translation_content}

    def route(self , state : BlogState): ## here we are setting the value in state graph but in french or german node we are just we are just setting current_language as that langguage but we are not manipulating the original state graph from which we are gonna take the values in future
        return {'current_language' : state['current_language']}
    
    def route_decision(self , state : BlogState):
        """
        Route the content to the respective language translation function
        """
        if state['current_language'] == 'german':
            return 'german'
        elif state['current_language'] == 'french':
            return 'french'
        else:
            return state['current_language']
