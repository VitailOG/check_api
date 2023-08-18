from decimal import Decimal
from datetime import datetime


class Printer:
    HEADER = """
            {name}
        ================================
    """
    BODY_ITEM = """
        {quantity} x {price}
        {name}    {total}
        ================================
    """
    PRICES = """
        СУМА                {total}
        Картка              {amount}
        Решта               {rest}
        ================================
    """
    FOOTER = """
        {date}
        Дякуємо за покупку!
    """

    def __init__(
        self,
        user: str,
        rest: Decimal,
        total: Decimal,
        amount: Decimal,
        products: list[dict[str, str | int]],
        created_at: datetime
    ):
        self.user = user
        self.rest = rest
        self.total = total
        self.amount = amount
        self.products = products
        self.created_at = created_at.strftime("%d.%m.%Y %H:%M")

    def render(self):
        header = self.HEADER.format(name=self.user)
        footer = self.FOOTER.format(date=self.created_at)
        prices = self.PRICES.format(total=self.total, amount=self.amount, rest=self.rest)
        body = ""
        for product in self.products:
            body += self.BODY_ITEM.format(**product)
        return header + body + prices + footer

