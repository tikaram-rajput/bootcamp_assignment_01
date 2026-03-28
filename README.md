# bootcamp_assignment_01
## Multimodal RAG System with FastAPI

### Course: Multimodal Retrieval-Augmented Generation Bootcamp

#  Problem Statement

## 1. Domain Identification  
This project is based on the domain of **automotive engineering**, focusing on **engine design, diagnostics, and service engineering**. Engineers and technicians rely on workshop manuals (such as Hino engine manuals) to understand engine systems, perform troubleshooting, and carry out maintenance. These manuals include a combination of text, tables, and engineering diagrams.

---

## 2. Problem Description  
Extracting useful information from these manuals is difficult and time-consuming. The documents are large and contain detailed technical content such as torque specifications, fault codes, and subsystem explanations.

Engineers often need quick answers like:
- What is the torque value for a component?  
- What are the causes of a fault code?  
- How does a system like fuel injection work?  

Traditional keyword search is not effective because it does not understand the meaning of queries. It also cannot properly interpret tables or diagrams. As a result, users must manually search through multiple pages, which is inefficient and error-prone.

---

## 3. Why This Problem Is Unique  
Automotive manuals have domain-specific challenges:
- Use of specialised technical terms  
- Important data stored in structured tables  
- Engineering diagrams that explain system behavior  
- Information spread across different sections  

A complete answer often requires combining text, tables, and diagrams. This makes the problem more complex than a general document question-answering task.

---

## 4. Why RAG Is the Right Approach  
Retrieval-Augmented Generation (RAG) is suitable for this problem because it retrieves relevant information directly from documents at query time.

Key advantages:
- Provides answers based on actual documents  
- Reduces incorrect or hallucinated responses  
- Works with semantic search (understands meaning)  
- No need for retraining when adding new data  

A multimodal RAG system can also handle text, tables, and images together, allowing better and more complete answers compared to traditional methods.

---

## 5. Expected Outcomes  
The system will enable users to:
- Ask technical questions about engine systems  
- Retrieve values from tables like torque specifications  
- Understand information from diagrams  
- Get answers with proper source references  

This will reduce time spent on manual searching and improve accuracy in diagnostics and maintenance tasks. The goal is to make complex workshop manuals easy to use through a simple question-answer interface.
