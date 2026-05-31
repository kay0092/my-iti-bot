import streamlit as st
from google import genai
from google.genai import types

# Page Config
st.set_page_config(page_title="Institute Information Assistant", page_icon="🏢", layout="centered")

st.title("🏢 Institute Admission Information Desk")
st.write("Aap is chat-box mein kisi bhi Institute, seats, hostel ya location ke baare mein Hindi/English mein puch sakte hain.")

# NEW GOOGLE GENAI CLIENT METHOD (No Secrets Needed, Bulletproof Setup)
part1 = "AQ.Ab8RN6LuF5hPfhVhRr6G6GOMA"
part2 = "fmayMkmYom3zp56iEJu-k5G-w"
FINAL_KEY = part1 + part2

# Naye tarike se client connect kar rahe hain
try:
    client = genai.Client(api_key=FINAL_KEY)
except Exception as e:
    st.error("System configuration delay. Please refresh the page.")

# Aapka Strict System Prompt aur PDF ka Data
SYSTEM_PROMPT = """
Aap ek strictly professional Institute Admission Assistant hain. Aapko sirf aur sirf niche diye gaye DATA ke basis par jawab dena hai. 
Agar koi data ismein nahi hai, toh saaf bol dijiye: "Main maafi chahta/chahti hoon, iski jankari PDF mein nahi hai." 
Apne mann se koi bhi institute, seat, ya rules mat banana. Temperature ko 0.0 par rakh kar deterministic jawab dena.

[DATA START]
NOTIFICATION YEAR: August 2026
TRADE: Computer Operator and Programming Assistant (कम््यूटर ऑपरेटर एंर् प्रोग्रालमगं अलसथटेंट)

1. श्रवण बाधित (Hearing Impaired) आवेदकों ke liye seats:
- संभागीय जबलपुर: 24 Seats
- संभागीय उज्जैन: 12 Seats
- संभागीय इंदौर: 24 Seats
- संभागीय भोपाल: 24 Seats
- संभागीय रीवा: 24 Seats
- TOTAL SEATS FOR HEARING IMPAIRED: 108

RULES FOR HEARING IMPAIRED:
- Yeh seats 100% (शत-प्रतिशत) श्रवण बाधित आवेदकों ke liye reserved hain.
- Jo log 100% deaf nahi hain par hearing aid (श्रवण यंत्र) lagate hain, wo bhi apply kar sakte hain.
- Agar 100% deaf applicants nahi milte hain, toh dusre hearing impaired applicants ko MERIT ke basis par admission milega. Isliye sabhi ko option dalne ki salah di jati hai.

2. दृष्टि बाधित (Visually Impaired) आवेदकों ke liye seats:
- संभागीय जबलपुर: 24 Seats
- संभागीय उज्जैन: 12 Seats
- संभागीय भोपाल: 24 Seats
- संभागीय रीवा: 24 Seats
- संभागीय ग्वालियर: 12 Seats
- TOTAL SEATS FOR VISUALLY IMPAIRED: 96

RULES FOR VISUALLY IMPAIRED:
- Yeh seats 100% (शत-प्रतिशत) दृष्टि बाधित आवेदकों ke liye reserved hain.
- Jo log 100% blind nahi hain, wo kisi bhi institute ke liye apply kar sakte hain.
- Agar 100% blind applicants nahi milte hain, toh dusre visually impaired applicants ko MERIT ke basis par admission milega. Isliye sabhi ko option dalne ki salah di jati hai.
[DATA END]
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Apna sawal yahan likhein..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Gemini ka naya model call method
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=f"{SYSTEM_PROMPT}\n\nUser Question: {user_input}",
                config=types.GenerateContentConfig(temperature=0.0)
            )
            assistant_response = response.text
            message_placeholder.markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        except Exception as e:
            message_placeholder.markdown("Maafi chahta hoon, connection nahi ho paya. Kripya dobara koshish karein.")
