import requests
import matplotlib.pyplot as plt

# 替换为您的 GitHub 用户名
GITHUB_USER = 'weitsunglin'

def fetch_languages(user):
    languages = {}
    repos = requests.get(f'https://api.github.com/users/{user}/repos').json()
    for repo in repos:
        if repo['fork'] is False:  # Ignore forks
            lang_url = repo['languages_url']
            lang_data = requests.get(lang_url).json()
            for lang, lines in lang_data.items():
                if lang in languages:
                    languages[lang] += lines
                else:
                    languages[lang] = lines
    return languages

def generate_bar_chart(languages):
    labels = languages.keys()
    sizes = languages.values()
    
    plt.figure(figsize=(10, 8))
    plt.bar(labels, sizes)
    
    plt.ylabel('Lines of Code')
    plt.title('Programming Languages Distribution')
    
    plt.xticks(rotation=45)  # Rotate labels to avoid overlap
    plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
    
    plt.show()

languages = fetch_languages(GITHUB_USER)
generate_bar_chart(languages)
