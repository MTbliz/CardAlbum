from flask import render_template
from flask_login import login_required, current_user

from src.order.order_service import OrderService


class DashboardController:

    def __init__(self) -> None:
        self.order_service: OrderService = OrderService()

    @login_required
    def get_orders_dashboard(self):
        orders_details_seller = self.order_service.get_orders_details_by_user_by_date(current_user.id)
        orders_details_customer = self.order_service.get_orders_details_by_customer_by_date(current_user.id)

        return render_template('dashboards/order_dashboards.html',
                               orders_details_seller=orders_details_seller,
                               orders_details_customer=orders_details_customer,
                               params={})
