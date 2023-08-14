import dotenv
import os
from langchain import PromptTemplate
from langchain import HuggingFaceHub
from langchain import LLMChain

dotenv.load_dotenv()

llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={ "temperature": 0.5, "max_length": 200 })
response = llm.predict("Hello")
print(response)
print("=============================================================================================")


template = """The following is a friendly conversation between a human and an AI.
The AI is talkative and provides lots of specific details from its context.
If the AI does not know the answer to a question, it truthfully says it does not know.

Human: {input}
AI Assistant:"""
prompt = PromptTemplate(template=template, input_variables=["input"])
formatted_prompt = prompt.format(input="Hello")
response = llm.predict(formatted_prompt)
print(response)
print("=============================================================================================")

chain = LLMChain(prompt=prompt, llm=llm, verbose=True)
response = chain.run({ "input": "Hello" })
print(response)
print("=============================================================================================")
