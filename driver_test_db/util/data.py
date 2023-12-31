from dataclasses import dataclass
from typing import Callable
from driver_test_db.util.language import TextLocalizations


TextTransformer = Callable[[TextLocalizations], TextLocalizations]


@dataclass
class Answer:
    text: TextLocalizations
    is_right_answer: bool

    def transform_texts(self, text_transformer: TextTransformer) -> "Answer":
        return Answer(
            text=text_transformer(self.text),
            is_right_answer=self.is_right_answer,
        )


@dataclass
class Question:
    orig_id: str | None
    text: TextLocalizations
    image: str | None
    answers: list[Answer]

    def transform_texts(self, text_transformer: TextTransformer) -> "Question":
        return Question(
            orig_id=self.orig_id,
            text=text_transformer(self.text),
            image=self.image,
            answers=[
                answer.transform_texts(text_transformer) for answer in self.answers
            ],
        )

    def transform_question_text(self, text_transformer: TextTransformer) -> "Question":
        return Question(
            orig_id=self.orig_id,
            text=text_transformer(self.text),
            image=self.image,
            answers=self.answers,
        )


@dataclass
class Test:
    title: TextLocalizations
    questions: list[Question]

    def transform_texts(self, text_transformer: TextTransformer) -> "Test":
        return Test(
            title=self.title,
            questions=[
                question.transform_texts(text_transformer)
                for question in self.questions
            ],
        )

    def transform_question_texts(self, text_transformer: TextTransformer) -> "Test":
        return Test(
            title=self.title,
            questions=[
                question.transform_question_text(text_transformer)
                for question in self.questions
            ],
        )
