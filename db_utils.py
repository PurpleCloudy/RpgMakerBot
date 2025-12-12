from database import KillsSaver, SessionLocal
import pandas as pd
from sqlalchemy import func
import matplotlib.pyplot as plt
import io


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


def get_kills():
    """
    Возвращает DataFrame с колонками: date, обычный, ивентовый
    """
    session = SessionLocal()
    try:
        query = session.query(func.date(KillsSaver.time).label("date"), KillsSaver.mob_type,
                              func.count().label("count")
                              ).group_by(func.date(KillsSaver.time),
                                         KillsSaver.mob_type).order_by("date")
        results = query.all()
        df = pd.DataFrame(results, columns=["date", "mob_type", "count"])
        if df.empty:
            return pd.DataFrame(columns=["date", "обычный", "ивентовый"])
        df_pivot = df.pivot(index="date", columns="mob_type", values="count").fillna(0)
        df_pivot.index = pd.to_datetime(df_pivot.index)
        return df_pivot.sort_index()
    finally:
        session.close()


def kills_to_table(df: pd.DataFrame) -> bytes:
    """
    Строит график и возвращает его как png
    """
    if df.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'Нет данных об убийствах', horizontalalignment='center', verticalalignment='center')
        ax.axis('off')
    else:
        df.plot(kind='bar', figsize=(12, 6), color=['#1f77b4', '#ff7f0e'])
        plt.title('Убийства монстров по дням')
        plt.xlabel('Дата')
        plt.ylabel('Количество')
        plt.xticks(rotation=45)
        plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()
