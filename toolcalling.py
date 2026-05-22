from unittest import result

from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool

from rich import print

#1 creating a tool 

@tool
def get_text_length(text : str)-> int:
    """Returns the number of character in a given text
    """
    return len(text)

#LLM

llm = ChatMistralAI(model="mistral-small-2506")
llm_with_tool = llm.bind_tools([get_text_length])

# step 1: LLM decides tool
result = llm_with_tool.invoke(
    "Use the get_text_length tool to find the length of: hello how are you "
)

# step 2-4 Execute tool
if result.tool_calls:
    tool_call = result.tool_calls[0]
    tool_result = get_text_length.invoke(tool_call["args"]) 


    #step 5: Send back to LLM
    final_response =  llm.invoke(
        f"The length of the text is {tool_result}"
    )

    print(final_response.content) 
    
