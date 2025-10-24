"""
RAG-based FAQ Bot using FAISS and sentence-transformers
"""
import json
import os
from pathlib import Path
from typing import Optional
import numpy as np

try:
    import faiss
    from sentence_transformers import SentenceTransformer
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

# Sample FAQs for the bot
SAMPLE_FAQS = [
    {
        "question": "How do I create a new server?",
        "answer": "Click the '+' button in the server list on the left sidebar, then enter a name for your server."
    },
    {
        "question": "How do I add a channel to my server?",
        "answer": "Navigate to your server, then click '+ Add Channel' in the channel list to create a new channel."
    },
    {
        "question": "How can I upload files?",
        "answer": "In any channel, click the paperclip icon (📎) next to the message input to upload files."
    },
    {
        "question": "How do I know if someone is typing?",
        "answer": "When someone types a message, you'll see 'User is typing...' indicator at the bottom of the chat."
    },
    {
        "question": "How do I send a message?",
        "answer": "Type your message in the input box at the bottom of the chat and press Enter or click Send."
    },
    {
        "question": "Can I delete my account?",
        "answer": "Contact an administrator to request account deletion. Your data will be permanently removed."
    },
    {
        "question": "Is this application free?",
        "answer": "Yes, Discord Clone is a free, open-source application built with Python and React."
    },
    {
        "question": "How do I change my password?",
        "answer": "Go to your account settings and click 'Change Password' to update your password."
    },
]

class RAGBot:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.index = None
        self.faqs = []
        self.embeddings = None
        
        if FAISS_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name)
            except Exception as e:
                print(f"Warning: Could not load sentence transformer: {e}")

    def train_from_faqs(self, faqs: list[dict]):
        """Train the bot from a list of FAQ dictionaries"""
        if not FAISS_AVAILABLE or not self.model:
            return False
        
        try:
            self.faqs = faqs
            questions = [faq["question"] for faq in faqs]
            
            # Generate embeddings for all questions
            self.embeddings = self.model.encode(questions)
            
            # Create FAISS index
            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(self.embeddings.astype('float32'))
            
            return True
        except Exception as e:
            print(f"Error training bot: {e}")
            return False

    def ask(self, question: str, top_k: int = 1) -> Optional[str]:
        """Ask the bot a question and get the most relevant answer"""
        if not self.model or not self.index or not self.faqs:
            return None
        
        try:
            # Encode the question
            question_embedding = self.model.encode([question])
            
            # Search in FAISS
            distances, indices = self.index.search(question_embedding.astype('float32'), top_k)
            
            # Get the most relevant FAQ
            if len(indices) > 0 and len(indices[0]) > 0:
                best_idx = indices[0][0]
                if 0 <= best_idx < len(self.faqs):
                    return self.faqs[best_idx]["answer"]
            
            return None
        except Exception as e:
            print(f"Error asking bot: {e}")
            return None

    def save(self, path: str):
        """Save the bot index and FAQs to disk"""
        try:
            os.makedirs(path, exist_ok=True)
            
            # Save index
            if self.index:
                faiss.write_index(self.index, os.path.join(path, "index.faiss"))
            
            # Save FAQs
            with open(os.path.join(path, "faqs.json"), "w") as f:
                json.dump(self.faqs, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving bot: {e}")
            return False

    def load(self, path: str):
        """Load bot index and FAQs from disk"""
        if not FAISS_AVAILABLE:
            return False
        
        try:
            # Load index
            index_path = os.path.join(path, "index.faiss")
            if os.path.exists(index_path):
                self.index = faiss.read_index(index_path)
            
            # Load FAQs
            faqs_path = os.path.join(path, "faqs.json")
            if os.path.exists(faqs_path):
                with open(faqs_path, "r") as f:
                    self.faqs = json.load(f)
            
            # Re-generate embeddings for reference
            if self.faqs and self.model:
                questions = [faq["question"] for faq in self.faqs]
                self.embeddings = self.model.encode(questions)
            
            return True
        except Exception as e:
            print(f"Error loading bot: {e}")
            return False


# Global bot instance
_bot_instance: Optional[RAGBot] = None

def get_bot() -> RAGBot:
    """Get or create the global bot instance"""
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = RAGBot()
    return _bot_instance

def initialize_bot():
    """Initialize the bot with sample FAQs"""
    bot = get_bot()
    
    # Try to load from disk first
    bot_path = Path("bot_data")
    if bot_path.exists():
        if bot.load(str(bot_path)):
            print("Bot loaded from disk")
            return
    
    # If not, train from sample FAQs
    if bot.train_from_faqs(SAMPLE_FAQS):
        bot.save(str(bot_path))
        print("Bot initialized with sample FAQs and saved")
    else:
        print("Warning: Could not initialize bot (FAISS/sentence-transformers may not be installed)")
