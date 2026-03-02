from app.api.auth_routes import forgot_password
from app.database.database import SessionLocal
import traceback

if __name__ == '__main__':
    db = SessionLocal()
    try:
        print('calling forgot_password')
        result = forgot_password('test@example.com', db)
        print('result:', result)
    except Exception as e:
        traceback.print_exc()
