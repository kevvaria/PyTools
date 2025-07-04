#!/usr/bin/env python3
"""
Gemini Assistant
A Python interface for Google's Gemini AI model
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional

# Try to import Google's Gemini library
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai library not found.")
    print("Install it with: pip install google-generativeai")

class GeminiAssistant:
    """
    A Python assistant using Google's Gemini AI model
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-pro"):
        """
        Initialize the Gemini Assistant
        
        Args:
            api_key (str, optional): Google API key for Gemini
            model_name (str): Name of the Gemini model to use
        """
        # Try to get API key from various sources
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY') or "AIzaSyA2hv_wbUFZLoC7ZpBUmGnWMMiM-DwU_jA"
        self.model_name = model_name
        self.model = None
        self.chat_history = []
        
        if GEMINI_AVAILABLE and self.api_key:
            self._initialize_model()
        else:
            print("Gemini not available. Please check your API key.")
    
    def _initialize_model(self):
        """Initialize the Gemini model"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            print(f"✅ Gemini Assistant initialized with model: {self.model_name}")
        except Exception as e:
            print(f"❌ Error initializing Gemini model: {str(e)}")
            self.model = None
    
    def chat(self, message: str) -> str:
        """
        Send a message to Gemini and get a response
        
        Args:
            message (str): The message to send
            
        Returns:
            str: Gemini's response
        """
        if not self.model:
            return "❌ Gemini model not available. Please check your API key."
        
        try:
            response = self.model.generate_content(message)
            response_text = response.text
            
            # Store in chat history
            self.chat_history.append({
                'user': message,
                'assistant': response_text,
                'timestamp': self._get_timestamp()
            })
            
            return response_text
            
        except Exception as e:
            error_msg = f"❌ Error communicating with Gemini: {str(e)}"
            print(error_msg)
            return error_msg
    
    def start_conversation(self):
        """Start an interactive conversation with Gemini"""
        if not self.model:
            print("❌ Gemini model not available. Please check your API key.")
            return
        
        print("\n🤖 Gemini Assistant - Interactive Chat")
        print("=" * 50)
        print("Type 'quit', 'exit', or 'bye' to end the conversation")
        print("Type 'history' to see chat history")
        print("Type 'clear' to clear chat history")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Goodbye! Thanks for chatting with Gemini Assistant!")
                    break
                elif user_input.lower() == 'history':
                    self._show_chat_history()
                    continue
                elif user_input.lower() == 'clear':
                    self.chat_history.clear()
                    print("✅ Chat history cleared!")
                    continue
                elif not user_input:
                    continue
                
                print("\n🤖 Gemini: ", end="")
                response = self.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for chatting with Gemini Assistant!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {str(e)}")
    
    def _show_chat_history(self):
        """Display the chat history"""
        if not self.chat_history:
            print("📝 No chat history available.")
            return
        
        print(f"\n📝 Chat History ({len(self.chat_history)} messages):")
        print("-" * 50)
        
        for i, entry in enumerate(self.chat_history, 1):
            print(f"\n{i}. {entry['timestamp']}")
            print(f"   👤 You: {entry['user']}")
            print(f"   🤖 Gemini: {entry['assistant']}")
            print("-" * 30)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def save_chat_history(self, filename: str = "gemini_chat_history.json"):
        """Save chat history to a JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, indent=2, ensure_ascii=False)
            print(f"✅ Chat history saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving chat history: {str(e)}")
    
    def load_chat_history(self, filename: str = "gemini_chat_history.json"):
        """Load chat history from a JSON file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    self.chat_history = json.load(f)
                print(f"✅ Chat history loaded from {filename}")
            else:
                print(f"📝 No existing chat history file found: {filename}")
        except Exception as e:
            print(f"❌ Error loading chat history: {str(e)}")

def main():
    """Main function to run the Gemini Assistant"""
    print("🤖 Gemini Assistant")
    print("=" * 30)
    
    # Check if Gemini is available
    if not GEMINI_AVAILABLE:
        print("❌ Required library not found.")
        print("Please install: pip install google-generativeai")
        return
    
    # Check for API key (now has fallback)
    api_key = os.getenv('GOOGLE_API_KEY') or "AIzaSyA2hv_wbUFZLoC7ZpBUmGnWMMiM-DwU_jA"
    if not api_key:
        print("❌ No API key available.")
        print("Please set your Google API key:")
        print("export GOOGLE_API_KEY='your-api-key-here'")
        return
    
    # Initialize assistant
    assistant = GeminiAssistant()
    
    # Load previous chat history if available
    assistant.load_chat_history()
    
    # Start conversation
    assistant.start_conversation()
    
    # Save chat history before exiting
    assistant.save_chat_history()

if __name__ == "__main__":
    main() 