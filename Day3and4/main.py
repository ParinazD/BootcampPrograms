

import os
from langchain_core.tools import Tool, tool
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.messages import (SystemMessage, HumanMessage, AIMessage, ToolMessage, BaseMessage)

'''
# Import LangChain agent components
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_core.tools import tool

# Import Groq chat model
from langchain_groq import ChatGroq

# Import conversation memory
from langchain.memory import ConversationBufferMemory
import os
'''
# Starting money values
revenue = 0
expenses = 0


# Tool 1: Make Coffee Function
@tool
def make_coffee(amount: str):
				"""
				Makes coffee and updates business finances.
				Each coffee costs $1 and sells for $2.
				This means n coffees gievs you $n profit
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
				return f"Current total profit is ${profit}"


# Create LangChain Tools
#make tool descriptions more explicit 
#about when to use each tool and what input to provide
tools = [make_coffee, calculate_profit]


# Initialize Groq LLM
llm = ChatGroq(

				# Groq model
				model="llama-3.3-70b-versatile",

				# Creativity level
				temperature=0,

				api_key= os.environ.get("GROQ_API_KEY")
)

#bind tools to llm
llmWithTools = llm.bind_tools(tools)

'''
# Create Agent with the new create_agent API
agent = create_agent(
				model=llm,
				tools=tools,
				system_prompt="You are a helpful coffee shop manager assistant. Help the user manage finances and make coffee.",
)
'''


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

		messages: list[BaseMessage] = [
				SystemMessage(content="You are a helpful coffee shop manager assistant. Help the user manage finances and make coffee. Each coffee is sold for 2 dollars but the expense is 1 dollar, making each coffee give 1 dollar profit."),
				HumanMessage(content=user_input)
		]

		# Send request to agent
		response = llmWithTools.invoke(messages)

		#Lets see the full RAW resopnse format
		print("Agent's raw response:",response)

		while response.tool_calls:
				
				#Save model response to memory
				messages.append(response)

				for tool_call in response.tool_calls:
					tool_name = tool_call["name"]
					tool_args = tool_call["args"]
					tool_id = tool_call["id"]
					print(f"Model requested using the tool: {tool_name} with args: {tool_args}")

					if tool_name == "make_coffee":
							#execute make_coffee
							tool_result = make_coffee.invoke(tool_args)
					elif tool_name == "calculate_profit":
							#call calculate profit
							tool_result = calculate_profit.invoke(tool_args)

					messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_id))
					#Give the llm the tool results to finish its response
					response = llmWithTools.invoke(messages)

					messages.append(response)
					#print("Agent Answer:",response)


		print("Agent: ",response)

		# Show current financial state
		print(
				f"💰 Revenue: ${revenue} | "
				f"Expenses: ${expenses} | "
				f"Profit: ${revenue-expenses}\n"
		)