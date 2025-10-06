#!/usr/bin/env python3
"""
Chunk a single client's brief into the document_chunks table
"""
import sys
import argparse
from vector_store import VectorStore

def chunk_client(client_id: str):
    """Chunk a single client's brief"""
    print(f"🔄 Chunking client brief for: {client_id}")
    
    vs = VectorStore()
    
    try:
        success = vs.save_client_brief_chunks(client_id)
        
        if success:
            print(f"✅ Successfully chunked and saved brief for {client_id}")
            return True
        else:
            print(f"❌ Failed to chunk brief for {client_id}")
            print("   Possible reasons:")
            print("   - Client doesn't exist in client_briefs table")
            print("   - Brief content is empty after filtering")
            print("   - Database connection issues")
            return False
            
    except Exception as e:
        print(f"❌ Error chunking {client_id}: {e}")
        return False

def list_available_clients():
    """List all clients that have briefs"""
    print("📋 Available clients with briefs:")
    
    vs = VectorStore()
    
    try:
        with vs.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT client_id, created_at FROM client_briefs ORDER BY client_id")
                clients = cur.fetchall()
        
        if clients:
            for client in clients:
                print(f"   - {client['client_id']} (brief created: {client['created_at'].strftime('%Y-%m-%d')})")
        else:
            print("   No clients found with briefs")
            
    except Exception as e:
        print(f"❌ Error listing clients: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Chunk a single client's brief into document_chunks table",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python chunk_single_client.py abundantly
  python chunk_single_client.py --list
  python chunk_single_client.py terra-collective
        """
    )
    
    parser.add_argument('client_id', nargs='?', help='Client ID to chunk')
    parser.add_argument('--list', '-l', action='store_true', help='List available clients')
    
    args = parser.parse_args()
    
    if args.list:
        list_available_clients()
        return 0
    
    if not args.client_id:
        print("❌ Error: Please provide a client_id or use --list to see available clients")
        parser.print_help()
        return 1
    
    success = chunk_client(args.client_id)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
