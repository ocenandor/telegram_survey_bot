from datetime import datetime, timezone

from db.models import PromoCode


def assign_promo_code(user_id: int, session):
    # Check if user already has a promo code
    existing = session.query(PromoCode).filter_by(used_by_user=user_id).first()
    if existing:
        return existing.code, False  # Return the same code

    # Get an unused promo code
    promo = session.query(PromoCode).filter_by(used_by_user=None).first()
    if not promo:
        return None, False  # No promo codes left

    promo.used_by_user = user_id
    promo.issued_at = datetime.now(timezone.utc)
    session.commit()
    return promo.code, True
