from django.test import TestCase, Client
from .models import QuizBank, Answer
from random import randint
from django.urls import reverse

# Create your tests here.
class QuizBankTestCase(TestCase):
    def test_quizbank_creation(self):
        quiz_bank = QuizBank.objects.create(
            question_text="What is 2+2?",
            question_type="MCQ",
            points=2,
        )
        self.assertEqual(quiz_bank.question_text, "What is 2+2?")
        self.assertEqual(quiz_bank.question_type, "MCQ")
        self.assertEqual(quiz_bank.points, 2)

    def test_quizbank_save_strips_whitespace(self):
        quiz_bank = QuizBank.objects.create(
            question_text="  What is 2+2?  ",
            question_type="MCQ",
            points=2,
        )
        self.assertEqual(quiz_bank.question_text, "What is 2+2?")

    def test_quizbank_edit_and_strips_whitespace(self):
        quiz_bank = QuizBank.objects.create(
            question_text="What is 2+2?",
            question_type="MCQ",
            points=2,
        )

        quiz_bank.question_text = '  What is 3+3?  '
        quiz_bank.save()

        self.assertEqual(quiz_bank.question_text, "What is 3+3?")
        self.assertEqual(quiz_bank.question_type, "MCQ")
        self.assertEqual(quiz_bank.points, 2)

class AnswerTestCase(TestCase):
    def setUp(self):
        self.quiz_bank = QuizBank.objects.create(
            question_text="What is the capital of France?",
            question_type="MCQ",
            points=1,
        )

    def test_answer_creation(self):
        answer = Answer.objects.create(
            question=self.quiz_bank,
            option_text="Paris",
            is_correct=True,
        )
        self.assertEqual(answer.option_text, "Paris")
        self.assertTrue(answer.is_correct)

    def test_answer_save_strips_whitespace(self):
        answer = Answer.objects.create(
            question=self.quiz_bank,
            option_text="  London  ",
            is_correct=False,
        )
        self.assertEqual(answer.option_text, "London")

    def test_answer_edit_and_strips_whitespace(self):
        answer = Answer.objects.create(
            question=self.quiz_bank,
            option_text="London",
            is_correct=False,
        )
        
        answer.option_text = '  Paris  '
        answer.is_correct = True
        answer.save()

        self.assertEqual(answer.option_text, "Paris")
        self.assertTrue(answer.is_correct)

    def test_answer_deletion(self):
        answer = Answer.objects.create(
            question=self.quiz_bank,
            option_text="London",
            is_correct=False,
        )

        answer.delete()

        self.assertFalse(Answer.objects.filter(id=answer.id).exists())

class TestQuizBankDeletionCascade(TestCase):
    def setUp(self):
        self.quiz_bank = QuizBank.objects.create(
            question_text="What is the capital of France?",
            question_type="MCQ",
            points=1,
        )
        
        Answer.objects.create(
            question=self.quiz_bank,
            option_text="Paris",
            is_correct=True,
        )
        
        Answer.objects.create(
            question=self.quiz_bank,
            option_text="London",
            is_correct=False,
        )

    def test_delete_quiz_bank_deletes_answers(self):
        self.quiz_bank.delete()
        
        # Check if the QuizBank instance is deleted
        self.assertFalse(QuizBank.objects.filter(id=self.quiz_bank.id).exists())
        
        # Check if the associated Answer instances are also deleted
        self.assertFalse(Answer.objects.filter(question=self.quiz_bank.id).exists())

class TestViews(TestCase):
    def test_normal_view(self):
        client = Client()
        response = client.get('/quiz_bank/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Quiz Bank - Home')

    def test_json_upload_view(self):
        client = Client()

        response = client.get(rf'/quiz_bank/json/upload')
        self.assertEqual(response.status_code, 200)

    def test_blocked_json_delete_view(self):
        client = Client()

        any_integer = randint(1, 2**8)

        response = client.get(rf'/quiz_bank/json/delete/{any_integer}')
        self.assertEqual(response.status_code, 400)

    
