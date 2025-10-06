"""
Core Email Handler with RAG and Hallucination Prevention
"""
from typing import Dict, List, Optional, Tuple
import logging
from openai import OpenAI
from anthropic import Anthropic

from config import (
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    SYSTEM_PROMPT_TEMPLATE,
    RELEVANCE_CHECK_PROMPT,
    VERIFICATION_PROMPT,
    TOP_K_RESULTS,
    CONFIDENCE_THRESHOLD
)
from vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailHandler:
    """Handles customer service emails with RAG and grounding"""
    
    def __init__(self, llm_provider: str = "openai"):
        """
        Initialize email handler
        
        Args:
            llm_provider: "openai" or "anthropic"
        """
        self.vector_store = VectorStore()
        self.llm_provider = llm_provider
        
        if llm_provider == "openai":
            self.llm_client = OpenAI(api_key=OPENAI_API_KEY)
            self.model = "gpt-4o"
        elif llm_provider == "anthropic":
            self.llm_client = Anthropic(api_key=ANTHROPIC_API_KEY)
            self.model = "claude-3-5-sonnet-20241022"
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")
    
    def extract_query(self, email_content: str) -> str:
        """
        Extract the main query/question from email content
        For now, returns the email content as-is
        Could be enhanced with query extraction logic
        """
        # Simple implementation - use email as query
        # Could enhance with LLM-based query extraction
        return email_content.strip()
    
    def check_relevance(self, query: str, context: str) -> Tuple[bool, str]:
        """
        Check if the retrieved context can answer the query
        
        Returns:
            Tuple of (is_relevant, reason)
        """
        try:
            prompt = RELEVANCE_CHECK_PROMPT.format(context=context, query=query)
            
            if self.llm_provider == "openai":
                response = self.llm_client.chat.completions.create(
                    model="gpt-4o-mini",  # Use cheaper model for checks
                    messages=[
                        {"role": "system", "content": "You are a relevance checker. Answer concisely."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )
                answer = response.choices[0].message.content.strip()
            else:  # anthropic
                response = self.llm_client.messages.create(
                    model="claude-3-5-haiku-20241022",  # Use cheaper model
                    max_tokens=200,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )
                answer = response.content[0].text.strip()
            
            is_relevant = answer.lower().startswith("yes")
            return is_relevant, answer
            
        except Exception as e:
            logger.error(f"Error checking relevance: {e}")
            # Default to assuming relevance to avoid blocking
            return True, "Error checking relevance"
    
    def verify_response(self, response: str, context: str) -> Tuple[bool, str]:
        """
        Verify that the response only contains information from context
        
        Returns:
            Tuple of (is_grounded, explanation)
        """
        try:
            prompt = VERIFICATION_PROMPT.format(context=context, response=response)
            
            if self.llm_provider == "openai":
                verification = self.llm_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a fact checker. Be strict."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )
                answer = verification.choices[0].message.content.strip()
            else:  # anthropic
                verification = self.llm_client.messages.create(
                    model="claude-3-5-haiku-20241022",
                    max_tokens=300,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )
                answer = verification.content[0].text.strip()
            
            is_grounded = answer.lower().startswith("yes")
            return is_grounded, answer
            
        except Exception as e:
            logger.error(f"Error verifying response: {e}")
            # Default to assuming grounded to avoid blocking
            return True, "Error during verification"
    
    def generate_response(self, query: str, context: str, client_name: str) -> str:
        """
        Generate response using LLM with strong grounding prompt
        
        Args:
            query: The customer's question
            context: Retrieved document context
            client_name: Name of the client for personalization
            
        Returns:
            Generated response
        """
        try:
            system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
                client_name=client_name,
                context=context,
                query=query
            )
            
            if self.llm_provider == "openai":
                response = self.llm_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Please answer this customer question: {query}"}
                    ],
                    temperature=0.3  # Lower temperature for more consistent responses
                )
                return response.choices[0].message.content.strip()
                
            else:  # anthropic
                response = self.llm_client.messages.create(
                    model=self.model,
                    max_tokens=1500,
                    messages=[
                        {"role": "user", "content": system_prompt}
                    ],
                    temperature=0.3
                )
                return response.content[0].text.strip()
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble generating a response right now. Please contact our support team directly."
    
    def handle_email(
        self,
        email_content: str,
        client_id: str,
        client_name: str,
        enable_verification: bool = True
    ) -> Dict:
        """
        Main handler for processing customer emails
        
        Args:
            email_content: The email text from customer
            client_id: Client identifier for filtering knowledge base
            client_name: Client name for response personalization
            enable_verification: Enable post-generation verification
            
        Returns:
            Dictionary with response and metadata
        """
        logger.info(f"Processing email for client_id={client_id}")
        
        # Step 1: Extract query
        query = self.extract_query(email_content)
        logger.info(f"Extracted query: {query[:100]}...")
        
        # Step 2: Retrieve relevant documents for this client
        relevant_docs = self.vector_store.search_documents(
            query=query,
            client_id=client_id,
            top_k=TOP_K_RESULTS
        )
        
        if not relevant_docs:
            logger.warning(f"No relevant documents found for client_id={client_id}")
            return {
                "success": False,
                "response": "I don't have access to information that can answer your question. Let me connect you with someone who can help.",
                "documents_found": 0,
                "confidence": 0.0,
                "metadata": {
                    "reason": "no_documents_found"
                }
            }
        
        logger.info(f"Found {len(relevant_docs)} relevant documents")
        
        # Step 3: Format context with document references
        context_parts = []
        for idx, doc in enumerate(relevant_docs, 1):
            doc_content = doc.get('content', '')
            similarity = doc.get('similarity', 0)
            context_parts.append(f"[Doc {idx}] (Similarity: {similarity:.2f})\n{doc_content}\n")
        
        context = "\n---\n".join(context_parts)
        
        # Step 4: Check relevance
        is_relevant, relevance_reason = self.check_relevance(query, context)
        
        if not is_relevant:
            logger.warning(f"Context not relevant: {relevance_reason}")
            return {
                "success": False,
                "response": "I don't have that specific information in our resources. Let me connect you with someone who can help.",
                "documents_found": len(relevant_docs),
                "confidence": 0.0,
                "metadata": {
                    "reason": "context_not_relevant",
                    "relevance_check": relevance_reason
                }
            }
        
        # Step 5: Generate response
        response = self.generate_response(query, context, client_name)
        
        # Step 6: Verify response (optional post-generation filter)
        is_grounded = True
        verification_result = "skipped"
        
        if enable_verification:
            is_grounded, verification_result = self.verify_response(response, context)
            
            if not is_grounded:
                logger.warning(f"Response not grounded: {verification_result}")
                return {
                    "success": False,
                    "response": "I'm not confident I can answer this accurately based on our documentation. Let me connect you with someone who can help.",
                    "documents_found": len(relevant_docs),
                    "confidence": 0.0,
                    "metadata": {
                        "reason": "verification_failed",
                        "verification": verification_result
                    }
                }
        
        # Step 7: Calculate confidence based on similarity scores
        avg_similarity = sum(doc.get('similarity', 0) for doc in relevant_docs) / len(relevant_docs)
        
        return {
            "success": True,
            "response": response,
            "documents_found": len(relevant_docs),
            "confidence": avg_similarity,
            "metadata": {
                "query": query,
                "documents": [
                    {
                        "id": doc.get('id'),
                        "similarity": doc.get('similarity'),
                        "metadata": doc.get('metadata')
                    }
                    for doc in relevant_docs
                ],
                "relevance_check": relevance_reason,
                "verification": verification_result,
                "is_grounded": is_grounded
            }
        }
