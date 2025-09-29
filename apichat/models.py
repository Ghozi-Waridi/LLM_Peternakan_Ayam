# api_chat/models.py


from django.db import models


# class TopicDebate(models.Model):
#     topic = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.topic


class DebateSession(models.Model):
    topic = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):

    session = models.ForeignKey(
        DebateSession, related_name="messages", on_delete=models.CASCADE
    )
    role = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
