# skill_coding/gemini.py
import google.generativeai as genai

genai.configure(api_key='AIzaSyBF_if642BpoY1mWeo_sA2fvHjMaIGwxv8')

model = genai.GenerativeModel('gemini-2.0-flash')

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text
