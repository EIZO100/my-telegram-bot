import requests
import os
from database import save_search_result

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.environ.get("SEARCH_ENGINE_ID")

def google_search(query, num_results=5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": num_results
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "items" not in data:
        return None
    results = []
    for item in data["items"]:
        results.append({
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": item.get("snippet", "")
        })
    return results

def format_results(results, query, user_id):
    if not results:
        return "ما لكيت نتائج للبحث هذا 😕"
    save_search_result(user_id, query, results)
    text = f"🔍 نتائج بحث: {query}\n\n"
    for i, r in enumerate(results, 1):
        text += f"{i}. {r['title']}\n"
        text += f"📝 {r['snippet']}\n"
        text += f"🔗 {r['link']}\n\n"
    return text
