#!/usr/bin/env python3
"""
Save client brief chunks for all clients
"""
from vector_store import VectorStore
import psycopg2

def save_all_client_brief_chunks():
    """Save client brief chunks for all clients that have briefs"""
    print("🚀 Saving client brief chunks for all clients")
    
    vs = VectorStore()
    
    # Get all clients that have briefs
    with vs.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT client_id FROM client_briefs ORDER BY client_id")
            clients = [row['client_id'] for row in cur.fetchall()]
    
    print(f"Found {len(clients)} clients with briefs: {', '.join(clients)}")
    
    success_count = 0
    failed_count = 0
    
    for client_id in clients:
        print(f"\n📋 Processing {client_id}...")
        
        try:
            success = vs.save_client_brief_chunks(client_id)
            if success:
                print(f"✅ Successfully saved chunks for {client_id}")
                success_count += 1
            else:
                print(f"❌ Failed to save chunks for {client_id}")
                failed_count += 1
        except Exception as e:
            print(f"❌ Error processing {client_id}: {e}")
            failed_count += 1
    
    print(f"\n📊 Summary:")
    print(f"  ✅ Successful: {success_count}")
    print(f"  ❌ Failed: {failed_count}")
    print(f"  📈 Success rate: {success_count/(success_count+failed_count)*100:.1f}%")
    
    return success_count > 0

if __name__ == "__main__":
    success = save_all_client_brief_chunks()
    exit(0 if success else 1)
