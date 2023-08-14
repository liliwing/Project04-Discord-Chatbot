import discord
import dotenv
import os
from langchain import OpenAI
from langchain.agents import initialize_agent
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.vectorstores import FAISS

dotenv.load_dotenv()
DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")

# Define LLM
llm = OpenAI()
# Define Embedding Model
embeddings = OpenAIEmbeddings()

# Create memory
memory = ConversationBufferWindowMemory(memory_key="chat_history", ai_prefix="AI", k=5)

# Google Search Tool
google_search = GoogleSearchAPIWrapper()
google_search_tool = Tool(
    name="Google Search",
    description="useful for when you need to answer questions about current events.",
    func=google_search.run)

# Document Search Tool
document = PyPDFLoader("hkpc_medical_handbook.pdf").load_and_split()
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len, separator="\n")
features = splitter.split_documents(document)
database = FAISS.from_documents(features, embeddings)
document_search = RetrievalQA.from_chain_type(llm=llm, retriever=database.as_retriever())
document_search_tool = Tool(
    name="Document Search",
    description="useful for when you need to get more details about HKPC medical benefit scheme. Input should be a fully formed question.",
    func=document_search.run)

# Create Agent
agent = initialize_agent(
    agent="conversational-react-description",
    llm=llm,
    tools=[google_search_tool, document_search_tool],
    memory=memory,
    verbose=True)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(1140504366785237083)
    await channel.send("Hello! My name is Botbot, your personal AI assistant. Ask me anything.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response = agent.run(input=message.content)
    await message.channel.send(response)

client.run(DISCORD_API_TOKEN)
