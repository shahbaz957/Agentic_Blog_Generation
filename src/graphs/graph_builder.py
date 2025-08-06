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
    
    def graph_language_builder(self):
        """Build Graph to Generate Blog using given topic and language"""
        llm = self.llm
        self.blog_node_obj = BlogNode(llm)

        self.graph.add_node("generate_title", self.blog_node_obj.generate_title)
        self.graph.add_node("content_generation" , self.blog_node_obj.content_generation)  
        self.graph.add_node('german_translation' , lambda state : self.blog_node_obj.translation({**state, "current_language" : 'german'}))
        self.graph.add_node('french_translation' , lambda state : self.blog_node_obj.translation({**state, "current_language": 'french'}))
        self.graph.add_node('route' , self.blog_node_obj.route) 

        ## Defining the Workflow


        self.graph.add_edge(START , "generate_title")
        self.graph.add_edge('generate_title' , 'content_generation')
        self.graph.add_edge('content_generation' , 'route')
        self.graph.add_conditional_edges('route' , self.blog_node_obj.route_decision , 
                                         {
                                             'german' : "german_translation",
                                             'french' : 'french_translation'
                                         })
        self.graph.add_edge('french_translation' , END)
        self.graph.add_edge('german_translation' , END)

    def setup_graph(self , usecase):

        if usecase == "topic":
            self.build_topic_graph()

        if usecase == 'language':
            self.graph_language_builder()

        return self.graph.compile()
    

## ALl the Definition are related to LangGraph studio Demonstration

llm = GroqLLM().get_llm()
graph_builder = GraphBuilder(llm)
graph = graph_builder.build_topic_graph().compile()