from crewai import Agent, LLM

import crewai.llms.cache as crew_cache

from config.settings import MODEL_NAME


# Groq does not support CrewAI's cache_breakpoint field.
crew_cache.mark_cache_breakpoint = lambda msg: msg


def create_validation_agent():
    llm = LLM(
        model=MODEL_NAME,
        api_key=None
    )

    return Agent(
        role="Order Validation Specialist",
        goal=(
            "Validate customer orders and determine whether all required "
            "information is available before an order can proceed."
        ),
        backstory=(
            "You are responsible for checking customer orders carefully. "
            "You identify missing information, detect invalid or unclear "
            "details, and determine whether an order is ready for confirmation. "
            "You never invent missing information."
        ),
        llm=llm,
        verbose=True
    )
