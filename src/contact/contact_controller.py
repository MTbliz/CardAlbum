from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from loguru import logger

from src.user.user_service import UserService
from src.contact.contact_forms import ContactForm


class ContactController:

    def __init__(self):
        self.user_service: UserService = UserService()

    @login_required
    def get_contacts(self):
        page: int = request.args.get('page', 1, type=int)
        ROWS_PER_PAGE: int = 10
        contacts = self.user_service.get_user_contacts(current_user.id, page, ROWS_PER_PAGE)
        user_invites = self.user_service.get_user_invites(current_user.id)
        form = ContactForm()
        if form.validate_on_submit():
            # Process the form data
            user_email = form.data.get('email')
            action_status = self.user_service.send_invite(current_user.id, user_email)
            if action_status:
                flash('Your email was sent successfully!', 'success')
            else:
                flash('Something went wrong! Please ensure that email is valid.', 'danger')
            return redirect(url_for('contact.get_contacts'))
        return render_template('contacts/contacts_page.html',
                               contacts=contacts,
                               user_invites=user_invites,
                               url_view="contact.get_contacts",
                               form=form,
                               params={})

    @login_required
    def delete_invite(self, invite_id: int):
        logger.info(f"Deleting invite with ID {invite_id}.")
        self.user_service.delete_invite(invite_id)
        logger.info(f"Invite '{invite_id}' deleted by user: {current_user.username}")
        return redirect(url_for('contact.get_contacts'))

    @login_required
    def accept_invite(self, invite_id: int):
        logger.info(f"Accept invite with ID {invite_id}.")
        self.user_service.add_contact(invite_id)
        logger.info(f"Invite '{invite_id}' accepted by user: {current_user.username}")
        return redirect(url_for('contact.get_contacts'))
