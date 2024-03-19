import requests
import matplotlib.pyplot as plt

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
    filtered_languages = {lang: lines for lang, lines in languages.items() if lines > 0}
    total = sum(filtered_languages.values())
    
    # 移除在总贡献中占比非常小的语言
    filtered_languages = {lang: lines for lang, lines in filtered_languages.items() if (lines / total) >= 0.01} # 调整阈值以排除贡献极小的语言

    if total > 0:
        sizes = [size for size in filtered_languages.values() if size/total >= 0.01]  # 再次过滤确保无0%贡献
        labels = [f'{lang} {size/total:.1%}' for lang, size in filtered_languages.items() if size/total >= 0.01]
        
        explode = [0.1] * len(labels)
        
        plt.figure(figsize=(6, 4))
        wedges, _, _ = plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=140, shadow=True)
        
        plt.axis('equal')
        plt.title('Programming Languages Distribution')
        
        plt.legend(wedges, labels, title="Languages", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.tight_layout()
        plt.savefig('code_exp.png')
    else:
        print("No significant language contributions found.")

languages = fetch_languages(GITHUB_USER)
generate_pie_chart(languages)
