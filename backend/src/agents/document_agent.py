"""
Document Agent - RAG (Retrieval-Augmented Generation)
Answers questions based on uploaded documents.

User: "What's in my documents about Python?"
Agent: Searches documents → Finds relevant sections → Answers based on content
"""

import os
from typing import List, Dict, Tuple
from src.agents.base_agent import BaseAgent


class DocumentLoader:
    """
    Load and chunk documents into smaller pieces.
    
    Documents are split into chunks so we can search them efficiently.
    
    JavaScript equivalent:
    class DocumentLoader {
        loadDocuments(folderPath) {
            // Load all .txt files from folder
        }
        
        chunkText(text, chunkSize = 500) {
            // Split text into chunks
        }
    }
    """
    
    def __init__(self, documents_folder: str = "documents"):
        """
        Initialize document loader.
        
        Parameters:
            documents_folder: Folder containing .txt files
        """
        self.documents_folder = documents_folder
        self.chunks: List[Dict[str, str]] = []
    
    def load_documents(self) -> List[Dict[str, str]]:
        """
        Load all .txt files from documents folder.
        
        Returns:
            List of document chunks with metadata
        
        JavaScript equivalent:
        loadDocuments() {
            const files = fs.readdirSync(this.documentsFolder);
            const chunks = [];
            
            for (const file of files) {
                if (file.endsWith('.txt')) {
                    const content = fs.readFileSync(path, 'utf8');
                    const fileChunks = this.chunkText(content);
                    chunks.push(...fileChunks);
                }
            }
            
            return chunks;
        }
        """
        
        # Create documents folder if it doesn't exist
        if not os.path.exists(self.documents_folder):
            os.makedirs(self.documents_folder)
            print(f"📁 Created {self.documents_folder} folder")
            return []
        
        chunks = []
        
        # Get all .txt files
        txt_files = [f for f in os.listdir(self.documents_folder) if f.endswith(".txt")]
        
        if not txt_files:
            print(f"⚠️ No .txt files found in {self.documents_folder}/")
            return []
        
        # Load each file
        for filename in txt_files:
            filepath = os.path.join(self.documents_folder, filename)
            
            try:
                # Read file content
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Split into chunks
                file_chunks = self._chunk_text(content, chunk_size=500)
                
                # Add metadata
                for i, chunk in enumerate(file_chunks):
                    chunks.append({
                        "file": filename,
                        "chunk_id": i,
                        "content": chunk
                    })
                
                print(f"✅ Loaded {filename}: {len(file_chunks)} chunks")
            
            except Exception as e:
                print(f"❌ Error loading {filename}: {str(e)}")
        
        self.chunks = chunks
        return chunks
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Chunks overlap so context is preserved at boundaries.
        
        Example:
        text = "The quick brown fox jumps over the lazy dog. The dog was very lazy."
        chunks = [
            "The quick brown fox jumps over the lazy dog.",  # Chunk 1
            "over the lazy dog. The dog was very lazy."      # Chunk 2 (overlaps)
        ]
        
        Parameters:
            text: Text to split
            chunk_size: Characters per chunk
            overlap: Overlap between chunks
        
        Returns:
            List of text chunks
        
        JavaScript equivalent:
        _chunkText(text, chunkSize = 500, overlap = 50) {
            const chunks = [];
            
            for (let i = 0; i < text.length; i += chunkSize - overlap) {
                const chunk = text.substring(i, i + chunkSize);
                chunks.push(chunk.trim());
            }
            
            return chunks;
        }
        """
        
        chunks = []
        
        # Split into chunks with overlap
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i : i + chunk_size].strip()
            
            if chunk:  # Only add non-empty chunks
                chunks.append(chunk)
        
        return chunks


class SimpleEmbedder:
    """
    Simple embedding using TF-IDF-like approach.
    
    Creates a simple vector representation of text.
    Not as good as neural embeddings, but works without ML libraries.
    
    This is educational - in production you'd use:
    - Sentence-BERT
    - OpenAI embeddings
    - Ollama embeddings
    """
    
    def __init__(self):
        """Initialize embedder."""
        self.vocabulary = set()
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Split text into words.
        
        Parameters:
            text: Text to tokenize
        
        Returns:
            List of words
        
        JavaScript equivalent:
        _tokenize(text) {
            return text.toLowerCase()
                       .split(/\W+/)  // Split on non-word chars
                       .filter(w => w.length > 0);
        }
        """
        # Convert to lowercase and split by non-word characters
        words = text.lower().split()
        # Remove punctuation
        words = [w.strip(".,!?;:") for w in words]
        return [w for w in words if w]
    
    def embed(self, text: str) -> Dict[str, float]:
        """
        Create simple embedding for text.
        
        Returns a bag-of-words representation.
        
        Parameters:
            text: Text to embed
        
        Returns:
            Dictionary mapping words to frequencies
        """
        words = self._tokenize(text)
        
        # Count word frequencies
        embedding = {}
        for word in words:
            embedding[word] = embedding.get(word, 0) + 1
        
        # Normalize (divide by total)
        total = sum(embedding.values())
        if total > 0:
            embedding = {k: v / total for k, v in embedding.items()}
        
        return embedding
    
    def cosine_similarity(self, emb1: Dict[str, float], emb2: Dict[str, float]) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Returns value between 0 (completely different) and 1 (identical).
        
        Parameters:
            emb1: First embedding
            emb2: Second embedding
        
        Returns:
            float: Similarity score (0-1)
        
        JavaScript equivalent:
        cosineSimilarity(emb1, emb2) {
            let dotProduct = 0;
            let magnitude1 = 0;
            let magnitude2 = 0;
            
            // Calculate dot product and magnitudes
            const allWords = new Set([...Object.keys(emb1), ...Object.keys(emb2)]);
            
            for (const word of allWords) {
                const v1 = emb1[word] || 0;
                const v2 = emb2[word] || 0;
                
                dotProduct += v1 * v2;
                magnitude1 += v1 * v1;
                magnitude2 += v2 * v2;
            }
            
            magnitude1 = Math.sqrt(magnitude1);
            magnitude2 = Math.sqrt(magnitude2);
            
            if (magnitude1 === 0 || magnitude2 === 0) return 0;
            return dotProduct / (magnitude1 * magnitude2);
        }
        """
        
        # Get all unique words
        all_words = set(emb1.keys()) | set(emb2.keys())
        
        # Calculate dot product
        dot_product = sum(emb1.get(w, 0) * emb2.get(w, 0) for w in all_words)
        
        # Calculate magnitudes
        mag1 = sum(v ** 2 for v in emb1.values()) ** 0.5
        mag2 = sum(v ** 2 for v in emb2.values()) ** 0.5
        
        # Avoid division by zero
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        # Calculate similarity
        return dot_product / (mag1 * mag2)


class DocumentAgent(BaseAgent):
    """
    Agent for answering questions based on documents.
    
    Uses RAG pattern:
    1. Search documents for relevant chunks
    2. Pass chunks to LLM as context
    3. LLM answers based on context
    """
    
    def __init__(self, documents_folder: str = "documents"):
        """
        Initialize Document Agent.
        
        Parameters:
            documents_folder: Folder containing documents
        """
        super().__init__(
            name="Document Agent",
            description="Answer questions based on uploaded documents"
        )
        
        self.loader = DocumentLoader(documents_folder)
        self.embedder = SimpleEmbedder()
        self.chunks = []
        
        # Load documents on startup
        self._load_documents()
    
    def _load_documents(self):
        """Load and prepare documents."""
        self.chunks = self.loader.load_documents()
        print(f"📚 Total chunks loaded: {len(self.chunks)}")
    
    def process(self, message: str, **kwargs) -> str:
        """
        Answer question based on documents.
        
        Flow:
        1. Search for relevant document chunks
        2. Combine chunks as context
        3. Use LLM to answer based on context
        
        Parameters:
            message: User's question
        
        Returns:
            str: Answer based on documents
        
        JavaScript equivalent:
        async process(message) {
            try {
                // Search documents
                const relevant = this.searchDocuments(message, topK: 3);
                
                if (relevant.length === 0) {
                    return "No relevant documents found.";
                }
                
                // Combine context
                const context = relevant.map(r => r.content).join("\n\n");
                
                // Ask LLM
                const prompt = `
                    Context:
                    ${context}
                    
                    Question: ${message}
                `;
                
                return await this.generateResponse(prompt);
            } catch (error) {
                return `Error: ${error.message}`;
            }
        }
        """
        
        try:
            if not self.chunks:
                return "No documents loaded. Please upload documents to the 'documents' folder."
            
            # Search for relevant chunks
            relevant_chunks = self._search_documents(message, top_k=3)
            
            if not relevant_chunks:
                return "I couldn't find relevant information in the documents. Try asking about different topics."
            
            # Combine chunks as context
            context = "\n\n".join([chunk["content"] for chunk in relevant_chunks])
            
            # Build prompt with context
            prompt = f"""You are a helpful assistant answering questions based on documents.

