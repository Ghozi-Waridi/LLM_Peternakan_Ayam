# api_chat/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import get_groq_response
from .models import DebateSession, ChatMessage


# class TopicDebateListAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         topic = request.data.get("topic")

#         if not topic:
#             return Response(
#                 {"error": "Topic is required"}, status=status.HTTP_400_BAD_REQUEST
#             )

#         if TopicDebate.objects.filter(topic=topic).exists():
#             return Response(
#                 {"error": "Topic already exists"}, status=status.HTTP_400_BAD_REQUEST
#             )

#         new_topic = TopicDebate.objects.create(topic=topic)

#         return Response(
#             {
#                 "id": new_topic.id,
#                 "topic": new_topic.topic,
#                 "message": "Topic created successfully",
#             },
#             status=status.HTTP_201_CREATED,
#         )

#     def get(self, request, *args, **kwargs):
#         topics = TopicDebate.objects.all()
#         data = [{"id": topic.id, "topic": topic.topic} for topic in topics]
#         return Response(data, status=status.HTTP_200_OK)


class GroqChatAPIView(APIView):
    """
    View untuk menangani logika chat debat.
    Bisa memulai sesi baru atau melanjutkan yang sudah ada.
    """

    def post(self, request, *args, **kwargs):
        print("Coba : ", request.data)
        user_prompt = request.data.get("prompt")
        session_id = request.data.get("sessionId")
        topic = request.data.get("topic")

        if session_id:
            try:
                session = DebateSession.objects.get(id=session_id)
            except DebateSession.DoesNotExist:
                return Response(
                    {"error": "Sesi debat tidak ditemukan."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            session = DebateSession.objects.create(topic=topic)
            user_prompt = f"{user_prompt}"
            print(f"User Prompt : {user_prompt}")

        print(session)
        ChatMessage.objects.create(session=session, content=user_prompt)
        print("User prompt: ", user_prompt, "sessionID : ", session)
        ai_response_text = get_groq_response(session.id, user_prompt)
        return Response(
            {"response": ai_response_text, "session_id": session.id},
            status=status.HTTP_200_OK,
        )
