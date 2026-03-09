# 💰 AI Personal Finance Advisor

<div align="center">

![Banner](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,24&height=200&section=header&text=AI%20Finance%20Advisor&fontSize=48&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Smart%20Spending%20Analysis%20%7C%20Powered%20by%20Gemini%20AI&descAlignY=55&descSize=16)

<p>
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gemini%20AI-Free%20API-4285F4?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/Plotly-Interactive%20Charts-3D4DB7?style=for-the-badge&logo=plotly&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/No%20Data%20Stored-100%25%20Private-brightgreen?style=for-the-badge&logo=lock"/>
</p>

<p>
  <b>Upload any bank/UPI statement CSV → Get instant AI-powered spending insights, beautiful charts, and personalised money-saving advice.</b><br/>
  Works with all Indian banks, Google Pay, PhonePe, Paytm, and any expense CSV.
</p>

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [How It Works](#-how-it-works) • [Supported Formats](#-supported-csv-formats) • [FAQ](#-faq)

</div>

---

## 🌟 Why This Project?

Managing personal finances is hard. Most people don't know where their money actually goes every month. This tool changes that:

- 📊 **Instant visual breakdown** of every rupee you spend
- 🤖 **AI advice** tailored to YOUR actual spending data — not generic tips
- 🔒 **100% private** — your data never leaves your machine
- ⚡ **Works in 2 minutes** — just upload your CSV, no account needed
- 🆓 **Free to use** — uses Google's free Gemini API (no credit card)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 **Smart CSV Parser** | Auto-detects Date, Description, Amount columns from any bank export |
| 🏷️ **Auto Categorization** | Automatically sorts 30+ transactions into 10 categories (Food, Transport, Shopping, etc.) |
| 📊 **Interactive Charts** | Pie chart, daily trend line, and horizontal bar chart — all zoomable and interactive |
| 🤖 **Gemini AI Advisor** | Sends your spending summary to Google Gemini for personalised financial advice |
| 💡 **Instant Insights** | Rule-based alerts fire without any API key — overspending warnings, subscription checks |
| 📐 **50/30/20 Planner** | Enter your income and see your ideal budget breakdown with comparison to actual spend |
| 🧾 **Transaction Table** | Filterable table of all transactions with category labels |
| 📥 **Sample Data** | Built-in sample dataset to explore the app immediately |
| 🔒 **Privacy First** | All CSV processing is done locally — no data is ever uploaded to any server |

---

## 🖥️ Demo

> Upload your CSV or click **"Load Sample Data"** in the sidebar to see this instantly:

```
╔══════════════════════════════════════════════════════════════════╗
║  💰 AI Finance Advisor                                           ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ ║
║  │  ₹38,716    │ │     30      │ │   ₹1,290    │ │ Shopping  │ ║
║  │ Total Spent │ │Transactions │ │  Avg/Day    │ │Top Cat    │ ║
║  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ ║
║                                                                  ║
║  🥧 Category Pie          📈 Daily Spending Trend               ║
║  ┌────────────────┐       ┌──────────────────────────────────┐  ║
║  │  Food 28%      │       │  ▂▃█▂▁▃▅▂▁▂▃▄▂▁▂▃▄▃▁▂▃▄▅▂▁▂▃▄▂  │  ║
║  │  Shopping 22%  │       │  ─────── 7-day avg ───────────── │  ║
║  │  Travel 18%... │       └──────────────────────────────────┘  ║
║  └────────────────┘                                             ║
║                                                                  ║
║  🤖 AI Advice: "Your food delivery spend is 28% of total..."    ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 📦 Installation

### Prerequisites
- Python 3.9+ → [Download here](https://www.python.org/downloads/)
- A free Google Gemini API key → [Get one here](https://aistudio.google.com) *(no credit card needed)*

---

### Step 1 — Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-finance-advisor.git
cd ai-finance-advisor
```

### Step 2 — Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the app
```bash
streamlit run app.py
```

The app opens automatically at **http://localhost:8501** 🎉

---

## 🚀 One-Click Deploy (Share with anyone)

Deploy for free on **Streamlit Community Cloud**:

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Click **Deploy** — your app is live with a public URL!

---

## 📂 Supported CSV Formats

The app auto-detects columns. Your CSV just needs three things:

| Column Type | Accepted Names |
|---|---|
| **Date** | `date`, `time`, `day`, `transaction date` |
| **Description** | `description`, `narration`, `details`, `particulars`, `merchant`, `remarks` |
| **Amount** | `amount`, `debit`, `credit`, `amt`, `value`, `withdrawal` |

### Works with exports from:
- 🏦 **Banks** — SBI, HDFC, ICICI, Axis, Kotak, PNB, BOB, Canara
- 📱 **UPI Apps** — Google Pay, PhonePe, Paytm, BHIM
- 💳 **Cards** — Any credit/debit card statement CSV
- 📊 **Expense Apps** — Walnut, Money Manager, YNAB CSV exports
- 🌍 **International** — Works with USD, EUR, GBP too (auto-parses symbols)

> **Tip:** Use the included `sample_transactions.csv` to test the app first.

---

## 🧠 How It Works

```
┌───────────────┐
│  Upload CSV   │
└──────┬────────┘
       │
       ▼
┌───────────────────────────────────────────────────────────┐
│  Column Auto-Detection  (date / description / amount)     │
└──────┬────────────────────────────────────────────────────┘
       │
       ▼
┌───────────────────────────────────────────────────────────┐
│  Auto-Categorization Engine                               │
│  Keyword matching → 10 categories (Food, Transport, etc.) │
└──────┬────────────────────────────────────────────────────┘
       │
       ├──────────────────────────────────────────┐
       ▼                                          ▼
┌──────────────────────┐              ┌───────────────────────────┐
│  Plotly Charts       │              │  Gemini AI (optional)     │
│  - Pie chart         │              │  Sends category summary   │
│  - Daily trend       │              │  Gets personalised advice │
│  - Category bars     │              │  back as formatted text   │
└──────────────────────┘              └───────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│  Rule-Based Insights  (no API needed)                    │
│  + 50/30/20 Budget Planner with income comparison        │
└──────────────────────────────────────────────────────────┘
```

### Category auto-detection covers:
`Food & Dining` · `Transport` · `Shopping` · `Entertainment` · `Health` · `Utilities` · `Groceries` · `Education` · `Travel` · `Transfers`

---

## 📁 Project Structure

```
ai-finance-advisor/
│
├── app.py                    # 🧠 Main Streamlit application
├── requirements.txt          # 📦 Python dependencies
├── sample_transactions.csv   # 📥 Sample data to test with
├── .gitignore                # 🚫 Excluded files
├── LICENSE                   # 📄 MIT License
└── README.md                 # 📖 You are here
```

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| [Python](https://python.org) | 3.9+ | Core language |
| [Streamlit](https://streamlit.io) | 1.35 | Web UI framework |
| [Pandas](https://pandas.pydata.org) | 2.2 | CSV parsing & data manipulation |
| [Plotly](https://plotly.com) | 5.22 | Interactive charts |
| [Google Gemini AI](https://aistudio.google.com) | 1.5 Flash | AI financial advice (free tier) |

---

## 🤔 FAQ

**Q: Is my financial data safe?**
> Yes. All CSV processing happens locally on your machine using Pandas. Your raw transaction data is never sent anywhere. Only a *category summary* (not individual transactions) is sent to Gemini if you choose to use the AI advice feature.

**Q: Do I need a Gemini API key?**
> No! The charts, category breakdown, quick insights, and 50/30/20 planner all work without any API key. The key is only needed for the AI advice section.

**Q: Is the Gemini API free?**
> Yes. Google's Gemini 1.5 Flash model has a generous free tier (15 requests/minute, 1 million tokens/day). Get your key at [aistudio.google.com](https://aistudio.google.com) — no credit card required.

**Q: My columns weren't auto-detected. What do I do?**
> The app will show manual dropdowns to map your columns. Just select the right ones and it'll work.

**Q: Can I use this with non-Indian currency?**
> Yes! The amount parser strips ₹, $, €, £ symbols automatically. The AI advice defaults to Indian Rupee context — you can modify the prompt in `app.py` if needed.

**Q: Can I deploy this online?**
> Yes! Deploy free on [Streamlit Community Cloud](https://share.streamlit.io). Add your Gemini key as a Secret in the deployment settings.

---

## 🗺️ Roadmap

- [ ] 📤 Export full report as PDF
- [ ] 📅 Month-over-month comparison view
- [ ] 🎯 Set spending goals per category with alerts
- [ ] 📈 Investment tracker integration (mutual funds, stocks)
- [ ] 🌐 Multi-currency support with live conversion
- [ ] 🏦 Direct bank API integration (Account Aggregator framework)
- [ ] 🤝 Split expenses with friends (like Splitwise)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'feat: add your feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — free to use, modify, and distribute. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io) — for making Python web apps effortless
- [Google Gemini](https://aistudio.google.com) — for the free, powerful AI API
- [Plotly](https://plotly.com) — for beautiful interactive charts

---

<div align="center">

**⭐ Found this useful? Star the repo — it really helps!**

Made with ❤️ and Python

![Footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,24&height=100&section=footer)

</div>
