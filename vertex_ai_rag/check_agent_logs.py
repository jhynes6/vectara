#!/usr/bin/env python3
"""
Check Agent Execution Logs
===========================
Fetches recent logs from Cloud Logging to see agent errors.
"""

import os
import sys
from datetime import datetime, timedelta
from google.cloud import logging as cloud_logging
from google.oauth2 import service_account

sys.path.insert(0, os.path.dirname(__file__))
from shared import config

def check_agent_logs(minutes_back: int = 10):
    """Check recent agent logs"""
    
    print("📜 CHECKING AGENT EXECUTION LOGS")
    print("=" * 80)
    print(f"Looking back: {minutes_back} minutes")
    print()
    
    # Initialize logging client
    credentials = service_account.Credentials.from_service_account_file(
        config.CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    
    logging_client = cloud_logging.Client(
        project=config.PROJECT_ID,
        credentials=credentials
    )
    
    # Get logs for reasoning engines
    filter_str = '''
    resource.type="aiplatform.googleapis.com/ReasoningEngine"
    severity>=ERROR
    '''
    
    print(f"🔍 Filter: {filter_str.strip()}")
    print("-" * 80)
    
    try:
        entries = logging_client.list_entries(
            filter_=filter_str,
            max_results=20,
            order_by=cloud_logging.DESCENDING
        )
        
        log_count = 0
        for entry in entries:
            log_count += 1
            print(f"\n📄 Log Entry #{log_count}")
            print(f"   Timestamp: {entry.timestamp}")
            print(f"   Severity: {entry.severity}")
            print(f"   Resource: {entry.resource}")
            print(f"   Payload: {entry.payload}")
            print("-" * 80)
        
        if log_count == 0:
            print("✅ No error logs found in last 10 minutes")
            print("\n💡 Try checking ALL logs (not just errors):")
            print("   https://console.cloud.google.com/logs/query?project=walkinto-473412")
        else:
            print(f"\n⚠️  Found {log_count} error log entries")
            
    except Exception as e:
        print(f"❌ Failed to fetch logs: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_agent_logs()
