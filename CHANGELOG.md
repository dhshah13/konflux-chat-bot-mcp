# Changelog

All notable changes to the Konflux Chatbot MCP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-10-24

### Fixed
- **CRITICAL FIX:** Changed to use `/stream_log` endpoint (same as playground) instead of `/rag-with-sources/invoke`
- Fixed payload format to match playground: now sends formatted string instead of structured JSON
- This fixes response quality issues - now gets same accurate answers as the playground
- Format: `"Urgency: ...\n\nApplication: ...\n\nQuestion: ...\n\nDetails: ..."`  instead of `{"question": ..., "urgency": ...}`

### Changed
- Input parameters are now formatted as a single string with labeled sections
- Urgency is automatically capitalized for consistency

## [1.0.0] - 2025-10-23

### Added
- Initial release of Konflux Chatbot MCP server
- `konflux_chat` tool for non-streaming chat
- `konflux_chat_stream` tool for streaming responses
- Docker/Podman support
- Hosted container on quay.io/dhshah/konflux
- Integration with Konflux AI chatbot backend
- Support for structured questions (tenant, application, component, details)
- SSL certificate handling for Red Hat internal services

### Documentation
- SIMPLE_SETUP.md for easy user onboarding
- README.md with development and usage instructions
- QUICKSTART.md for detailed documentation
- Example configuration files for different deployment methods

