import panel as pn
from ..controllers.CrewAi.crew import JobChatbotCrew

# Load the CrewAI configuration
crew = JobChatbotCrew().crew()





async def chatWithLLM(user_msg):
    user_message = user_msg
    if user_message.strip():
        # Simulate running the CrewAI chatbot
        inputs = {"user_message": user_message}
        try:
            response = crew.kickoff(inputs=inputs)
            print(response)
            return response
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
