from google.adk.agents import LlmAgent

from .config.agent_config import agent_config
from .tools.get_customer import get_customer_tool
from .tools.get_order import get_order_tool


# In the JS version, ADK sends a failed tool call (e.g. a Zod error) back to the
# model as { error }, so it can try again. Python ADK raises instead, so we do it here.
def send_tool_error_to_model(tool, args, tool_context, error):
    return {"error": f"Error in tool '{tool.name}': {error}"}


root_agent = LlmAgent(
    name=agent_config["name"],
    model=agent_config["model"],
    description=agent_config["description"],
    instruction=agent_config["instruction"],
    tools=[get_customer_tool, get_order_tool],
    on_tool_error_callback=send_tool_error_to_model,
)
