import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """
أنت بوت عراقي ذكي واجتماعي، تحكي باللهجة العراقية البغدادية الأصيلة.

قواعد ثابتة:
- استخدم كلمات عراقية طبيعية: شنو، هواية، بعدين، عدل، چا، واجد، بس، يعني، أكو، شكو ماكو
- لا تستخدم الفصحى إلا لو السياق يحتاجها
- ردودك مريحة وطبيعية، مو رسمية
- إذا سألك سؤال تقني، اشرحه بأسلوب عراقي بسيط
- إذا المستخدم يحكيلك بلهجة ثانية، رد عليه بالعراقي بس افهمه
- كن ودود، خفيف دم، وذكي
"""

def ask_claude(user_message, history=[], user_style=""):
    messages = []

    for msg, _ in reversed(history):
        messages.append({"role": "user", "content": msg})

    messages.append({"role": "user", "content": user_message})

    dynamic_system = SYSTEM_PROMPT
    if user_style:
        dynamic_system += f"\n\nملاحظات عن هذا المستخدم:\n{user_style}"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=dynamic_system,
        messages=messages
    )
    return response.content[0].text

def analyze_user_style(history):
    if len(history) < 3:
        return ""
    messages_text = "\n".join([msg for msg, _ in history])
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        system="حلل أسلوب الكتابة وارجع ملاحظات قصيرة عن اللهجة والكلمات المفضلة. بدون مقدمات.",
        messages=[{"role": "user", "content": f"حلل:\n{messages_text}"}]
    )
    return response.content[0].text
