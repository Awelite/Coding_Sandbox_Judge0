<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=250&section=header&text=Coding%20SandBox&fontSize=60&fontAlignY=35&desc=AI-Powered%20Interview%20Copilot&descAlignY=55&descAlign=50" alt="Coding SandBox Header" />

  <p align="center">
    <strong>Elevate Your Coding Interviews with Real-Time AI Assistance & Seamless Code Execution.</strong>
  </p>

  <p align="center">
    <a href="#features">Features</a> •
    <a href="#tech-stack">Tech Stack</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#project-structure">Project Structure</a> •
    <a href="#contributing">Contributing</a>
  </p>
  
  <p align="center">
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Judge0-000000?style=for-the-badge&logo=codeforces&logoColor=white" alt="Judge0" />
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  </p>
</div>

---

## ✨ Overview

**Coding SandBox (AI Interviewer Copilot)** is a full-stack, dynamic coding playground designed to simulate real-world coding interviews. Combining the power of an intelligent AI copilot with robust code execution via Judge0, it provides a comprehensive environment for practicing algorithms, data structures, and system design.

Whether you're preparing for FAANG interviews or just honing your skills, Coding SandBox offers an immersive, LeetCode-style experience right on your local machine.

## 🚀 Key Features

- **🧠 AI Interviewer Copilot:** Get real-time hints, code reviews, and performance feedback from an integrated AI assistant.
- **⚡ Dynamic Code Execution:** Write, compile, and run code safely in an isolated sandbox powered by Judge0.
- **📚 Rich Problem Library:** Access a database-driven collection of coding problems with server-side filtering.
- **✅ Automated Test Cases:** Instantly evaluate your solutions against public and hidden test cases.
- **📊 Real-time Status Tracking:** Monitor your progress, solved exercises, and performance scores through a stunning dashboard.
- **💅 Premium UI/UX:** Enjoy a sleek, professional, and responsive interface designed for focus and productivity.

## 💻 Tech Stack

- **Frontend:** React, TailwindCSS, Framer Motion (for smooth animations)
- **Backend:** Python, FastAPI, SQLAlchemy (Database ORM)
- **Code Execution Environment:** Judge0 (running on WSL2/Docker)
- **Database:** PostgreSQL / SQLite (Configurable)

## 🛠️ Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Node.js & npm (or yarn)
- Python 3.8+
- Docker & Docker Compose (for Judge0)
- WSL2 (If on Windows)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/coding-sandbox.git
   cd coding-sandbox
   ```

2. **Setup the Backend**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Setup the Frontend**
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

4. **Initialize Judge0 Engine**
   ```bash
   cd ../judge0
   docker-compose up -d
   ```

## 📂 Project Structure

```text
coding-sandbox/
├── backend/          # FastAPI server, AI logic, and API endpoints
├── frontend/         # React application, UI components, and state
├── judge0/           # Configuration and scripts for the Judge0 sandbox
├── .gitignore        # Git ignore rules
└── README.md         # You are here!
```

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <p>Built with ❤️ by Hassi & Contributors</p>
</div>
