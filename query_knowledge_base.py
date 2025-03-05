# external modules import
import os
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

# internal modules import
from modules import QAConfig, QueryAgent, QMConfig, QueryManager


# function definition
def query_knowledge_base(query_manager: QueryManager, questions_file_path: Path) -> None:
    answers = {}
    with open(questions_file_path, 'r', encoding='utf-8') as f:
        for question_number, question in enumerate(f):
            answers[question_number] = query_manager.answer_question(question=question)
            logger.info(f'Question: {question}')
            logger.info(f'Answer: {answers[question_number].dishes_codes}')
    query_manager.memorize_answers(answers=answers)

    return

# main-like execution
if __name__ == '__main__':

    # load environment variables
    load_dotenv()

    # create query manager object
    query_manager_ = QueryManager(
        config=QMConfig(
            kb_path=Path(__file__).parent / 'data' / 'processed' / 'dishes',
            planet_distances_path=Path(__file__).parent / 'data' / 'planets_distances.csv'
        ),
        query_agent=QueryAgent(
            config=QAConfig(
                ollama_server_uri=os.getenv('OLLAMA_SERVER_URI'),
                ollama_model_name=os.getenv('LBP_MODEL_NAME')
            )
        )
    )

    # execute questions submission pipeline
    query_knowledge_base(query_manager=query_manager_, questions_file_path=Path(__file__).parent / 'data' / 'test_questions.csv')
