import requests
import matplotlib.pyplot as plt

# 替换为您的 GitHub 用户名
GITHUB_USER = 'weitsunglin'

def fetch_languages(user):
    languages = {}
    repos = requests.get(f'https://api.github.com/users/{user}/repos').json()
    print("repos", repos)
    for repo in repos:
        if (repo['fork'] is False 
                and repo['name'] != 'ios_line_sdk' 
                and repo['name'] != 'llvm-mingw-20240518-msvcrt-x86_64'):  # Ignore forks and specific repo
            lang_url = repo['languages_url']
            lang_data = requests.get(lang_url).json()
            for lang, lines in lang_data.items():
                # Exclude specific languages
                if lang not in ['HLSL', 'ShaderLab']:
                    languages[lang] = languages.get(lang, 0) + lines
    
    # Sort languages by lines of code in descending order and get the top 5
    sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
    top_languages = {lang: lines for lang, lines in sorted_languages}
    
    return top_languages

def generate_bar_chart(languages):
    # Sort languages by lines of code in descending order
    sorted_languages = {lang: lines for lang, lines in sorted(languages.items(), key=lambda item: item[1], reverse=True)}
    
    # Prepare data for bar chart
    labels = sorted_languages.keys()
    sizes = sorted_languages.values()
    
    # Plot bar chart
   plt.figure(figsize=(5, 3))  # 調整圖像大小

    plt.bar(labels, sizes, color='skyblue')
    
    # Adding title and labels
    plt.title('Top 5 Programming Languages by Lines of Code')
    plt.xlabel('Programming Languages')
    plt.ylabel('Lines of Code')
    
    # Save the chart as an image
    plt.tight_layout()
    plt.savefig('code_exp_bar.png')
    plt.show()

# Fetch languages and generate bar chart
languages = fetch_languages(GITHUB_USER)
generate_bar_chart(languages)
