from crewai import Agent, LLM

import crewai.llms.cache as crew_cache

from config.settings import MODEL_NAME
from rag.knowledge import create_business_knowledge


# Groq does not support CrewAI's cache_breakpoint field.
crew_cache.mark_cache_breakpoint = lambda msg: msg


def create_order_agent():
    llm = LLM(
        model=MODEL_NAME,
        api_key=None
    )

    knowledge_sources = create_business_knowledge()

    embedder = {
        "provider": "sentence-transformer",
        "config": {
            "model_name": "sentence-transformers/all-MiniLM-L6-v2"
        }
    }

    return Agent(
        role="Order Processing Specialist",
        goal=(
            "Understand customer orders accurately using the restaurant's "
            "business knowledge. Extract order details, verify products "
            "and options against the available menu, and identify missing "
            "information."
        ),
        backstory=(
            "You are an order processing specialist for Urban Bites. "
            "You use the restaurant's knowledge base to answer questions "
            "about menu items, prices, delivery areas, delivery fees, "
            "payment methods, and restaurant policies. "
            "You never invent business information."
        ),
        llm=llm,
        knowledge_sources=knowledge_sources,
        embedder=embedder,
        verbose=True
    )
