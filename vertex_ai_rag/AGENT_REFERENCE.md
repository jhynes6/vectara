# Agent Reference Guide

Quick reference for all 4 Vertex AI agents and their usage.

## Agent Overview

| Agent | Purpose | Tools | Best For |
|-------|---------|-------|----------|
| **Unique Mechanism Researcher** | Research marketing strategies | RAG + Web Search | Finding innovative tactics and mechanisms |
| **Client Materials Summarizer** | Analyze capabilities | RAG | Extracting services and differentiators |
| **Client Intake Summarizer** | Extract requirements | RAG | Understanding project scope and needs |
| **Case Study Summarizer** | Structure case studies | RAG | Getting results and mechanisms |

---

## 1. Unique Mechanism Researcher

### Purpose
Discovers innovative marketing and business strategies using both your knowledge base and current web content.

### Tools
- **RAG Corpus Search**: Searches internal case studies and documentation
- **Google Web Search**: Finds latest strategies and trends online

### Best Queries
```bash
# Research innovative strategies
"What are the most effective lead generation strategies for B2B SaaS in 2024?"

# Find specific mechanisms
"What mechanisms drive high conversion rates in e-commerce checkout flows?"

# Discover trends
"What are emerging content marketing tactics for technology companies?"

# Competitive research
"What unique positioning strategies are working for marketing agencies?"
```

### Output Format
- **MECHANISM NAME**: Clear descriptive name
- **DESCRIPTION**: 2-3 sentence explanation
- **HOW IT WORKS**: Step-by-step breakdown
- **EVIDENCE**: Supporting data and examples
- **APPLICATIONS**: Where it can be applied
- **SOURCE**: Citations with URLs

### Model Settings
- **Model**: GPT-5
- **Temperature**: 0.7 (creative exploration)
- **Reasoning**: Medium
- **Top-K**: 10 results

---

## 2. Client Materials Summarizer

### Purpose
Analyzes brochures, capabilities decks, presentations to extract comprehensive service information.

### Tools
- **RAG Corpus Search**: Client materials corpus

### Best Queries
```bash
# Extract all services
"What services and capabilities does the client offer?"

# Find differentiators
"What makes this client unique compared to competitors?"

# Industry focus
"What industries and markets does the client target?"

# Technical capabilities
"What are the client's technical capabilities and tools?"
```

### Output Format
```
## SERVICES OFFERED
[Comprehensive categorized list]

## CAPABILITIES & EXPERTISE
[Technical, industry, methodologies]

## DIFFERENTIATORS
[Unique value propositions]

## TARGET MARKETS
[Industries, company sizes, use cases]
```

### Model Settings
- **Model**: GPT-5
- **Temperature**: 0.3 (consistent extraction)
- **Reasoning**: Medium
- **Top-K**: 15 results (comprehensive)

---

## 3. Client Intake Summarizer

### Purpose
Extracts project requirements, preferences, and constraints from client intake forms.

### Tools
- **RAG Corpus Search**: Filtered for intake forms

### Best Queries
```bash
# Full summary
"Summarize the client intake form with all requirements"

# Specific aspects
"What are the timeline requirements and deadlines?"
"What is the budget range and constraints?"
"Who are the key stakeholders and decision makers?"

# Project details
"What type of project is the client requesting?"
"What are the technical requirements?"
```

### Output Format
```
## CLIENT INFORMATION
Company, industry, size, location

## PROJECT OVERVIEW
Type, objectives, scope

## REQUIREMENTS
Complete list (functional, technical, design, content)

## TIMELINE & URGENCY
Dates, deadlines, milestones

## BUDGET & CONSTRAINTS
Range, limitations

## PREFERENCES & SPECIAL NOTES
Style, examples, considerations

## STAKEHOLDERS & DECISION MAKERS
Contacts, team members
```

### Model Settings
- **Model**: GPT-5
- **Temperature**: 0.2 (precise extraction)
- **Reasoning**: Medium
- **Top-K**: 10 results

---

## 4. Case Study Summarizer

### Purpose
Structures case study information into standardized format with all quantitative and qualitative results.

### Tools
- **RAG Corpus Search**: Case studies corpus

### Best Queries
```bash
# Single case study
"Summarize the [Client Name] case study"

# Results focus
"What were the quantitative results in the [Client Name] case study?"

# Mechanism focus
"How did [Service] produce [Result] in the [Client Name] case study?"

# Multiple case studies
"Summarize all case studies showing revenue growth"
"Find case studies in the healthcare industry"
```

### Output Format
```
## CLIENT
Name, industry, type, background

## SERVICES RENDERED
Specific services provided (bullet points)

## RESULTS

### Quantitative Results
- All metrics listed separately
- Revenue, traffic, conversions, etc.

### Qualitative Results
- Brand perception changes
- Process improvements
- Strategic advantages

## MECHANISM
How services produced results

## CHALLENGES & SOLUTIONS
Problems solved and approach

## SOURCE
Document name, URL, date
```

