# 🚀 Moonshot Opportunities

Research project for discovering and analyzing high-potential AI opportunities.

## What It Does

**Moonshot Opportunities** is a research tool that scans multiple sources to find the most promising AI projects, technologies, and trends. It aggregates data from:

- **GitHub Trending** - Hottest AI/ML repositories
- **Hacker News** - Top AI discussions and stories

The tool scores each opportunity based on community engagement (stars, points) to surface the highest-potential moonshot ideas.

## Installation

```bash
# Clone the repository
git clone https://github.com/aamsilva/moonshot-opportunities.git
cd moonshot-opportunities

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run the research report

```bash
python research.py
```

This will:
1. Fetch trending AI repositories from GitHub
2. Fetch top AI stories from Hacker News
3. Score each opportunity based on engagement
4. Print a ranked report
5. Save results to `moonshot_report.json`

### Sample Output

```
============================================================
🚀 MOONSHOT OPPORTUNITIES REPORT
============================================================
Generated: 2026-03-26T12:02:00

📊 TOP OPPORTUNITIES:
------------------------------------------------------------

1. anthropic/claude-code
   Score: ⭐⭐⭐ (3/6)
   Stars/Points: 1542
   URL: https://github.com/anthropic/claude-code
   Description: Claude Code - AI coding assistant...

2. openai/gpt-5-leaks
   Score: ⭐⭐ (2/6)
   Stars/Points: 892
   ...
```

## Project Structure

```
moonshot-opportunities/
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── research.py         # Main research tool
└── moonshot_report.json # Generated report (after running)
```

## Requirements

- Python 3.8+
- requests
- pandas

## API Rate Limits

This tool uses public APIs:
- GitHub: 60 requests/hour (unauthenticated)
- Hacker News: No rate limit

For higher limits, add a GitHub token:

```python
# In research.py, add your token:
self.session.headers["Authorization"] = f"token YOUR_GITHUB_TOKEN"
```

## License

MIT License

---

Built with 🔥 by Augusto