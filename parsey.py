import os
import re
import json

def parse_and_save_claude_response(text: str, out_path='parsed_output.json'):
    """
    Parse Claude's response and save the parsed data to JSON file.
    Combines parsing and saving functionality in one function.
    """
    blocks = text.strip().split('---')
    parsed = []

    for block in blocks:
        lines = block.strip().splitlines()
        if not lines:
            continue

        header = lines[0].strip()
        match = re.match(r"#(.+?)/(.+)", header)
        if not match:
            continue

        project = match.group(1).strip()
        filename = match.group(2).strip()
        path = f"{project}/{filename}"
        ext = os.path.splitext(filename)[1].replace('.', '').lower()

        content = '\n'.join(lines[1:]).strip() + '\n'

        parsed.append({
            "path": path,
            "filename": filename,
            "project": project,
            "language": ext,
            "content": content
        })

    # Save to JSON file
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved parsed data to {out_path}")
    
    return parsed

# if __name__ == "__main__":
#     # Paste Claude's response here as a raw multi-line string
#     raw_text = '''
# # ai_powershell_automation/main.py
# """
# Main script for AI-powered code generation using local Ollama server.
# Handles user interaction and orchestrates the entire workflow.
# """

# import sys
# import os
# from ai_client import OllamaClient
# from parser import CodeBlockParser
# from file_creator import FileCreator

# def get_user_prompt():
#     """Get natural language prompt from user."""
#     print("🤖 AI Code Generator")
#     print("=" * 50)
#     prompt = input("Enter your project description: ").strip()
    
#     if not prompt:
#         print("❌ Error: Please provide a valid prompt.")
#         return None
    
#     return prompt

# def generate_folder_name(prompt):
#     """Generate folder name from first three words of prompt."""
#     words = prompt.lower().split()[:3]
#     # Clean words to be filesystem-safe
#     clean_words = []
#     for word in words:
#         clean_word = ''.join(c for c in word if c.isalnum())
#         if clean_word:
#             clean_words.append(clean_word)
    
#     return '_'.join(clean_words) if clean_words else 'ai_generated_project'

# def main():
#     """Main application flow."""
#     try:
#         # Get user prompt
#         user_prompt = get_user_prompt()
#         if not user_prompt:
#             return
        
#         print(f"\n🔄 Processing: '{user_prompt}'")
        
#         # Initialize components
#         ollama_client = OllamaClient()
#         parser = CodeBlockParser()
#         file_creator = FileCreator()
        
#         # Send request to Ollama
#         print("📡 Sending request to Ollama server...")
#         response_text = ollama_client.generate_code(user_prompt)
        
#         if not response_text:
#             print("❌ Failed to get response from Ollama server.")
#             return
        
#         # Parse code blocks from response
#         print("🔍 Parsing code blocks...")
#         files_data = parser.parse_code_blocks(response_text)
        
#         if not files_data:
#             print("⚠️  No code blocks found in response.")
#             print("Raw response:")
#             print(response_text[:500] + "..." if len(response_text) > 500 else response_text)
#             return
        
#         # Generate folder name and create files
#         folder_name = generate_folder_name(user_prompt)
#         print(f"📁 Creating project in folder: {folder_name}")
        
#         success = file_creator.create_project(folder_name, files_data)
        
#         if success:
#             print(f"\n✅ Project created successfully!")
#             print(f"📂 Location: ./{folder_name}/")
#             print(f"📄 Files created: {len(files_data)}")
#             for filename in files_data.keys():
#                 print(f"   - {filename}")
#         else:
#             print("❌ Failed to create project files.")
    
#     except KeyboardInterrupt:
#         print("\n\n👋 Goodbye!")
#     except Exception as e:
#         print(f"❌ Unexpected error: {str(e)}")

# if __name__ == "__main__":
#     main()

# ---

# # ai_powershell_automation/ai_client.py
# """
# Handles communication with the local Ollama server.
# Sends HTTP requests and manages responses.
# """

# import requests
# import json
# import time

# class OllamaClient:
#     def __init__(self, base_url="http://localhost:11434", model="deepseek-coder"):
#         """Initialize Ollama client with server URL and model."""
#         self.base_url = base_url
#         self.model = model
#         self.generate_url = f"{base_url}/api/generate"
#         self.timeout = 120  # 2 minutes timeout
    
