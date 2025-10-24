#!/usr/bin/env python3
"""
Konflux Chatbot MCP Server

This MCP server provides access to the Konflux AI chatbot through Cursor.
It connects to the existing LangServe backend and exposes chat functionality
as MCP tools.
"""

import asyncio
import json
import os
import warnings
from typing import Optional, Any
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Suppress SSL warnings for internal Red Hat certificates
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


# Configuration
CHATBOT_URL = os.getenv(
    "KONFLUX_CHATBOT_URL",
    "https://chatbot-deployment-sp-support-chatbot--runtime-int.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com"
)


class KonfluxChatbotMCP:
    """MCP Server for Konflux Chatbot integration"""
    
    def __init__(self):
        self.server = Server("konflux-chatbot")
        self.chatbot_url = CHATBOT_URL
        
        # Register tools
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="konflux_chat",
                    description="""
                    Chat with the Konflux AI assistant for troubleshooting, questions, and guidance.
                    
                    The assistant is a Principal Konflux Platform Engineer with expertise in:
                    - Software Engineering
                    - Quality/Testing Engineering  
                    - Site Reliability Engineering (SRE)
                    - DevOps practices
                    
                    Use this for:
                    - Troubleshooting Konflux platform issues
                    - Getting documentation and guidance
                    - Understanding error messages
                    - Learning best practices
                    
                    The response will include:
                    - Diagnostic Assessment
                    - Solution/Answer
                    - Notes and warnings
                    - Confidence Level
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "Your question or issue description"
                            },
                            "urgency": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Urgency level (default: medium)",
                                "default": "medium"
                            },
                            "tenant": {
                                "type": "string",
                                "description": "Optional: Your tenant/project name"
                            },
                            "application": {
                                "type": "string",
                                "description": "Optional: Your application name"
                            },
                            "component": {
                                "type": "string",
                                "description": "Optional: Your component name"
                            },
                            "details": {
                                "type": "string",
                                "description": "Optional: Additional context, error logs, or details"
                            }
                        },
                        "required": ["question"]
                    }
                ),
                Tool(
                    name="konflux_chat_stream",
                    description="""
                    Chat with Konflux AI assistant with streaming responses.
                    Same as konflux_chat but returns response in real-time as it's generated.
                    Use this for longer responses where you want immediate feedback.
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "Your question or issue description"
                            },
                            "urgency": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Urgency level (default: medium)",
                                "default": "medium"
                            },
                            "tenant": {
                                "type": "string",
                                "description": "Optional: Your tenant/project name"
                            },
                            "application": {
                                "type": "string",
                                "description": "Optional: Your application name"
                            },
                            "component": {
                                "type": "string",
                                "description": "Optional: Your component name"
                            },
                            "details": {
                                "type": "string",
                                "description": "Optional: Additional context, error logs, or details"
                            }
                        },
                        "required": ["question"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            if name == "konflux_chat":
                result = await self._chat(arguments)
                return [TextContent(type="text", text=result)]
            elif name == "konflux_chat_stream":
                result = await self._chat_stream(arguments)
                return [TextContent(type="text", text=result)]
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def _chat(self, args: dict) -> str:
        """Non-streaming chat with Konflux chatbot"""
        try:
            # Build the input string in the same format as the playground
            # Format: "Urgency: ...\n\nTenant: ...\n\nApplication: ...\n\nComponent: ...\n\nQuestion: ...\n\nDetails: ..."
            input_parts = []
            
            # Add urgency
            urgency = args.get("urgency", "medium")
            input_parts.append(f"Urgency: {urgency.capitalize()}")
            
            # Add tenant if provided
            if args.get("tenant"):
                input_parts.append(f"Tenant: {args['tenant']}")
            
            # Add application if provided
            if args.get("application"):
                input_parts.append(f"Application: {args['application']}")
            
            # Add component if provided
            if args.get("component"):
                input_parts.append(f"Component: {args['component']}")
            
            # Add question
            input_parts.append(f"Question: {args['question']}")
            
            # Add details if provided
            if args.get("details"):
                input_parts.append(f"Details: {args['details']}")
            
            # Join with double newlines
            input_string = "\n\n".join(input_parts)
            
            # Call /stream_log endpoint (returns Server-Sent Events format)
            # Note: verify=False for internal Red Hat certificates
            async with httpx.AsyncClient(timeout=120.0, verify=False) as client:
                async with client.stream(
                    "POST",
                    f"{self.chatbot_url}/stream_log",
                    json={"input": input_string, "config": {}}
                ) as response:
                    response.raise_for_status()
                    
                    final_output = None
                    
                    # Parse Server-Sent Events (SSE) format
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            try:
                                # Remove "data: " prefix and parse JSON
                                data = json.loads(line[6:])
                                
                                # Look for final_output in the ops
                                if isinstance(data, dict) and "ops" in data:
                                    for op in data["ops"]:
                                        if op.get("path") == "/final_output" and "value" in op:
                                            final_output = op["value"]
                                        # Also check for replace operations on final_output
                                        elif op.get("op") == "replace" and op.get("path") == "/final_output":
                                            final_output = op.get("value")
                            except json.JSONDecodeError:
                                continue
                    
                    if final_output:
                        return str(final_output)
                    else:
                        return "No response received from chatbot"
                    
        except httpx.HTTPError as e:
            return f"Error communicating with Konflux chatbot: {str(e)}\n\nPlease check:\n1. The chatbot URL is correct\n2. You have network access (VPN required for Red Hat internal services)\n3. The chatbot service is running"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    async def _chat_stream(self, args: dict) -> str:
        """Streaming chat with Konflux chatbot"""
        try:
            # Build the input string in the same format as the playground
            input_parts = []
            
            # Add urgency
            urgency = args.get("urgency", "medium")
            input_parts.append(f"Urgency: {urgency.capitalize()}")
            
            # Add tenant if provided
            if args.get("tenant"):
                input_parts.append(f"Tenant: {args['tenant']}")
            
            # Add application if provided
            if args.get("application"):
                input_parts.append(f"Application: {args['application']}")
            
            # Add component if provided
            if args.get("component"):
                input_parts.append(f"Component: {args['component']}")
            
            # Add question
            input_parts.append(f"Question: {args['question']}")
            
            # Add details if provided
            if args.get("details"):
                input_parts.append(f"Details: {args['details']}")
            
            # Join with double newlines
            input_string = "\n\n".join(input_parts)
            
            # Call /stream_log endpoint (returns Server-Sent Events format)
            # Note: verify=False for internal Red Hat certificates
            async with httpx.AsyncClient(timeout=120.0, verify=False) as client:
                async with client.stream(
                    "POST",
                    f"{self.chatbot_url}/stream_log",
                    json={"input": input_string, "config": {}}
                ) as response:
                    response.raise_for_status()
                    
                    final_output = None
                    
                    # Parse Server-Sent Events (SSE) format
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            try:
                                # Remove "data: " prefix and parse JSON
                                data = json.loads(line[6:])
                                
                                # Look for final_output in the ops
                                if isinstance(data, dict) and "ops" in data:
                                    for op in data["ops"]:
                                        if op.get("path") == "/final_output" and "value" in op:
                                            final_output = op["value"]
                                        # Also check for replace operations on final_output
                                        elif op.get("op") == "replace" and op.get("path") == "/final_output":
                                            final_output = op.get("value")
                            except json.JSONDecodeError:
                                continue
                    
                    if final_output:
                        return str(final_output)
                    else:
                        return "No response received from chatbot"
                    
        except httpx.HTTPError as e:
            return f"Error communicating with Konflux chatbot: {str(e)}\n\nPlease check:\n1. The chatbot URL is correct\n2. You have network access (VPN required for Red Hat internal services)\n3. The chatbot service is running"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point"""
    server = KonfluxChatbotMCP()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())

