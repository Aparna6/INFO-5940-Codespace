# INFO 5940 Assignment 1 🧠
Welcome to Aparna's Q&A RAG Application! 

This application allows you to upload one or more files (.pdf or .txt) and ask questions about the content within. It is a streamlit application which implements a **Retrieval-Augmented Generation (RAG)** pipeline using **LangChain**, **Chroma**, and **OpenAI GPT-4o**.

## ⚙️ Environment Setup

The app runs directly in the **provided Codespace** setup — no changes required. Use the command **"API_KEY="YOUR-API-KEY" streamlit run chat_with_pdf.py** in your terminal to run the application.

In case of an authentication error, add your API Key to devcontainer.json, and rebuild container before running the application again.

### 1. Dependencies
All dependencies are installed through `requirements.txt` and `.devcontainer/setup.sh`.  

### 2. Change made to original configuration
Version of pandas changed from "pandas==2" to "pandas" in `requirements.txt` due to a conflict at runtime.

## 🚀 Features
- User can upload multiple `.txt` and `.pdf` files  
- Automatic text extraction from diverse file types
- Automatic chunking using LangChain's 'RecursiveCharacterTextSplitter'
- Vector embedding and document retrieval using Chroma vector database  
- Accurate answers using retrieved context from uploaded files only
- Conversational interface with user-friendly UI 

## General steps to Fork the repository and run the code in your Codespace

### Step 1: Fork this repository 
1. Click the **Fork** button (top right of this page).
2. This will create a copy of the repo under **your own GitHub account**.

### Step 2: Open your forked repo Codespace
1. Go to **your forked repo**.
2. Click the green **Code** button and switch to the **Codespaces** tab.  
3. Select **Create Codespace**.
4. Wait a few minutes for the environment to finish setting up.

### Step 3: Verify your environment 
Once the Codespace is ready: 
1. If you are in `langgraph_chroma_retreiver.ipynb` in your codespace.
2. Install the Python 3.11.13 Kernel.  In the top-right corner, click **Select Kernel**.
    1. If **Install/Enable suggested extensions Python + Jupyter** appears, select it, and wait for the install to finish before moving on to the next step.
    2. Select **Python Environments** choose **Python 3.11.13 (first option)**.
3. Run the code block to check your setup. 

---

<p align="center">🌸 Made with ❤️ by Aparna 🌸</p>