#     def check_server_health(self):
#         """Check if Ollama server is running and accessible."""
#         try:
#             health_url = f"{self.base_url}/api/tags"
#             response = requests.get(health_url, timeout=5)
#             return response.status_code == 200
#         except requests.RequestException:
#             return False
    
#     def generate_code(self, prompt):
#         """
#         Send code generation request to Ollama server.
#         Returns the complete response text or None if failed.
#         """
#         if not self.check_server_health():
#             print("❌ Cannot connect to Ollama server. Please ensure:")
#             print("   - Ollama is installed and running")
#             print("   - Server is accessible at http://localhost:11434")
#             print("   - Deepseek-Coder model is available")
#             return None
        
#         # Enhanced prompt for better code generation
#         enhanced_prompt = f"""
# Generate a complete project for: {prompt}

# Please provide the response with clear file structure using markdown code blocks.
# Format each file like this:
# ```filename.ext
# [file content here]
# ```

# Include all necessary files (HTML, CSS, JavaScript, Python, etc.) with proper file extensions.
# Make the code production-ready and well-commented.
# """
        
#         payload = {
#             "model": self.model,
#             "prompt": enhanced_prompt,
#             "stream": False,
#             "options": {
#                 "temperature": 0.7,
#                 "top_k": 40,
#                 "top_p": 0.9
#             }
#         }
        
#         try:
#             print(f"🔗 Connecting to {self.generate_url}")
            
#             response = requests.post(
#                 self.generate_url,
#                 json=payload,
#                 timeout=self.timeout,
#                 headers={'Content-Type': 'application/json'}
#             )
            
#             response.raise_for_status()
            
#             result = response.json()
            
#             if 'response' in result:
#                 return result['response']
#             else:
#                 print("❌ Unexpected response format from Ollama")
#                 print(f"Response keys: {list(result.keys())}")
#                 return None
                
#         except requests.exceptions.Timeout:
#             print(f"⏰ Request timed out after {self.timeout} seconds")
#             return None
#         except requests.exceptions.ConnectionError:
#             print("❌ Connection error. Is Ollama server running?")
#             return None
#         except requests.exceptions.HTTPError as e:
#             print(f"❌ HTTP error: {e}")
#             return None
#         except json.JSONDecodeError:
#             print("❌ Invalid JSON response from server")
#             return None
#         except Exception as e:
#             print(f"❌ Unexpected error: {str(e)}")
#             return None

# ---

# # ai_powershell_automation/parser.py
# """
# Parses markdown code blocks from Ollama response.
# Extracts filenames and corresponding code content.
# """

# import re
# from typing import Dict, Optional

# class CodeBlockParser:
#     def __init__(self):
#         """Initialize the parser with regex patterns."""
#         # Pattern to match markdown code blocks with optional language/filename
#         self.code_block_pattern = re.compile(
#             r'```(?:(\w+(?:\.\w+)*)|(\w+))?\s*\n(.*?)```',
#             re.DOTALL | re.MULTILINE
#         )
        
#         # Pattern to match filename comments in code
#         self.filename_comment_pattern = re.compile(
#             r'(?:#|//|<!--)\s*(?:filename|file):\s*([^\s\n]+)',
#             re.IGNORECASE
#         )
    
#     def extract_filename_from_content(self, content: str, language: str = "") -> Optional[str]:
#         """Extract filename from code content comments."""
#         # Look for filename comments
#         match = self.filename_comment_pattern.search(content)
#         if match:
#             return match.group(1).strip()
        
#         # Default filenames based on language
#         default_extensions = {
#             'html': 'index.html',
#             'css': 'styles.css',
#             'javascript': 'script.js',
#             'js': 'script.js',
#             'python': 'main.py',
#             'py': 'main.py',
#             'java': 'Main.java',
#             'cpp': 'main.cpp',
#             'c': 'main.c',
#             'php': 'index.php',
#             'ruby': 'main.rb',
#             'go': 'main.go',
#             'rust': 'main.rs',
#             'swift': 'main.swift',
#             'kotlin': 'main.kt',
#             'typescript': 'main.ts',
#             'ts': 'main.ts'
#         }
        
