### Entire Chatbot With LangGraph
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from components.state import CardioState
from components.tools.tools import  get_tools
### Node definition

from langchain_groq import ChatGroq

llm=ChatGroq(model="llama-3.1-8b-instant")

tools = get_tools()
llm_with_tools = llm.bind_tools(tools)

def tool_calling_llm(state:CardioState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def building_graph():
    tools = get_tools()
    print(tools)
    # Build graph
    builder = StateGraph(CardioState)
    builder.add_node("tool_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "tool_llm")
    builder.add_conditional_edges(
        "tool_llm",
        tools_condition,
    )
    builder.add_edge("tools","tool_llm")


    graph = builder.compile()

    # View
    png_bytes = graph.get_graph().draw_mermaid_png()

    with open("cardio_graph.png", "wb") as f:
        f.write(png_bytes)
        
    return graph
  
  
  
