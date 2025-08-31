import requests
import json

def get_problem_details(title_slug):
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    
    # GraphQL query for fetching problem details
    query = """
    query questionDetail($titleSlug: String!) {
        languageList {
            id
            name
        }
        submittableLanguageList {
            id
            name
            verboseName
        }
        statusList {
            id
            name
        }
        questionDiscussionTopic(questionSlug: $titleSlug) {
            id
            commentCount
            topLevelCommentCount
        }
        ugcArticleOfficialSolutionArticle(questionSlug: $titleSlug) {
            uuid
            chargeType
            canSee
            hasVideoArticle
        }
        question(titleSlug: $titleSlug) {
            title
            titleSlug
            questionId
            questionFrontendId
            questionTitle
            translatedTitle
            content
            translatedContent
            categoryTitle
            difficulty
            stats
            companyTagStatsV2
            topicTags {
                name
                slug
                translatedName
            }
            similarQuestionList {
                difficulty
                titleSlug
                title
                translatedTitle
                isPaidOnly
            }
            mysqlSchemas
            dataSchemas
            frontendPreviews
            likes
            dislikes
            isPaidOnly
            status
            canSeeQuestion
            enableTestMode
            metaData
            enableRunCode
            enableSubmit
            enableDebugger
            envInfo
            isLiked
            nextChallenges {
                difficulty
                title
                titleSlug
                questionFrontendId
            }
            libraryUrl
            adminUrl
            hints
            codeSnippets {
                code
                lang
                langSlug
            }
            exampleTestcaseList
            hasFrontendPreview
            featuredContests {
                titleSlug
                title
            }
        }
    }
    """
    
    # Request payload
    payload = {
        "query": query,
        "variables": {
            "titleSlug": title_slug
        },
        "operationName": "questionDetail"
    }

    # Send POST request to LeetCode GraphQL API
    response = requests.post(url, headers=headers, json=payload)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        # Extract the problem details from the response data
        problem_details = data.get("data", {}).get("question", {})
        return problem_details
    else:
        print(f"Error: {response.status_code}")
        return None


# Example usage: Fetch details for the "Two Sum" problem
problem_slug = "two-sum"
problem_data = get_problem_details(problem_slug)

if problem_data:
    print(json.dumps(problem_data, indent=4))  # Pretty print the result
