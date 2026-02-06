# modules/database.py
import os
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()

# Check if MongoDB is available
try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    print("Warning: pymongo not installed. Using fallback JSON storage.")

class Database:
    def __init__(self):
        """Initialize database connection"""
        self.use_mongodb = False
        
        if MONGODB_AVAILABLE:
            mongodb_uri = os.getenv("MONGODB_URI")
            
            if mongodb_uri:
                try:
                    self.client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
                    # Test connection
                    self.client.server_info()
                    self.db = self.client['study_assistant']
                    self.use_mongodb = True
                    print("✅ Connected to MongoDB")
                except ConnectionFailure:
                    print("⚠️ MongoDB connection failed. Using JSON fallback.")
                    self.use_mongodb = False
            else:
                print("⚠️ MONGODB_URI not found. Using JSON fallback.")
        
        # Fallback to JSON files if MongoDB not available
        if not self.use_mongodb:
            self.data_dir = "data"
            os.makedirs(self.data_dir, exist_ok=True)
    
    def save_questions(self, user_id, questions, question_type, content):
        """Save generated questions to database"""
        data = {
            'user_id': user_id,
            'questions': questions,
            'question_type': question_type,
            'content': content[:500],  # Store first 500 chars
            'created_at': datetime.now().isoformat()
        }
        
        if self.use_mongodb:
            try:
                self.db.questions.insert_one(data)
                return True
            except Exception as e:
                print(f"Error saving to MongoDB: {e}")
                return False
        else:
            # JSON fallback
            try:
                file_path = os.path.join(self.data_dir, f"questions_{user_id}.json")
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                return True
            except Exception as e:
                print(f"Error saving to JSON: {e}")
                return False
    
    def save_quiz_result(self, user_id, questions, answers, scores, total_score):
        """Save quiz results to database"""
        data = {
            'user_id': user_id,
            'questions_count': len(questions),
            'answers': answers,
            'scores': scores,
            'total_score': total_score,
            'completed_at': datetime.now().isoformat()
        }
        
        if self.use_mongodb:
            try:
                self.db.quiz_results.insert_one(data)
                return True
            except Exception as e:
                print(f"Error saving quiz result: {e}")
                return False
        else:
            # JSON fallback
            try:
                file_path = os.path.join(self.data_dir, f"quiz_results_{user_id}.json")
                
                # Load existing results
                results = []
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        results = json.load(f)
                
                # Append new result
                results.append(data)
                
                # Save back
                with open(file_path, 'w') as f:
                    json.dump(results, f, indent=2)
                
                return True
            except Exception as e:
                print(f"Error saving quiz result to JSON: {e}")
                return False
    
    def get_quiz_history(self, user_id, limit=10):
        """Get quiz history for a user"""
        if self.use_mongodb:
            try:
                results = list(self.db.quiz_results.find(
                    {'user_id': user_id}
                ).sort('completed_at', -1).limit(limit))
                
                # Convert ObjectId to string
                for result in results:
                    result['_id'] = str(result['_id'])
                
                return results
            except Exception as e:
                print(f"Error getting quiz history: {e}")
                return []
        else:
            # JSON fallback
            try:
                file_path = os.path.join(self.data_dir, f"quiz_results_{user_id}.json")
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        results = json.load(f)
                    return results[-limit:][::-1]  # Last 'limit' items, reversed
                return []
            except Exception as e:
                print(f"Error reading quiz history: {e}")
                return []
    
    def save_flashcard_progress(self, user_id, total_cards, known_cards, review_cards):
        """Save flashcard progress"""
        data = {
            'user_id': user_id,
            'total_cards': total_cards,
            'known_cards': known_cards,
            'review_cards': review_cards,
            'updated_at': datetime.now().isoformat()
        }
        
        if self.use_mongodb:
            try:
                # Upsert (update or insert)
                self.db.flashcard_progress.update_one(
                    {'user_id': user_id},
                    {'$set': data},
                    upsert=True
                )
                return True
            except Exception as e:
                print(f"Error saving flashcard progress: {e}")
                return False
        else:
            # JSON fallback
            try:
                file_path = os.path.join(self.data_dir, f"flashcards_{user_id}.json")
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                return True
            except Exception as e:
                print(f"Error saving flashcard progress: {e}")
                return False
    
    def get_user_stats(self, user_id):
        """Get user statistics"""
        stats = {
            'total_quizzes': 0,
            'average_score': 0,
            'total_questions_answered': 0,
            'flashcards_known': 0
        }
        
        if self.use_mongodb:
            try:
                # Quiz stats
                quiz_results = list(self.db.quiz_results.find({'user_id': user_id}))
                if quiz_results:
                    stats['total_quizzes'] = len(quiz_results)
                    stats['average_score'] = sum(r['total_score'] for r in quiz_results) / len(quiz_results)
                    stats['total_questions_answered'] = sum(r['questions_count'] for r in quiz_results)
                
                # Flashcard stats
                flashcard_data = self.db.flashcard_progress.find_one({'user_id': user_id})
                if flashcard_data:
                    stats['flashcards_known'] = len(flashcard_data.get('known_cards', []))
                
                return stats
            except Exception as e:
                print(f"Error getting user stats: {e}")
                return stats
        else:
            # JSON fallback
            try:
                # Quiz stats
                quiz_file = os.path.join(self.data_dir, f"quiz_results_{user_id}.json")
                if os.path.exists(quiz_file):
                    with open(quiz_file, 'r') as f:
                        quiz_results = json.load(f)
                    if quiz_results:
                        stats['total_quizzes'] = len(quiz_results)
                        stats['average_score'] = sum(r['total_score'] for r in quiz_results) / len(quiz_results)
                        stats['total_questions_answered'] = sum(r['questions_count'] for r in quiz_results)
                
                # Flashcard stats
                flashcard_file = os.path.join(self.data_dir, f"flashcards_{user_id}.json")
                if os.path.exists(flashcard_file):
                    with open(flashcard_file, 'r') as f:
                        flashcard_data = json.load(f)
                    stats['flashcards_known'] = len(flashcard_data.get('known_cards', []))
                
                return stats
            except Exception as e:
                print(f"Error getting user stats: {e}")
                return stats

# Global database instance
_db = None

def get_database():
    """Get database instance (singleton)"""
    global _db
    if _db is None:
        _db = Database()
    return _db