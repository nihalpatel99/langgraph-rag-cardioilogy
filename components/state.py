from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing_extensions import Annotated
from langchain_core.messages import AnyMessage
from typing import List, Optional
class CardioState(TypedDict):
  
  
  
  # List of messages
  messages: Annotated[List[AnyMessage],add_messages]
  
  
  final_answer: Optional[str]
  
  