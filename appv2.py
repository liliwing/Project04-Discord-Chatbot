import discord
import dotenv
import os
from langchain import PromptTemplate
from langchain import HuggingFaceHub
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

dotenv.load_dotenv()
DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")

# Define LLM
llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={ "temperature": 0.5, "max_length": 200 })

# Define Prompt Template
template = """The following is a friendly conversation between a human and an AI.
The AI is talkative and provides lots of specific details from its context.
If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{chat_history}
Human: {input}
AI Assistant:"""
prompt = PromptTemplate(template=template, input_variables=["chat_history", "input"])

# Create memory
memory = ConversationBufferMemory(memory_key="chat_history", ai_prefix="AI Assistant")

# Define chain
chain = ConversationChain(prompt=prompt, llm=llm, memory=memory, verbose=True)


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(1139173944386125846)
    await channel.send("Hello! My name is Botbot, your personal AI assistant. Ask me anything.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response = chain.run({ "input": message.content })
    await message.channel.send(response)

client.run(DISCORD_API_TOKEN)
