# Vertex AI MCP Server Setup

## Overview

The Vertex AI MCP (Model Context Protocol) Server is now installed and configured in your project. It provides **30+ AI-powered tools** that integrate directly with Cursor/Cline.

**Location**: `/Users/hynes/dev/vectara/vertex-ai-mcp-server/`

## ✅ Setup Complete

The server has been fully configured with:
- ✅ Dependencies installed
- ✅ Server compiled and built
- ✅ Environment variables configured
- ✅ MCP configuration added to Cursor
- ✅ Authentication via your existing service account

## Configuration

### Environment Variables (`.env`)

```env
AI_PROVIDER="vertex"
GOOGLE_CLOUD_PROJECT="automation-402014"
GOOGLE_CLOUD_LOCATION="us-central1"
VERTEX_MODEL_ID="gemini-2.0-flash-exp"
AI_TEMPERATURE="0.0"
AI_USE_STREAMING="true"
AI_MAX_OUTPUT_TOKENS="65536"
GOOGLE_APPLICATION_CREDENTIALS="/Users/hynes/dev/vectara/service_account.json"
```

### Cursor/Cline Configuration (`.cursor/mcp.json`)

The server is configured to run automatically with Cursor. Configuration file location:
```
/Users/hynes/dev/vectara/.cursor/mcp.json
```

## Available Tools

### 🤖 AI Query & Generation

| Tool | Description |
|------|-------------|
| `answer_query_websearch` | Answers queries using Vertex AI enhanced with Google Search results |
| `answer_query_direct` | Answers queries using only the model's internal knowledge |
| `explain_topic_with_docs` | Detailed explanations from official documentation via web search |
| `get_doc_snippets` | Precise code snippets or answers from technical documentation |
| `generate_project_guidelines` | Creates structured project guidelines based on tech stack |

### 🔍 Research & Analysis

| Tool | Description |
|------|-------------|
| `code_analysis_with_docs` | Analyzes code against best practices from official docs |
| `technical_comparison` | Compares technologies/frameworks with pros/cons |
| `architecture_pattern_recommendation` | Suggests architecture patterns for use cases |
| `dependency_vulnerability_scan` | Analyzes dependencies for security vulnerabilities |
| `database_schema_analyzer` | Reviews DB schemas for optimization opportunities |
| `security_best_practices_advisor` | Provides security recommendations with code examples |
| `testing_strategy_generator` | Creates comprehensive testing strategies |
| `regulatory_compliance_advisor` | Guidance on GDPR, HIPAA, and other regulations |
| `microservice_design_assistant` | Helps design microservice architectures |
| `documentation_generator` | Creates comprehensive technical documentation |

### 📁 Filesystem Operations

| Tool | Description |
|------|-------------|
| `read_file_content` | Read complete contents of one or more files |
| `write_file_content` | Create new files or overwrite existing files |
| `edit_file_content` | Make line-based edits with diff preview |
| `list_directory_contents` | List files/directories in a path |
| `get_directory_tree` | Recursive tree view of files and directories |
| `move_file_or_directory` | Move or rename files and directories |
| `search_filesystem` | Search for files matching patterns |
| `get_filesystem_info` | Get detailed file/directory metadata |
| `execute_terminal_command` | Execute shell commands with optional cwd/timeout |

### 💾 Combined AI + Filesystem Operations

| Tool | Description |
|------|-------------|
| `save_generate_project_guidelines` | Generate and save project guidelines |
| `save_doc_snippet` | Find and save code snippets from docs |
| `save_topic_explanation` | Generate and save topic explanations |
| `save_answer_query_direct` | Answer and save query responses |
| `save_answer_query_websearch` | Answer with web search and save |

## How to Use

### 1. Restart Cursor

After setup, restart Cursor to load the MCP server configuration.

### 2. Use MCP Tools in Chat

In Cursor's chat interface, the MCP tools will be available automatically. Examples:

**Generate Project Guidelines:**
```
@vertex-ai-mcp-server generate_project_guidelines for a Python FastAPI project with PostgreSQL and Redis
```

**Analyze Code:**
```
@vertex-ai-mcp-server analyze this code snippet against Python best practices:
[paste your code]
```

**Get Documentation Snippets:**
```
@vertex-ai-mcp-server get code snippet for setting up Vertex AI RAG in Python
```

**Compare Technologies:**
```
@vertex-ai-mcp-server compare FastAPI vs Flask for building REST APIs
```

