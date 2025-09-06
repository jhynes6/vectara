# Vectara Workspace Inspector

A Python script to inspect your Vectara workspace and list:
- 🤖 All agents (if available via API)
- 📚 All corpora 
- 📄 All documents in each corpus

## Setup

### 1. Virtual Environment

The project is already set up with a Python virtual environment. To activate it:

```bash
source .venv/bin/activate
```

### 2. Dependencies

Dependencies are already installed from the consolidated requirements of:
- `vectara-agentic` (AI agent library)
- `vectara-ingest` (data ingestion framework)

### 3. Configuration

Create a `.env` file with your Vectara API key:

```bash
cp env.template .env
```

Then edit `.env` and add your actual API key:

```
VECTARA_API_KEY=your_actual_vectara_api_key_here
```

You can get your API key from the [Vectara Console](https://console.vectara.com).

## Usage

### Basic Usage

```bash
python vectara_inspector.py
```

### With Command Line Options

```bash
# Specify API key directly
python vectara_inspector.py --api-key "your-api-key"

# Enable verbose output
python vectara_inspector.py --verbose

# Use custom endpoint
python vectara_inspector.py --endpoint "https://custom-vectara.domain.com"

# Show help
python vectara_inspector.py --help
```

### Environment Variables

You can also set these environment variables:

- `VECTARA_API_KEY`: Your Vectara API key (required)
- `VECTARA_ENDPOINT`: Vectara API endpoint (optional, defaults to https://api.vectara.io)

## Output

The script will display:

1. **Agents**: Currently, agents are managed through the vectara-agentic library and may not be available via REST API yet.

2. **Corpora**: A table showing:
   - Corpus name
   - Corpus key
   - Description
   - Creation date

3. **Documents**: For each corpus, a table showing:
   - Document ID
   - Document title
   - Source URL
   - Creation date

## Features

- 🎨 Beautiful terminal output using Rich
- 📊 Tabular data presentation
- 🔄 Paginated API calls (handles large workspaces)
- 🛡️ Error handling with informative messages
- 🔧 Configurable via command line or environment variables

## Troubleshooting

### Authentication Errors

If you get authentication errors:
1. Verify your API key is correct
2. Make sure your API key has the necessary permissions
3. Check that you're using the correct Vectara endpoint

### No Data Found

If no corpora or documents are found:
1. Verify you're using the correct Vectara account
2. Check that your API key has read permissions
3. Ensure you have corpora created in your Vectara workspace

## Dependencies

This project combines dependencies from the Vectara ecosystem:
- Core Vectara libraries for API interaction
- Rich for beautiful terminal output
- Typer for command-line interface
- Requests for HTTP operations
