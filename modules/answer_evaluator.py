# modules/answer_evaluator.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

class AnswerEvaluator:
    def __init__(self):
        """Initialize the answer evaluator"""
        print("Loading evaluation model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded!")
    
    def evaluate_mcq(self, student_answer, correct_answer):
        """Evaluate multiple choice answer"""
        student_answer = student_answer.upper().strip()
        correct_answer = correct_answer.upper().strip()
        
        is_correct = student_answer == correct_answer
        score = 100 if is_correct else 0
        
        return {
            'score': score,
            'is_correct': is_correct,
            'feedback': 'Correct! Well done!' if is_correct else f'Incorrect. The correct answer is {correct_answer}.'
        }
    
    def evaluate_true_false(self, student_answer, correct_answer):
        """Evaluate True/False answer"""
        if isinstance(student_answer, str):
            student_answer = student_answer.lower() in ['true', 't', 'yes', '1']
        
        is_correct = student_answer == correct_answer
        score = 100 if is_correct else 0
        
        return {
            'score': score,
            'is_correct': is_correct,
            'feedback': 'Correct!' if is_correct else f'Incorrect. The answer is {correct_answer}.'
        }
    
    def evaluate_short_answer(self, student_answer, correct_answer, key_points=None):
        """Evaluate short answer using multiple methods"""
        if not student_answer or not student_answer.strip():
            return {
                'score': 0,
                'is_correct': False,
                'feedback': 'No answer provided.',
                'breakdown': {
                    'semantic_similarity': 0,
                    'keyword_match': 0,
                    'length_appropriateness': 0
                }
            }
        
        # Calculate scores
        semantic_score = self._calculate_semantic_similarity(student_answer, correct_answer)
        keyword_score = self._calculate_keyword_match(student_answer, correct_answer, key_points)
        length_score = self._calculate_length_score(student_answer, correct_answer)
        
        # Combined score
        final_score = (
            semantic_score * 0.5 +
            keyword_score * 0.35 +
            length_score * 0.15
        )
        
        # Generate feedback
        feedback = self._generate_feedback(final_score, semantic_score, keyword_score, key_points, student_answer)
        
        return {
            'score': round(final_score, 2),
            'is_correct': final_score >= 60,
            'feedback': feedback,
            'breakdown': {
                'semantic_similarity': round(semantic_score, 2),
                'keyword_match': round(keyword_score, 2),
                'length_appropriateness': round(length_score, 2)
            }
        }
    
    def _calculate_semantic_similarity(self, student_answer, correct_answer):
        """Calculate semantic similarity using embeddings"""
        try:
            student_embedding = self.model.encode([student_answer])
            correct_embedding = self.model.encode([correct_answer])
            
            similarity = cosine_similarity(student_embedding, correct_embedding)[0][0]
            
            return max(0, min(100, similarity * 100))
        except Exception as e:
            print(f"Error calculating semantic similarity: {e}")
            return 0
    
    def _calculate_keyword_match(self, student_answer, correct_answer, key_points=None):
        """Calculate keyword match percentage"""
        correct_keywords = set(self._extract_keywords(correct_answer))
        
        if key_points:
            for point in key_points:
                correct_keywords.update(self._extract_keywords(point))
        
        student_keywords = set(self._extract_keywords(student_answer))
        
        if not correct_keywords:
            return 0
        
        matched = len(student_keywords.intersection(correct_keywords))
        total = len(correct_keywords)
        
        return (matched / total) * 100
    
    def _extract_keywords(self, text):
        """Extract meaningful keywords from text"""
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
                     'this', 'that', 'these', 'those', 'it', 'its'}
        
        words = re.findall(r'\b[a-z]+\b', text.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        return keywords
    
    def _calculate_length_score(self, student_answer, correct_answer):
        """Calculate if answer length is appropriate"""
        student_words = len(student_answer.split())
        correct_words = len(correct_answer.split())
        
        if correct_words == 0:
            return 0
        
        ratio = student_words / correct_words
        
        if 0.5 <= ratio <= 1.5:
            return 100
        elif 0.3 <= ratio < 0.5 or 1.5 < ratio <= 2.0:
            return 70
        else:
            return 40
    
    def _generate_feedback(self, score, semantic_score, keyword_score, key_points, student_answer):
        """Generate helpful feedback based on scores"""
        if score >= 90:
            return "Excellent answer! You demonstrated strong understanding."
        elif score >= 75:
            return "Good answer! You covered most key points effectively."
        elif score >= 60:
            return "Satisfactory answer. You got the main idea but could add more detail."
        elif score >= 40:
            feedback = "Partial understanding shown. "
            if keyword_score < 40 and key_points:
                missing = []
                for point in key_points[:2]:
                    if point.lower() not in student_answer.lower():
                        missing.append(point)
                if missing:
                    feedback += f"Consider mentioning: {', '.join(missing)}. "
            if semantic_score < 50:
                feedback += "Try to align your answer more closely with the core concept."
            return feedback
        else:
            return "Your answer needs significant improvement. Review the material and try to include key concepts."
