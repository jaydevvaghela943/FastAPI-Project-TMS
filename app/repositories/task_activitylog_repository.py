from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints import transactions
from app.models.transaction import Transactions

#for Join Table
from sqlalchemy.orm import joinedload

#Repositories: Performs database queries : Healper class to interact with the database for transaction-related operations.

class TransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, transaction_id: int, user_id: int) -> Transactions | None:
        result = await self.db.execute(
            select(Transactions)
            .options(joinedload(Transactions.categories),joinedload(Transactions.user))  # Eager load the related category
            .where(Transactions.id == transaction_id, Transactions.user_id == user_id)
        )
        return result.scalar_one_or_none()

    
    async def create(self, transaction_data: dict) -> Transactions:
        transaction = Transactions(**transaction_data)
        self.db.add(transaction)
        await self.db.flush()
        return transaction
    async def update(self, transaction: Transactions, update_data: dict) -> Transactions:
        for key, value in update_data.items():
            setattr(transaction, key, value)

        await self.db.flush()
        await self.db.refresh(transaction)
        return transaction

    async def delete(self, transaction: Transactions) -> None:
        await self.db.delete(transaction)
        await self.db.flush()

    async def get_all(self, user_id: int, offset: int, limit: int) -> tuple[list[Transactions], int]:
        result = await self.db.execute(
            select(Transactions)
            .options(joinedload(Transactions.categories),joinedload(Transactions.user))  # Eager load the related category
            .where(Transactions.user_id == user_id)
            .order_by(Transactions.id.desc())
            .offset(offset)
            .limit(limit)
        )

        transactions = list(result.scalars().all())
        count_total = await self.db.execute(
            select(func.count())
            .select_from(Transactions)
            .where(Transactions.user_id == user_id)
        )
        total = count_total.scalar_one()

        return transactions, total
        
