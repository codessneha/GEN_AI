from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
#create table
db=SQLDatabase.from_uri("sqlite:///my_tasks.db")
db.run("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT CHECK (status IN ('pending', 'in_progress', 'completed')) NOT NULL DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

#llm,tools,memory,system prompt
llm=ChatGroq(
    model="openai/gpt-oss-120b",
)
toolkit=SQLDatabaseToolkit(db=db, llm=llm)
tools=toolkit.get_tools()
memory=InMemorySaver()
system_prompt= """
You are a task management assistant that interacts with a SQLite database. You can use the following tools
TASK RULES
1.LIMIT select queries to 10 rows WITH ORDER BY created_at DESC.
2.AFTER create, update, or delete operations, return a confirmation message.
3.ONLY use the provided tools for database interactions.
crud operations
CREATE:iNSERT INTO tasks (title, description, status) VALUES ('Task Title', 'Task Description', 'pending');
READ:SELECT * FROM tasks WHERE status='pending' ORDER BY created_at DESC LIMIT 10  
UPDATE:UPDATE tasks SET status='completed' WHERE id=?;
DELETE:DELETE FROM tasks WHERE id=?;

TASK SCHEMA:
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK (status IN ('pending', 'in_progress', 'completed')) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""
agent=create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt,
    checkpointer=memory,
)

while True:
    query=input("Enter your query (or type 'exit' to quit): ")
    if query.lower()=="exit":
        break
    response=agent.invoke(
        {
            "messages":[
                {
                    "role":"user",
                    "content":query
                }
            ]
        },
        {
            "configurable":{
                "thread_id":"1"
            }
        }
    )
    print("AI:",response["messages"][-1].content)
print("DB created successfully")
