from components.graph import building_graph
from langchain_core.messages import AIMessage, HumanMessage

    
graph = building_graph()
    

result = graph.invoke({
"messages": [
     HumanMessage(content="Latest peer reviewed articles on Cardiology")
    ]
})
final_message = result["messages"][-1]
print(final_message.content)
    
    
