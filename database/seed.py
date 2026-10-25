from datetime import datetime, timedelta

from sqlalchemy import text

from src.db import db
from src.models import Customer, Order

# Each customer: { name, email, phone, orders }
#   phone: digits only; customers verify with the last 4
# Each order: { order_number, product, status, days_ago, carrier?, tracking_number? }
#   status: "PENDING" | "SHIPPED" | "DELIVERED" | "CANCELLED"
#   carrier, tracking_number: optional; set both to use exact values (e.g. for the demo)

# Sara and James are the demo customers used on the slides. Keep them first.
customers = [
    {
        "name": "Sara Ahmed",
        "email": "sara@example.com",
        "phone": "03005551234",
        "orders": [
            {
                "order_number": 4512,
                "product": "Wireless Earbuds",
                "status": "SHIPPED",
                "days_ago": 3,
                "carrier": "TCS",
                "tracking_number": "TCS-88412093",
            },
            {
                "order_number": 4513,
                "product": "Mechanical Keyboard",
                "status": "DELIVERED",
                "days_ago": 14,
            },
            {
                "order_number": 4514,
                "product": "Laptop Sleeve",
                "status": "PENDING",
                "days_ago": 0,
            },
        ],
    },
    {
        "name": "James Carter",
        "email": "james@example.com",
        "phone": "4155550199",
        "orders": [
            {
                "order_number": 5120,
                "product": "Laptop Stand",
                "status": "SHIPPED",
                "days_ago": 2,
            },
            {
                "order_number": 5121,
                "product": "Phone Case",
                "status": "CANCELLED",
                "days_ago": 20,
            },
        ],
    },
    {
        "name": "Ayesha Khan",
        "email": "ayesha@example.com",
        "phone": "03215552048",
        "orders": [
            {
                "order_number": 5201,
                "product": "Smart Watch",
                "status": "DELIVERED",
                "days_ago": 9,
            },
            {
                "order_number": 5202,
                "product": "Watch Strap",
                "status": "SHIPPED",
                "days_ago": 1,
            },
        ],
    },
    {
        "name": "Bilal Hussain",
        "email": "bilal@example.com",
        "phone": "03335553317",
        "orders": [
            {
                "order_number": 5301,
                "product": "Gaming Mouse",
                "status": "PENDING",
                "days_ago": 0,
            },
        ],
    },
    {
        "name": "Emily Johnson",
        "email": "emily@example.com",
        "phone": "2125554821",
        "orders": [
            {
                "order_number": 5401,
                "product": "Noise-Cancelling Headphones",
                "status": "DELIVERED",
                "days_ago": 30,
            },
            {
                "order_number": 5402,
                "product": "Headphone Case",
                "status": "DELIVERED",
                "days_ago": 28,
            },
            {
                "order_number": 5403,
                "product": "USB-C Charger",
                "status": "SHIPPED",
                "days_ago": 2,
            },
        ],
    },
    {
        "name": "Hamza Ali",
        "email": "hamza@example.com",
        "phone": "03455556602",
        "orders": [
            {
                "order_number": 5501,
                "product": "Portable SSD 1TB",
                "status": "SHIPPED",
                "days_ago": 4,
            },
        ],
    },
    {
        "name": "Fatima Noor",
        "email": "fatima@example.com",
        "phone": "03015557719",
        "orders": [
            {
                "order_number": 5601,
                "product": "Electric Kettle",
                "status": "DELIVERED",
                "days_ago": 6,
            },
            {
                "order_number": 5602,
                "product": "Coffee Grinder",
                "status": "CANCELLED",
                "days_ago": 12,
            },
        ],
    },
    {
        "name": "Daniel Smith",
        "email": "daniel@example.com",
        "phone": "3125558830",
        "orders": [
            {
                "order_number": 5701,
                "product": "Webcam 1080p",
                "status": "PENDING",
                "days_ago": 1,
            },
        ],
    },
    {
        "name": "Zainab Raza",
        "email": "zainab@example.com",
        "phone": "03125559945",
        "orders": [
            {
                "order_number": 5801,
                "product": "Yoga Mat",
                "status": "DELIVERED",
                "days_ago": 18,
            },
            {
                "order_number": 5802,
                "product": "Resistance Bands",
                "status": "SHIPPED",
                "days_ago": 3,
            },
        ],
    },
    {
        "name": "Usman Tariq",
        "email": "usman@example.com",
        "phone": "03075551056",
        "orders": [
            {
                "order_number": 5901,
                "product": "27-inch Monitor",
                "status": "SHIPPED",
                "days_ago": 5,
            },
        ],
    },
    {
        "name": "Olivia Brown",
        "email": "olivia@example.com",
        "phone": "6175552167",
        "orders": [
            {
                "order_number": 6001,
                "product": "Desk Lamp",
                "status": "DELIVERED",
                "days_ago": 11,
            },
            {
                "order_number": 6002,
                "product": "Notebook Set",
                "status": "DELIVERED",
                "days_ago": 11,
            },
        ],
    },
    {
        "name": "Ali Raza",
        "email": "ali@example.com",
        "phone": "03235553278",
        "orders": [
            {
                "order_number": 6101,
                "product": "Bluetooth Speaker",
                "status": "CANCELLED",
                "days_ago": 7,
            },
        ],
    },
    {
        "name": "Mariam Siddiqui",
        "email": "mariam@example.com",
        "phone": "03335554389",
        "orders": [
            {
                "order_number": 6201,
                "product": "Hair Dryer",
                "status": "SHIPPED",
                "days_ago": 2,
            },
            {
                "order_number": 6202,
                "product": "Travel Pouch",
                "status": "PENDING",
                "days_ago": 0,
            },
        ],
    },
    {
        "name": "Michael Lee",
        "email": "michael@example.com",
        "phone": "4085555490",
        "orders": [
            {
                "order_number": 6301,
                "product": "Graphics Tablet",
                "status": "DELIVERED",
                "days_ago": 22,
            },
        ],
    },
    {
        "name": "Hira Javed",
        "email": "hira@example.com",
        "phone": "03465556501",
        "orders": [
            {"order_number": 6401, "product": "Sneakers", "status": "SHIPPED", "days_ago": 3},
            {
                "order_number": 6402,
                "product": "Running Socks",
                "status": "SHIPPED",
                "days_ago": 3,
            },
        ],
    },
    {
        "name": "Omar Farooq",
        "email": "omar@example.com",
        "phone": "03005557612",
        "orders": [
            {
                "order_number": 6501,
                "product": "Power Bank 20000mAh",
                "status": "DELIVERED",
                "days_ago": 8,
            },
        ],
    },
    {
        "name": "Sophia Martinez",
        "email": "sophia@example.com",
        "phone": "3055558723",
        "orders": [
            {
                "order_number": 6601,
                "product": "Air Fryer",
                "status": "PENDING",
                "days_ago": 1,
            },
            {
                "order_number": 6602,
                "product": "Cookbook",
                "status": "DELIVERED",
                "days_ago": 25,
            },
        ],
    },
    {
        "name": "Kashif Mehmood",
        "email": "kashif@example.com",
        "phone": "03215559834",
        "orders": [
            {
                "order_number": 6701,
                "product": "Router (Wi-Fi 6)",
                "status": "SHIPPED",
                "days_ago": 6,
            },
        ],
    },
    {
        "name": "Noor Fatima",
        "email": "noor@example.com",
        "phone": "03135550945",
        "orders": [
            {
                "order_number": 6801,
                "product": "Backpack",
                "status": "DELIVERED",
                "days_ago": 15,
            },
            {
                "order_number": 6802,
                "product": "Water Bottle",
                "status": "CANCELLED",
                "days_ago": 13,
            },
        ],
    },
    {
        "name": "David Wilson",
        "email": "david@example.com",
        "phone": "2065551256",
        "orders": [
            {
                "order_number": 6901,
                "product": "Office Chair",
                "status": "SHIPPED",
                "days_ago": 4,
            },
        ],
    },
    {
        "name": "Sana Iqbal",
        "email": "sana@example.com",
        "phone": "03365552367",
        "orders": [
            {
                "order_number": 7001,
                "product": "Mobile Phone Stand",
                "status": "DELIVERED",
                "days_ago": 10,
            },
            {
                "order_number": 7002,
                "product": "Screen Protector",
                "status": "PENDING",
                "days_ago": 0,
            },
        ],
    },
    {
        "name": "Ahmed Shah",
        "email": "ahmed@example.com",
        "phone": "03025553478",
        "orders": [
            {
                "order_number": 7101,
                "product": "Electric Toothbrush",
                "status": "SHIPPED",
                "days_ago": 1,
            },
        ],
    },
]

