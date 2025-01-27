# Slack Bot README

## 설치 및 설정 (Korean)

### 사전 준비
- Python 3.x 필요

### 설치 단계
1. 가상환경 생성
   ```bash
   python -m venv myenv
   ```

2. 가상환경 활성화
   - Windows: `myenv\Scripts\activate`
   - Mac/Linux: `source myenv/bin/activate`

3. 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```

4. 환경변수 설정
   - `SLACK_BOT_TOKEN`: Slack Bot Token
   - `SLACK_APP_TOKEN`: Slack App Token

### Slack 앱 구성

#### [OAuth & Permissions]

- **접근 방법**:
  1. [Slack API 대시보드](https://api.slack.com/apps)로 이동
  2. 개발 중인 앱 선택
  3. "OAuth & Permissions" 메뉴 선택

- **필요 권한 설정**:
  - `channels:history`: 채널 메시지 히스토리 읽기
  - `channels:write.invites`: 퍼블릭 채널에 멤버 초대
  - `channels:write.topic`: 퍼블릭 채널 설명 변경
  - `chat:write`: 메시지 전송
  - `commands`: 슬래시 명령어 처리
  - `files:write`: 파일 업로드, 편집, 삭제
  - `groups:write`: 개인 채널 관리 및 생성
  - `im:history`: 다이렉트 메시지 히스토리 읽기
  - `im:write`: 다이렉트 메시지 시작
  - `mpim:write`: 그룹 다이렉트 메시지 시작
  - `users:read`: 사용자 정보 접근

#### [Slash Commands]
- **접근 방법**:
  1. [Slack API 대시보드](https://api.slack.com/apps)로 이동
  2. 개발 중인 앱 선택
  3. "Slash Commands" 메뉴 선택

- **슬래시 명령어 구성**:
  - 명령어: `/문장제출`, `/제출내역`

5. 봇 실행
   ```bash
   python main.py
   ```

### 사용법
- "ㅎㅇ"로 인사말 받기
- `/문장제출`로 질문 제출
- 질문은 `data/questions.csv`에 저장

### 파일 구조
- `main.py`: 봇 메인 코드
- `requirements.txt`: 패키지 목록
- `data/`: 질문 저장 디렉토리

---

## Installation & Setup (English)

### Prerequisites
- Python 3.x required

### Installation Steps
1. Create virtual environment
   ```bash
   python -m venv myenv
   ```

2. Activate virtual environment
   - Windows: `myenv\Scripts\activate`
   - Mac/Linux: `source myenv/bin/activate`

3. Install packages
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables
   - `SLACK_BOT_TOKEN`: Slack Bot Token
   - `SLACK_APP_TOKEN`: Slack App Token

### Slack App Configuration

#### [OAuth & Permissions]

- **How to Access**:
  1. Go to [Slack API Dashboard](https://api.slack.com/apps)
  2. Select the app under development
  3. Choose the "OAuth & Permissions" menu

- **Required Permissions**:
  - `channels:history`: Read channel message history
  - `channels:write.invites`: Invite members to public channels
  - `channels:write.topic`: Set the description of public channels
  - `chat:write`: Send messages
  - `commands`: Handle slash commands
  - `files:write`: Upload, edit, and delete files
  - `groups:write`: Manage private channels and create new ones
  - `im:history`: View direct message history
  - `im:write`: Start direct messages with people
  - `mpim:write`: Start group direct messages with people
  - `users:read`: Access user information

#### [Slash Commands]
- **How to Access**:
  1. Go to [Slack API Dashboard](https://api.slack.com/apps)
  2. Select app under development
  3. Choose "Slash Commands" menu

- **Slash Command Configuration**:
  - Command: `/문장제출`
  - Set Request URL
  - Add description and usage hint

5. Run bot
   ```bash
   python main.py
   ```

### Usage
- Receive greeting with "ㅎㅇ"
- Submit questions with `/문장제출`
- Questions saved in `data/questions.csv`

### File Structure
- `main.py`: Bot main code
- `requirements.txt`: Package list
- `data/`: Question storage directory
