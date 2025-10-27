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
	base_url="https://api.ai.it.cornell.edu",
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
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the file(s) that has(have) been uploaded"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# if question and uploaded_files:
if uploaded_files:
    documents = []

    for uploaded_file in uploaded_files:

    #load file based on type
        if uploaded_file.name.endswith(".pdf"):
            loader = PyPDFLoader(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            loader = TextLoader(uploaded_file)
        else:
            st.error(f"Unsupported file type: {uploaded_file.name}")
            continue
        
        docs = loader.load()
        documents.extend(docs)

        # Read the content of the uploaded file
        # file_content = uploaded_files.read().decode("utf-8")
        # print(file_content)

        #Chunking the documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)

        # Creating Chroma vector store
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=OpenAIEmbeddings(model="openai.text-embedding-3-small")
        )

        # Retrieve 
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

        if question:
            # Append the user's question to the messages
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)
            
            #Retrieve relevant documents based on the question
            relevant_docs = retriever.get_relevant_documents(question)
            file_content = "\n\n".join([doc.page_content for doc in relevant_docs])

            

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model="gpt-4o",  # Change this to a valid model name
                    messages=[
                        {"role": "system", "content": f"Here's the content of the file:\n\n{file_content}"},
                        *st.session_state.messages
                    ],
                    stream=True
                )
                response = st.write_stream(stream)

            # Append the assistant's response to the messages
            st.session_state.messages.append({"role": "assistant", "content": response})