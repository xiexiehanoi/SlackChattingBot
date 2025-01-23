# Slack Bot

## 설정 (Korean)

### 사전 준비
- Python 3.x 설치 필요

### 설치 단계
1. 가상환경 생성
   ```bash
   python -m venv myenv
   ```

2. 가상환경 활성화
   - Windows: `myenv\Scripts\activate`
   - Mac/Linux: `source myenv/bin/activate`

3. 필요한 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```

4. 환경변수 설정
   - `SLACK_BOT_TOKEN`: Slack에서 발급받은 Bot Token
   - `SLACK_APP_TOKEN`: Slack에서 발급받은 App Token

5. Slack 앱 권한 설정
   - [Slack API 대시보드](https://api.slack.com/apps)에서 앱 선택
   - OAuth & Permissions 메뉴에서 Bot Token Scopes에 다음 권한 추가:
     * `channels:history`
     * `chat:write`
     * `commands`
     * `im:history`
     * `users:read`

6. 봇 실행
   ```bash
   python main.py
   ```

### 사용법
- "ㅎㅇ" 메시지 전송 시 인사말 받기
- `/문장제출` 명령어로 질문 제출
- 제출된 질문은 `data/questions.csv`에 저장됨

### 파일 구조
- `main.py`: 봇 메인 코드
- `requirements.txt`: 파이썬 패키지 목록
- `data/`: 제출된 질문 저장 디렉토리

---

## Setup (English)

### Prerequisites
- Python 3.x installation required

### Installation Steps
1. Create virtual environment
   ```bash
   python -m venv myenv
   ```

2. Activate virtual environment
   - Windows: `myenv\Scripts\activate`
   - Mac/Linux: `source myenv/bin/activate`

3. Install required packages
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables
   - `SLACK_BOT_TOKEN`: Bot Token from Slack
   - `SLACK_APP_TOKEN`: App Token from Slack

5. Configure Slack app permissions
   - Go to [Slack API Dashboard](https://api.slack.com/apps)
   - Select your app
   - In OAuth & Permissions, add the following scopes to Bot Token Scopes:
     * `channels:history`
     * `chat:write`
     * `commands`
     * `im:history`
     * `users:read`

6. Run the bot
   ```bash
   python main.py
   ```

### Usage
- Send "ㅎㅇ" to receive a greeting
- Use `/문장제출` command to submit a question
- Submitted questions are saved in `data/questions.csv`

### File Structure
- `main.py`: Main bot code
- `requirements.txt`: List of Python packages
- `data/`: Directory to store submitted questions
