import streamlit as st
import os
from openai import OpenAI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_chroma import Chroma
from os import environ

client = OpenAI(
	api_key=os.environ["API_KEY"],
	base_url="https://api.ai.it.cornell.edu/v1",
)

#Connect to LLM
llm = ChatOpenAI(
    model="openai.gpt-4o",
    temperature=0.2,
)

st.title("📝 Aparna's File Q&A with OpenAI")
#change to allow .pdf instead of .md and allow multiple files to be uploaded
uploaded_files = st.file_uploader("Upload one or more files (Allowed formats: .txt or .pdf)", type=("txt", "pdf"), accept_multiple_files=True)

question = st.chat_input(
    "Ask something about the content in the uploaded files",
    disabled=not uploaded_files,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the file(s) uploaded"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# if question and uploaded_files: previous code, ignore

if uploaded_files:
    documents = []

    for uploaded_file in uploaded_files:

        # Save uploaded file to a temporary location
        file_path = os.path.join("temp_" + uploaded_file.name)

        if uploaded_file.name.endswith(".txt"):
            text_content = uploaded_file.read().decode("utf-8")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text_content)

        else:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

    #load file based on type
        if uploaded_file.name.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif uploaded_file.name.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            st.error(f"Unsupported file type: {uploaded_file.name}")
            continue
        
        docs = loader.load()
        documents.extend(docs)

        os.remove(file_path)

        #Read the content of the uploaded file older code
        # file_content = uploaded_files.read().decode("utf-8")
        # print(file_content)

    #Chunking the documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = text_splitter.split_documents(documents)

    # Creating Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(model="openai.text-embedding-3-small")
        )        
    # Retriever based on similarity search 
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    if question:
        # Append the user's question to the messages
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("user").write(question)
        
        #Retrieve relevant documents based on the question
        relevant_docs = retriever.invoke(question)
        file_content = "\n\n".join([doc.page_content for doc in relevant_docs])

        #Define system prompt and get response from OpenAI
        system_prompt = """
        You are an assistant for question-answering tasks. Use only the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
        
        Context:{file_content}
        
        Question: {question}
        
        Answer:
        """

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="openai.gpt-4o",  # Change this to a valid model name
                messages=[
                    {"role": "system", "content": system_prompt.format(file_content=file_content, question=question)},
                    {"role": "user", "content": question}
                ],
                stream=True
            )
            response = st.write_stream(stream)

        # Append the assistant's response to the messages
        st.session_state.messages.append({"role": "assistant", "content": response})

        #pandas==2
     
