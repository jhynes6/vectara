# Agentic Workflow with OpenAI Assistants

## Overview

This project now includes an **agentic workflow orchestrator** that uses OpenAI's Assistants API to coordinate the complete client onboarding process. Instead of rigid sequential execution, the workflow uses AI agents to make intelligent decisions about task execution, error handling, and process flow.

## Architecture

### Agent-Based Design

The workflow uses a **Coordinator Agent** that orchestrates the entire process through:

1. **Ingestion Phase**: Website scraping + Google Drive content ingestion
2. **PDF Processing Phase**: Reprocessing failed PDF extractions  
3. **Upload Phase**: Uploading content to Vertex AI RAG
4. **Brief Generation Phase**: Creating comprehensive client briefs

### Key Components

#### 1. Coordinator Agent
- Orchestrates the entire workflow
- Makes decisions about task execution order
- Handles errors and decides whether to continue or abort
- Uses OpenAI's function calling to invoke tools

#### 2. Workflow Tools
The coordinator has access to these tools:
- `run_ingestion()` - Ingests website and Drive content
- `reprocess_pdfs()` - Fixes failed PDF extractions
- `upload_to_vertex()` - Uploads to Vertex AI RAG
- `generate_brief()` - Creates client brief
- `get_state()` - Checks workflow state

#### 3. Intelligent Orchestration
The agent:
- Decides when to execute each tool
- Analyzes results before proceeding
- Handles failures gracefully
- Provides clear status updates

## Why Agents?

Traditional workflow systems are rigid and linear. With agents:

✅ **Intelligent Decision Making**: The agent analyzes results and decides next steps  
✅ **Adaptive Error Handling**: Can retry, skip, or abort based on error severity  
✅ **Natural Language Control**: Can be guided with plain English instructions  
✅ **Self-Documenting**: Agent provides clear reasoning for each decision  
✅ **Extensible**: Easy to add new tools or modify agent behavior

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Key new dependencies:
- `openai>=2.1.0` - OpenAI SDK with Assistants API support

### 2. Set Environment Variables

Create a `.env` file with:

```bash
# Required for OpenAI Assistants
OPENAI_API_KEY=your_openai_api_key_here

# Required for Vertex AI RAG
VECTARA_API_KEY=your_vectara_api_key_here

# Optional for LLM categorization
# (can reuse OPENAI_API_KEY)

# Google Drive credentials file path
# (default: ./service_account.json)
```

## Usage

### Interactive Mode (Recommended)

Simply run the script and follow the prompts:

```bash
python agentic_workflow.py
```

The agent will prompt you for:
- Client ID
- Google Drive folder ID/URL
- Client homepage URL
- Optional settings (workers, PDF processor, etc.)

### Batch Mode

Provide all arguments for automated execution:

```bash
python agentic_workflow.py \
  --client-id "client-name" \
  --drive-folder-id "1ABC123..." \
  --client-homepage-url "https://example.com" \
  --batch-mode
```

### Advanced Options

```bash
# Custom PDF processor
python agentic_workflow.py \
  --client-id "client-name" \
  --drive-folder-id "1ABC..." \
  --client-homepage-url "https://example.com" \
  --pdf-processor markitdown \
  --workers 8

# Disable LLM categorization (faster, less accurate)
python agentic_workflow.py \
  --client-id "client-name" \
  --drive-folder-id "1ABC..." \
  --client-homepage-url "https://example.com" \
  --no-llm-categories

# Custom output directory and credentials
python agentic_workflow.py \
  --client-id "client-name" \
  --drive-folder-id "1ABC..." \
  --client-homepage-url "https://example.com" \
  --output-dir "./custom/output" \
  --credentials "./my-service-account.json"
```

## How It Works

### 1. Agent Creation

The orchestrator creates a Coordinator Agent with:
- Clear instructions about the workflow phases
- Access to workflow tools (functions)
- GPT-4 model for intelligent decision making

### 2. Workflow Execution

```
User Request → Coordinator Agent → Decides First Action
                     ↓
              run_ingestion() tool
                     ↓
              Analyzes result → Decides Next Action
                     ↓
              reprocess_pdfs() tool
                     ↓
              Analyzes result → Decides Next Action
                     ↓
              upload_to_vertex() tool
                     ↓
              Analyzes result → Decides Next Action
                     ↓
              generate_brief() tool
                     ↓
              Reports completion
```

### 3. Tool Execution

When the agent calls a tool:
1. The orchestrator receives the tool call request
2. Executes the corresponding Python function
3. Returns the result to the agent
4. Agent analyzes and decides next step

### 4. Error Handling

The agent can:
- Detect errors in tool outputs
- Decide whether to retry, skip, or abort
- Provide meaningful error messages
- Continue with partial success when appropriate

## Example Output

