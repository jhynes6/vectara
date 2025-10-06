# Google Workspace MCP Server Setup

## Overview

The Google Workspace MCP Server provides **full natural language control** over Google Calendar, Drive, Gmail, Docs, Sheets, Slides, Forms, Tasks, and Chat through Cursor and other MCP clients.

**Location**: `/Users/hynes/dev/vectara/google_workspace_mcp/`

## ✅ Setup Status

- ✅ Dependencies installed
- ⚠️  OAuth credentials needed
- ⏳ Cursor configuration pending

## 🚀 Quick Start

### Step 1: Create Google OAuth Credentials

You need to set up OAuth 2.0 credentials in Google Cloud Console.

#### 1.1 Go to Google Cloud Console

1. Visit https://console.cloud.google.com/apis/credentials
2. Select your project: **automation-402014** (or create a new one)

#### 1.2 Create OAuth 2.0 Client ID

1. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
2. If prompted, configure the **OAuth consent screen**:
   - User Type: **External** (for testing) or **Internal** (for Google Workspace)
   - App name: `Google Workspace MCP`
   - User support email: Your email
   - Developer contact: Your email
   - Scopes: Add these scopes:
     - `https://www.googleapis.com/auth/gmail.modify`
     - `https://www.googleapis.com/auth/drive`
     - `https://www.googleapis.com/auth/calendar`
     - `https://www.googleapis.com/auth/documents`
     - `https://www.googleapis.com/auth/spreadsheets`
     - `https://www.googleapis.com/auth/presentations`
     - `https://www.googleapis.com/auth/forms`
     - `https://www.googleapis.com/auth/tasks`
     - `https://www.googleapis.com/auth/chat.spaces`
   - Test users: Add your email
3. Choose Application type: **Desktop app**
4. Name: `Google Workspace MCP Desktop`
5. Click **CREATE**
6. **Download the JSON** or copy the Client ID and Client Secret

#### 1.3 Enable Required APIs

Enable these Google Workspace APIs in your project:

```
https://console.cloud.google.com/apis/library
```

Search for and enable:
- ✅ Gmail API
- ✅ Google Drive API
- ✅ Google Calendar API
- ✅ Google Docs API
- ✅ Google Sheets API
- ✅ Google Slides API
- ✅ Google Forms API
- ✅ Google Tasks API
- ✅ Google Chat API (for Workspace accounts)

### Step 2: Configure Environment Variables

Edit the `.env` file in the Google Workspace MCP directory:

```bash
cd /Users/hynes/dev/vectara/google_workspace_mcp
nano .env  # or use your preferred editor
```

Update these values:

```env
GOOGLE_OAUTH_CLIENT_ID="YOUR-CLIENT-ID.apps.googleusercontent.com"
GOOGLE_OAUTH_CLIENT_SECRET="YOUR-CLIENT-SECRET"
```

### Step 3: Add to Cursor MCP Configuration

The server has been added to your Cursor MCP configuration at `.cursor/mcp.json`.

### Step 4: Test the Server

Once OAuth credentials are configured, restart Cursor and test:

```bash
# Or run directly for testing
cd /Users/hynes/dev/vectara/google_workspace_mcp
uv run main.py --tool-tier core
```

On first run, it will open a browser for you to authorize the app with your Google account.

## Available Services

### 📧 Gmail
- Send, read, search emails
- Manage labels, drafts
- Attachment handling
- Message threading

### 📁 Google Drive
- File operations (create, read, update, delete)
- Folder management
- File sharing and permissions
- Search and list files

### 📅 Calendar
- Event management
- Calendar operations
- Recurring events
- Event invitations

### 📄 Google Docs
- Document creation and editing
- Text formatting
- Comments and suggestions
- Table management

### 📊 Google Sheets
- Spreadsheet operations
- Cell manipulation
- Formula management
- Data validation

### 📽️ Google Slides
- Presentation creation
- Slide manipulation
- Content management
- Layout operations

### 📝 Forms
- Form creation and editing
- Question management
- Response handling
- Publish settings

### ✅ Tasks
- Task management
- Task lists
- Due dates and notes
- Task hierarchy

