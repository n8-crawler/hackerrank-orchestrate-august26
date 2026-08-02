from pathlib import Path
import time
from services.dataloader import DataLoader
from pipeline.nodes import build_context_node, build_prompt_node, build_response_node, image_analyse_node, parser_node, vision_parser,parsed_claim,user_history,evidence,decision,final_output, voice_analysis_node
from pipeline.dataclass import NotificationState, StateClass
from langgraph.graph import StateGraph,START,END
from pandas import DataFrame

graph = StateGraph(NotificationState)

graph.add_node("context", build_context_node)
graph.add_node("image", image_analyse_node)
graph.add_node("voice", voice_analysis_node)
graph.add_node("prompt", build_prompt_node)
graph.add_node("reason", build_response_node)
graph.add_node("parser", parser_node)

graph.add_edge(START,"context")
graph.add_edge("parser",END)

graph_compile = graph.compile()
