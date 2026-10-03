from crewai import Crew, Process

from tasks.order_tasks import create_order_task
from tasks.validation_tasks import create_validation_task


def create_order_crew(customer_message):

    order_task = create_order_task(
        customer_message
    )

    validation_task = create_validation_task()

    validation_task.context = [
        order_task
    ]

    crew = Crew(
        agents=[
            order_task.agent,
            validation_task.agent,
        ],
        tasks=[
            order_task,
            validation_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    return crew
