from crewai.knowledge.source.text_file_knowledge_source import (
    TextFileKnowledgeSource,
)


def create_business_knowledge():
    menu = TextFileKnowledgeSource(
        file_paths=["menu.txt"]
    )

    delivery = TextFileKnowledgeSource(
        file_paths=["delivery.txt"]
    )

    policies = TextFileKnowledgeSource(
        file_paths=["policies.txt"]
    )

    faq = TextFileKnowledgeSource(
        file_paths=["faq.txt"]
    )

    return [
        menu,
        delivery,
        policies,
        faq,
    ]
