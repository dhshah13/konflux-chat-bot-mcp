# Konflux Chatbot MCP Server

Connect to the Konflux AI chatbot directly from Cursor using the Model Context Protocol (MCP).

## What You Get

- 🤖 Ask Konflux questions directly in Cursor
- 🔄 Automatic intelligent routing for Konflux-related questions
- 📋 Structured responses with confidence levels
- 🎯 Support for tenant, application, and component context

## Quick Setup (5 Minutes)

Choose your preferred setup method:

### Option A: Direct Python (Recommended for Quick Start)

**Step 1: Clone This Repository**

```bash
git clone <this-repo-url>
cd konflux-chatbot-mcp
```

**Step 2: Install Python Dependencies**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Step 3: Configure Cursor**

Get your current directory path:
```bash
pwd
```

Copy the example configuration:
```bash
cat cursor_config_example.json
```

Add this to your Cursor settings (`~/.cursor/mcp.json`), replacing `/YOUR/CLONE/PATH/` with your path from `pwd`.

**Example:** If `pwd` shows `/Users/jane/konflux-chatbot-mcp`, use:
```json
"args": ["/Users/jane/konflux-chatbot-mcp/server.py"]
```

**Note:** The chatbot URL is already configured with the default production endpoint. No additional configuration needed!

**Step 4: Restart Cursor**

Restart Cursor to load the MCP server.

---

### Option B: Using Podman/Docker (Containerized)

**Step 1: Clone This Repository**

```bash
git clone <this-repo-url>
cd konflux-chatbot-mcp
```

**Step 2: Build the Container Image**

```bash
podman build -t konflux-chatbot-mcp:latest .
# Or with Docker:
# docker build -t konflux-chatbot-mcp:latest .
```

**Step 3: Configure Cursor**

Copy the example configuration to your Cursor settings:

```bash
# Copy the Podman example to your Cursor settings
cat cursor_config_podman_example.json
```

Then add it to `~/.cursor/mcp.json`.

For Docker, replace `"command": "podman"` with `"command": "docker"`.

**Step 4: Restart Cursor**

Restart Cursor to load the MCP server.

---

### Step 5: Try It!

Just ask any Konflux question in Cursor:
- "What is Konflux?"
- "How do I troubleshoot a failing pipeline?"
- "Why is my component build failing?"

The chatbot will automatically respond!

## How to Ask Questions

You can provide structured information for better answers:

```
Application: my-app
Component: my-component
Question: Why is my build failing?
Details: Error: signature verification failed on ppc64le
```

All fields except `Question` are optional.

## What Happens

When you ask a Konflux question:

1. **Cursor routes it to the chatbot** via this MCP server
2. **Chatbot responds** with structured analysis
3. **Cursor adds extra help** when confidence is medium/low
4. **You continue the conversation** with follow-up questions

## Response Format

You'll get:

- **Diagnostic Assessment**: What's happening
- **Solution**: Step-by-step fix
- **Notes**: Important warnings
- **Confidence Level**: High/Medium/Low

Plus additional analysis from Cursor when helpful.

## Troubleshooting

**Server not connecting?**
- Check the path in `mcp.json` is correct and absolute
- Make sure you're using the venv Python path
- Restart Cursor after config changes

**Getting errors?**
- Verify Python 3.10+ is installed
- Try reinstalling: `pip install --force-reinstall -r requirements.txt`
- Check Cursor's MCP logs (Help → Toggle Developer Tools → Console)

**Questions not routing?**
- Make sure you're asking Konflux-related questions
- The `.cursorrules` file enables auto-routing
- For general coding questions, it responds normally

## Files in This Repo

- `server.py` - The MCP server (handles communication with Konflux chatbot)
- `requirements.txt` - Python dependencies
- `.cursorrules` - Automatic routing configuration for Cursor
- `env.example` - Example environment file
- `cursor_config_example.json` - Example Cursor MCP configuration
- `QUICKSTART.md` - Detailed setup guide

## Get Help

**Can't access resources mentioned in responses?**
- Share your files/logs directly in Cursor chat
- Reach out to **#konflux-users** Slack channel

**Need more info?**
- See `QUICKSTART.md` for detailed documentation
- Check the example files for configuration templates

## Requirements

- Python 3.10+
- Cursor editor
- Network access to Konflux chatbot endpoint

That's it! Happy chatting with Konflux! 🚀
