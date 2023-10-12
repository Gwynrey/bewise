from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import requests
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String)
    answer_text = Column(String)
    create_date = Column(DateTime, default=datetime.utcnow)


engine = create_engine("postgresql://postgres:password@localhost/mydatabase")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class QuestionRequest(BaseModel):
    questions_num: int


@app.post("/questions/")
def generate_questions(questions: QuestionRequest):
    session = SessionLocal()
    try:
        existing_questions = session.query(Question).all()
        if len(existing_questions) > 0:
            raise HTTPException(status_code=422,
                                detail="Question already exists")

        response = requests.get(f"https://jservice.io/api/random?count={questions.questions_num}")
        if response.status_code == 200:
            data = response.json()
            for question in data:
                db_question = Question(question_text=question["question"],
                                       answer_text=question["answer"])
                session.add(db_question)
            session.commit()
            return data
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch questions from API")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@app.get("/questions/")
def get_question():
    session = SessionLocal()
    try:
        existing_questions = session.query(Question).all()
        if len(existing_questions) > 0:
            return existing_questions[0]
        else:
            return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
