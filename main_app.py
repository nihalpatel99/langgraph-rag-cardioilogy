from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from components.graph import building_graph
import uvicorn
# ----------------------
# FastAPI App
# ----------------------
app = FastAPI()

# Build your graph once at startup
graph = building_graph()

# Request model
class QueryRequest(BaseModel):
    query: str

# ----------------------
# Endpoint
# ----------------------
@app.post("/cardio")
def run_cardio_graph(request: QueryRequest):
    # Ensure messages is a list
    result = graph.invoke({
        "messages": [HumanMessage(content=request.query)]
    })

    # Get final response (last AI message)
    final_response = result["messages"][-1].content

    return {"response": final_response}

# ----------------------
# Run embedded for debug
# ----------------------
if __name__ == "__main__":
    
   uvicorn.run("main_app:app", host="127.0.0.1", port=8080, reload=True)