DOCUMENTS CONTEXT:
{context}

USER QUESTION: {message}

Answer the question based only on the documents provided. If you can't find the answer, say "I don't have that information in the documents." Be concise and helpful."""
            
            # Generate response using LLM
            response = self.generate_response(prompt)
            
            return response
        
        except Exception as e:
            return f"Error processing document query: {str(e)}"
    
    def _search_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search documents for chunks similar to query.
        
        Parameters:
            query: Search query
            top_k: Number of top results to return
        
        Returns:
            List of most relevant chunks
        
        JavaScript equivalent:
        _searchDocuments(query, topK = 3) {
            const queryEmb = this.embedder.embed(query);
            
            const scores = this.chunks.map(chunk => ({
                ...chunk,
                score: this.embedder.cosineSimilarity(
                    queryEmb,
                    this.embedder.embed(chunk.content)
                )
            }));
            
            // Sort by score and return top K
            return scores
                .sort((a, b) => b.score - a.score)
                .slice(0, topK);
        }
        """
        
        # Embed the query
        query_embedding = self.embedder.embed(query)
        
        # Score all chunks
        scored_chunks = []
        for chunk in self.chunks:
            # Embed chunk content
            chunk_embedding = self.embedder.embed(chunk["content"])
            
            # Calculate similarity
            score = self.embedder.cosine_similarity(query_embedding, chunk_embedding)
            
            # Store with score
            scored_chunks.append({
                **chunk,
                "score": score
            })
        
        # Sort by score (highest first) and get top K
        sorted_chunks = sorted(scored_chunks, key=lambda x: x["score"], reverse=True)
        
        return sorted_chunks[:top_k]


# Example usage:
if __name__ == "__main__":
    agent = DocumentAgent()
    
    print(f"Agent: {agent.name}")
    print(f"Description: {agent.description}")
    print(f"Loaded chunks: {len(agent.chunks)}")
    print()
    
    # Test (will fail if no documents)
    print("Test: 'What is machine learning?'")
    response = agent.process("What is machine learning?")
    print(f"Response: {response}")