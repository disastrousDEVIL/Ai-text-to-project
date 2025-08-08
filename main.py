from file_creator import create_files_from_json
from parsey import parse_and_save_claude_response
import os
import tempfile

def get_multiline_input_via_editor():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w+", encoding="utf-8") as tf:
        temp_path = tf.name
        tf.write("# Paste your full Claude response below.\n")
        tf.write("# Save and close the editor when you're done.\n")

    editor = os.environ.get("EDITOR", "notepad" if os.name == "nt" else "nano")
    os.system(f"{editor} {temp_path}")

    with open(temp_path, "r", encoding="utf-8") as f:
        text = f.read()

    os.remove(temp_path)
    return text.strip()

if __name__ == "__main__":
    print("📝 Opening editor to paste Claude response...")
    raw_text = get_multiline_input_via_editor()

    parsed_data = parse_and_save_claude_response(raw_text)
    create_files_from_json(parsed_data)

    print("✅ Files created successfully!")
