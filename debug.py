
messages = [
    {
        "role": "system",
        "content": "You are an expert at adding and multiplying numbers together. Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.",
    },
    {"role": "user", "content": "Hello!"},
]

from typing import List, Dict

class Message:
    def __init__(
        self,
        role: str,
        content: str,
        tool_calls: List=[],
        tool_call_id: str = None,
        name: str = None
    ):
        self.role = role
        self.content = content
        self.tool_calls = tool_calls
        self.tool_call_id = tool_call_id
        self.name = name
        
        
    def to_dict(self):
        message_dict = {'role': self.role, 'content': self.content}
        if self.tool_calls:
            message_dict['tool_calls'] = self.tool_calls
        if self.tool_call_id:
            message_dict['tool_call_id'] = self.tool_call_id
        if self.name:
            message_dict['name'] = self.name
        return message_dict
    
    
class Conversation:
    def __init__(self, messages: List[Dict[str,str]]):
        self.messages = [Message(**message) for message in messages]
        
    def __iter__(self):
        for message in self.messages:
            yield message
            
    def to_dict(self):
        return [message.to_dict() for message in self.messages]
    
    def add_message(self, message: Dict[str,str]):
        self.messages.append(Message(**message))
        
    def add_system_message(self, completion):
        self.add_message(
            {
                'role' : completion.choices[0].message.role,
                'content' : completion.choices[0].message.content,
                'tool_calls' : completion.choices[0].message.tool_calls,
            }
        )
        
    def add_human_message(self, message):
        self.add_message(
            {
                'role' : 'user',
                'content' : message
            }
        )
        
    def add_tool_message(self, tool_called, response):
        self.add_message(
            {
                'role' : 'tool', 
                'name' : tool_called.function_name,
                'tool_call_id': tool_called.id,
                'content' : str(response)
            }
        )
        
    def print_conversation(self): 
        for message in self.messages:
            print(f"{message.role} : {message.content}")
            
conversation = Conversation(messages)
conversation.print_conversation()