# Carrier name → tracking number prefix.
CARRIERS = {
    "TCS": "TCS",
    "Leopards": "LCS",
    "DHL": "DHL",
    "FedEx": "FDX",
    "M&P": "MNP",
}
CARRIER_NAMES = list(CARRIERS.keys())


def days_ago(days):
    """A date `days` days before now, so the data always looks recent."""
    return datetime.now() - timedelta(days=days)


def shipping_for(order):
    """Shipped and delivered orders get a carrier and tracking number; others don't."""
    if order["status"] != "SHIPPED" and order["status"] != "DELIVERED":
        return {"carrier": None, "tracking_number": None}

    # Pick a carrier from the order number so the data is varied but always the same.
    carrier = order.get("carrier") or CARRIER_NAMES[order["order_number"] % len(CARRIER_NAMES)]
    tracking_number = order.get("tracking_number") or f"{CARRIERS[carrier]}-88{order['order_number']}"

    return {"carrier": carrier, "tracking_number": tracking_number}


def main():
    with db() as session:
        # Empty the tables and restart IDs at 1, so Sara is always customer 1.
        session.execute(text('TRUNCATE TABLE "Ticket", "Order", "Customer" RESTART IDENTITY CASCADE'))

        for customer in customers:
            session.add(
                Customer(
                    name=customer["name"],
                    email=customer["email"],
                    phone=customer["phone"],
                    orders=[
                        Order(
                            order_number=order["order_number"],
                            product=order["product"],
                            status=order["status"],
                            placed_at=days_ago(order["days_ago"]),
                            **shipping_for(order),
                        )
                        for order in customer["orders"]
                    ],
                )
            )

        session.commit()

    order_count = sum(len(customer["orders"]) for customer in customers)
    print(f"Seeded {len(customers)} customers and {order_count} orders.")


if __name__ == "__main__":
    main()
