
## 🧠 LLM-Powered E-commerce Product Search

[▶️ Watch Demo on YouTube](https://youtu.be/YRdhz58UdcU?si=h8fdZUOjXqG_3KjI)

> Natural Language → SQL → PostgreSQL → Results


---

### 🔍 Overview

This project enables users to **search for mobile phones and laptops using natural language**, powered by an **LLM (Gemini or LLaMA3 via Ollama)**. The system converts the query into **secure SQL**, executes it on a **PostgreSQL** database, and displays results via a **Streamlit UI**.

---

### 📌 Features

* ✨ LLM-based SQL generation (`SELECT` only)
* 🛒 Product search: mobiles & laptops
* 🔐 Safe query validation & execution
* 🧱 Modular architecture (LLM, DB API, UI)
* 🗃️ PostgreSQL backend with real product data
* 🔁 Switchable LLM backend (Gemini / Ollama)

---

### 🧱 Architecture

```bash
User 🔁 Streamlit UI 
        │
        ▼
Prompt 🔁 LLM Service (FastAPI)
        │
        ▼
     SQL Query 🔁 DB Service (Express + pg)
        │
        ▼
   Result Table 📦 PostgreSQL
```

---

### ⚙️ Tech Stack

| Layer          | Technology                   |
| -------------- | ---------------------------- |
| 🧠 LLM         | Gemini API / Ollama (LLaMA3) |
| 🧮 DB Engine   | PostgreSQL                   |
| 🧪 Query API   | Node.js + Express.js + `pg`  |
| ⚡ LLM Backend  | Python + FastAPI + LangChain |
| 🌐 UI Frontend | Python + Streamlit           |

---

### 📁 Folder Structure

```bash
project-root/
│
├── llm-service/           # Natural language → SQL
│   ├── main.py
│   ├── llm/sql_query_generator.py
│   ├── api/generate_sql.py
│   └── .env
│
├── server/                # PostgreSQL query runner
│   ├── index.js
│   ├── routes/runSql.js
│   ├── db/pool.js
│   └── utils/validateSql.js
│
├── llm-ui/                # Streamlit frontend
│   ├── main.py
│   ├── api/query_llm.py
│   ├── api/run_query.py
│   └── .env
│
├── .gitignore
└── README.md
```

---

### 🚀 Getting Started

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/llm-ecommerce-search.git
cd llm-ecommerce-search
```

---

#### 2. Setup `.env` Files

> **llm-service/.env**

```env
LLM_PORT=4001
GEMINI_API_KEY="your-gemini-or-ollama-key"
```

> **server/.env**

```env
PORT=4000
PGHOST=localhost
PGUSER=postgres
PGPASSWORD=yourpassword
PGDATABASE=yourdb
PGPORT=5432
```

> **llm-ui/.env**

```env
LLM_API_URL=http://localhost:4001/generate-sql
DB_API_URL=http://localhost:4000/run-sql
```

---

#### 3. Install Dependencies

```bash
# LLM Backend
cd llm-service
pip install -r requirements.txt

# DB Service
cd ../server
npm install

# Frontend
cd ../llm-ui
pip install -r requirements.txt
```

---

#### 4. Run All Services

```bash
# LLM Service
cd llm-service
uvicorn main:app --reload --port 4001

# DB Service
cd ../server
node index.js

# Streamlit UI
cd ../llm-ui
streamlit run main.py
```

---

### 💬 Example Query

> *“Show me laptops from HP or Dell under ₹60,000 with at least 16GB RAM”*

🧠 → LLM generates:

```sql
SELECT * FROM laptops 
WHERE brand ILIKE 'HP' OR brand ILIKE 'Dell' 
  AND price < 60000 AND ram >= 16;
```

📦 → Results displayed in a table

---

### 🔒 Security

* ✅ Only **safe SELECT** queries are allowed
* 🚫 `INSERT`, `UPDATE`, `DELETE`, `DROP` are **blocked**
* ✅ Queries validated before execution
* 🔐 Sensitive configs kept in `.env`

---

### 🌟 Future Enhancements

* 🗣️ Voice-based product search
* 🖼️ Image similarity search
* 🎯 Personalized product recommendations
* 🧾 Query history and feedback loop
* 🧠 Context-aware multi-turn chat

---

### 🙌 Author

Made with ❤️ by \[Shubham Kumar]
[GitHub](https://github.com/ShubhamKNIT) | [LinkedIn](https://linkedin.com/in/shubhamknit11)
