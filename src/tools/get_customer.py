from typing import Annotated

from google.adk.tools import FunctionTool, ToolContext
from pydantic import ConfigDict, Field, validate_call
from sqlalchemy import select

from ..config.tools_config import get_customer_config
from ..db import db
from ..models import Customer


# Checks every argument against its Field rules, like Zod in the JS version.
@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
def get_customer(
    email: Annotated[str, Field(description="The customer's email address")],
    phone_last4: Annotated[
        str, Field(pattern=r"^\d{4}$", description="Last 4 digits of their phone numbers")
    ],
    tool_context: ToolContext,
) -> dict:
    with db() as session:
        customer = session.scalar(select(Customer).where(Customer.email == email))

    if not customer or not customer.phone.endswith(phone_last4):
        return {"status": "error", "message": "These detailes don't matchs"}

    tool_context.state["customeId"] = customer.id

    return {"status": "success", "name": customer.name}


# Python ADK reads a tool's name and description from the function's name and docstring.
get_customer.__name__ = get_customer_config["name"]
get_customer.__doc__ = get_customer_config["description"]

get_customer_tool = FunctionTool(get_customer)