```
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
AGENTIC CLIENT ONBOARDING WORKFLOW (OpenAI Assistants)
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
Client: example-client
Started: 2025-10-04 10:30:00

✅ Created coordinator agent: asst_abc123...
Created conversation thread: thread_xyz789...
🤖 Coordinator agent is now orchestrating the workflow...

Agent status: requires_action (iteration 1)
Agent requested 1 tool call(s)
  📞 Tool call: run_ingestion
🛠️  Executing tool: run_ingestion
  [Ingestion process output...]
✅ Tool run_ingestion completed: True

Agent status: requires_action (iteration 2)
Agent requested 1 tool call(s)
  📞 Tool call: reprocess_pdfs
🛠️  Executing tool: reprocess_pdfs
  [PDF reprocessing output...]
✅ Tool reprocess_pdfs completed: True

Agent status: requires_action (iteration 3)
Agent requested 1 tool call(s)
  📞 Tool call: upload_to_vertex
🛠️  Executing tool: upload_to_vertex
  [Upload output...]
✅ Tool upload_to_vertex completed: True

Agent status: requires_action (iteration 4)
Agent requested 1 tool call(s)
  📞 Tool call: generate_brief
🛠️  Executing tool: generate_brief
  [Brief generation output...]
✅ Tool generate_brief completed: True

Agent status: completed (iteration 5)
✅ Workflow completed!

================================================================================
🎉 AGENTIC WORKFLOW FINISHED
================================================================================
Client: example-client
Duration: 245.3 seconds (4.1 minutes)

Results:
  ✅ Ingestion: Complete
  ✅ PDF Reprocessing: Complete
  ✅ Vertex Upload: Complete
  ✅ Brief Generation: Complete
================================================================================

🧹 Cleaned up agent: asst_abc123...
```

## Advantages Over Traditional Workflow

| Traditional Workflow | Agentic Workflow |
|---------------------|------------------|
| Fixed execution order | Adaptive decision making |
| Hard-coded error handling | Intelligent error recovery |
| Rigid conditional logic | Natural language reasoning |
| Manual monitoring required | Self-monitoring and reporting |
| Difficult to modify | Easy to extend with new tools |

## Extending the Workflow

### Adding New Tools

1. Add a tool method to `WorkflowTools` class:

```python
def my_new_tool(self) -> Dict[str, Any]:
    """My new tool description"""
    try:
        # Tool implementation
        result = do_something()
        return {'success': True, 'result': result}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

2. Add tool to agent's tools specification:

```python
{
    "type": "function",
    "function": {
        "name": "my_new_tool",
        "description": "What this tool does",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Parameter description"
                }
            },
            "required": ["param1"]
        }
    }
}
```

3. Register in tool executor:

```python
tool_methods = {
    'run_ingestion': self.tools.run_ingestion,
    'my_new_tool': self.tools.my_new_tool,
    # ... other tools
}
```

### Customizing Agent Behavior

Modify the agent's instructions in `create_coordinator_agent()`:

```python
instructions = """You are the Coordinator Agent...

Your custom instructions here:
- Special handling for certain scenarios
- Priority ordering of tasks
- Custom decision criteria
"""
```

## Troubleshooting

### Agent Not Calling Tools

**Issue**: Agent completes without calling any tools

**Solution**: 
- Check agent instructions are clear
- Verify tools are properly defined
- Ensure initial message clearly requests action

### Tool Execution Failures

**Issue**: Tools return errors

**Solution**:
- Check environment variables are set
- Verify file paths and credentials
- Review tool-specific logs

### OpenAI API Errors

**Issue**: API rate limits or authentication errors

**Solution**:
- Verify `OPENAI_API_KEY` is valid
- Check API usage limits
- Add delays between requests if needed

### Agent Stuck in Loop

**Issue**: Agent repeatedly calls same tool

**Solution**:
- Check tool outputs are clear and informative
- Verify agent can parse tool results
- Review agent logs for decision reasoning

## Cost Considerations

The agentic workflow uses OpenAI's GPT-4o model, which incurs costs:

- **Model**: GPT-4o (November 2024)
- **Typical workflow**: 10-20 agent turns
- **Cost per run**: ~$0.10-0.50 depending on complexity

To reduce costs:
- Use fewer agent interactions (optimize tool outputs)
- Consider GPT-4o-mini for simpler workflows
- Cache common agent responses

## Best Practices

1. **Clear Tool Outputs**: Return structured JSON with clear success/failure indicators
2. **Detailed Logging**: Log all agent decisions and tool executions
3. **Error Context**: Include helpful error messages in tool outputs
4. **State Management**: Keep workflow state clean and accessible
5. **Agent Cleanup**: Always delete agents after completion to avoid clutter

## Comparison with Non-Agentic Approach

If you prefer the traditional sequential approach, you can still use:

```bash
# Traditional approach (if implemented)
python run_complete_workflow.py --client-id "..." --drive-folder-id "..." --client-homepage-url "..."
```

However, the agentic approach offers:
- Better error recovery
- More intelligent decision making
- Easier to extend and modify
- Self-documenting execution flow

## Future Enhancements

Planned improvements:
- [ ] Multiple specialized agents (Ingestion Agent, PDF Agent, etc.)
- [ ] Agent-to-agent handoffs for complex tasks
- [ ] Persistent agent memory across runs
- [ ] Web interface for monitoring agent decisions
- [ ] Custom agent personalities and behaviors
- [ ] Multi-client parallel processing with agent pool

## Support

For issues or questions:
- Check logs in the console output
- Review agent responses for decision reasoning
- Verify environment variables and credentials
- Test individual tools separately

## License

Same as the main project.