#         return default_extensions.get(language.lower(), f"file.{language.lower()}" if language else "code.txt")
    
#     def clean_code_content(self, content: str) -> str:
#         """Clean and prepare code content for file writing."""
#         # Remove filename comments
#         content = self.filename_comment_pattern.sub('', content)
        
#         # Strip leading/trailing whitespace but preserve internal formatting
#         content = content.strip()
        
#         # Ensure file ends with newline
#         if content and not content.endswith('\n'):
#             content += '\n'
        
#         return content
    
#     def parse_code_blocks(self, response_text: str) -> Dict[str, str]:
#         """
#         Parse markdown code blocks from Ollama response.
#         Returns a dictionary mapping filenames to their content.
#         """
#         files_data = {}
        
#         if not response_text:
#             return files_data
        
#         # Find all code blocks
#         matches = self.code_block_pattern.findall(response_text)
        
#         for match in matches:
#             filename_or_lang = match[0] or match[1] or ""
#             content = match[2]
            
#             if not content.strip():
#                 continue
            
#             # Determine if the first capture group is a filename or language
#             if '.' in filename_or_lang and not filename_or_lang.startswith('.'):
#                 # Likely a filename
#                 filename = filename_or_lang
#                 language = filename.split('.')[-1] if '.' in filename else ""
#             else:
#                 # Likely a language identifier
#                 language = filename_or_lang
#                 filename = self.extract_filename_from_content(content, language)
            
#             # Clean the content
#             clean_content = self.clean_code_content(content)
            
#             # Handle duplicate filenames
#             original_filename = filename
#             counter = 1
#             while filename in files_data:
#                 name, ext = os.path.splitext(original_filename)
#                 filename = f"{name}_{counter}{ext}"
#                 counter += 1
            
#             files_data[filename] = clean_content
#             print(f"   📄 Parsed: {filename} ({len(clean_content)} chars)")
        
#         return files_data
    
#     def detect_project_type(self, files_data: Dict[str, str]) -> str:
#         """Detect the type of project based on file extensions."""
#         extensions = set()
#         for filename in files_data.keys():
#             if '.' in filename:
#                 ext = filename.split('.')[-1].lower()
#                 extensions.add(ext)
        
#         if 'html' in extensions:
#             return "Web Application"
#         elif 'py' in extensions:
#             return "Python Project"
#         elif 'js' in extensions and 'json' in extensions:
#             return "Node.js Project"
#         elif 'java' in extensions:
#             return "Java Project"
#         elif 'cpp' in extensions or 'c' in extensions:
#             return "C/C++ Project"
#         else:
#             return "Mixed Project"

# ---

# # ai_powershell_automation/file_creator.py
# """
# Handles creation of project directories and files.
# Manages file system operations with proper error handling.
# """

# import os
# import shutil
# from typing import Dict

# class FileCreator:
#     def __init__(self):
#         """Initialize file creator."""
#         self.created_files = []
#         self.created_dirs = []
    
#     def sanitize_filename(self, filename: str) -> str:
#         """Sanitize filename to be filesystem-safe."""
#         # Remove or replace invalid characters
#         invalid_chars = '<>:"/\\|?*'
#         for char in invalid_chars:
#             filename = filename.replace(char, '_')
        
#         # Remove leading/trailing dots and spaces
#         filename = filename.strip('. ')
        
#         # Ensure filename is not empty
#         if not filename:
#             filename = "untitled"
        
#         return filename
    
#     def create_directory(self, dir_path: str) -> bool:
#         """Create directory if it doesn't exist."""
#         try:
#             if os.path.exists(dir_path):
#                 print(f"⚠️  Directory {dir_path} already exists.")
                
#                 # Ask user if they want to continue
#                 response = input("Do you want to continue and potentially overwrite files? (y/N): ").strip().lower()
#                 if response not in ['y', 'yes']:
#                     print("Operation cancelled by user.")
#                     return False
                
#                 # Backup existing directory
#                 backup_path = f"{dir_path}_backup_{int(time.time())}"
#                 print(f"📦 Creating backup at: {backup_path}")
#                 shutil.copytree(dir_path, backup_path)
            
