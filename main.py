import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from datetime import datetime
import csv

load_dotenv()

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# Add middleware / listeners here
@app.message("ㅎㅇ")
def say_hello(message, say):
    user = message["user"]
    print(user)
    say(f"Hi there, <@{user}>!")


@app.command("/문의사항 보내기")
def handle_submit_command(ack, body, client):
    ack()
    print(body)
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "submit_view",
            "private_metadata": body["channel_id"],
            "title": {"type": "plain_text", "text": "My App"},
            "submit": {"type": "plain_text", "text": "제출"},
            "close": {"type": "plain_text", "text": "취소"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "질문 게시판에 오신것을 환영합니다.",
                    },
                },
                {
                    "type": "input",
                    "block_id": "user_block_id",
                    "label": {
                        "type": "plain_text",
                        "text": "성함을 넣어주세요.",
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "user_action_id",
                        "multiline": False,
                    },
                },
                {
                    "type": "input",
                    "block_id": "title_block_id",
                    "label": {
                        "type": "plain_text",
                        "text": "제목을 넣어주세요.",
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "title_action_id",
                        "multiline": False,
                    },
                },
                {
                    "type": "input",
                    "block_id": "question_block_id",
                    "label": {
                        "type": "plain_text",
                        "text": "질문 사항을 넣어주세요.",
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "input_action_id",
                        "multiline": True,
                    },
                },
            ],
        },
    )


@app.view("submit_view")
def handle_view_submission_events(ack, body, client, logger):

    # 입력값에 대한 유효성 검사
    channel_id = body["view"]["private_metadata"]
    if channel_id != "C089DHKF4KE":
        ack(
            response_action="errors",
            errors={
                "question_block_id": "#질문은 소셜 게시판에서만 제출 할 수 있습니다."
            },
        )
        return None
    question = body["view"]["state"]["values"]["question_block_id"]["input_action_id"][
        "value"
    ]
    if len(question) < 3:
        ack(
            response_action="errors",
            errors={"question_block_id": "#질문은 3자이상이야 합니다."},
        )
        return None
    ack()

    # 저장할 데이터
    user_info = client.users_info(user=body["user"]["id"])
    user_name = body["view"]["state"]["values"]["user_block_id"]["user_action_id"][
        "value"
    ]
    # 질문 제목
    title = body["view"]["state"]["values"]["title_block_id"]["title_action_id"][
        "value"
    ]
    # 생성일자
    create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(create_at)

    # data 디렉토리가 없다면 생성
    if not os.path.exists("data"):
        os.makedirs("data")

        # 제출 정보를 CSV 파일에 저장
    with open("data/questions.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not os.path.getsize("data/questions.csv") > 0:
            writer.writerow(["user_name", "title", "question", "create_at"])
        writer.writerow([user_name, title, question, create_at])

    # 제출 후 완료 메세지
    text = f"*<@{user_info['user']['name']}>님의 `질문`이 제출되었습니다. "
    client.chat_postMessage(channel=channel_id, text=text)


# Start your app
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
