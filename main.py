import os
import csv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# Add middleware / listeners here
@app.message("ㅎㅇ")
def say_hello(message, say):
    user = message["user"]
    print(user)
    say(f"Hi there, <@{user}>!")


@app.command("/문의사항제출")
def handle_submit_command(ack, body, client):
    ack()
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
    user_id = body["user"]["id"]
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

    # data 디렉토리가 없다면 생성
    if not os.path.exists("data"):
        os.makedirs("data")

        # 제출 정보를 CSV 파일에 저장
    with open("data/questions.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not os.path.getsize("data/questions.csv") > 0:
            writer.writerow(["user_id", "user_name", "title", "question", "create_at"])
        writer.writerow([user_id, user_name, title, question, create_at])

    # 제출 후 완료 메세지
    text = f"*<@{user_info['user']['name']}>님의 `문의 사항`이 제출되었습니다. "
    client.chat_postMessage(channel=channel_id, text=text)


@app.command("/제출내역")
def handle_submission_history_command(ack, body, client: WebClient):
    ack()
    user_id = body["user_id"]

    # 사용자의 DM 채널 ID 가져오기
    response = client.conversations_open(users=user_id)
    dm_channel_id = response["channel"]["id"]
    # 만약에 제출내역 파일이 없다면 "제출내역 파일 없음"이라고 메세지 전송하고 종료
    if not os.path.exists("data/questions.csv"):
        client.chat_postMessage(channel=dm_channel_id, text="*제출내역이 없습니다.*")
        return None
    # 사용자의 제출내역만 필터링
    submission_list = []

    with open("data/questions.csv", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["user_id"] == user_id:
                submission_list.append(row)
    print(submission_list, "submission_list")
    # 만약에 제출내역이 없다면 "제출내역 없음"이라고 메세지를 전송하고 종료
    if not submission_list:
        client.chat_postMessage(channel=dm_channel_id, text="*제출내역이 없습니다.*")
        return None
    # 사용자의 제출내역을 csv 파일로 임시 저장 후 전송
    temp_dir = "data/temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    temp_file_path = f"{temp_dir}/{user_id}.csv"
    with open(temp_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        writer.writerows(submission_list)

    client.files_upload_v2(
        channel=dm_channel_id,
        file=temp_file_path,
        initial_comment=f"<@{user_id}>님의 제출내역입니다!",
    )
    # 임시로 생성한 csv 파일 삭제
    os.remove(temp_file_path)


@app.command("/관리자")
def handle_admin_command(ack, body, client: WebClient):
    ack()

    # 관리자인지 확인 후 아니라면 메시지 전송 후 종료
    user_id = body["user_id"]
    if user_id != "U089ZS8NVK2":
        client.chat_postEphemeral(
            channel=body["channel_id"],
            user=user_id,
            text="관리자만 사용 가능한 명령어입니다.",
        )
        return None
    # 관리자용 버튼 전송(전체 제출내역을 반환)
    client.chat_postEphemeral(
        channel=body["channel_id"],
        user=user_id,
        text="관리자 메뉴를 선택해주세요.",
        blocks=[
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "전체 제출내역 조회",
                            "emoji": True,
                        },
                        "value": "admin_value_1",
                        "action_id": "fetch_all_submissions",
                    }
                ],
            }
        ],
    )


@app.action("fetch_all_submissions")
def handle_some_action(ack, body, client: WebClient):
    ack()
    # 관리자의 DM 채녈 ID 가져오기
    response = client.conversations_open(users=body["user"]["id"])
    dm_channel_id = response["channel"]["id"]

    # 전체 제출내역을 불러와서 전송
    file_path = "data/questions.csv"
    if not os.path.exists(file_path):
        client.chat_postMessage(channel=dm_channel_id, text="제출내역이 없습니다.")
        return None

    client.files_upload_v2(
        channel=dm_channel_id,
        file=file_path,
        initial_comment="전체 제출내역 입니다!",
    )


# Start your app
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
