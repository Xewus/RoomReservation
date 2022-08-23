# RoomReservation

### Python 3.10
### FastAPI

Room Management application.
Allows you to select and book the desired room.

Create virtual environment
```
python3.10  -m venv venv
```
Go into
```
cd RoomReservation/
```
Upgrade pip
```
pip install -U pip
```
Install requirements
```
pip install -r requriments.txt
```
creat `.env` file
```
touch .env
```
fill like it
```
APP_TITLE=<Your title>
DATABASE_URL=<sqlite+aiosqlite:///./fastapi.db>
VERSION=0.1.1
DESCRIPTION=<Your description>
SECRET_KEY=<Your long string>
```
