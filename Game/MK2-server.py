from flask import Flask, Response
from PIL import Image, ImageDraw
import io
import time

app = Flask(__name__)

# Konstanten für das Spiel
WIDTH = 800
HEIGHT = 400
BALL_RADIUS = 10
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 75
BALL_SPEED_X = 4
BALL_SPEED_Y = 4

# Spiel-Status
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = BALL_SPEED_X
ball_dy = BALL_SPEED_Y
paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2

# Das Spiel läuft in einer Endlosschleife
@app.route('/game')
def game():
    def generate_frames():
        global ball_x, ball_y, ball_dx, ball_dy, paddle_y

        while True:
            # Spiellogik
            ball_x += ball_dx
            ball_y += ball_dy

            if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
                ball_dy = -ball_dy

            if ball_x - BALL_RADIUS <= PADDLE_WIDTH and paddle_y <= ball_y <= paddle_y + PADDLE_HEIGHT:
                ball_dx = -ball_dx

            if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= WIDTH:
                ball_x = WIDTH // 2
                ball_y = HEIGHT // 2
                ball_dx = BALL_SPEED_X
                ball_dy = BALL_SPEED_Y

            # Zeichnen des Spiels
            img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Ball zeichnen
            draw.ellipse((ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, ball_x + BALL_RADIUS, ball_y + BALL_RADIUS), fill=(255, 255, 255))

            # Paddle zeichnen
            draw.rectangle((0, paddle_y, PADDLE_WIDTH, paddle_y + PADDLE_HEIGHT), fill=(255, 255, 255))

            # Bild als PNG zurückgeben
            img_io = io.BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            yield (b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + img_io.read() + b'\r\n')

            # Pause für das Frame-Update (60 FPS)
            time.sleep(1 / 60)

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
