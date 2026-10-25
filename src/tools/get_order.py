from typing import Annotated

from google.adk.tools import FunctionTool, ToolContext
from pydantic import ConfigDict, Field, validate_call
from sqlalchemy import select

from ..config.tools_config import get_order_config
from ..db import db
from ..models import Order


# Checks every argument against its Field rules, like Zod in the JS version.
@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
def get_order(
    order_number: Annotated[int, Field(ge=1, description="Tje order numnber, e.g. 4512")],
    tool_context: ToolContext,
) -> dict:
    customer_id = tool_context.state.get("customeId")

    if not customer_id:
        return {
            "staus": "error",
            "message": "Customer not verified.",
        }

    with db() as session:
        order = session.execute(
            select(
                Order.order_number,
                Order.product,
                Order.status,
                Order.carrier,
                Order.tracking_number,
            ).where(Order.order_number == order_number, Order.customer_id == customer_id)
        ).one_or_none()

    if not order:
        return {
            "status": "error",
            "message": "No order with that number on this customer's account",
        }

    return {
        "status": "success",
        "order": {**order._asdict(), "status": order.status.value},
    }


# Python ADK reads a tool's name and description from the function's name and docstring.
get_order.__name__ = get_order_config["name"]
get_order.__doc__ = get_order_config["description"]

get_order_tool = FunctionTool(get_order)
