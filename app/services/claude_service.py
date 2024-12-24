import anthropic
from anthropic import APIError, APITimeoutError, APIConnectionError, RateLimitError
from typing import Optional
from flask import current_app

class ClaudeService:
    def __init__(self, app):
        self.logger = app.logger
        self.api_key = app.config["ANTHROPIC_API_KEY"]
        if not self.api_key:
            self.logger.error("ANTHROPIC_API_KEY not configured")
            raise ValueError("ANTHROPIC_API_KEY not configured")
        
        try:
            self.client = anthropic.Client(api_key=self.api_key)
            self.logger.info("Claude API client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Claude API client: {str(e)}")
            raise

    def get_response(self, call_id: str, question: str, transcript: str) -> Optional[str]:
        """Get AI response for a question about a call transcript."""
        # Input validation
        if not all([call_id, question, transcript]):
            missing = []
            if not call_id: missing.append("call_id")
            if not question: missing.append("question")
            if not transcript: missing.append("transcript")
            error_msg = f"Missing required parameters: {', '.join(missing)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        self.logger.info(f"Processing question for call {call_id}: {question[:100]}...")
            
        try:
            system_prompt = "You are a helpful AI assistant analyzing sales call transcripts. Provide concise, focused answers based only on the information in the transcript."
            
            prompt = f"""Given this sales call transcript:

{transcript}

Please answer this question about the call: {question}

Keep your answer concise and focused on the specific question asked.
If you can't find a clear answer in the transcript, please say so."""

            self.logger.debug(f"Sending request to Claude API for call {call_id}")
            message = self.client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=300,
                temperature=0,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            response = message.content[0].text
            self.logger.info(f"Successfully got response for call {call_id}")
            self.logger.debug(f"Response length: {len(response)} characters")
            return response

        except RateLimitError as e:
            self.logger.error(f"Rate limit exceeded for call {call_id}: {str(e)}")
            raise Exception("Too many requests. Please try again later.") from e
            
        except APITimeoutError as e:
            self.logger.error(f"API timeout for call {call_id}: {str(e)}")
            raise Exception("Request timed out. Please try again.") from e
            
        except APIConnectionError as e:
            self.logger.error(f"Connection error for call {call_id}: {str(e)}")
            raise Exception("Unable to connect to AI service. Please try again later.") from e
            
        except APIError as e:
            self.logger.error(f"API error for call {call_id}: {str(e)}")
            raise Exception("AI service error. Please try again later.") from e
            
        except Exception as e:
            self.logger.error(f"Unexpected error processing question for call {call_id}: {str(e)}")
            raise Exception("An unexpected error occurred. Please try again later.") from e 

    def ask_question(self, question: str, call: dict) -> str:
        """Ask a question about a specific call."""
        if current_app.config.get('TESTING'):
            return "This is a test response from Claude"
            
        # Use the existing get_response method
        return self.get_response(
            call_id=call['id'],
            question=question,
            transcript=call['transcript']['text']
        ) 