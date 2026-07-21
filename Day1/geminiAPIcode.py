#IMPORTS
import os
import google.generativeai as genai


#OUR FLOWCHART:
def get_gemini_response(prompt: str) -> str:
   # 1. Configure API key
   api_key = os.environ.get("GEMINI_API_KEY")
  
   # Check if API key is set
   if not api_key:
       return 'API Key Error'
  
   try:
       genai.configure(api_key=api_key)
      
       # 2. Initialize model
       model = genai.GenerativeModel("gemini-1.5-flash")
      
       # 3. Generate content
       response = model.generate_content(prompt)
      
       # 4. Return response
       return response.text


   except Exception as e:
       # Handle initialization/generation errors
       return f"Error: {str(e)}"


#CHAT LOOP
def start_chat():
   print("Gemini Chat Started! (Type 'quit' or 'exit' to stop)\n" + "-"*45)
  
   while True:
       user_input = input("You: ")
      
       # Exit condition
       if user_input.strip().lower() in ["quit", "exit"]:
           print("Goodbye!")
           break
          
       # Ignore empty inputs
       if not user_input.strip():
           continue
          
       # Get and display response
       response = get_gemini_response(user_input)
       print(f"Gemini: {response}\n")


if __name__ == "__main__":
   start_chat()





