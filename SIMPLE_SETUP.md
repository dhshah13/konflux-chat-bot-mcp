# Konflux Chatbot MCP - Quick Setup

Get Konflux AI assistance directly in Cursor with zero installation!

**Current Version:** 1.0.1 | **Image:** `quay.io/dhshah/konflux:latest`

## Setup (2 Steps)

### 1. Add to Cursor Config

Open/create `~/.cursor/mcp.json` and add:

#### For Podman users:
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

#### For Docker users:
```json
{
  "mcpServers": {
    "konflux-chatbot": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "quay.io/dhshah/konflux:latest"]
    }
  }
}
```

### 2. Restart Cursor

That's it! The container will be automatically pulled on first use.

## Usage

Just ask Konflux questions naturally in Cursor:

- "What is Konflux?"
- "Why is my pipeline failing?"
- "How do I configure hermetic builds?"

### For Better Answers

Include specific details:

```
Application: my-app
Component: backend-service
Question: Why is my ppc64le build failing?
Details: [paste error logs here]
```

## What You Get

**From Konflux AI:**
- Diagnostic Assessment
- Step-by-step Solutions
- Confidence Level (High/Medium/Low)
- Relevant documentation links

**Plus from Cursor:**
- Additional technical analysis when needed
- Suggestions for follow-up actions

## Troubleshooting

**MCP server not showing up?**
- Make sure you restarted Cursor after editing `mcp.json`
- Check that podman/docker is installed: `podman --version` or `docker --version`

**Getting connection errors?**
- Make sure you're on Red Hat VPN (required for internal chatbot access)
- Check if you can access: https://chatbot-deployment-sp-support-chatbot--runtime-int.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com

**Need more help?**
- Join **#konflux-users** on Slack
- Check full docs: [Konflux Documentation](https://konflux.pages.redhat.com/docs/users/)

## Updates

The MCP automatically uses `:latest`, so you'll get updates when:
1. A new version is released
2. You restart Cursor (it checks for updates)

To manually update:

```bash
# Pull latest image
podman pull quay.io/dhshah/konflux:latest
# or
docker pull quay.io/dhshah/konflux:latest

# Restart Cursor
```

**Available versions:** You can also pin to a specific version if needed:
- `quay.io/dhshah/konflux:latest` - Always the newest (recommended)
- `quay.io/dhshah/konflux:v1.0.1` - Latest stable
- `quay.io/dhshah/konflux:v1.0.0` - Initial release

## For Developers

Want to contribute or run locally? See [README.md](./README.md) for development setup.

