import requests
import json

# GraphQL API URL (replace this with the actual API URL)
api_url = "https://leetcode.com/graphql"

# Your GraphQL query for fetching favorite question list
query = """
query favoriteQuestionList($favoriteSlug: String!, $filter: FavoriteQuestionFilterInput, $filtersV2: QuestionFilterInput, $searchKeyword: String, $sortBy: QuestionSortByInput, $limit: Int, $skip: Int, $version: String = "v2") {
  favoriteQuestionList(
    favoriteSlug: $favoriteSlug
    filter: $filter
    filtersV2: $filtersV2
    searchKeyword: $searchKeyword
    sortBy: $sortBy
    limit: $limit
    skip: $skip
    version: $version
  ) {
    questions {
      difficulty
      id
      paidOnly
      questionFrontendId
      status
      title
      titleSlug
      translatedTitle
      isInMyFavorites
      frequency
      acRate
      contestPoint
      topicTags {
        name
        nameTranslated
        slug
      }
    }
    totalLength
    hasMore
  }
}
"""

# Set up the headers for the request (you might need to include authentication headers if required)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY",  # Replace with actual authorization token if needed
}

# Function to fetch favorite question list
def fetch_favorite_question_list(favorite_slug, filter=None, filters_v2=None, search_keyword=None, sort_by=None, limit=10, skip=0):
    # Define the variables for the GraphQL query
    variables = {
        "favoriteSlug": favorite_slug,
        "filter": filter,
        "filtersV2": filters_v2,
        "searchKeyword": search_keyword,
        "sortBy": sort_by,
        "limit": limit,
        "skip": skip,
        "version": "v2"  # Default version
    }

    # Prepare the payload
    payload = {
        "query": query,
        "variables": variables
    }

    # Send the request to the GraphQL endpoint
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Ensure the data structure is correct and not None
            if data and 'data' in data and data['data'] is not None:
                questions = data['data']['favoriteQuestionList']['questions']
                
                if questions:
                    # Process and print the favorite question list
                    for question in questions:
                        print(f"ID: {question['questionFrontendId']}, Title: {question['title']}, Difficulty: {question['difficulty']}")
                        print(f"AC Rate: {question['acRate']}%, Status: {question['status']}")
                        print(f"Tags: {[tag['name'] for tag in question['topicTags']]}")
                        print(f"Paid: {'Yes' if question['paidOnly'] else 'No'}")
                        print(f"Contest Points: {question['contestPoint']}\n")
                    
                    # Check if more questions are available
                    if data['data']['favoriteQuestionList']['hasMore']:
                        print("There are more questions available. Consider fetching the next page...")
                else:
                    print("No questions found for the given favorite list.")
            else:
                print("No data found or invalid response structure.")
        else:
            print(f"Failed to fetch favorite question list: {response.status_code}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage: Fetching questions from a specific favorite list (e.g., "algorithms")
favorite_slug = "walmart-labs-six-months"  # Replace with the desired favorite slug
fetch_favorite_question_list(favorite_slug, limit=10, skip=0)
