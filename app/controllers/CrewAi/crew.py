from crewai import Agent, Task, Crew, LLM
from crewai.project import CrewBase, agent, task, crew
import yaml
import os

os.environ["AWS_REGION_NAME"] = "us-east-1"

# Initialize LangChain's BedrockChat for Claude v3
llm = LLM(
        model="bedrock/anthropic.claude-3-haiku-20240307-v1:0"
    )


@CrewBase
class JobChatbotCrew:

        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        tasks_config_path = os.path.join(base_dir, "config", "tasks.yaml") 
        print(f"Tasks config path: {tasks_config_path}")
        
        agents_config_path = os.path.join(base_dir, "config", "agents.yaml") 
        print(f"Agents config path: {agents_config_path}")

        agents_config = agents_config_path
        tasks_config = tasks_config_path
 

        
           
        def __init__(self):
            super().__init__()
            
            # Load tasks and agents configuration files
            with open(self.tasks_config, 'r') as f:
                self.tasks_config = yaml.safe_load(f)
            with open(self.agents_config, 'r') as f:
                self.agents_config = yaml.safe_load(f)
             

        @agent
        def base_question_agent(self):
            """Creates the Base Question Agent."""
            agent_config = self.agents_config["agents"]["base_question_agent"]
            return Agent(
                role=agent_config["role"],
                goal=agent_config["goal"],
                backstory=agent_config["backstory"],
                llm=llm,  # Use BedrockChat instance
                verbose=True,
            )

        @agent
        def contextual_question_agent(self):
            """Creates the Contextual Question Agent."""
            agent_config = self.agents_config["agents"]["contextual_question_agent"]
            return Agent(
                role=agent_config["role"],
                goal=agent_config["goal"],
                backstory=agent_config["backstory"],
                llm=llm,  # Use BedrockChat instance
                verbose=True,
            )

        @task
        def ask_base_question_task(self):
            """Creates the task for asking base questions."""
            task_config = self.tasks_config["tasks"]["ask_base_question"]
            return Task(
                description=task_config["description"],
                expected_output=task_config["expected_output"],
                agent=self.base_question_agent(),
            )

        @task
        def ask_contextual_question_task(self):
            """Creates the task for asking contextual questions."""
            task_config = self.tasks_config["tasks"]["ask_contextual_question"]
            return Task(
                description=task_config["description"],
                expected_output=task_config["expected_output"],
                agent=self.contextual_question_agent(),
            )

        @crew
        def crew(self):
            """Creates the crew with agents and tasks."""
            return Crew(
                agents=[
                    self.base_question_agent(),
                    self.contextual_question_agent(),
                ],
                tasks=[
                    self.ask_base_question_task(),
                    self.ask_contextual_question_task(),
                ],
                process="sequential",
                verbose=True,
            )