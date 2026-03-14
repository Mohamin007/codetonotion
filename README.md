# CodeToNotion 🚀

> Turn your VS Code comments into organized Notion notes — automatically.
> Made by Mohamin Mushtaq (FYIMP Data Science and AI)

## The Problem
As a developer, your knowledge is scattered everywhere. You write comments inside your code files explaining what you learned, how something works, why you made a decision. But those comments are buried inside hundreds of lines of code. You can't easily find them, you can't read them on your phone, and you can't share them with anyone.

## The Solution
CodeToNotion automatically extracts your comments from VS Code files, refines them into clean study notes using AI, and organizes them in Notion. Mirroring your exact folder structure.

Write code normally. Add comments as you always do. Run one command. Your knowledge is now in Notion. Organized, beautiful, accessible anywhere.

## How It Works
1. You write Python code with comments in VS Code
2. When done, run one command
3. CodeToNotion extracts all comments (hashtag, inline, and docstrings)
4. Groq AI refines them into proper study notes
5. Notes appear in Notion. Organized by folder and file

## Features
- ✅ Syncs single file or entire folder at once
- ✅ Reads all comment types: `#hashtag`, `inline #comments`, and `"""docstrings"""`
- ✅ AI-powered note refinement using Groq (llama-3.3-70b)
- ✅ Mirrors your VS Code folder structure in Notion automatically
- ✅ Private file protection: add `# PRIVATE - DO NOT SYNC` to skip any file
- ✅ Beautiful Notion formatting: headers, bullet points, sections
- ✅ Built on Notion MCP + Notion API

## Tech Stack
- Python
- Notion MCP (Claude Desktop Integration)
- Notion API
- Groq API (llama-3.3-70b-versatile)
- notion-client
- python-dotenv
- watchdog

## Setup

### 1. Clone the repository
```
git clone https://github.com/Mohamin007/codetonotion
cd codetonotion
```

### 2. Install dependencies
```
pip install notion-client groq python-dotenv watchdog
```

### 3. Set up environment variables
Copy `.env.example` to `.env` and fill in your credentials:
```
NOTION_TOKEN=your_notion_integration_token
NOTION_ROOT_PAGE_ID=your_notion_page_id
GROQ_API_KEY=your_groq_api_key
```

### 4. Get your credentials
- **Notion Token** → notion.com/my-integrations → Create integration → Copy token
- **Notion Page ID** → Open your Notion page → Copy link → ID is the long string at the end
- **Groq API Key** → console.groq.com → Create API key → Copy it

### 5. Connect Notion integration to your pages
In Notion → open your root page → three dots → Connections → select your integration

### 6. Run
```
python codetonotion.py
```

## Usage
When prompted, choose:
- **Option 1** - sync a single file
- **Option 2** - sync an entire folder

### Example
Your VS Code:
```
📁 conditionals/
   📄 forloop.py  (with comments inside)
   📄 ifelse.py   (with comments inside)
```

After running CodeToNotion, your Notion:
```
📁 conditionals/
   📄 For Loop  (organized study notes)
   📄 If Else   (organized study notes)
```

## Privacy
Any file with `# PRIVATE - DO NOT SYNC` as the first line will be completely skipped, never sent to AI or Notion.

## Notion MCP Integration
CodeToNotion uses TWO powerful integrations:

### 1. Notion API (Automated Sync)
The Python script connects directly to Notion API to automatically create and organize pages.

### 2. Notion MCP (Claude Desktop)
Claude Desktop is connected to your Notion workspace via MCP protocol. This means Claude can intelligently READ and INTERACT with your synced notes!

**Setup Claude Desktop + Notion MCP:**
1. Install Claude Desktop
2. Go to Settings → Developer → Edit Config
3. Add this to your config:
```json
{
  "mcpServers": {
    "notionApi": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "OPENAPI_MCP_HEADERS": "{\"Authorization\": \"Bearer YOUR_NOTION_TOKEN\", \"Notion-Version\": \"2022-06-28\"}"
      }
    }
  }
}
```
4. Restart Claude Desktop
5. Connect your Notion pages to the integration

**Now ask Claude Desktop things like:**
- "Summarize what I learned about for loops today"
- "What are all the concepts I studied this week?"
- "Explain the notes I wrote about functions"
- "Create a revision plan based on my Notion notes"

Claude will read your actual Notion pages and respond intelligently — making your notes truly interactive! 🔥

**The Complete Workflow:**
```
Write Code in VS Code
        ↓
Add Comments while learning
        ↓
Run CodeToNotion
        ↓
Notes organized in Notion automatically
        ↓
Ask Claude Desktop to summarize, quiz you, or create revision plans!
```
## Built By
**Mohamin Mir**
19 year old developer from Kashmir, India
FYIMP Data Science & AI, University of Kashmir

[![GitHub](https://img.shields.io/badge/GitHub-Mohamin007-black?style=flat&logo=github)](https://github.com/Mohamin007)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-moham7n-blue?style=flat&logo=linkedin)](https://linkedin.com/in/moham7n)

---
*Built for MLH Global Hack Week - Cloud Week 2026* 🔥
