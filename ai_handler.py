import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """أنت بوت عراقي ذكي واجتماعي، تحكي باللهجة العراقية البغدادية الأصيلة.
- استخدم كلمات عراقية: شنو، هواية، بعدين، واجد، أكو، شكو ماكو
- كن ودود وخفيف دم وذكي
"""

def ask_claude(user_message, history=[], user_style=""):
    prompt = SYSTEM_PROMPT
    if user_style:
        prompt += f"\nملاحظات عن المستخدم:\n{user_style}"
    prompt += f"\n\nالمستخدم: {user_message}"
    
    response = model.generate_content(prompt)
    return response.text

def analyze_user_style(history):
    if len(history) < 3:
        return ""
    messages_text = "\n".join([msg for msg, _ in history])
    response = model.generate_content(
        f"حلل أسلوب الكتابة بإيجاز:\n{messages_text}"
    )
    return response.text
