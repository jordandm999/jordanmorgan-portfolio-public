import openai
import os
from rest_framework.views import APIView
from rest_framework.response import Response

class ChatAPIView(APIView):
    def post(self, request):
        user_message = request.data.get("message")
        if not user_message:
            return Response({"error": "No message provided"}, status=400)

        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.responses.create(
            model="gpt-4o-mini",
            tools=[
                {
                    "type": "mcp",
                    "server_label": "characters-mcp",
                    "server_url": "https://jordan-morgan.onrender.com/api/mcp_server",
                    "require_approval": "never"
                }
            ],
            input=user_message
        )
        return Response({"response": response.output_text})
