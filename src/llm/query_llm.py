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
You are an expert SQL generator for a company database.

Here is the table you can use:

Table: employees
Columns:
- id (integer)
- name (text)
- city (text)
- department (text)

Rules:
- Only generate SQL queries based on this table and columns.
- Do not make up any other tables or columns.
- Only return the SQL code, no explanations or apologies.
- Keep the SQL clean and formatted.

Convert the following natural language question into an SQL query:

Question: {question}

SQL Query:
"""
)


# function to generate SQL
async def generate_sql_from_question(question: str) -> str:
    chain = prompt | llm
    response = await chain.ainvoke({"question": question})
    return response.content.strip()
