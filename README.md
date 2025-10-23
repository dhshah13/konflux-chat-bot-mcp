# Konflux Chatbot MCP Server

Ask Konflux questions directly in Cursor using the Konflux AI chatbot.

## Setup

### Option A: Direct Python (Recommended)

```bash
# 1. Clone and install
git clone <this-repo-url>
cd konflux-chatbot-mcp
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Get your path
pwd

# 3. Add to ~/.cursor/mcp.json (replace YOUR_PATH with output from pwd)
{
  "mcpServers": {
    "konflux-chatbot": {
      "command": "python3",
      "args": ["YOUR_PATH/server.py"]
    }
  }
}

# 4. Restart Cursor
```

### Option B: Podman/Docker

```bash
# 1. Clone and build
git clone <this-repo-url>
cd konflux-chatbot-mcp
podman build -t konflux-chatbot-mcp:latest .

# 2. Add to ~/.cursor/mcp.json
{
  "mcpServers": {
    "konflux-chatbot": {
      "command": "podman",
      "args": ["run", "-i", "--rm", "konflux-chatbot-mcp:latest"]
    }
  }
}

# 3. Restart Cursor
```

## Usage

Just ask Konflux questions naturally:

- "What is Konflux?"
- "Why is my pipeline failing?"
- "How do I configure hermetic builds?"

### Structured Questions

For better answers, use this format:

```
Application: my-app
Component: my-component
Question: Why is my build failing on ppc64le?
Details: [paste your error logs here]
```

All fields except `Question` are optional.

## What You Get

**Chatbot Response:**
- Diagnostic Assessment
- Solution steps
- Confidence Level (High/Medium/Low)

**Plus Additional Analysis from Cursor** when confidence is medium/low

## Troubleshooting

**Server not working?**
- Check absolute paths in `mcp.json`
- Restart Cursor after config changes
- For Python: make sure venv is created
- For Podman: make sure image is built

**Getting generic answers?**
- Provide more details in your question
- Share specific error logs, files, or URLs
- If you can't access resources, ask in **#konflux-users** Slack

## Files

- `server.py` - MCP server
- `.cursorrules` - Auto-routing for Konflux questions
- `Containerfile` - For Podman/Docker deployment
- `cursor_config_example.json` - Python setup example
- `cursor_config_podman_example.json` - Podman setup example

See `QUICKSTART.md` for detailed documentation.
