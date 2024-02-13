from flask import Blueprint

from src.contact.contact_controller import ContactController

bp = Blueprint('contact', __name__)

contact_controller = ContactController()
bp.add_url_rule('/', view_func=contact_controller.get_contacts, methods=['GET', 'POST'])
bp.add_url_rule('/delete/<int:invite_id>', view_func=contact_controller.delete_invite, methods=['GET'])
bp.add_url_rule('/accept/<int:invite_id>', view_func=contact_controller.accept_invite, methods=['GET'])


