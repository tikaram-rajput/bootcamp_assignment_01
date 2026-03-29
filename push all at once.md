# -------- SET USER (FIRST TIME ONLY) --------
git config --global user.name "tikaram-rajput"
git config --global user.email "tikaramsinghrajput@gmail.com"

# -------- INITIALIZE REPO --------
git init

# -------- ADD REMOTE (CHANGE IF NEEDED) --------
git remote add origin https://github.com/tikaram-rajput/multimodal-rag-engine-system.git

# -------- REMOVE UNWANTED FILES (SAFE) --------
git rm -r --cached venv
git rm -r --cached __pycache__

# -------- ADD FILES --------
git add .

# -------- COMMIT --------
git commit -m "Initial commit: clean project setup with RAG system code"

# -------- SET MAIN BRANCH --------
git branch -M main

# -------- PUSH --------
git push -u origin main