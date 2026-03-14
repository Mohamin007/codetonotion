import os
from notion_client import Client
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_ROOT_PAGE_ID = os.getenv("NOTION_ROOT_PAGE_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Initialize clients
notion = Client(auth=NOTION_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)

def is_private(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            return "PRIVATE - DO NOT SYNC" in first_line
    except:
        return False

def extract_comments_and_code(filepath):
    comments = []
    code_snippets = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # Extract docstrings (triple quotes)
    import re
    docstrings = re.findall(r'"""(.*?)"""', content, re.DOTALL)
    for doc in docstrings:
        cleaned = doc.strip()
        if cleaned:
            comments.append(cleaned)
    
    # Extract regular and inline comments
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            comments.append(stripped[1:].strip())
        elif '#' in stripped and not stripped.startswith('"""'):
            code_part = stripped[:stripped.index('#')].strip()
            comment_part = stripped[stripped.index('#')+1:].strip()
            if code_part:
                code_snippets.append(code_part)
            if comment_part:
                comments.append(comment_part)
        elif stripped and not stripped.startswith('"""') and not stripped.startswith("'''"):
            code_snippets.append(stripped)
    
    return comments, code_snippets

def refine_with_ai(filename, comments, code_snippets):
    comments_text = "\n".join(comments)
    code_text = "\n".join(code_snippets[:10])
    
    prompt = f"""You are a study notes formatter.
File: {filename}
Developer Comments: {comments_text}
Code Sample: {code_text}

Create structured study notes with these EXACT sections using plain text only, no markdown symbols like # or **:

SUMMARY
Write 2 sentences about what this file does.

KEY CONCEPTS
- concept 1
- concept 2
- concept 3

MY NOTES
Write polished version of the developer comments here.

CODE HIGHLIGHT
Show the most important code snippet and explain it simply.

Keep it concise and student friendly. NO markdown symbols."""

    message = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.choices[0].message.content

# Cache to store already created folders
folder_cache = {}

def get_or_create_folder(folder_name):
    # Check cache first
    if folder_name in folder_cache:
        return folder_cache[folder_name]
    
    # Search existing pages
    results = notion.search(query=folder_name).get("results", [])
    for page in results:
        if page["object"] == "page":
            title = page["properties"].get("title", {}).get("title", [])
            if title and title[0]["text"]["content"] == folder_name:
                folder_cache[folder_name] = page["id"]
                return page["id"]
    
    # Create new folder
    new_page = notion.pages.create(
        parent={"page_id": NOTION_ROOT_PAGE_ID},
        properties={
            "title": {"title": [{"text": {"content": folder_name}}]}
        }
    )
    folder_cache[folder_name] = new_page["id"]
    return new_page["id"]

def create_notion_page(folder_id, filename, refined_notes):
    page_name = filename.replace('.py', '').replace('_', ' ').title()
    
    # Split notes into paragraphs
    paragraphs = [p.strip() for p in refined_notes.split('\n') if p.strip()]
    
    # Build blocks
    children = []
    for para in paragraphs:
        if para in ['SUMMARY', 'KEY CONCEPTS', 'MY NOTES', 'CODE HIGHLIGHT']:
            children.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": para}}]
                }
            })
        elif para.startswith('-'):
            children.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": para[1:].strip()}}]
                }
            })
        else:
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": para}}]
                }
            })
    
    notion.pages.create(
        parent={"page_id": folder_id},
        properties={
            "title": {"title": [{"text": {"content": page_name}}]}
        },
        children=children
    )
    print(f"✅ Successfully synced: {page_name} → Notion!")

def sync_file(filepath):
    if not filepath.endswith('.py'):
        print("⚠️ Only Python files supported right now!")
        return
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return
        
    if is_private(filepath):
        print(f"🔒 Skipping private file!")
        return
    
    print(f"📄 Processing: {filepath}")
    filename = os.path.basename(filepath)
    folder_name = os.path.basename(os.path.dirname(filepath))
    
    comments, code_snippets = extract_comments_and_code(filepath)
    
    if not comments:
        print(f"⚠️ No comments found! Add comments to your code first.")
        return
    
    print("🤖 Refining notes with AI...")
    refined_notes = refine_with_ai(filename, comments, code_snippets)
    
    print("📚 Creating Notion page...")
    folder_id = get_or_create_folder(folder_name)
    create_notion_page(folder_id, filename, refined_notes)

if __name__ == '__main__':
    print("🚀 CodeToNotion — Sync your code notes to Notion!")
    print("=" * 50)
    print("What do you want to sync?")
    print("1 — Single file")
    print("2 — Entire folder")
    choice = input("\nEnter 1 or 2: ").strip()
    
    if choice == "1":
        filepath = input("📁 Enter the full path of your Python file: ")
        filepath = filepath.strip().strip('"')
        sync_file(filepath)
        
    elif choice == "2":
        folderpath = input("📁 Enter the full path of your folder: ")
        folderpath = folderpath.strip().strip('"')
        
        if not os.path.exists(folderpath):
            print("❌ Folder not found!")
        else:
            py_files = []
            for root, dirs, files in os.walk(folderpath):
                for file in files:
                    if file.endswith('.py'):
                        py_files.append(os.path.join(root, file))
            
            if not py_files:
                print("⚠️ No Python files found in this folder!")
            else:
                print(f"\n📂 Found {len(py_files)} Python files!")
                print("Starting sync...\n")
                for filepath in py_files:
                    sync_file(filepath)
                    
    print("\n✅ All done! Check your Notion workspace! 🎉")