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

def generate_pie_chart(languages):
    # Sort the languages by lines of code in descending order
    sorted_languages = {lang: lines for lang, lines in sorted(languages.items(), key=lambda item: item[1], reverse=True)}
    
    sizes = sorted_languages.values()
    total = sum(sizes)
    labels = [f'{lang} {size/total:.1%}' for lang, size in sorted_languages.items()]
    
    explode = [0.1] * len(labels)  # 'Explode' all slices slightly to give a 3D effect
    
    plt.figure(figsize=(5, 3))
    wedges, texts, autotexts = plt.pie(sizes, autopct='', startangle=140, explode=explode, shadow=True)
    
    plt.axis('equal')
    
    plt.title('Programming Languages Distribution')
    
    plt.legend(wedges, labels, title="Languages", loc="center left", bbox_to_anchor=(1, 0.5))
    
    plt.tight_layout()
    plt.savefig('code_exp.png')

languages = fetch_languages(GITHUB_USER)
generate_pie_chart(languages)
