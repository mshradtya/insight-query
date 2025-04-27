from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# load env
load_dotenv()

# init model
llm = ChatOpenAI(
    model="gpt-4o",  # chat-based model
    temperature=0.2,
)

# create prompt template
prompt = ChatPromptTemplate.from_template(
    """
You are an expert SQL generator.
Convert the following natural language question into a correct SQL query.

Question: {question}

SQL Query:
"""
)


# function to generate SQL
async def generate_sql_from_question(question: str) -> str:
    chain = prompt | llm
    response = await chain.ainvoke({"question": question})
    return response.content.strip()
