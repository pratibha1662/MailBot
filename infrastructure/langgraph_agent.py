from constants.prompts import mailbot_sys_prompt
from constants import config_constants
from typing import Annotated

from typing_extensions import TypedDict
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI

class GraphState(TypedDict):
    messages: Annotated[list, add_messages]

mailbot_instructions = SystemMessage(content = mailbot_sys_prompt)
llm = ChatGoogleGenerativeAI(api_key = config_constants.GEMINI_API_KEY, model = config_constants.GEMINI_MODEL)


def mailbot(state : GraphState):
    messages = [mailbot_instructions] + state["messages"]
    response = llm.invoke(messages)
    return {
        "messages" : [response]
    }

workflow_builder = StateGraph(GraphState)
workflow_builder.add_node("mailbot", mailbot)
workflow_builder.add_edge(START, "mailbot")
workflow_builder.add_edge("mailbot", END)
workflow = workflow_builder.compile()

# png_data = workflow.get_graph(xray=1).draw_mermaid_png()
# output_file = "Mailbot_graph.png"
# with open(output_file, "wb") as file:
#     file.write(png_data)