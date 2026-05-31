import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Institute Information Assistant",
    page_icon="🏢",
    layout="centered",
)

st.title("🏢 Institute Admission Information Desk")
st.write(
    "Aap is chat-box mein kisi bhi Institute, seats, hostel ya location ke baare mein Hindi/English mein puch sakte hain."
)

client = None

try:
    gemini_api_key = st.secrets.get("GEMINI_API_KEY", "")
    if gemini_api_key:
        client = genai.Client(api_key=gemini_api_key)
    else:
        st.error("API Key missing! Advanced settings ke Secrets mein GEMINI_API_KEY add karein.")
except Exception as e:
    st.error(f"Secrets Configuration Error: {str(e)}")

SYSTEM_PROMPT = """
Aap ek strictly professional Institute Admission Assistant hain. Aapko sirf aur sirf niche diye gaye DATA ke basis par jawab dena hai.
Agar koi data ismein nahi hai, toh saaf bol dijiye: "Main maafi chahta/chahti hoon, iski jankari PDF mein nahi hai."
Apne mann se koi bhi institute, seat, ya rules mat banana.

[DATA START]
NOTIFICATION YEAR: August 2026
TRADE: Computer Operator and Programming Assistant (कंप्यूटर ऑपरेटर एंड प्रोग्रामिंग असिस्टेंट)

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

user_input = st.chat_input("Apna sawal yahan likhein...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    if client is None:
        with st.chat_message("assistant"):
            st.warning(
                "API client ready nahi hai. Streamlit Advanced settings ke Secrets mein "
                'GEMINI_API_KEY = "aapki_api_key" add karke app reboot karein.'
            )
        st.stop()

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"{SYSTEM_PROMPT}\n\nUser Question: {user_input}",
                config=types.GenerateContentConfig(
                    temperature=0.0,
                    max_output_tokens=500,
                ),
            )

            assistant_response = response.text or "Koi response nahi mila."
            message_placeholder.markdown(assistant_response)

            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_response}
            )

        except Exception as e:
            message_placeholder.error(
                f"Connection Diagnostic Error: {str(e)}\n\n"
                "Kripya check karein: Secrets mein GEMINI_API_KEY sahi hai, app reboot hua hai, "
                "aur requirements.txt mein google-genai added hai."
            )
