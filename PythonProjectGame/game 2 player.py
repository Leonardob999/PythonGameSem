import turtle
import winsound
import time
import Game.connectMqtt1 as Mqtt1
import Game.connectMqtt2 as Mqtt2

wn = turtle.Screen()
wn.title("Pong by Robin")
wn.bgcolor("black")
wn.setup(width=800, height=600)

game_initiated = False
game_paused = True

# Score
score_a = 0
score_b = 0

# Paddle A (left)
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B (right)
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(+350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("green")
ball.penup()
ball.goto(0, 0)
ball.dx = 4
ball.dy = 4

# Pen for score and messages
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Drücke k um das Spiel zu starten", align="center", font=("Courier", 24, "normal"))

# Pen for pause messages
pen2 = turtle.Turtle()
pen2.speed(0)
pen2.color("white")
pen2.penup()
pen2.hideturtle()
pen2.goto(0, 200)

# Functions
def start_game():
    global game_initiated, game_paused
    game_initiated = True
    game_paused = False
    pen.clear()
    pen.write(f"player a: {score_a}    player b: {score_b}", align="center", font=("Courier", 24, "normal"))
    pen2.clear()

def pause_game():
    global game_paused
    if not game_paused:
        game_paused = True
        pen2.write("PAUSED", align="center", font=("Courier", 32, "normal"))
    else:
        game_paused = False
        pen2.clear()

def paddle_a_up():
    if not game_paused and game_initiated:  # Only move the paddle if the game is running and not paused
        y = paddle_a.ycor()
        y += 20
        paddle_a.sety(y)

def paddle_a_down():
    if not game_paused and game_initiated:  # Only move the paddle if the game is running and not paused
        y = paddle_a.ycor()
        y -= 20
        paddle_a.sety(y)



def paddle_b_up():
    if not game_paused and game_initiated:  # Only move the paddle if the game is running and not paused
        y = paddle_b.ycor()
        y += 20
        paddle_b.sety(y)

def paddle_b_down():
    if not game_paused and game_initiated:  # Only move the paddle if the game is running and not paused
        y = paddle_b.ycor()
        y -= 20
        paddle_b.sety(y)


def update():
    breakpoint()

def ragequit():
    winsound.PlaySound("2025-01-22-22-05-40.wav", winsound.SND_ASYNC)
    time.sleep(2.9)
    turtle.bye()

# Keyboard bindings
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")

wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")

wn.onkeypress(ragequit, "h")
wn.onkeypress(start_game, "k")
wn.onkeypress(pause_game, "p")

# Main Game Loop
while True:
    wn.update()

    if not game_initiated or game_paused:
        continue

    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    #MPU controls, rechte seite
    if Mqtt1.a_x_data > 3:
        y = paddle_b.ycor()
        y += 10
        paddle_b.sety(y)

    if Mqtt1.a_x_data < -3:
        y = paddle_b.ycor()
        y -= 10
        paddle_b.sety(y)

    #MPU controls, linke Seite
    if Mqtt2.a_x_data > 3:
        y = paddle_a.ycor()
        y += 10
        paddle_a.sety(y)

    if Mqtt2.a_x_data < -3:
        y = paddle_a.ycor()
        y -= 10
        paddle_a.sety(y)


    # border action

    # wenn Ball oben / unten berührt, richtung umdrehen
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    # wenn Ball rechts / links raus, zurrück zur Mitte, in gegenrichtung los
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        pen.clear()  # Entferne die vorherige Anzeige, bevor du neu schreibst
        pen.write(f'player a: {score_a}    player b: {score_b}', align="center", font=("Courier", 24, "normal"))
        winsound.PlaySound("Unbenanntes-Video-–-Mit-Clipchamp-erstellt-_8_.wav", winsound.SND_ASYNC)

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        pen.clear()  # Entferne die vorherige Anzeige
        pen.write(f'player a: {score_a}    player b: {score_b}', align="center", font=("Courier", 24, "normal"))
        winsound.PlaySound("Unbenanntes-Video-–-Mit-Clipchamp-erstellt-_8_.wav", winsound.SND_ASYNC)

    # wenn paddle oben / unten berühren, anhalten
    if paddle_a.ycor() < -280:
        paddle_a.goto(-350, -280)
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    if paddle_a.ycor() > 280:
        paddle_a.goto(-350, 280)
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    if paddle_b.ycor() < -280:
        paddle_b.goto(350, -280)
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    if paddle_b.ycor() > 280:
        paddle_b.goto(350, 280)
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    # paddle - ball berührung
    # paddle b rechts
    if (ball.xcor() > 330 and ball.xcor() < 340) and (
            ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50):
        ball.setx(330)
        ball.dx *= -1  # Reverse horizontal direction

        # Calculate the vertical displacement where the ball hits the paddle
        hit_position = ball.ycor() - paddle_b.ycor()  # Difference from the center of paddle b

        # Adjust the ball's vertical direction (dy) based on where it hits the paddle
        ball.dy = hit_position * 0.2  # Scale the effect, 0.15 is the multiplier for control

        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    # paddle a links
    if (ball.xcor() < -330 and ball.xcor() > -340) and (
            ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50):
        ball.setx(-330)
        ball.dx *= -1  # Reverse horizontal direction

        # Calculate the vertical displacement where the ball hits the paddle
        hit_position = ball.ycor() - paddle_a.ycor()  # Difference from the center of paddle a

        # Adjust the ball's vertical direction (dy) based on where it hits the paddle
        ball.dy = hit_position * 0.2  # Scale the effect, 0.15 is the multiplier for control

        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

