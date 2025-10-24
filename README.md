# Konflux Chatbot MCP Server

Ask Konflux questions directly in Cursor using the Konflux AI chatbot.

## Quick Setup (Recommended)

**For end users who just want to use the MCP:**

See **[SIMPLE_SETUP.md](./SIMPLE_SETUP.md)** for zero-installation setup using the hosted container.

**TL;DR:** Add this to `~/.cursor/mcp.json` and restart Cursor:

```json
{
  "mcpServers": {
    "konflux-chatbot": {
      "command": "podman",
      "args": ["run", "-i", "--rm", "quay.io/dhshah/konflux:latest"]
    }
  }
}
```

## Development Setup

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

## Releases

**Current Version:** `1.0.1` (see [CHANGELOG.md](./CHANGELOG.md))

**For Maintainers:** Use the release script to publish new versions:

```bash
# Update version and release
./release.sh 1.0.1

# Or release current VERSION
./release.sh
```

This will:
1. Build the image with version tag and `:latest`
2. Push both tags to quay.io
3. Update the VERSION file

## Files

- `server.py` - MCP server implementation
- `Containerfile` - Container build configuration
- `release.sh` - Release automation script
- `VERSION` - Current version number
- `CHANGELOG.md` - Version history and changes
- `SIMPLE_SETUP.md` - **Quick setup guide for end users (hosted container)**
- `cursor_config_hosted.json` - Podman config using hosted image (recommended)
- `cursor_config_docker.json` - Docker config using hosted image
- `cursor_config_example.json` - Python local development config
- `cursor_config_podman_example.json` - Podman local build config
- `.cursorrules` - Auto-routing for Konflux questions

See `QUICKSTART.md` for detailed documentation.
