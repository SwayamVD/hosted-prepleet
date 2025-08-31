import requests
import json

def fetch_problem_details(slug):
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/problems/longest-palindromic-substring/",
        "User-Agent": "Mozilla/5.0"
    }

    query = {
        "operationName": "questionData",
        "variables": {
            "titleSlug": slug
        },
        "query": """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionId
            title
            content
            difficulty
            likes
            dislikes
            exampleTestcases
            topicTags {
              name
              slug
            }
          }
        }
        """
    }

    response = requests.post(url, headers=headers, data=json.dumps(query))

    if response.status_code == 200:
        data = response.json()
        question = data.get("data", {}).get("question", {})
        if question:
            print("Title:", question["title"])
            print("Difficulty:", question["difficulty"])
            print("Tags:", [tag["name"] for tag in question["topicTags"]])
            print("Description:\n", question["content"])  # This is HTML
            return question
        else:
            print("Question not found.")
            return None
    else:
        print(f"Failed to fetch. Status: {response.status_code}")
        return None

# Example usage
fetch_problem_details("longest-palindromic-substring")
