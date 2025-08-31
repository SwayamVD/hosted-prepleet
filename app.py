from flask import Flask, jsonify, render_template, request
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import json
import google.generativeai as genai
genai.configure(api_key="AIzaSyBPurTgr1YTZgAsNNvjgC2G_ZgirEwS4OQ")
app = Flask(__name__)

# Load CSVs from the 'questions' folder
DATA_DIR = 'questions'
import re
def extract_slug_from_url(url):
    match = re.search(r'/problems/([^/]+)/?', url)
    return match.group(1) if match else ""


def load_questions():
    questions = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.csv'):
            company = filename.replace('.csv', '')
            filepath = os.path.join(DATA_DIR, filename)
            df = pd.read_csv(filepath)
            for _, row in df.iterrows():
                questions.append({
                    "Company": company,
                    "Title": row.get("Title", ""),
                    "Difficulty": row.get("Difficulty", ""),
                    "Frequency": row.get("Frequency", ""),
                    "AcceptanceRate": row.get("Acceptance Rate", ""),
                    "Link": row.get("Link", ""),
                    "Slug": extract_slug_from_url(row.get("Link",""))
                })
    return questions

all_questions = load_questions()





# Function to fetch problem details using LeetCode's internal API
def fetch_problem_details(slug):
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/problems/{slug}/",
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
            exampleTestcaseList
            topicTags {
              name
              slug
            }
            similarQuestionList {
                difficulty
                titleSlug
                title
            }
            hints
            codeSnippets {
                code
                lang
                langSlug
            }
          }
        }
        """
    }

    response = requests.post(url, headers=headers, data=json.dumps(query))

    if response.status_code == 200:
        data = response.json()
        return data.get("data", {}).get("question", {})
    else:
        return None

@app.route("/solve")
def solve():
    slug = request.args.get("title")
    if not slug:
        return "Missing title slug!", 400

    problem = fetch_problem_details(slug)
    if not problem:
        return "Problem not found or error occurred.", 404

    return render_template("solve.html", problem=problem)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/questions', methods=['GET'])
def get_all_questions():
    return jsonify(all_questions)

@app.route('/questions/<company>', methods=['GET'])
def get_company_questions(company):
    filtered = [q for q in all_questions if q["Company"].lower() == company.lower()]
    return jsonify(filtered)



@app.route("/analyze", methods=["POST"])
def analyze_code():
    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "unknown")
    idtitle = "Leetcode Question: " + data.get("idtitle")



    # Load prompt
    prompt = """
            Analyze the Python code below, which is a solution to a LeetCode problem. The code may be a standalone function.
            1) Return a JSON object with keys:
            - verify: if you found any mistakes (logical, syntax, or didnt satify the leetcode question description) alert or else just say Correct Code.
            - time_complexity: {best, average, worst} (Big-O strings) -give short reason why
            - space_complexity: string (Big-O) -give short reason why
            - explanation: step-by-step explanation (short)
            - optimization_suggestions: bullet list (short)
            - refactored_code: code (if applicable)

            2) ONLY return valid JSON (no extra text).
        """

    full_prompt = f"{idtitle}\n{prompt}\n\nLanguage: {language}\n\nCode:\n{code}"
    # Debug print (you should see this in your terminal logs)
    # print("📩 Received data:", full_prompt)
    # return jsonify({"status": "ok", "echo": data})


    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(full_prompt)
    raw_text = response.text.strip()

    cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_text, flags=re.DOTALL).strip()

    try:
        parsed_json = json.loads(cleaned)
    except Exception as e:
        parsed_json = {
            "error": f"Failed to parse JSON: {str(e)}",
            "raw_output": raw_text
        }

    return jsonify(parsed_json)  


@app.route("/gotstuck", methods=["POST"])
def gotstuck():
    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "unknown")
    idtitle = data.get("idtitle")


    prompt=f"""
        I am stuck while solving a programming problem.
        I am solving a leetcode problem {idtitle}
        Please analyze what I am trying to do, identify any misconceptions, and guide me with the correct approach to solve the problem.
        Do not give the full solution.
        Explain the key concept(s) I need to understand in very short, simple terms.
        Focus on helping me learn and think through the problem, not just giving the answer.


        ONLY return valid JSON (no extra text) with following fields.
        - analysis: analyze the code and tell the vulnerability or find where he went wrong
        - keyconcepts: suggest one concept that i can help the user , explain in short how to implement it.
        """



    full_prompt = f"{prompt}\n\nLanguage: {language}\n\nCode:\n{code}"


    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(full_prompt)
    raw_text = response.text.strip()

    cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_text, flags=re.DOTALL).strip()
    print(cleaned)
    try:
        parsed_json = json.loads(cleaned)
    except Exception as e:
        parsed_json = {
            "error": f"Failed to parse JSON: {str(e)}",
            "raw_output": raw_text
        }

    return jsonify(parsed_json)

@app.route("/getquestionset/<name>",methods=["GET"])
def getquesset(name):
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

    variables = {
        "skip": 0,
        # "favoriteSlug": "eeudwo2i",  # Replace with your desired favoriteSlug
        "favoriteSlug": name,
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

    response = requests.post(url, headers=headers, json=payload)
    print("correct till here")
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        questions = data['data']['favoriteQuestionList']['questions']
        
        return jsonify(questions)
    else:
        print(f"Failed to fetch data: {response.status_code}")



if __name__ == '__main__':
    app.run(debug=True)
