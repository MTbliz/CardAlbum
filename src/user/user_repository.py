from datetime import datetime, timedelta

from src import db
from src.models import User, user_contacts, Invite


class UserRepository:

    def get_possible_customers(self, user_id: int) -> list[User]:
        possible_customers = User.query.join(user_contacts, User.id == user_contacts.c.contact_id)\
            .filter(user_contacts.c.user_id == user_id)\
            .all()
        return possible_customers

    def get_user_by_email(self, email: str) -> User:
        user: User = User.query.filter_by(email=email).first()
        return user

    def get_user_contacts(self, user_id: int, page: int, ROWS_PER_PAGE: int) -> list[User]:
        contacts = User.query.join(user_contacts, User.id == user_contacts.c.contact_id).filter(user_contacts.c.user_id == user_id)\
            .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)
        return contacts

    def get_user_invites(self, user_id: int) -> list[User]:
        user: User = User.query.filter(User.id == user_id).first()
        invites = user.invites_received
        return invites

    def get_invite(self, invite_id: int) -> Invite:
        invite: Invite = Invite.query.filter_by(id=invite_id).first()
        return invite

    def send_invite(self, user_id: int, user_email: str) -> bool:
        contact = self.get_user_by_email(user_email)
        invite = Invite(
            invite_date=datetime.utcnow(),
            expiration_date=datetime.utcnow() + timedelta(days=1),
            user_id=user_id,
            contact_id=contact.id
        )
        db.session.add(invite)
        db.session.commit()

    def delete_invite(self, invite_id: int) -> bool:
        invite: Invite = Invite.query.filter_by(id=invite_id).first()
        if not invite:
            return False
        else:
            db.session.delete(invite)
            db.session.commit()
            return True

    def add_contact(self, invite: Invite) -> None:

        # user accept invite.
        # In this case he want to add user (invite.user_id) who created invite to his contacts.
        user_id = invite.contact_id
        contact_id = invite.user_id
        user: User = User.query.filter_by(id=user_id).first()
        contact: User = User.query.filter_by(id=contact_id).first()
        user.contacts.append(contact)
        db.session.commit()
        self.delete_invite(invite.id)
