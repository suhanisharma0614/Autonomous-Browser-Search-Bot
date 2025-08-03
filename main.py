import os
import asyncio
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel
from browser_use.llm import ChatOpenAI
from browser_use import Agent, BrowserSession, Controller
load_dotenv()

# Define Pydantic model
class Post(BaseModel):
    caption: str
    url: str

# Create a controller instance
controller = Controller(output_model=Post)

# Define browser session
browser_session = BrowserSession(
    executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    user_data_dir=os.path.expanduser('~\\AppData\\Local\\browseruse\\profiles\\default'),
    # headless=False,  # Optional: shows browser window for debugging
)

# Use OpenAI model (or switch to Anthropic if needed)
llm = ChatOpenAI(
    model="gpt-4.1",
)

# async main
async def main():
    agent = Agent(
        task="Search Google for the top 3 AI research papers in 2025 and return only their titles and links.",
        llm=llm,
        browser_session=browser_session,
        controller=controller
    )
    result = await agent.run()
    print(result.final_result())
    data = result.final_result()
    parsed: Post = Post.model_validate_json(data)
    await browser_session.close()

# Run it
asyncio.run(main())