### Model Settings
- **Model**: GPT-5
- **Temperature**: 0.3 (consistent structure)
- **Reasoning**: Medium
- **Top-K**: 12 results

---

## Usage Examples

### Python SDK

```python
from shared import config
import vertexai
from vertexai import agent_engines

# Initialize
vertexai.init(
    project=config.PROJECT_ID,
    location=config.LOCATION
)

# Get agent
researcher = agent_engines.get(config.AGENT_UNIQUE_MECHANISM_RESEARCHER)

# Query
response = researcher.query(
    "What are innovative SEO strategies for local businesses?"
)

print(response['response'])
```

### CLI

```bash
# Single query
python deployment/query_agent.py \
  --agent unique_mechanism_researcher \
  --query "Your question here"

# With verbose output
python deployment/query_agent.py \
  --agent case_study_summarizer \
  --query "Summarize all case studies" \
  --verbose
```

### Batch Processing

```python
import asyncio
from shared import config
import vertexai
from vertexai import agent_engines

async def query_multiple(agent_name, queries):
    """Query agent with multiple questions"""
    vertexai.init(
        project=config.PROJECT_ID,
        location=config.LOCATION
    )
    
    agent_resource = getattr(config, f"AGENT_{agent_name.upper()}")
    agent = agent_engines.get(agent_resource)
    
    results = []
    for query in queries:
        response = agent.query(query)
        results.append({
            'query': query,
            'response': response['response']
        })
    
    return results

# Usage
queries = [
    "What services are offered?",
    "What industries are targeted?",
    "What are the key differentiators?"
]

results = asyncio.run(
    query_multiple('client_materials_summarizer', queries)
)
```

---

## Best Practices

### Query Formulation

**DO:**
- Be specific about what you want
- Mention document names when targeting specific content
- Ask follow-up questions for clarification
- Use industry-standard terminology

**DON'T:**
- Ask overly broad questions without context
- Mix multiple unrelated questions in one query
- Expect information not in the corpus (except for web search)
- Use ambiguous pronouns without context

### For Best Results

1. **Start Broad, Then Narrow**
   ```
   First: "What services does the client offer?"
   Then: "Tell me more about their paid advertising services"
   ```

2. **Reference Specific Documents**
   ```
   "Summarize the Q4 2024 capabilities deck"
   "What results are mentioned in the Acme Corp case study?"
   ```

3. **Ask for Specific Formats**
   ```
   "List all services in bullet points"
   "Create a table of quantitative results by case study"
   ```

4. **Combine RAG and Web Search** (Researcher only)
   ```
   "Find internal case studies about SEO, then search for latest SEO trends"
   ```

---

## Troubleshooting

### Agent returns "No relevant information found"

**Causes:**
- Query doesn't match document content
- Similarity threshold too high
- Documents not uploaded correctly

**Solutions:**
1. Rephrase query with different keywords
2. Check if documents exist in corpus:
   ```bash
   python setup_corpus.py --list
   ```
3. Verify upload was successful

### Agent gives incomplete results

**Causes:**
- Top-K setting too low
- Relevant content split across multiple chunks
- Distance threshold too strict

**Solutions:**
1. Ask follow-up questions to get more detail
2. Request specific sections explicitly
3. Adjust agent parameters (requires redeployment)

### Web search not working (Researcher)

**Causes:**
- Google Search API quota exceeded
- API key invalid
- Search Engine ID incorrect

**Solutions:**
1. Check API quotas in Google Cloud Console
2. Verify API keys in `.env`
3. Test search API directly:
   ```bash
   curl "https://www.googleapis.com/customsearch/v1?key=YOUR_KEY&cx=YOUR_ENGINE_ID&q=test"
   ```

---

## Cost Optimization

### Reduce Costs

1. **Lower Top-K** for less critical queries (faster, cheaper)
2. **Cache frequent queries** at application level
3. **Batch related questions** in single query
4. **Use appropriate agents** (don't use researcher for internal-only questions)

### Monitor Usage

```bash
# Check Vertex AI usage
gcloud ai operations list --location=us-central1 \
  --filter="done=true" \
  --limit=100

# OpenAI usage: Check dashboard.openai.com
```

---

## Resource Names

After deployment, your `.env` contains:

```bash
# Main corpus
RAG_CORPUS_MAIN=projects/PROJECT_ID/locations/LOCATION/ragCorpora/CORPUS_ID

# Agent resource names
AGENT_UNIQUE_MECHANISM_RESEARCHER=projects/PROJECT_ID/locations/LOCATION/reasoningEngines/ENGINE_ID
AGENT_CLIENT_MATERIALS_SUMMARIZER=projects/PROJECT_ID/locations/LOCATION/reasoningEngines/ENGINE_ID
AGENT_CLIENT_INTAKE_SUMMARIZER=projects/PROJECT_ID/locations/LOCATION/reasoningEngines/ENGINE_ID
AGENT_CASE_STUDY_SUMMARIZER=projects/PROJECT_ID/locations/LOCATION/reasoningEngines/ENGINE_ID
```

Use these for direct API access or monitoring.
