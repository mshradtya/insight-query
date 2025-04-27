from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from db.schema_fetcher import get_database_schema

# load env
load_dotenv()

# init model
llm = ChatOpenAI(
    model="gpt-4o",  # chat-based model
    temperature=0.2,
)


async def generate_sql_from_question(question: str) -> str:
    schema_info = await get_database_schema()
    print(schema_info)

    prompt = ChatPromptTemplate.from_template(
        f"""
You are an expert SQL generator.

Available tables and columns:
{schema_info}

Rules:
- Only use available tables and columns.
- Do not hallucinate nonexistent tables or columns.
- Only return pure SQL, in a single line, without markdown code blocks.
- No explanation, only SQL.

Question: {{question}}
"""
    )

    chain = prompt | llm
    response = await chain.ainvoke({"question": question})
    return response.content.strip()
