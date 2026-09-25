"""
Universitet Chatbotu üçün Sadə RAG (Retrieval-Augmented Generation) Nümunəsi
==============================================================================

Bu skript RAG-ın necə işlədiyini göstərir:
1. Məlumat bazası (bizim halda universitet FAQ-ları) yaradılır
2. İstifadəçi sual verir
3. Sual ilə ən uyğun məlumat tapılır (retrieval)
4. Tapılan məlumat əsasında cavab formalaşdırılır (generation)

Quraşdırma (əvvəlcə terminalda işə salın):
    pip install chromadb

İşə salmaq üçün:
    python rag_demo.py
"""

import chromadb

# ----------------------------------------------------------------------
# ADDIM 1: Vector Database yaratmaq
# ----------------------------------------------------------------------
# ChromaDB avtomatik olaraq mətnləri "embedding"-ə (rəqəmsal vektora)
# çevirir, ona görə bizim əlavə bir embedding modeli qurmağımıza
# ehtiyac yoxdur - bu, built-in gəlir.

client = chromadb.Client()
collection = client.create_collection(name="university_faq")

# ----------------------------------------------------------------------
# ADDIM 2: Nümunə məlumat bazası (real layihədə bu, sizin universitetdən
# topladığınız real suallar/cavablar olacaq)
# ----------------------------------------------------------------------

faq_documents = [
    "İmtahan qeydiyyatı hər semestrin əvvəlində Tələbə Portalı üzərindən aparılır.",
    "Kitabxana bazar ertəsi-cümə günləri saat 09:00-dan 20:00-a qədər açıqdır.",
    "Kurs seçimi (registration) semestr başlamazdan 2 həftə əvvəl açılır.",
    "Akademik arayış üçün Dekanlıq ofisinə müraciət etmək lazımdır.",
    "Buraxılış imtahanına düşməmək üçün minimum davamiyyət 75% olmalıdır.",
]

# Hər sənədə unikal ID verilir
doc_ids = [f"doc_{i}" for i in range(len(faq_documents))]

collection.add(
    documents=faq_documents,
    ids=doc_ids,
)

print("✅ Məlumat bazası hazırdır!\n")


# ----------------------------------------------------------------------
# ADDIM 3: Sual-cavab funksiyası (Retrieval hissəsi)
# ----------------------------------------------------------------------

def cavab_tap(sual: str, neçe_netice: int = 2):
    """
    İstifadəçinin sualına ən uyğun məlumatları tapır.
    """
    natijeler = collection.query(
        query_texts=[sual],
        n_results=neçe_netice,
    )
    return natijeler["documents"][0]


# ----------------------------------------------------------------------
# ADDIM 4: Test edək
# ----------------------------------------------------------------------

test_suallari = [
    "Kitabxana neçəyə qədər açıqdır?",
    "Davamiyyət faizi nə qədər olmalıdır?",
    "Kurs seçimi nə vaxt başlayır?",
]

for sual in test_suallari:
    print(f"❓ Sual: {sual}")
    cavablar = cavab_tap(sual, neçe_netice=1)
    print(f"📄 Tapılan məlumat: {cavablar[0]}\n")


# ----------------------------------------------------------------------
# QEYD: Bu, RAG-ın yalnız "Retrieval" (tapma) hissəsidir.
# ----------------------------------------------------------------------
# Real chatbotda bundan sonra addım əlavə olunur:
#   tapılan_melumat = cavab_tap(sual)
#   llm_cavab = llm.generate(f"Bu məlumata əsaslanaraq cavab ver: {tapılan_melumat}\n\nSual: {sual}")
#
# Yəni tapılan mətni bir LLM-ə (Claude, GPT və s.) göndərirsiniz ki,
# onu təbii, insan kimi cavaba çevirsin. Bunun üçün Anthropic və ya
# OpenAI API-dən istifadə edə bilərsiniz - istəsəniz bu hissəni də
# əlavə edə bilərəm.
