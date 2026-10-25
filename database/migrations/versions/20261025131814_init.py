"""init

The same SQL as prisma/migrations/20261025131814_init/migration.sql in the JS
version, so both versions create an identical database.

Revision ID: 20261025131814
Revises:
Create Date: 2026-10-25 13:18:14
"""
from alembic import op

revision = "20261025131814"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # CreateEnum
    op.execute("""CREATE TYPE "OrderStatus" AS ENUM ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED')""")

    # CreateTable
    op.execute("""
        CREATE TABLE "Customer" (
            "id" SERIAL NOT NULL,
            "name" TEXT NOT NULL,
            "email" TEXT NOT NULL,
            "phone" TEXT NOT NULL,
            "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

            CONSTRAINT "Customer_pkey" PRIMARY KEY ("id")
        )
    """)

    # CreateTable
    op.execute("""
        CREATE TABLE "Order" (
            "id" SERIAL NOT NULL,
            "orderNumber" INTEGER NOT NULL,
            "product" TEXT NOT NULL,
            "status" "OrderStatus" NOT NULL,
            "carrier" TEXT,
            "trackingNumber" TEXT,
            "placedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "customerId" INTEGER NOT NULL,

            CONSTRAINT "Order_pkey" PRIMARY KEY ("id")
        )
    """)

    # CreateTable
    op.execute("""
        CREATE TABLE "Ticket" (
            "id" SERIAL NOT NULL,
            "subject" TEXT NOT NULL,
            "description" TEXT NOT NULL,
            "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "customerId" INTEGER NOT NULL,
            "orderId" INTEGER,

            CONSTRAINT "Ticket_pkey" PRIMARY KEY ("id")
        )
    """)

    # CreateIndex
    op.execute("""CREATE UNIQUE INDEX "Customer_email_key" ON "Customer"("email")""")

    # CreateIndex
    op.execute("""CREATE UNIQUE INDEX "Order_orderNumber_key" ON "Order"("orderNumber")""")

    # CreateIndex
    op.execute("""CREATE INDEX "Order_customerId_idx" ON "Order"("customerId")""")

    # CreateIndex
    op.execute("""CREATE INDEX "Ticket_customerId_idx" ON "Ticket"("customerId")""")

    # AddForeignKey
    op.execute("""ALTER TABLE "Order" ADD CONSTRAINT "Order_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES "Customer"("id") ON DELETE RESTRICT ON UPDATE CASCADE""")

    # AddForeignKey
    op.execute("""ALTER TABLE "Ticket" ADD CONSTRAINT "Ticket_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES "Customer"("id") ON DELETE RESTRICT ON UPDATE CASCADE""")

    # AddForeignKey
    op.execute("""ALTER TABLE "Ticket" ADD CONSTRAINT "Ticket_orderId_fkey" FOREIGN KEY ("orderId") REFERENCES "Order"("id") ON DELETE SET NULL ON UPDATE CASCADE""")


def downgrade() -> None:
    op.execute('DROP TABLE "Ticket"')
    op.execute('DROP TABLE "Order"')
    op.execute('DROP TABLE "Customer"')
    op.execute('DROP TYPE "OrderStatus"')