#             os.makedirs(dir_path, exist_ok=True)
#             self.created_dirs.append(dir_path)
#             print(f"📁 Created directory: {dir_path}")
#             return True
            
#         except PermissionError:
#             print(f"❌ Permission denied creating directory: {dir_path}")
#             return False
#         except Exception as e:
#             print(f"❌ Error creating directory {dir_path}: {str(e)}")
#             return False
    
#     def write_file(self, file_path: str, content: str) -> bool:
#         """Write content to file with proper error handling."""
#         try:
#             # Create parent directories if they don't exist
#             parent_dir = os.path.dirname(file_path)
#             if parent_dir and not os.path.exists(parent_dir):
#                 os.makedirs(parent_dir, exist_ok=True)
            
#             # Write file
#             with open(file_path, 'w', encoding='utf-8') as f:
#                 f.write(content)
            
#             self.created_files.append(file_path)
#             file_size = len(content.encode('utf-8'))
#             print(f"   ✅ Created: {os.path.basename(file_path)} ({file_size} bytes)")
#             return True
            
#         except PermissionError:
#             print(f"❌ Permission denied writing file: {file_path}")
#             return False
#         except UnicodeEncodeError:
#             print(f"❌ Unicode encoding error for file: {file_path}")
#             return False
#         except Exception as e:
#             print(f"❌ Error writing file {file_path}: {str(e)}")
#             return False
    
#     def create_project(self, folder_name: str, files_data: Dict[str, str]) -> bool:
#         """
#         Create complete project with folder and all files.
#         Returns True if successful, False otherwise.
#         """
#         if not files_data:
#             print("❌ No files to create.")
#             return False
        
#         # Sanitize folder name
#         folder_name = self.sanitize_filename(folder_name)
        
#         # Create main project directory
#         if not self.create_directory(folder_name):
#             return False
        
#         success_count = 0
#         total_files = len(files_data)
        
#         # Create each file
#         for filename, content in files_data.items():
#             sanitized_filename = self.sanitize_filename(filename)
#             file_path = os.path.join(folder_name, sanitized_filename)
            
#             if self.write_file(file_path, content):
#                 success_count += 1
#             else:
#                 print(f"⚠️  Failed to create: {sanitized_filename}")
        
#         # Create a README.md with project info
#         readme_content = f"""# {folder_name.replace('_', ' ').title()}

# This project was generated using AI-powered code generation.

# ## Files Created:
# {chr(10).join(f'- {filename}' for filename in files_data.keys())}

# ## Generated on:
# {time.strftime('%Y-%m-%d %H:%M:%S')}

# ## Setup Instructions:
# 1. Navigate to this directory
# 2. Follow any setup instructions in the generated files
# 3. Install any required dependencies
# """
        
#         readme_path = os.path.join(folder_name, "README.md")
#         self.write_file(readme_path, readme_content)
        
#         print(f"\n📊 Summary: {success_count}/{total_files} files created successfully")
        
#         return success_count > 0
    
#     def cleanup_on_failure(self):
#         """Clean up created files and directories on failure."""
#         print("🧹 Cleaning up created files...")
        
#         # Remove created files
#         for file_path in reversed(self.created_files):
#             try:
#                 if os.path.exists(file_path):
#                     os.remove(file_path)
#                     print(f"   🗑️  Removed: {file_path}")
#             except Exception as e:
#                 print(f"   ⚠️  Could not remove {file_path}: {str(e)}")
        
#         # Remove created directories
#         for dir_path in reversed(self.created_dirs):
#             try:
#                 if os.path.exists(dir_path) and not os.listdir(dir_path):
#                     os.rmdir(dir_path)
#                     print(f"   🗑️  Removed directory: {dir_path}")
#             except Exception as e:
#                 print(f"   ⚠️  Could not remove directory {dir_path}: {str(e)}")

# import time  # Add this import at the top

# ---

# # ai_powershell_automation/requirements.txt
# # Core dependencies for AI PowerShell Automation
# requests>=2.31.0
# python-dotenv>=1.0.0

# # Optional: For enhanced parsing and validation
# pyyaml>=6.0
# '''.strip()

#     parsed_data = parse_and_save_claude_response(raw_text)
