from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from newsletter_gen.tools.custom_tool import SearchAndContents, FindSimilar, GetContents
from datetime import datetime


# Uncomment the following line to use an example of a custom tool
# from newsletter_gen.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class NewsletterGenCrew():
    """NewsletterGen crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[SearchAndContents(), FindSimilar(), GetContents()],
            verbose=True
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'],
            tools=[SearchAndContents(), FindSimilar(), GetContents()],
            verbose=True
        )

    @agent
    def designer(self) -> Agent:
        return Agent(
            config=self.agents_config['designer'],
            tools=[],
            verbose=True,
            allow_delegation=False  # CrewAI by default functionality that agent can delegating
            # their work or asking questions to any other agent when they are stuck, but this
            # agent will not get any help from other agents
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.researcher(),
            output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_research_task.md"
        )

    @task
    def edit_task(self) -> Task:
        return Task(
            config=self.tasks_config['edit_task'],
            agent=self.editor(),
            output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_edit_task.md"
        )

    @task
    def newsletter_task(self) -> Task:
        return Task(
            config=self.tasks_config['newsletter_task'],
            agent=self.designer(),
            output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_newsletter_task.html"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the NewsletterGen crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
