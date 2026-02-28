# 📈 Indian Stock Market Swing Trading Agent

A production-ready, multi-agent artificial intelligence system designed to automate the screening, fundamental analysis, and risk management of Indian mid-cap and small-cap equities. 

This project is built using **LangGraph** for deterministic agent orchestration and is designed to identify high-probability swing trade setups based on Mark Minervini's trend templates.

## 🏗️ Architecture & Tech Stack

* **Orchestration:** LangGraph (Hierarchical Supervisor Pattern)
* **LLM Engine:** Gemini 1.5 Pro (via LangChain)
* **Data Ingestion:** `yfinance`, custom Chartink parsers
* **Infrastructure:** Containerized via Docker, orchestrated with Kubernetes, and provisioned on AWS using Terraform.
* **State Management:** SQLite / Python `TypedDict`

## 🤖 The Agent Syndicate

1. **Supervisor Node:** Manages the LangGraph state machine and routes tickers based on worker agent outputs.
2. **Technical Analyst Agent:** Executes Python tools to calculate Moving Averages (50, 150, 200 SMA) and 52-week highs to validate structural setups.
3. **Fundamental Analyst Agent:** Evaluates quarterly EPS and sales growth data.
4. **Risk Management Agent:** Calculates Average True Range (ATR) to establish stop-loss levels and strict 1% account risk position sizing.

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* AWS CLI configured (for infrastructure deployment)
* Terraform installed 
