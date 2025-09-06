# Case Study Summarizer Setup - Using Existing Workspace Agent

## Quick Start

The Case Study Summarizer connects to your existing case-study-summarizer agent from the Vectara workspace and generates comprehensive case study summaries from documents using document ID filtering.

### Prerequisites

1. **Vectara Account**: Make sure you have access to a Vectara corpus
2. **API Keys**: Obtain your Vectara API key and corpus key
3. **OpenAI API Key**: For the LLM processing (or configure another provider)

### Environment Setup

1. Create a `.env` file in your project root:

```bash
# Vectara Configuration
VECTARA_API_KEY=your_vectara_api_key_here
VECTARA_CORPUS_KEY=your_corpus_key_here

# OpenAI Configuration (or use another provider)
OPENAI_API_KEY=your_openai_api_key_here
```

2. Install additional dependencies if needed:

```bash
pip install -r case_study_requirements.txt
```

### Usage Examples

#### List Available Agents
First, discover all agents in your workspace:

```bash
python case_study_summarizer.py --list-agents
```

#### Basic Usage
Generate a case study summary using the existing workspace agent:

```bash
python case_study_summarizer.py --doc-id "clients_rapid-pos.md"
```

#### Show Agent Attributes
View all attributes of the loaded agent:

```bash
python case_study_summarizer.py --doc-id "clients_rapid-pos.md" --show-attributes
```

#### Use Specific Agent
Work with a specific agent by ID:

```bash
python case_study_summarizer.py --agent-id "agt_your_agent_id" --doc-id "clients_rapid-pos.md"
```

#### Custom Query
Focus the summary on specific aspects:

```bash
python case_study_summarizer.py --doc-id "clients_rapid-pos.md" --query "What were the main technical challenges and how were they solved?"
```

#### Async Processing
Use async processing for better performance:

```bash
python case_study_summarizer.py --doc-id "clients_rapid-pos.md" --async
```

#### Verbose Output
See additional debugging information:

```bash
python case_study_summarizer.py --doc-id "clients_rapid-pos.md" --verbose
```

### How It Works

1. **Agent Discovery**: Connects to the Vectara workspace and finds your existing case-study-summarizer agent
2. **Configuration Loading**: Pulls the agent's complete configuration including model, tools, and instructions
3. **Local Agent Creation**: Creates a local agent instance that mirrors the workspace configuration
4. **Document Filtering**: Applies the metadata filter `doc.id = 'your-doc-id'` to your Vectara corpus
5. **RAG Query**: Uses the workspace agent's configuration with Vectara's RAG pipeline
6. **AI Summarization**: Processes content using the workspace agent's LLM and instructions
7. **Structured Output**: Returns a comprehensive summary following the agent's configured format

### Output Structure

The generated case study summary includes:

- **Executive Summary**: Brief overview
- **Background**: Context and situation
- **Challenge**: Key problems faced
- **Solution**: Approach and implementation
- **Results**: Quantifiable outcomes
- **Key Learnings**: Important insights
- **Impact**: Long-term effects

### Metadata Filter Format

The script automatically converts your `--doc-id` parameter into the Vectara metadata filter:

```
"metadata_filter": "doc.id = 'your-document-id'"
```

This ensures that only content from the specified document is used for the case study summary.

### Troubleshooting

- **Missing credentials**: Ensure your `.env` file contains valid API keys
- **Document not found**: Verify the document ID exists in your corpus
- **Import errors**: Make sure vectara-agentic is properly installed and in your Python path

### Customization

You can modify the agent's behavior by:

1. Editing the `case_study_instructions` in the script
2. Adjusting the RAG tool parameters (summary_num_results, lambda_val, etc.)
3. Changing the LLM model in the `AgentConfig`
4. Adding additional metadata filters or search parameters
