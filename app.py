import streamlit as st
import requests
import json

if "questions" not in st.session_state:
    st.session_state.questions = None


# konfigurasi
st.set_page_config(
    page_title="🧑‍💼📝 AI Interview Assistant",
    layout="centered"
)

# custom css
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@600;700;800&display=swap');

.stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #dbeafe 100%);
    background-attachment: fixed;
    color: #1f2937;
}

html {
    scroll-behavior: smooth;
}

h1 {
    font-family: 'Poppins', sans-serif;
    color: #1e40af;
    font-weight: 800;
}
            
.app-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
    border-bottom: 3px solid #3b82f6;
    padding-bottom: 1rem;
}

.title-text {
    color: #1e40af;
}

.title-emoji {
    color: initial;
}

h2 {
    font-family: 'Poppins', sans-serif;
    color: #1e40af;
    font-weight: 700;
    font-size: 1.875rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
    letter-spacing: -0.3px;
}

h3 {
    font-family: 'Poppins', sans-serif;
    color: #1e40af;
    font-weight: 600;
    font-size: 1.5rem;
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
}

p {
    line-height: 1.7;
    color: #374151;
    margin-bottom: 1rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #eff6ff 0%, #dbeafe 50%, #bfdbfe 100%);
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #1e40af;
    font-weight: 600;
    border-bottom: 2px solid #3b82f6;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

[data-testid="stSidebar"] a {
    color: #2563eb;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
    border-bottom: 1px solid transparent;
}

[data-testid="stSidebar"] a:hover {
    color: #1d4ed8;
    border-bottom-color: #1d4ed8;
}

[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown li {
    color: #374151;
}


.stButton > button {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    font-weight: 600;
    font-size: 1rem;
    border-radius: 10px;
    padding: 0.875rem 2rem;
    border: none;
    box-shadow: 0 4px 6px rgba(59, 130, 246, 0.25), 0 2px 4px rgba(0, 0, 0, 0.06);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    width: 100%;
    font-family: 'Inter', sans-serif;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    box-shadow: 0 8px 12px rgba(59, 130, 246, 0.35), 0 4px 6px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
}

.stButton > button:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(59, 130, 246, 0.25);
}

.stButton > button:disabled {
    background: linear-gradient(135deg, #cbd5e1 0%, #94a3b8 100%);
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
    opacity: 0.6;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select {
    border: 2px solid #e5e7eb;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    transition: all 0.3s ease;
    background-color: white;
    color: #1f2937;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    font-family: 'Inter', sans-serif;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > select:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1), 0 1px 3px rgba(0, 0, 0, 0.05);
    outline: none;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #9ca3af;
    font-style: italic;
    opacity: 0.7;
}

.stTextInput > label,
.stTextArea > label,
.stSelectbox > label {
    font-weight: 600;
    color: #374151;
    font-size: 1rem;
    margin-bottom: 0.5rem;
    display: block;
}

.question-box {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 10px 15px rgba(0, 0, 0, 0.03);
    margin: 1.5rem 0;
    border: 1px solid #e5e7eb;
    border-left: 5px solid #3b82f6;
    animation: fadeIn 0.5s ease-out;
}

.feedback-box {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    padding: 2rem;
    border-radius: 12px;
    border-left: 5px solid #0ea5e9;
    margin: 1.5rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 10px 15px rgba(0, 0, 0, 0.03);
    position: relative;
    overflow: hidden;
    animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# judul dan deskripsi aplikasi (memisahkan emoji dan teks untuk styling)
st.markdown("""
<h1 class="app-title">
  <span class="title-emoji">🧑‍💼📝</span>
  <span class="title-text">AI Interview Assistant</span>
</h1>
""", unsafe_allow_html=True)
st.write("Bantu kamu mempersiapkan diri untuk interview kerja dengan pertanyaan dan feedback dari AI sesuai posisi yang kamu dilamar.")

# sidebar
st.sidebar.header("⚙️ Pengaturan")
api_key = st.sidebar.text_input("OpenRouter API Key", type="password")
st.sidebar.markdown("[🔑 Dapatkan API Key di OpenRouter](https://openrouter.ai/)")

model = st.sidebar.selectbox(
    "Pilih Model AI",
    [
        "mistralai/mistral-7b-instruct",
        "qwen/qwen-2.5-7b-instruct",
        "gpt-4o-mini"
    ]
)

bahasa = st.sidebar.selectbox(
    "Bahasa Pertanyaan",
    ["Indonesia", "Inggris"]
)

st.sidebar.subheader("💡 Cara Penggunaan: ")
st.sidebar.markdown("""
1. Masukkan API Key dari OpenRouter (https://openrouter.ai/)
2. Pilih model AI yang diinginkan
3. Pilih bahasa pertanyaan yang akan di tampilkan AI
4. Masukkan posisi kerja yang ingin dilamar
5. Pilih jenis interview (HR, Technical, atau keduanya)
6. Klik "Generate Pertanyaan Interview" untuk mendapatkan pertanyaan interview
7. Jawab pertanyaan yang dihasilkan
8. Klik "Berikan Feedback AI" untuk mendapatkan feedback dari AI
""")

# kelas untuk menghasilkan pertanyaan interview
class InterviewGenerator:
    def __init__(self, api_key, model, bahasa):
        self.api_key = api_key
        self.model = model
        self.bahasa = bahasa
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    
    def generate(self, job_title, interview_type):
        prompt = f"""
        Kamu adalah {interview_type} profesional.
        Buat 5 pertanyaan interview {interview_type}
        dalam bahasa {self.bahasa}
        untuk posisi {job_title}.
        Sertakan dalam kurung tips singkat menjawab setiap pertanyaan di bawah setiap pertanyaan
        dan untuk setiap pertanyaan baru beri jarak 1 baris serta gunakan format list seperti berikut:
        1. Pertanyaan pertama
            (tips menjawab)
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(self.url, headers=headers, json=data)
        result = response.json()
        
        if "choices" not in result:
            return f"Terjadi kesalahan: {result}"
        
        return result["choices"][0]["message"]["content"]
    
    def _send_request(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": [
            {"role": "user", "content": prompt}
        ]
    }

        response = requests.post(self.url, headers=headers, json=data)
        result = response.json()

        if "choices" not in result:
            return f"Terjadi kesalahan: {result}"
    
        return result["choices"][0]["message"]["content"]

    
    def evaluate(self, questions, user_answer):
        prompt = f"""
        Kamu adalah perekrut profesional.

        Bahasa: {self.bahasa}
        Pertanyaan interview:
        {questions}

        Jawaban kandidat:
        {user_answer}

        Berikan evaluasi singkat terhadap jawaban kandidat berdasarkan: (translate to {self.bahasa})
        1. Nilai kejelasan (1 - 10)
        2. Nilai relevansi (1 - 10)
        3. Nilai kepercayaan diri (1 - 10)
        4. Saran perbaikan:
        """
        return self._send_request(prompt)

job_title = st.text_input("Posisi Kerja yang Dilamar")


interview_type = st.selectbox(
    "Jenis Interview",
    ["HR", "Technical", "HR & Technical"]
)

if st.button("Generate Pertanyaan Interview"):
    if not api_key or not job_title:
        st.warning("posisi kerja dan API Key tidak boleh kosong.")
    else:
        with st.spinner("Loading..."):
            generator = InterviewGenerator(api_key, model, bahasa)
            st.session_state.questions = generator.generate(job_title, interview_type)

if st.session_state.questions:
    st.subheader("Hasil Pertanyaan Interview")
    st.write(st.session_state.questions)
    user_answer = st.text_area(
        "Tulis jawaban interview kamu di sini..."
    )

    if st.button("Berikan Feedback AI"):
        if not api_key or not user_answer:
            st.warning("Isi jawaban interview terlebih dahulu.")
        else:
            with st.spinner("Loading..."):
                generator = InterviewGenerator(api_key, model, bahasa)
                feedback = generator.evaluate(
                    st.session_state.questions,
                    user_answer
                )

            st.subheader("Feedback AI")
            st.write(feedback)

    if st.button("Reset AI"):
        st.session_state.questions = None
        st.rerun()



st.markdown("---")
st.caption("AI Yang membantu kamu dalam persiapan interview kerja. Dibuat dengan ❤️ oleh Ordrick")