### 3. Tool Confirmation

By default, Cursor will ask for confirmation before executing MCP tools. You can:
- Approve tools individually
- Add frequently used tools to `alwaysAllow` in `.cursor/mcp.json`

Example of allowing tools without confirmation:
```json
{
  "mcpServers": {
    "vertex-ai-mcp-server": {
      ...
      "alwaysAllow": [
        "answer_query_websearch",
        "get_doc_snippets",
        "code_analysis_with_docs"
      ]
    }
  }
}
```

## Use Cases for Your Project

### 1. Client Onboarding Documentation
```
Generate comprehensive documentation for the client onboarding system
```

### 2. Code Analysis
```
Analyze the Vertex AI RAG integration code for best practices and potential issues
```

### 3. Security Review
```
Review the ingestion pipeline for security vulnerabilities and data handling best practices
```

### 4. Architecture Recommendations
```
Suggest architecture patterns for scaling the client onboarding system to handle 100+ clients
```

### 5. Testing Strategy
```
Generate a testing strategy for the MarkItDown file processing pipeline
```

### 6. Dependency Scanning
```
Scan project dependencies for security vulnerabilities
```

## Configuration Options

### Change Model

Edit `.cursor/mcp.json` to use a different model:
```json
"VERTEX_MODEL_ID": "gemini-1.5-pro-latest"
```

Available models:
- `gemini-2.0-flash-exp` (default, fastest)
- `gemini-1.5-pro-latest` (more capable)
- `gemini-1.5-flash-latest` (balanced)

### Adjust Temperature

For more creative responses, increase temperature:
```json
"AI_TEMPERATURE": "0.7"
```

Range: `0.0` (deterministic) to `1.0` (creative)

### Disable Streaming

If you prefer complete responses:
```json
"AI_USE_STREAMING": "false"
```

### Increase Timeout

For long-running operations:
```json
"timeout": 7200
```

Value in seconds.

## Troubleshooting

### Issue: Server not appearing in Cursor

**Solution:**
1. Restart Cursor completely
2. Check `.cursor/mcp.json` exists and is valid JSON
3. Check logs in Cursor's developer console

### Issue: Authentication errors

**Solution:**
1. Verify service account exists: `ls -la /Users/hynes/dev/vectara/service_account.json`
2. Check service account has Vertex AI permissions
3. Verify project ID is correct: `automation-402014`

### Issue: Model not found errors

**Solution:**
1. Verify the model ID is available in your region
2. Check Vertex AI API is enabled in your GCP project
3. Try a different model like `gemini-1.5-flash-latest`

### Issue: Rate limiting

**Solution:**
1. Reduce `AI_MAX_RETRIES` in configuration
2. Increase `AI_RETRY_DELAY_MS` to space out requests
3. Consider using a different model with higher quotas

## Development

### Rebuild Server

If you make changes to the server code:

```bash
cd /Users/hynes/dev/vectara/vertex-ai-mcp-server
bun run build
```

Then restart Cursor to load the updated build.

### Watch Mode

For active development:

```bash
cd /Users/hynes/dev/vectara/vertex-ai-mcp-server
bun run watch
```

### Test Server

To test the server directly:

```bash
cd /Users/hynes/dev/vectara/vertex-ai-mcp-server
bunx @modelcontextprotocol/inspector build/index.js
```

This launches the MCP inspector for testing tools.

## Security Notes

1. **API Keys**: The service account credentials provide full access to your GCP project. Keep them secure.

2. **Safety Filters**: The server uses minimal safety filters (`BLOCK_NONE`). Review outputs carefully for production use.

3. **File Operations**: The filesystem tools have full access to your filesystem. Be cautious when using write/edit operations.

4. **Command Execution**: The `execute_terminal_command` tool can run any shell command. Only use with trusted prompts.

## Resources

- **GitHub Repo**: https://github.com/shariqriazz/vertex-ai-mcp-server
- **MCP Documentation**: https://modelcontextprotocol.io/
- **Vertex AI Docs**: https://cloud.google.com/vertex-ai/docs

## Related Documentation

- [Vertex AI RAG Integration](./INTEGRATION_COMPLETE.md)
- [Complete Workflow Guide](./COMPLETE_WORKFLOW_GUIDE.md)
- [Project Structure](./PROJECT_STRUCTURE.md)

---

**Last Updated**: October 3, 2025  
**Version**: 0.4.0  
**Status**: ✅ Configured and Ready

