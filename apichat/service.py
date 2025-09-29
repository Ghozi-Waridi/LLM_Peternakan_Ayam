# api_chat/services.py

from groq import Groq
from django.conf import settings
import logging
from .models import ChatMessage, DebateSession  # <-- Import yang benar

logger = logging.getLogger(__name__)


def get_groq_response(session_id: int, user_prompt: str):
    """
    Mengirim prompt ke Groq API dengan menyertakan history dari database
    dan mengembalikan respons teks dari LLM.
    """

    api_key = settings.GROQ_API_KEY

    if not api_key:
        logger.error("GROQ_API_KEY tidak ditemukan.")
        return "Error: Konfigurasi API Key Groq tidak ditemukan."

    try:
        chat_history_from_db = ChatMessage.objects.filter(
            session_id=session_id
        ).order_by("created_at")
        print(chat_history_from_db)

        # messages_for_groq = [
        #     {
        #         "role": "system",
        #         "content": "Anda adalah seorang lulusan S2 yang sudah ahli dalam analisis, sekrang anda menjadi seorang bos di peternakan ayam petelur.",
        #     }
        # ]

        # for message in chat_history_from_db:
        #     print("Message from DB: ", message.role)
        #     messages_for_groq.append({"role": message.role, "content": message.content})

        # messages_for_groq.append({"role": "user", "content": user_prompt})

        messages_for_groq = [
            {
                "role": "system",
                "content": "Anda adalah seorang lulusan S2 yang sudah ahli dalam analisis, sekrang anda menjadi seorang bos di peternakan ayam petelur.",
            }
        ]

        valid_roles = {"system", "user", "assistant"}

        for message in chat_history_from_db:
            role = (message.role or "user").lower()
            if role not in valid_roles:
                role = "user"
            messages_for_groq.append({"role": role, "content": message.content})

        messages_for_groq.append({"role": "user", "content": user_prompt})

        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=messages_for_groq,
            model="gemma2-9b-it",
            temperature=0.2,
            # max_tokens=200,
        )

        response_text = chat_completion.choices[0].message.content

        if response_text:
            ChatMessage.objects.create(
                session_id=session_id, role="assistant", content=response_text
            )

        return response_text

    except DebateSession.DoesNotExist:
        logger.error(f"Sesi debat dengan ID {session_id} tidak ditemukan.")
        return "Error: Sesi debat tidak valid."
    except Exception as e:
        logger.error(f"Terjadi error saat menghubungi Groq API: {e}")
        return "Maaf, terjadi kesalahan internal saat memproses permintaan Anda."
