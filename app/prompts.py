from langchain_core.prompts import ChatPromptTemplate

FALLBACK_MESSAGE = "I could not find this in the eBook. Please ask another question related to the eBook."     

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers the user question based on the provided context. "     # role + rules 2, 3, 4, 5
    "If the answer is not in the context, reply exactly: "
    + FALLBACK_MESSAGE
    + "\n\nContext:\n{context}"
)

rag_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{question}"),
])