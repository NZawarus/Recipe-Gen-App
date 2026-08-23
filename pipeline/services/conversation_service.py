from database.conversations_databridge import ConversationDatabaseBridge
from models.conversations import Conversation, ConversationCreate, ConversationGet, ConversationUpdate, ConversationDelete, Message

class ConversationService:
    def __init__(self):
        self.db = ConversationDatabaseBridge()

    def create_conversation(self, conversation: ConversationCreate):
        return self.db.create_conversation(conversation)
    
    def get_conversation(self, conversation_id: int):
        return self.db.get_conversation(conversation_id)    
    
    def update_conversation(self, conversation_id: int, conversation: ConversationUpdate):
        return self.db.update_conversation(conversation_id, conversation)
    
    def delete_conversation(self, conversation_id: int):
        return self.db.delete_conversation(conversation_id)
    
    def get_all_conversations(self):
        return self.db.get_all_conversations()
