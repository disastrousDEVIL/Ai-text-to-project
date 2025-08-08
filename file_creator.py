import os
def create_files_from_json(data):
    project_name=data[0]["project"]
    folder_name = project_name
    os.makedirs(folder_name, exist_ok=True)
    for item in data:
        filename = item['filename']
        content = item['content']
        file_path = os.path.join(folder_name, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        
# if __name__ == "__main__":
#     # Example usage: load parsed_output.json and create files
#     with open("parsed_output.json", "r", encoding="utf-8") as f:
#         data = json.load(f)
#     k=create_files_from_json(data)
#     print(k)