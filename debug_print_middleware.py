from app.main import app
print('User middleware:', app.user_middleware)
print('Middleware:', app.user_middleware)
for mw in app.user_middleware:
    print(type(mw), mw)
