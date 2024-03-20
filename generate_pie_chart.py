import requests
import matplotlib.pyplot as plt

# 替换为您的 GitHub 用户名
GITHUB_USER = 'weitsunglin'

def fetch_languages(user):
    languages = {}
    repos = requests.get(f'https://api.github.com/users/{user}/repos').json()
    for repo in repos:
        if repo['fork'] is False and repo['name'] != 'ios_line_sdk':  # Ignore forks
            lang_url = repo['languages_url']
            lang_data = requests.get(lang_url).json()
            for lang, lines in lang_data.items():
                # 排除指定的语言
                if lang not in ['HLSL', 'ShaderLab']:
                    if lang in languages:
                        languages[lang] += lines
                    else:
                        languages[lang] = lines
    return languages

def generate_pie_chart(languages):
    sizes = languages.values()
    total = sum(sizes)
    labels = [f'{lang} {size/total:.1%}' for lang, size in languages.items()]
    
    explode = [0.1] * len(labels)  # 'Explode' all slices slightly to give a 3D effect
    
    plt.figure(figsize=(5, 3))
    wedges, texts, autotexts = plt.pie(sizes, autopct='', startangle=140, explode=explode, shadow=True)
    
    plt.axis('equal')
    
    plt.title('Programming Languages Distribution')
    
    # Display the legend with language names and their corresponding percentages
    plt.legend(wedges, labels, title="Languages", loc="center left", bbox_to_anchor=(1, 0.5))
    
    plt.tight_layout()
    plt.savefig('code_exp.png')  # Save the figure as a file

languages = fetch_languages(GITHUB_USER)
generate_pie_chart(languages)
