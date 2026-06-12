from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            Order.objects.filter(id=order.id).update(created_at=date)
        for ticket in tickets:
            Ticket.objects.create(movie_session_id=ticket["movie_session"],
                                  row=ticket["row"],
                                  seat=ticket["seat"],
                                  order=order
                                  )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
