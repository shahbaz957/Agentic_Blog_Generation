from src.states.blogState import BlogState
from src.llms.groqllm import GroqLLM
from langgraph.graph import START , StateGraph , END
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self , llm):
        self.llm = llm 
        self.graph = StateGraph(BlogState)

    def build_topic_graph(self):
        """Build a graph to generate Blog based on topic"""

        llm = self.llm
        self.blog_node_obj = BlogNode(llm)
        self.graph.add_node("generate_title", self.blog_node_obj.generate_title)
        self.graph.add_node("content_generation" , self.blog_node_obj.content_generation)

        ## Defining the Workflow

        self.graph.add_edge(START , "generate_title")
        self.graph.add_edge('generate_title' , 'content_generation')
        self.graph.add_edge('content_generation' , END)

        return self.graph
    
    def setup_graph(self , usecase):
        if usecase == "topic":
            self.build_topic_graph()
        return self.graph.compile()