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
    # 移除贡献为0的语言
    filtered_languages = {lang: lines for lang, lines in languages.items() if lines > 0}
    
    # 确保总贡献大于0以避免除以0的错误
    total = sum(filtered_languages.values())
    if total > 0:
        # 过滤出贡献比例确实大于0的语言
        filtered_languages = {lang: lines for lang, lines in filtered_languages.items() if (lines / total) > 0.0001}  # 设定一个小的阈值以排除贡献非常小的语言

        sizes = filtered_languages.values()
        labels = [f'{lang} {size/total:.1%}' for lang, size in filtered_languages.items()]
        
        explode = [0.1] * len(labels)  # 'Explode' all slices slightly to give a 3D effect
        
        plt.figure(figsize=(6, 4))
        wedges, texts, autotexts = plt.pie(sizes, autopct='', startangle=140, explode=explode, shadow=True)
        
        plt.axis('equal')
        
        plt.title('Programming Languages Distribution')
        
        # Display the legend with language names and their corresponding percentages
        plt.legend(wedges, labels, title="Languages", loc="center left", bbox_to_anchor=(1, 0.5))
        
        plt.tight_layout()
        plt.savefig('code_exp.png')  # Save the figure as a file
    else:
        print("No significant language contributions found.")



languages = fetch_languages(GITHUB_USER)
generate_pie_chart(languages)
