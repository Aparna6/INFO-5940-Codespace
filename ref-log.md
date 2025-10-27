### 🧾 **`ref-log.md`**

```markdown
# 📘 Reference Log

### 🧩 Purpose
This document lists all external sources and tools used in the implementation of assignment 1.

## 📚 References & Resources

| Source | Type | Description / Use |
|---------|------|-------------------|
| LangChain Documentation ([https://python.langchain.com](https://python.langchain.com)) | Used for document loaders, text splitters, and Chroma retriever examples alongwith `langgraph_chroma_retreiver.ipynb` 


## 🤖 GenAI Assistance

| Tool | Purpose | Rationale |
|------|----------|-----------|
| ChatGPT (GPT-5) | Helped refine code to save file into a temporary location | Used to resolve errors encountered in trying to save the file in a temporary location and pass its file_path to the loader |
| GitHub Agent(GPT-5 mini) | Helped understand code and which library to use for .pdf files | Used to look up PyPDFLoader and its example use in `langgraph_chroma_retreiver.ipynb` |
| ChatGPT (GPT-5) | Used to get a draft structure for README.md and ref-log.md for formatting | Used for formatting reference in alignment with the requirements of these documents |

## 🧱 Development Notes
- AI assistance was used for guidance, troubleshooting and documentation clarity.  
- All the code was written, reviewed and tested by the developer.
- Any reference code was reviewed, understood, and tested by the developer (from template or corrections suggested by Gen AI for troubleshooting).
- No external materials were incorporated.  
- No modifications made to `.devcontainer` or `setup.sh`.  
- Tested with both `.txt` and `.pdf` files under Codespace environment.  
