from pathlib import Path
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'fitbuddy.db'}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(String(20), nullable=False)
    goal = Column(String(100), nullable=False)
    intensity = Column(String(20), nullable=False)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text)
    nutrition_tip = Column(Text)
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def save_user(user_id, username, age, weight, goal, intensity):
    db = SessionLocal()
    try:
        user = User(user_id=user_id, username=username, age=age, weight=str(weight), goal=goal, intensity=intensity, original_plan="")
        db.add(user); db.commit()
    finally: db.close()

def save_plan(user_id, plan, nutrition_tip):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.original_plan = plan; user.nutrition_tip = nutrition_tip; db.commit()
    finally: db.close()

def get_user(user_id):
    db = SessionLocal()
    try: return db.query(User).filter(User.user_id == user_id).first()
    finally: db.close()

def get_all_users():
    db = SessionLocal()
    try: return db.query(User).order_by(User.id.desc()).all()
    finally: db.close()

def update_plan(user_id, updated_text, feedback):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.updated_plan = updated_text; user.feedback = feedback; db.commit()
    finally: db.close()

def delete_user(user_id):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user: db.delete(user); db.commit()
    finally: db.close()
