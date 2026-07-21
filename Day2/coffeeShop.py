# Import LangChain agent components
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.tools import tool

# Import Groq chat model
from langchain_groq import ChatGroq

# Import conversation memory
from langchain.memory import ConversationBufferMemory
import os

# Starting money values
revenue = 0
expenses = 0


# Tool 1: Make Coffee Function
@tool
def make_coffee(amount: str):
    """
    Makes coffee and updates business finances.
    Each coffee costs $1 and sells for $2.
    """

    global revenue, expenses

    # Convert input into integer number of coffees
    coffees = int(amount)

    # Add sales revenue
    revenue += coffees * 2

    # Add coffee production expenses
    expenses += coffees * 1

    # Print coffee production
    print(f"☕ Made {coffees} coffee(s)!")

    # Return information to agent
    return (
        f"Made {coffees} coffees. "
        f"Revenue: ${revenue}, Expenses: ${expenses}"
    )


# Tool 2: Profit Calculator
@tool
def calculate_profit(query=""):
    """
    Calculates current coffee shop profit.
    """

    # Calculate profit
    profit = revenue - expenses

    # Return current status
    return f"Current profit is ${profit}"


# Create LangChain Tools
#make tool descriptions more explicit 
#about when to use each tool and what input to provide
tools = [

    Tool(
        name="make_coffee",
        func=make_coffee,
        description=(
            "USE THIS TOOL when the user wants to make money, "
            "increase profit, earn revenue, or reach a profit goal. "
            "Each coffee creates exactly $1 profit because it costs $1 "
            "and sells for $2. "
            "Input should be the number of coffees to make."
        )
    ),

    Tool(
        name="calculate_profit",
        func=calculate_profit,
        description=(
            "USE THIS TOOL only when the user asks to check, view, "
            "or calculate the current profit. "
            "Do NOT use this tool to create profit."
        )
    )
]



# Initialize Groq LLM
llm = ChatGroq(

    # Groq model
    model="llama-3.3-70b-versatile",

    # Creativity level
    temperature=0,

    api_key= os.environ.get("GROQ_API_KEY")

)


# Add Conversation Memory
memory = ConversationBufferMemory(

    # Store messages
    memory_key="chat_history",

    # Return messages to agent
    return_messages=True
)


# Create Agent
agent = initialize_agent(

    # Give agent tools
    tools,

    # Give agent brain
    llm,

    # Agent reasoning loop
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,

    # Add memory/context
    memory=memory,

    # Show reasoning steps
    verbose=True
)


# Chat Loop

import os
print("GROQ_API_KEY:", os.environ.get("GROQ_API_KEY"))

print("☕ Coffee Shop Agent Started!")
print("Ask me to make profit of $n or check earnings.")
print("Type 'exit' to stop.\n")


while True:

    # Get user request
    user_input = input("You: ")

    # Stop program
    if user_input.lower() == "exit":
        break

    # Send request to agent
    response = agent.invoke(
        {
            "input": user_input
        }
    )

    # Print agent response
    print("\nAgent:", response["output"])

    # Show current financial state
    print(
        f"💰 Revenue: ${revenue} | "
        f"Expenses: ${expenses} | "
        f"Profit: ${revenue-expenses}\n"
    )