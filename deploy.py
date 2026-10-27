import os
import subprocess
import json
import urllib.request
import urllib.error
from huggingface_hub import HfApi

# 1. Get Hugging Face Token from Desktop/.env
hf_token = None
with open(r'C:\Users\Gubernatr\Desktop\.env', 'r', encoding='utf-8') as f:
    for line in f:
        if 'hugging_face_token' in line:
            hf_token = line.split('=', 1)[1].strip().strip('"\'')
            break

print("HF Token loaded:", bool(hf_token))

# 2. Get GitHub Token from Git Credential Manager
p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = p.communicate(input='protocol=https\nhost=github.com\n\n')

gh_token = None
gh_user = 'Newuser3301'
for line in stdout.splitlines():
    if line.startswith('username='):
        gh_user = line.split('=', 1)[1].strip()
    elif line.startswith('password='):
        gh_token = line.split('=', 1)[1].strip()

print(f"GitHub User: {gh_user}, Token loaded: {bool(gh_token)}")

repo_name = "3d-biocyber-oncology-lab"
repo_desc = "3D Bio-Cyber Oncology Lab // Interactive ML Visualizer & Real-Time Retraining with Three.js & Scikit-Learn"

# 3. Create GitHub Repository
print(f"Creating GitHub repository: {gh_user}/{repo_name}...")
create_repo_url = "https://api.github.com/user/repos"
req_data = json.dumps({
    "name": repo_name,
    "description": repo_desc,
    "private": False
}).encode('utf-8')

req = urllib.request.Request(create_repo_url, data=req_data, headers={
    'Authorization': f'token {gh_token}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'Python'
})

github_repo_url = f"https://github.com/{gh_user}/{repo_name}"
try:
    with urllib.request.urlopen(req) as resp:
        print("GitHub repo created successfully!")
except urllib.error.HTTPError as e:
    err_body = e.read().decode('utf-8')
    if "already exists" in err_body:
        print("GitHub repo already exists, proceeding to push.")
    else:
        print(f"GitHub API Error ({e.code}): {err_body}")

# 4. Git Init, Add, Commit, Push to GitHub
working_dir = r'C:\Users\Gubernatr\Desktop\new'
os.chdir(working_dir)

# Remove temporary files before git add
for temp_f in ['check_hf.py', 'find_quotes.py']:
    if os.path.exists(temp_f):
        try: os.remove(temp_f)
        except: pass

subprocess.run(['git', 'init'], check=True)
subprocess.run(['git', 'config', 'user.name', gh_user])
subprocess.run(['git', 'config', 'user.email', 'newuser4584@gmail.com'])
subprocess.run(['git', 'add', '.'])
subprocess.run(['git', 'commit', '-m', 'Initial commit: 3D Bio-Cyber Oncology Lab with real-time ML retraining'])
subprocess.run(['git', 'branch', '-M', 'main'])

# Set remote with authenticated URL
auth_remote_url = f"https://{gh_user}:{gh_token}@github.com/{gh_user}/{repo_name}.git"
subprocess.run(['git', 'remote', 'remove', 'origin'], stderr=subprocess.DEVNULL)
subprocess.run(['git', 'remote', 'add', 'origin', auth_remote_url])

print("Pushing to GitHub main branch...")
push_res = subprocess.run(['git', 'push', '-u', 'origin', 'main', '--force'])
if push_res.returncode == 0:
    print("Successfully pushed to GitHub!")
else:
    print("Git push failed with code:", push_res.returncode)

# 5. Create and Deploy to Hugging Face Space
print(f"Deploying to Hugging Face Spaces: {gh_user}/{repo_name}...")
hf_api = HfApi(token=hf_token)
space_id = f"{gh_user}/{repo_name}"

try:
    hf_api.create_repo(
        repo_id=space_id,
        repo_type="space",
        space_sdk="docker",
        private=False,
        exist_ok=True
    )
    print("Hugging Face Space repository confirmed!")
except Exception as e:
    print("Error creating HF space:", e)

# Upload directory to Hugging Face Space
print("Uploading files to Hugging Face Space...")
try:
    hf_api.upload_folder(
        folder_path=working_dir,
        repo_id=space_id,
        repo_type="space",
        ignore_patterns=["__pycache__", "*.pyc", ".git", ".gitignore", "deploy.py"]
    )
    print("Successfully uploaded all files to Hugging Face Space!")
    print(f"Hugging Face Space URL: https://huggingface.co/spaces/{space_id}")
except Exception as e:
    print("Error uploading to HF space:", e)
