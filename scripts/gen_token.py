import secrets

LENGTH = 32

if __name__ == "__main__":
    token = secrets.token_urlsafe(LENGTH)
    print(token)
