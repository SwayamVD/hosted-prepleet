import requests
import json

# GraphQL API URL (replace this with the actual API URL)
api_url = "https://leetcode.com/graphql"

# Your GraphQL query for fetching questions by category
query = """
query problemsetQuestionListV2($filters: QuestionFilterInput, $limit: Int, $searchKeyword: String, $skip: Int, $sortBy: QuestionSortByInput, $categorySlug: String) {
  problemsetQuestionListV2(
    filters: $filters
    limit: $limit
    searchKeyword: $searchKeyword
    skip: $skip
    sortBy: $sortBy
    categorySlug: $categorySlug
  ) {
    questions {
      id
      titleSlug
      title
      translatedTitle
      questionFrontendId
      paidOnly
      difficulty
      topicTags {
        name
        slug
        nameTranslated
      }
      status
      isInMyFavorites
      frequency
      acRate
      contestPoint
    }
    totalLength
    finishedLength
    hasMore
  }
}
"""

# Set up the headers for the request (you might need to include authentication headers if required)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY",  # Replace with actual authorization token if needed
}

# Function to fetch questions category-wise
def fetch_questions_by_category(category_slug, filters=None, limit=10, skip=0, sort_by=None):
    # Define the variables for the GraphQL query
    variables = {
        "filters": filters,
        "limit": limit,
        "searchKeyword": None,
        "skip": skip,
        "sortBy": sort_by,
        "categorySlug": category_slug
    }

    # Prepare the payload
    payload = {
        "query": query,
        "variables": variables
    }

    # Send the request to the GraphQL endpoint
    response = requests.post(api_url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        questions = data['data']['problemsetQuestionListV2']['questions']
        
        # Process and print the questions
        for question in questions:
            print(f"ID: {question['questionFrontendId']}, Title: {question['title']}, Difficulty: {question['difficulty']}")
            print(f"Tags: {[tag['name'] for tag in question['topicTags']]}")
            print(f"AC Rate: {question['acRate']}%\n")
        
        # Check if more questions are available
        if data['data']['problemsetQuestionListV2']['hasMore']:
            print("There are more questions available. Consider fetching the next page...")
    else:
        print(f"Failed to fetch questions: {response.status_code}")

# Example usage: Fetching questions from a specific category (e.g., "algorithms")
category_slug = "algorithm"  # Replace with the desired category slug
fetch_questions_by_category(category_slug)