### 💬 Chat (Workspace only)
- Space management
- Message sending
- Space discovery

### 🔍 Custom Search
- Programmable Search Engine integration
- Web search capabilities

## Tool Tiers

The server supports different tool tiers for flexibility:

| Tier | Description | Tools |
|------|-------------|-------|
| `core` | Essential tools | Most commonly used operations |
| `extended` | Core + extras | Additional useful tools |
| `complete` | Everything | All available tools |

### Specify Tool Tier

```bash
# Core tools only
uv run main.py --tool-tier core

# Extended tools
uv run main.py --tool-tier extended

# All tools
uv run main.py --tool-tier complete

# Or specific services
uv run main.py --tools gmail drive calendar docs
```

## Usage in Cursor

Once configured, you can use natural language to interact with Google Workspace:

### Gmail Examples
```
@google-workspace read my latest 5 emails

@google-workspace send an email to john@example.com with subject "Meeting Tomorrow" and body "Let's meet at 2 PM"

@google-workspace search for emails from boss@company.com in the last week
```

### Drive Examples
```
@google-workspace list files in my Drive

@google-workspace create a new folder called "Project Documents"

@google-workspace upload the content "Hello World" to a file named "test.txt"
```

### Calendar Examples
```
@google-workspace show my calendar events for today

@google-workspace create a calendar event for tomorrow at 2 PM titled "Team Meeting"

@google-workspace find all events this week
```

### Docs Examples
```
@google-workspace create a new Google Doc titled "Project Plan"

@google-workspace add text "Introduction" to the doc

@google-workspace format the text as a heading
```

### Sheets Examples
```
@google-workspace create a new spreadsheet called "Budget 2025"

@google-workspace add data to cell A1: "Revenue"

@google-workspace insert a formula in B1: "=SUM(B2:B10)"
```

## Configuration Options

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_OAUTH_CLIENT_ID` | ✅ Yes | - | OAuth 2.0 Client ID |
| `GOOGLE_OAUTH_CLIENT_SECRET` | ✅ Yes | - | OAuth 2.0 Client Secret |
| `OAUTHLIB_INSECURE_TRANSPORT` | Dev only | 0 | Allow HTTP (for localhost) |
| `USER_GOOGLE_EMAIL` | No | - | Default email for single-user |
| `GOOGLE_PSE_API_KEY` | No | - | Custom Search API key |
| `GOOGLE_PSE_ENGINE_ID` | No | - | Custom Search Engine ID |
| `MCP_ENABLE_OAUTH21` | No | false | Enable OAuth 2.1 support |
| `WORKSPACE_MCP_STATELESS_MODE` | No | false | Stateless operation |

### Cursor MCP Configuration

Your `.cursor/mcp.json` configuration:

```json
{
  "mcpServers": {
    "google-workspace": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/hynes/dev/vectara/google_workspace_mcp",
        "run",
        "main.py",
        "--tool-tier",
        "core"
      ],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
        "GOOGLE_OAUTH_CLIENT_SECRET": "your-client-secret",
        "OAUTHLIB_INSECURE_TRANSPORT": "1"
      },
      "disabled": false
    }
  }
}
```

**Note**: You'll need to update the `env` section with your actual OAuth credentials.

## Authentication Flow

1. **First Run**: Browser opens automatically
2. **Sign In**: Authenticate with your Google account
3. **Grant Permissions**: Approve requested scopes
4. **Token Storage**: Credentials cached in `.credentials/`
5. **Auto-Refresh**: Tokens refreshed automatically

### Token Storage

Tokens are stored in:
```
/Users/hynes/dev/vectara/google_workspace_mcp/.credentials/
```

To reset authentication (if needed):
```bash
rm -rf /Users/hynes/dev/vectara/google_workspace_mcp/.credentials
```

## Troubleshooting

### Issue: "OAuth client credentials not configured"

**Solution**: Make sure you've:
1. Created OAuth credentials in Google Cloud Console
2. Set `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET` in `.env`
3. Restarted Cursor

### Issue: "API not enabled"

**Solution**: Enable the required Google Workspace API in Console:
```
https://console.cloud.google.com/apis/library
```

### Issue: "Access denied" during OAuth

**Solution**: 
1. Check OAuth consent screen configuration
2. Add your email as a test user (for External apps)
3. Verify scopes are correctly configured

### Issue: "Invalid credentials"

**Solution**:
1. Verify Client ID and Secret are correct
2. Check for extra spaces or quotes
3. Try regenerating credentials in Console

### Issue: "Redirect URI mismatch"

**Solution**: 
- Use **Desktop App** type (not Web application)
- Desktop apps don't require redirect URI configuration

### Issue: Browser doesn't open for authentication

**Solution**:
```bash
# Run manually to see the auth URL
cd /Users/hynes/dev/vectara/google_workspace_mcp
uv run main.py --tool-tier core
```

Copy the URL from terminal and open in browser manually.

## Security Notes

1. **Credentials Security**: 
   - Never commit `.env` file to git (already in `.gitignore`)
   - Keep OAuth credentials secret
   - Don't share token files in `.credentials/`

2. **Scope Permissions**:
   - Only grant necessary scopes
   - Review permissions during OAuth consent
   - Can revoke access at https://myaccount.google.com/permissions

3. **Token Management**:
   - Tokens are cached locally
   - Automatically refreshed when expired
   - Delete `.credentials/` to revoke local access

## Advanced Features

### Multi-User OAuth 2.1 Support

For multi-user scenarios (e.g., web app with multiple Google accounts):

```env
MCP_ENABLE_OAUTH21=true
WORKSPACE_MCP_STATELESS_MODE=true
```

### Custom Search Integration

To enable Google Custom Search:

1. Create a Programmable Search Engine: https://programmablesearchengine.google.com/
2. Get API key: https://console.cloud.google.com/apis/credentials
3. Configure in `.env`:

```env
GOOGLE_PSE_API_KEY="your-api-key"
GOOGLE_PSE_ENGINE_ID="your-engine-id"
```

### Tool Selection

Run only specific tools:

```bash
# Only Gmail and Drive
uv run main.py --tools gmail drive

