"""
Universitet Chatbotu - Frontend (Streamlit)
=============================================

Bu, chatbotumuz üçün veb interfeysdir. Streamlit sayəsində
HTML/CSS/JS bilmədən tam işlək bir chat ekranı qururuq.

Quraşdırma (terminalda):
    pip install streamlit chromadb

İşə salmaq (VACIB - adi "python" ilə yox!):
    streamlit run frontend_app.py

Bu əmr avtomatik brauzerdə bir səhifə açacaq.
"""

import streamlit as st
import chromadb

# ----------------------------------------------------------------------
# Səhifə tənzimləmələri
# ----------------------------------------------------------------------
st.set_page_config(page_title="Universitet Köməkçisi", page_icon="🎓")
st.title("🎓 Universitet Köməkçi Chatbotu")
st.caption("Kurs, cədvəl və digər universitet sualları üçün")


# ----------------------------------------------------------------------
# Vector Database-i yaratmaq (bir dəfə, cache ilə - hər dəfə yenidən
# qurulmasın deyə)
# ----------------------------------------------------------------------

@st.cache_resource
def db_qur():
    client = chromadb.Client()
    collection = client.create_collection(name="university_faq")

    faq_documents = [
        "İmtahan qeydiyyatı hər semestrin əvvəlində Tələbə Portalı üzərindən aparılır.",
        "Kitabxana bazar ertəsi-cümə günləri saat 09:00-dan 20:00-a qədər açıqdır.",
        "Kurs seçimi (registration) semestr başlamazdan 2 həftə əvvəl açılır.",
        "Akademik arayış üçün Dekanlıq ofisinə müraciət etmək lazımdır.",
        "Buraxılış imtahanına düşməmək üçün minimum davamiyyət 75% olmalıdır.",
    ]
    doc_ids = [f"doc_{i}" for i in range(len(faq_documents))]
    collection.add(documents=faq_documents, ids=doc_ids)
    return collection


collection = db_qur()


def cavab_tap(sual: str):
    natijeler = collection.query(query_texts=[sual], n_results=1)
    return natijeler["documents"][0][0]


# ----------------------------------------------------------------------
# Chat tarixçəsini yadda saxlamaq üçün (session state)
# ----------------------------------------------------------------------

if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

# Köhnə mesajları göstər
for mesaj in st.session_state.mesajlar:
    with st.chat_message(mesaj["rol"]):
        st.write(mesaj["metn"])


# ----------------------------------------------------------------------
# İstifadəçi sual yazanda
# ----------------------------------------------------------------------

sual = st.chat_input("Sualınızı yazın...")

if sual:
    # İstifadəçinin sualını göstər və yadda saxla
    st.session_state.mesajlar.append({"rol": "user", "metn": sual})
    with st.chat_message("user"):
        st.write(sual)

    # Cavabı tap və göstər
    cavab = cavab_tap(sual)
    st.session_state.mesajlar.append({"rol": "assistant", "metn": cavab})
    with st.chat_message("assistant"):
        st.write(cavab)

# ----------------------------------------------------------------------
# QEYD: Hazırda bu, birbaşa tapılan məlumatı göstərir (LLM olmadan).
# Ollama-nı qurduqdan sonra, "cavab_tap" funksiyasını "cavab_yarat"
# ilə (əvvəlki fayldakı kimi) əvəz edib, daha təbii cavablar ala bilərik.
# ----------------------------------------------------------------------
