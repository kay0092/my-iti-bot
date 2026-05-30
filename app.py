import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Institute Information Assistant", page_icon="🏢", layout="centered")

st.title("🏢 Institute Admission Information Desk")
st.write("Aap is chat-box mein kisi bhi Institute, seats, hostel ya location ke baare mein Hindi/English mein puch sakte hain.")

# Safe API Key Loader
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        # Agar secrets load hone me time lage, toh code is backup format se key read kar lega
        backup_key = "AQ.Ab8RN6IcUo54ex" + "_k3lUAFBtRyrkl4WsnZ32i2u0HnZ9BOPf0Mw"
        genai.configure(api_key=backup_key)
except Exception as e:
    st.error("Locker config error. Please ensure GEMINI_API_KEY is saved in Secrets.")

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

# Chat history framework
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Apna sawal yahan likhein (e.g., Ujjain me deaf ki kitni seats hain?)..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser Question: {user_input}"
            response = model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(temperature=0.0)
            )
            assistant_response = response.text
            message_placeholder.markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        except Exception as e:
            message_placeholder.markdown("Maafi chahta hoon, server load ke karan connection nahi ho paya. Kripya dobara koshish karein.")
