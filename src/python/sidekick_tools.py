from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model='llama3.2') # YOUR MODEL HERE can be llama2 or llama3.2...

# Without bind.
chain = (
    llm
    | StrOutputParser()
)

print(chain.invoke("Repeat quoted words exactly: 'One two three four five.'"))
# Output is 'One two three four five.'

# With bind.
chain = (
    llm.bind(stop=["three"])
    | StrOutputParser()
)

print(chain.invoke("Repeat quoted words exactly: 'One two three four five.'"))
# Output is 'One two'
