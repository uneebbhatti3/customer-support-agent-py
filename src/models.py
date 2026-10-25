# The same tables as prisma/schema.prisma in the JS version, with the same
# table and column names, so both versions can share one database.
import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import Enum, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class Customer(Base):
    __tablename__ = "Customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str]  # digits only, e.g. "03005551234"
    created_at: Mapped[datetime] = mapped_column(
        "createdAt", TIMESTAMP(precision=3), server_default=func.current_timestamp()
    )
    orders: Mapped[list["Order"]] = relationship(back_populates="customer")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="customer")


class Order(Base):
    __tablename__ = "Order"
    __table_args__ = (Index("Order_customerId_idx", "customerId"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    order_number: Mapped[int] = mapped_column("orderNumber", unique=True)
    product: Mapped[str]
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, name="OrderStatus"))
    carrier: Mapped[Optional[str]]
    tracking_number: Mapped[Optional[str]] = mapped_column("trackingNumber")
    placed_at: Mapped[datetime] = mapped_column(
        "placedAt", TIMESTAMP(precision=3), server_default=func.current_timestamp()
    )
    customer_id: Mapped[int] = mapped_column(
        "customerId", ForeignKey("Customer.id", ondelete="RESTRICT", onupdate="CASCADE")
    )
    customer: Mapped["Customer"] = relationship(back_populates="orders")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="order")


class Ticket(Base):
    __tablename__ = "Ticket"
    __table_args__ = (Index("Ticket_customerId_idx", "customerId"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        "createdAt", TIMESTAMP(precision=3), server_default=func.current_timestamp()
    )
    customer_id: Mapped[int] = mapped_column(
        "customerId", ForeignKey("Customer.id", ondelete="RESTRICT", onupdate="CASCADE")
    )
    customer: Mapped["Customer"] = relationship(back_populates="tickets")
    order_id: Mapped[Optional[int]] = mapped_column(
        "orderId", ForeignKey("Order.id", ondelete="SET NULL", onupdate="CASCADE")
    )
    order: Mapped[Optional["Order"]] = relationship(back_populates="tickets")
