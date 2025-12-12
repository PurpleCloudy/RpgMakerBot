from database import KillsSaver, SessionLocal


def save_kill(player_id: int, mob_type: str) -> int:
    db = SessionLocal()
    try:
        db_string = KillsSaver(player_id=player_id, mob_type=mob_type)
        db.add(db_string)
        db.commit()
        db.refresh(db_string)
        return db_string.id
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
