import requests
import matplotlib.pyplot as plt

# Replace with your GitHub username
GITHUB_USER = 'weitsunglin'

def fetch_topics(user):
    topics = {}
    repos = requests.get(f'https://api.github.com/users/{user}/repos').json()
    
    for repo in repos:
        if (repo['fork'] is False 
                and repo['name'] != 'ios_line_sdk' 
                and repo['name'] != 'llvm-mingw-20240518-msvcrt-x86_64'):  # Ignore forks and specific repos
            repo_name = repo['name']
            # Fetch topics for each repository
            headers = {"Accept": "application/vnd.github.mercy-preview+json"}
            topic_url = f"https://api.github.com/repos/{user}/{repo_name}/topics"
            topic_data = requests.get(topic_url, headers=headers).json()
            for topic in topic_data.get("names", []):
                topics[topic] = topics.get(topic, 0) + 1
    
    # Sort topics by frequency and get the top 5
    sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:5]
    top_topics = {topic: count for topic, count in sorted_topics}
    
    return top_topics

def generate_bar_chart(topics):
    # Sort topics by frequency in descending order
    sorted_topics = {topic: count for topic, count in sorted(topics.items(), key=lambda item: item[1], reverse=True)}
    
    # Prepare data for bar chart
    labels = sorted_topics.keys()
    sizes = sorted_topics.values()
    
    # Plot bar chart
    plt.figure(figsize=(5, 3))
    plt.bar(labels, sizes, color='skyblue')
    
    # Adding title and labels
    plt.title('Top 5 Repository Topics')
    plt.xlabel('Topics')
    plt.ylabel('Frequency')
    
    # Save the chart as an image
    plt.tight_layout()
    plt.savefig('topics_bar.png')
    plt.show()

# Fetch topics and generate bar chart
topics = fetch_topics(GITHUB_USER)
generate_bar_chart(topics)
