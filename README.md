

# AI Text to Project

**AI Text to Project** is a lightweight tool that parses structured AI-generated text (e.g. from Claude, ChatGPT) into a real project folder — complete with files, directories, and actual code/content.  
Perfect for developers who use AI to prototype and want to avoid manual copy-pasting.

---

## 🚀 Features

- Converts annotated AI responses into full project structures
- Automatically creates files, directories, and adds code
- Supports **any file type** – not just Python
- Works from raw multiline input in the terminal or editor

---

## 🛠 How It Works

1. You paste AI-generated text in a format like:

<pre> 
  #project-name/filename.ext 
  code here 
  ---
  #project-name/another-file.ext code here 
  code here 
  --- 
  #project-name/another-file.ext code here 
  code here 
  --- 
</pre>

2. The parser reads the structure and content

3. Files and folders are created on disk

---

## 🧑‍💻 Usage

1. Clone the repo:
```bash
git clone https://github.com/disastrousDEVIL/Ai-text-to-project.git
cd Ai-text-to-project
````

2. Run the tool:

 ```bash
 python main.py
 ```

3. Paste the AI output and save/close the temp file editor (e.g. VS Code, nano)

5. Done! Your files are created.

---


## 💬 Prompting Guide (GPT & Claude)

To use this tool effectively, you need to prompt the AI in a structured format. Here’s how:

### 🧠 GPT (ChatGPT, OpenAI)
<pre>
“Give me all code files for this project in the format:

#project-name/filename.ext  
<your code>  
---  

Specify the file path for each file in the header and separate files using '---'. This helps me generate and save them automatically.”

</pre>

### 🤖 Claude (Anthropic) (Easiest One)
<pre>
Use this prompt:

Give me the code while specifying the file names in the same code .
</pre>

## 📁 Example Input Format

<pre>
#my_project/app.py
print("Hello from AI!")
---

#my_project/helpers.js
function greet() {
  console.log("Hello from JS helper!");
}
---</pre>
---
## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

Let me know if you want this auto-added and committed to your repo, or want badges like “Made with Python” / “MIT License” etc.
