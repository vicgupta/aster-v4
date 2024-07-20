question_prompts = """
## TASK ##
- You are creating a mobile applications for that chats using the OpenAI API. 
- Write user stories.

## INSTRUCTIONS ##
- Ask short 5 questions with options about the task at hand.
- Alwasys respond in the following JSON format:
{
    "questions": [
        {
            "question": "question text",
            "options": ["option1", "option2", "option3"]
        },
        {
            "question": "question text",
            "options": ["option1", "option2", "option3"]
        },
    ]
}
"""
