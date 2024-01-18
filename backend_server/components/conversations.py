class Conversation:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.messages = []

    def add_message(self, message: str, sender: str):
        self.messages.append({"message": message, "sender": sender})

    def get_messages(self):
        return self.messages