# Only Calendar
uv run main.py --tools calendar
```

Available tools:
- `gmail` - Gmail operations
- `drive` - Google Drive
- `calendar` - Google Calendar
- `docs` - Google Docs
- `sheets` - Google Sheets
- `slides` - Google Slides
- `forms` - Google Forms
- `tasks` - Google Tasks
- `chat` - Google Chat (Workspace only)
- `search` - Custom Search

## Performance Tips

1. **Tool Tier**: Use `core` tier for better performance
2. **Specific Tools**: Load only needed tools with `--tools`
3. **Caching**: Service objects are cached for efficiency
4. **Token Refresh**: Handled automatically

## Development

### Running in Development Mode

```bash
cd /Users/hynes/dev/vectara/google_workspace_mcp
uv run main.py --tool-tier core
```

### Debugging

Enable debug logging:

```env
OAUTH2_ENABLE_DEBUG=true
```

Check logs:
```bash
tail -f /Users/hynes/dev/vectara/google_workspace_mcp/mcp_server_debug.log
```

### Running Tests

```bash
cd /Users/hynes/dev/vectara/google_workspace_mcp
uv run pytest tests/
```

## Resources

- **Homepage**: https://workspacemcp.com
- **GitHub**: https://github.com/taylorwilsdon/google_workspace_mcp
- **Issues**: https://github.com/taylorwilsdon/google_workspace_mcp/issues
- **Google Cloud Console**: https://console.cloud.google.com
- **OAuth 2.0 Setup**: https://developers.google.com/identity/protocols/oauth2

## Related Documentation

- [Vertex AI MCP Server](./VERTEX_AI_MCP_SERVER.md)
- [Complete Workflow Guide](./COMPLETE_WORKFLOW_GUIDE.md)
- [Project Structure](./PROJECT_STRUCTURE.md)

---

**Last Updated**: October 3, 2025  
**Version**: 1.4.8  
**Status**: ⚠️ OAuth Credentials Needed

