import requests
import json

# Define the GraphQL query
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

# Define the query variables
variables = {
    "skip": 0,
    "limit": 100,
    "favoriteSlug": "eeudwo2i",  # Replace with your desired favoriteSlug
    "filtersV2": {
        "filterCombineType": "ALL",
        "statusFilter": {"questionStatuses": [], "operator": "IS"},
        "difficultyFilter": {"difficulties": [], "operator": "IS"},
        "languageFilter": {"languageSlugs": [], "operator": "IS"},
        "topicFilter": {"topicSlugs": [], "operator": "IS"},
    },
    "searchKeyword": "",
    "sortBy": {"sortField": "CUSTOM", "sortOrder": "ASCENDING"}
}

# Set the URL for the GraphQL endpoint
url = 'https://leetcode.com/graphql'

# Headers for the request (you might need to add authorization headers if necessary)
headers = {
    'Content-Type': 'application/json',
    # 'Authorization': 'Bearer YOUR_AUTH_TOKEN',  # Uncomment and add your token if required
}

# Prepare the request payload
payload = {
    'query': query,
    'variables': variables
}

# Send the request to the API
response = requests.post(url, headers=headers, json=payload)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    questions = data['data']['favoriteQuestionList']['questions']
    
    # Process the question data (display question titles)
    for question in questions:
        print(f"Title: {question['title']}, Difficulty: {question['difficulty']}")
else:
    print(f"Failed to fetch data: {response.status_code}")
