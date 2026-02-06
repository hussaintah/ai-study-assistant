import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import json
import re

load_dotenv()

class QuestionGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="llama-3.1-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
            temperature=0.7
        )
    
    def generate_mcq(self, content, num_questions=5):
        prompt = f"""You are an expert educational content creator. Generate {num_questions} multiple choice questions from the following content.

Content:
{content[:2000]}

Requirements:
1. Questions should test understanding, not just memorization
2. Each question should have 4 options (A, B, C, D)
3. Only ONE option should be correct
4. Incorrect options should be plausible but clearly wrong
5. Return ONLY valid JSON, no other text

Return format (JSON array):
[
  {{
    "question": "What is...",
    "options": {{
      "A": "Option 1",
      "B": "Option 2",
      "C": "Option 3",
      "D": "Option 4"
    }},
    "correct_answer": "B",
    "explanation": "Brief explanation why B is correct"
  }}
]

Generate the questions now:"""
        
        try:
            response = self.llm.invoke(prompt)
            result = response.content
            json_match = re.search(r'```json\s*(.*?)\s*```', result, re.DOTALL)
            if json_match:
                result = json_match.group(1)
            questions = json.loads(result)
            return questions
        except Exception as e:
            print(f"Error generating MCQ: {e}")
            return []
    
    def generate_true_false(self, content, num_questions=5):
        prompt = f"""Generate {num_questions} True/False questions from this content.

Content:
{content[:2000]}

Requirements:
1. Create clear statements that are definitively true or false
2. Mix true and false statements
3. Include explanation for each
4. Return ONLY valid JSON

Return format:
[
  {{
    "statement": "The statement here",
    "answer": true,
    "explanation": "Why this is true/false"
  }}
]

Generate the questions:"""
        
        try:
            response = self.llm.invoke(prompt)
            result = response.content
            json_match = re.search(r'```json\s*(.*?)\s*```', result, re.DOTALL)
            if json_match:
                result = json_match.group(1)
            questions = json.loads(result)
            return questions
        except Exception as e:
            print(f"Error generating T/F: {e}")
            return []
    
    def generate_short_answer(self, content, num_questions=3):
        prompt = f"""Generate {num_questions} short answer questions from this content.

Content:
{content[:2000]}

Requirements:
1. Questions should require 2-3 sentence answers
2. Test conceptual understanding
3. Include sample correct answer for each
4. Return ONLY valid JSON

Return format:
[
  {{
    "question": "Explain...",
    "sample_answer": "Sample correct answer here",
    "key_points": ["point1", "point2", "point3"]
  }}
]

Generate the questions:"""
        
        try:
            response = self.llm.invoke(prompt)
            result = response.content
            json_match = re.search(r'```json\s*(.*?)\s*```', result, re.DOTALL)
            if json_match:
                result = json_match.group(1)
            questions = json.loads(result)
            return questions
        except Exception as e:
            print(f"Error generating short answer: {e}")
            return []