import wikipedia
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from components.state import CardioState
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.retrievers import PubMedRetriever
from langchain_core.messages import HumanMessage, AIMessage
from typing import Dict,List

from langchain_core.tools import tool
from langchain_community.retrievers import PubMedRetriever
from langchain_core.utils.pydantic import BaseModel
from langchain_core.tools import StructuredTool
from dotenv import load_dotenv
load_dotenv()

import os

os.environ["TAVILY_API_KEY"]=os.getenv("TAVILY_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"]="ReAct-agent"

# Wikimedia now rate-limits/blocks the wikipedia package's default generic
# User-Agent; a distinct one is required for API requests to succeed.
wikipedia.set_user_agent("CardioApp/1.0 (nihal1999patel@gmail.com)")

api_wrapper_wiki=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=500)

# tool 1
wiki=WikipediaQueryRun(api_wrapper=api_wrapper_wiki)

# tool 2
tavily = TavilySearchResults(k=5)

# tool 3
retriever = PubMedRetriever(k=5)

class PubMedArgs(BaseModel):
    query: str


def pubmed_search(query: str) -> str:
    # Replace this with your actual PubMed logic
    return f"Searching PubMed for: {query}"
  
pubmed_tool = StructuredTool(
    name="pubmed_search",
    func=pubmed_search,
    description="Search PubMed for articles.",
    args_schema=PubMedArgs
)

tools=[wiki,tavily,pubmed_tool]




  
def get_tools() -> List:
  return tools

  

