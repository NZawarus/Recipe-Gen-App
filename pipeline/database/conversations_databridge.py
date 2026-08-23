import pymysql
from models.conversations import Conversation, ConversationCreate, ConversationGet, ConversationUpdate, ConversationDelete, Message

class ConversationDatabaseBridge:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1517109mysql-', db='food_users')
        self.cursor = self.conn.cursor()

    def create_conversation(self, conversation: ConversationCreate):
        self.cursor.execute("INSERT INTO conversations (user_id) VALUES (%s)", (conversation.user_id,))
        self.conn.commit()
        return conversation.user_id
    
    def get_conversation(self, conversation_id: int):
        self.cursor.execute("SELECT * FROM conversations WHERE id = %s", (conversation_id,))
        return self.cursor.fetchone()
    
    def update_conversation(self, conversation_id: int, conversation: ConversationUpdate):
        self.cursor.execute("UPDATE conversations SET user_id = %s WHERE id = %s", (conversation.user_id, conversation_id))
        self.conn.commit()
        return conversation_id
    
    def delete_conversation(self, conversation_id: int):
        self.cursor.execute("DELETE FROM conversations WHERE id = %s", (conversation_id,))
        self.conn.commit()
        return conversation_id
    
    def get_all_conversations(self):
        self.cursor.execute("SELECT * FROM conversations")
        return self.cursor.fetchall()

