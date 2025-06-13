import random
import string

from db.init import SessionLocal, init_db
from db.models import PromoCode

CHARACTERS = string.ascii_uppercase + string.digits
PROMO_LENGTH = 10
NUM_CODES = 100

def generate_unique_code(existing_codes):
    while True:
        code = ''.join(random.choices(CHARACTERS, k=PROMO_LENGTH))
        if code not in existing_codes:
            return code

def generate_and_insert_promos():
    init_db()
    session = SessionLocal()
    existing = {p.code for p in session.query(PromoCode.code).all()}
    
    new_codes = []
    for _ in range(NUM_CODES):
        code = generate_unique_code(existing)
        new_codes.append(PromoCode(code=code, used_by_user=None))
        existing.add(code)

    session.add_all(new_codes)
    session.commit()
    session.close()
    print(f"{NUM_CODES} promo codes generated and saved.")

if __name__ == "__main__":
    generate_and_insert_promos()
