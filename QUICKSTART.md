# Konflux Chatbot MCP - Quick Start Guide

Get the Konflux chatbot working in Cursor in 5 minutes!

## Prerequisites

- Python 3.10+
- Cursor editor
- Network access to the chatbot (Red Hat VPN if using internal services)

## Step 1: Install Dependencies

```bash
cd mcp-server
pip install -r requirements.txt
```

## Step 2: Test the Connection

```bash
python test_local.py
```

This will test:
- ✅ Playground accessibility
- ✅ Chat /invoke endpoint
- ✅ Streaming /stream endpoint

If all tests pass, you're ready to configure Cursor!

## Step 3: Configure Cursor

Add this to your Cursor MCP settings:

**Mac/Linux:** `~/.cursor/mcp_config.json` or Cursor Settings → MCP Servers

```json
{
  "mcpServers": {
    "konflux-chatbot": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/chatbot-instances/mcp-server/server.py"]
    }
  }
}
```

**Replace `/ABSOLUTE/PATH/TO/`** with your actual path!

### Finding Your Absolute Path

```bash
cd /path/to/chatbot-instances/mcp-server
pwd
# Copy the output and use it in the config above
```

## Step 4: Restart Cursor

Close and reopen Cursor to load the MCP server.

## Step 5: Test in Cursor

Try these prompts in Cursor:

```
Use the konflux_chat tool to ask: What is Konflux?
```

```
Query Konflux chatbot: How do I troubleshoot a failed pipeline?
```

```
Ask Konflux about: What are the best practices for container builds?
```

## Success! 🎉

You should now see responses from the Konflux AI assistant directly in Cursor.

## Troubleshooting

### "Command not found" or Python errors

Use the full path to Python:

```json
{
  "mcpServers": {
    "konflux-chatbot": {
      "command": "/usr/bin/python3",
      "args": ["/ABSOLUTE/PATH/TO/mcp-server/server.py"]
    }
  }
}
```

Find your Python path with: `which python3`

### "Connection refused" errors

1. Test the chatbot directly: `python test_local.py`
2. Check VPN connection if using internal services
3. Verify the URL in `env.example` is correct

### Cursor doesn't see the tool

1. Check Cursor's MCP server logs (Settings → MCP Servers → View Logs)
2. Ensure you used **absolute paths** (not `~/` or `./`)
3. Restart Cursor completely
4. Try running the server manually first to see errors:
   ```bash
   python server.py
   ```

### Still having issues?

Run the test script for detailed diagnostics:

```bash
python test_local.py
```

Check the full README.md for more troubleshooting steps.

## Advanced: Using with Virtual Environment

If you're using a venv:

```bash
cd mcp-server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Then in Cursor config, use the venv Python:

```json
{
  "mcpServers": {
    "konflux-chatbot": {
      "command": "/ABSOLUTE/PATH/TO/mcp-server/venv/bin/python",
      "args": ["/ABSOLUTE/PATH/TO/mcp-server/server.py"]
    }
  }
}
```

## What You Get

The chatbot provides structured responses:

```
Diagnostic Assessment:
[Analysis of your question/issue]

Solution:
[Step-by-step solution or detailed answer]

Notes:
[Important warnings or next steps]

Confidence Level: [High/Medium/Low]
[Why the assistant has this confidence level]
```

## Available Tools

- **konflux_chat**: Standard chat (best for most questions)
- **konflux_chat_stream**: Streaming responses (for longer answers)

Both support:
- `question` (required): Your question
- `urgency`: low/medium/high
- `tenant`: Your project name
- `details`: Additional context

## Next Steps

- Read the full [README.md](README.md) for more details
- Check out example queries in the README
- Learn about deployment options for team use

Happy chatting with Konflux! 🚀

