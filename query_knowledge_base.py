# external modules import
from pathlib import Path
from dotenv import load_dotenv

# internal modules import
from modules import QueryManager


# function definition
def query_knowledge_base(query_manager: QueryManager, questions_file_path: Path):
    pass


# main-like execution
if __name__ == '__main__':

    # load environment variables
    load_dotenv()

    # create query manager object
    query_manager_ = QueryManager()

    # execute questions submission pipeline
    query_knowledge_base(query_manager=query_manager_, questions_file_path=Path(__file__).parent / 'data' / 'test_questions.csv')
