from dataclasses import dataclass
from decimal import Decimal
from typing import Self

@dataclass(frozen=True)
class Money:
    amount: Decimal

    def __post_init__(self):
        if self.amount < Decimal('0.00'):
            raise ValueError("Amount cannot be less than zero.")

    def __mul__(self, multiplier: int) -> Self:
        """
        Fungsi ini digunakan nanti untuk mengalikan harga tiket dengan kuantitas (BR21).
        """
        if multiplier < 0:
            raise ValueError("Multiplier cannot be negative.")
        return Money(self.amount * Decimal(multiplier))

    def __add__(self, other: Self) -> Self:
        """
        Fungsi ini berguna jika ada penambahan biaya layanan (service fee) ke harga total.
        """
        return Money(self.amount + other.amount)
        
    def __str__(self) -> str:
        return f"Rp {self.amount:,.2f}"