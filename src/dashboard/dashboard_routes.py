from flask import Blueprint

from src.dashboard.dashboard_controller import DashboardController

bp = Blueprint('dashboard', __name__)

dashboard_controller = DashboardController()
bp.add_url_rule('/', view_func=dashboard_controller.get_orders_dashboard, methods=['GET', 'POST'])