# chatGIT code explanation

## high-level overview

chatGIT is a code analysis tool that combines:
- **vector search** (finding similar code using embeddings)
- **pagerank** (ranking important files/functions like google ranks websites)
- **LLM chat** (using groq's API to answer questions about code)
- **code enhancement** (adding line numbers and file locations to responses)

## file structure

```
api.py                    # main backend server (fastAPI)
snippet_extractor.py      # finds where code snippets are located
pagerank_analyzer.py      # calculates importance scores
dependency_analyzer.py    # builds call graphs
rag_101/retriever.py      # handles embeddings and AST parsing
chatgit-react/frontend/   # react frontend ui
```

## how it works (step by step)

### step 1: loading a repository

when you paste a github URL:

1. **clone the repo** - downloads it to `~/Documents/github_repos/`
2. **read all files** - loads .py, .js, .ts, .java, .cpp, etc.
3. **build file tree** - creates a markdown structure showing folders/files
4. **parse AST** - abstract syntax tree = code broken down into functions/classes
5. **run pagerank** - calculates which files/functions are most important
6. **create embeddings** - converts code into vectors (numbers) for search
7. **store everything** - keeps it in memory for fast access

### step 2: asking questions

when you ask a question about the code:

1. **search** - finds 20 most similar code chunks using vector similarity
2. **re-rank** - sorts them by relevance + pagerank score
3. **diversify** - picks max 3 chunks from same file (avoid repetition)
4. **build context** - creates a prompt with the most relevant code
5. **ask LLM** - sends to groq API (uses llama 3.1 model)
6. **enhance response** - adds line numbers and file locations to code blocks
7. **return answer** - shows in chat with proper formatting

### step 3: code enhancement

when the LLM returns code in its response:

1. **detect code blocks** - finds ```python or ```javascript blocks
2. **search for location** - uses similarity matching to find where it exists
3. **extract line numbers** - gets the actual line numbers from the file
4. **add metadata** - shows filename, line range, confidence score
5. **display with context** - shows 2 lines before/after for context

## key concepts explained

### vector embeddings

- converts text/code into a list of numbers (vector)
- similar code has similar vectors
- this lets us "search by meaning" not just keywords
- uses BAAI/bge-small-en-v1.5 model from huggingface

### pagerank

- algorithm that ranks importance (used by google)
- applied to code: files/functions that are used by many others = important
- helps prioritize which code to show in context
- calculated using networkx library

### RAG (retrieval augmented generation)

- don't send entire codebase to LLM (too big)
- instead: retrieve relevant parts, then generate answer
- this is what llamaindex helps us do
- much faster and cheaper than alternatives

### call graph

- shows which functions call which other functions
- helps understand code flow
- visualized using vis-network in frontend

## main components

### api.py (backend server)

this is the main file that handles everything:

```python
# think of this as the "brain" - it coordinates everything

# main endpoints:
/api/load_repo          # clones and analyzes a repository
/api/chat               # handles Q&A about code
/api/pagerank/files     # returns top 10 important files
/api/pagerank/functions # returns top 10 important functions
/api/call_graph         # returns function call relationships
```

**key flow in /api/chat endpoint:**

1. user sends a question
2. search vector index for relevant code (similarity_top_k=20)
3. score each result by: `base_score * (1 + pagerank * 10)`
4. pick top 8 results, max 3 per file
5. build context with ~6000 tokens
6. send to groq LLM (temperature=0.1 for factual responses)
7. enhance code blocks with line numbers
8. return answer

**session management:**

- everything stored in `session` object (global variable)
- cleared when you load a new repo
- in production you'd use redis or database

### snippet_extractor.py

finds where code appears in the repository:

```python
# the problem: LLM returns code, but doesn't know where it came from
# the solution: search through files to find matching code

class ImprovedCodeSnippetExtractor:
    
    def find_code_location(self, code_snippet):
        # normalize: remove line numbers, clean whitespace
        # search: slide through each file looking for matches
        # score: use difflib.SequenceMatcher for similarity
        # threshold: only accept 80%+ matches
        # return: file path, line numbers, confidence
```

**how it works:**

1. gets code from LLM response
2. cleans it (removes existing line numbers)
3. searches all repo files
4. uses sequence matching (like git diff)
5. finds best match with 80%+ confidence
6. returns location with line numbers

**example:**
```
Input: "def hello():\n    print('hi')"
Output: {
    'file': 'src/utils.py',
    'start_line': 42,
    'end_line': 43,
    'confidence': 0.95
}
```

### pagerank_analyzer.py

calculates importance using graph algorithms:

```python
# two-pass system for accuracy

# pass 1: collect all functions
# - walks through all files
# - extracts function definitions
# - builds a map: function_name -> [file1::func1, file2::func1, ...]

# pass 2: build call graph
# - finds where functions are called
# - matches calls to definitions (uses the map from pass 1)
# - creates edges: caller -> callee

# then: run pagerank
# - uses networkx.pagerank algorithm
# - alpha=0.85 (standard pagerank damping)
# - returns sorted list of (name, score) tuples
```

**graphs maintained:**

1. `file_graph` - files importing other files
2. `function_graph` - functions calling other functions
3. `import_graph` - all imports (including external libs)

**filtering:**

- only returns actual files (not modules like 'os' or 'sys')
- checks file extensions (.py, .js, .ts, etc.)
- fallback: if filtering removes everything, shows non-module results

### dependency_analyzer.py

builds function call graphs:

```python
# simpler than pagerank - just finds "who calls who"

# for python:
# - uses ast.parse to get function definitions
# - finds ast.Call nodes to detect function calls
# - creates directed graph: caller -> callee

# for javascript/typescript:
# - uses regex patterns
# - looks for: function foo(), const bar = () => {...}
# - finds calls: foo()

# output: networkx graph for visualization
```

### frontend (react)

**Dashboard.jsx** - shows repository stats and pagerank

```javascript
// fetches data from API endpoints
// displays in tabs: FILES | FUNCTIONS | MODULES
// shows top 10 of each ranked by importance
```

**Chat.jsx** - handles Q&A interface

```javascript
// sends messages to /api/chat
// renders responses with react-markdown
// uses syntax-highlighter for code blocks
// detects line numbers and uses startingLineNumber prop
```

**CallGraph.jsx** - visualizes function relationships

```javascript
// uses vis-network library
// nodes = functions
// edges = calls
// interactive: click nodes to see dependencies
```

## important details

### why two pagerank passes?

**problem:** if you parse calls before you know all functions, you can't connect them

**solution:**
- pass 1: collect ALL function definitions across entire repo
- pass 2: when you find a call, look it up in the collected definitions

**example:**
```python
# file1.py
def helper():
    pass

# file2.py
def main():
    helper()  # <-- pass 2 can now connect this to file1.py::helper
```

### why filter by file extensions?

**problem:** pagerank graph includes module names like 'os', 'sys', 're'

**solution:** only show nodes ending with .py, .js, .ts, etc.

**fallback:** if that removes everything, show anything except known external libs

### why limit to 3 chunks per file?

**problem:** if one file matches query really well, all 8 results might be from it

**solution:** max 3 chunks per file ensures diversity

**benefit:** LLM sees information from multiple relevant files

### why temperature=0.1?

**low temperature** = more deterministic, factual responses

**high temperature** = more creative, varied responses

for code Q&A we want facts, not creativity

### why enhance_code is optional?

**with enhancement:**
- finds exact file locations
- adds line numbers
- shows context
- takes extra time (~200ms per code block)

**without enhancement:**
- just shows code as-is
- faster responses
- still useful for general questions

## common issues and fixes

### empty pagerank results

**symptom:** no files/functions showing up in dashboard

**causes:**
1. filtering too strict (file extensions don't match)
2. no edges in graph (no imports/calls detected)
3. pagerank failed silently

**fixes:**
- added fallback logic (show unfiltered if filtered is empty)
- check for 0-degree nodes (degree > 0 filter)
- added logging to debug

### line numbers not showing

**symptom:** code blocks missing line numbers in chat

**cause:** frontend was disabling syntax-highlighter line numbers when backend added them

**fix:** 
- extract starting line number from backend format
- strip line numbers from code text
- pass to syntax-highlighter with `startingLineNumber` prop

### slow responses

**symptom:** chat takes 10+ seconds

**causes:**
1. retrieving too many chunks (similarity_top_k too high)
2. context too large (hitting token limits)
3. LLM model slow

**fixes:**
- balanced retrieval: 20 chunks, pick top 8
- limit context to 6000 tokens
- use groq (fastest LLM provider)

## environment setup

### required environment variables

```bash
GROQ_API_KEY=your_api_key_here   # get from console.groq.com
```

### required dependencies

**backend:**
```
fastapi
uvicorn
llama-index
groq
networkx
python-dotenv
langchain
sentence-transformers
```

**frontend:**
```
react
axios
react-markdown
react-syntax-highlighter
vis-network
```

## extending the system

### adding support for a new language

1. add file extension to supported list
2. add regex patterns for function detection
3. add import patterns
4. test pagerank calculation

### adding a new pagerank metric

1. create method in `CodePageRankAnalyzer`
2. add API endpoint in `api.py`
3. add frontend component to display it
4. wire up in Dashboard.jsx

### changing embedding model

1. update `load_embedding_model()` in `rag_101/retriever.py`
2. clear existing embeddings
3. re-index repositories

## debugging tips

### enable verbose logging

```python
# in api.py
print(f"[DEBUG] context length: {len(context_block)}")
print(f"[DEBUG] top results: {[r['snippet'].metadata.get('file_name') for r in top_results]}")
```

### inspect vector search results

```python
# in /api/chat endpoint, after retrieval
for i, item in enumerate(results[:5]):
    print(f"Result {i}: {item.metadata.get('file_name')} - score: {item.score}")
```

### check pagerank scores

```python
# in pagerank_analyzer.py
ranked = self.get_file_pagerank()
for file, score in ranked[:10]:
    print(f"{file}: {score:.4f}")
```

### view call graph structure

```python
# in dependency_analyzer.py
print(f"Nodes: {list(self.graph.nodes())[:10]}")
print(f"Edges: {list(self.graph.edges())[:10]}")
```

## performance characteristics

### repository loading

- small repo (10-50 files): ~5-10 seconds
- medium repo (100-500 files): ~20-40 seconds
- large repo (1000+ files): ~1-2 minutes

**bottlenecks:**
1. git clone (network speed)
2. embedding generation (cpu intensive)
3. AST parsing (python ast module)

### chat responses

- typical: 2-5 seconds
- with enhancement: 3-6 seconds
- complex questions: 5-10 seconds

**bottlenecks:**
1. vector search (acceptable)
2. LLM inference (using groq = fast)
3. code enhancement (similarity matching)

### memory usage

- base: ~200mb
- small repo: +100mb
- medium repo: +500mb
- large repo: +2GB

**mostly from:**
1. vector embeddings (largest)
2. networkx graphs
3. cached file contents

## best practices

### for users

1. **ask specific questions** - better retrieval results
2. **mention file names** - helps narrow search
3. **use technical terms** - better embedding matches
4. **ask follow-ups** - conversation history helps

### for developers

1. **add error logging** - helps debug issues
2. **validate inputs** - prevent crashes
3. **use type hints** - easier to understand
4. **add fallbacks** - graceful degradation
5. **test with different repos** - find edge cases

## future improvements

### possible enhancements

1. **multi-repo support** - analyze dependencies across repos
2. **semantic code search** - search by natural language
3. **automated refactoring suggestions** - using pagerank + LLM
4. **git history analysis** - find frequently changed files
5. **caching** - persist analysis results
6. **streaming responses** - show LLM output as it generates
7. **better code location** - use tree-sitter for precise parsing
8. **collaborative features** - share analyses with team

### scaling considerations

1. **database** - move from in-memory to postgres/mongo
2. **redis** - cache embeddings and pagerank results
3. **celery** - background job queue for analysis
4. **docker** - containerize for deployment
5. **kubernetes** - horizontal scaling
6. **cdn** - serve frontend assets faster

## conclusion

chatGIT combines multiple techniques to create an intelligent code assistant:

- **RAG** ensures relevant context
- **PageRank** prioritizes important code
- **Enhancement** makes responses precise
- **Multi-language** works across ecosystems

the key insight: don't just search code, **rank** it by importance and **present** it clearly.
