from app import app
from app.extensions import socket

if __name__ == "__main__":
    socket.run(app)
