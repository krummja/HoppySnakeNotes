import random
import time
import turtle


class Frame:
    """Application window and screen surface."""

    def __init__(self):
        self.window = turtle.Screen()
        self.window.tracer(0)
        self.screen = turtle.Turtle()


class Player:
    """Representation of the player's character."""

    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.height = 5.0
        self.sprite = turtle.RawTurtle(canvas)
        self.sprite.penup()
        self.sprite.setheading(90.0)
        self.sprite.goto(x, y)

    def jump(self):
        if self.sprite.ycor() <= 0.0:
            self.height = 6.0

    def run(self, gravity):
        self.height -= gravity
        y = self.sprite.ycor()
        y += self.height
        if y >= 0.0:
            self.sprite.sety(y)
        else:
            self.sprite.sety(0.0)


class Ground:
    """Sprite representing the ground - a straight line."""

    def __init__(self, ground_level, canvas):
        self.sprite = turtle.RawTurtle(canvas)
        self.sprite.hideturtle()
        self.sprite.penup()
        self.sprite.goto(-400, ground_level)
        self.sprite.pendown()
        self.sprite.fd(800)


class Obstacle:
    """A basic sprite representing an obstacle that will kill the player."""

    def __init__(self, x, y, canvas):
        self.sprite = turtle.RawTurtle(canvas)
        self.sprite.penup()
        self.sprite.goto(x, y)
        self.sprite.setheading(180)


class Stage:
    """The visible play area of the game."""

    def __init__(self, game_instance):
        self.game = game_instance
        self.resettable = False
        self.player = None
        self.ground = None
        self.obstacles = []
        self.gravity = 0.2

    def destroy_obstacle(self, i):
        self.obstacles[i].sprite.setx(500)
        self.obstacles.remove(self.obstacles[i])

    def handle_input(self):
        """Register mappings of keyboard inputs to functions."""
        self.game.window.onkeypress(self.game.quit, "Escape")
        self.game.window.onkeypress(self.game.reset, "space")
        self.game.window.onkeypress(self.player.jump, "Up")

    def loop(self):
        self.player.run(self.gravity)

        if len(self.obstacles) < 5:
            self.spawn_obstacle()

        for i in range(len(self.obstacles)):
            x = self.obstacles[i].sprite.xcor()
            self.obstacles[i].sprite.setx(x - 2)
            self.measure_distance(i)
            if x < -400:
                self.destroy_obstacle(i)
                break

    def measure_distance(self, i):
        x = self.player.sprite.xcor()
        y = self.player.sprite.ycor()
        distance = ((x - self.obstacles[i].sprite.xcor()) ** 2) + \
                   ((y - self.obstacles[i].sprite.ycor()) ** 2) ** 0.5

        if distance < 100:
            if (x + 40 > self.obstacles[i].sprite.xcor() - 40) and (
                x - 30 < self.obstacles[i].sprite.ycor() + 30):
                if y - 10 < self.obstacles[i].sprite.ycor() + 10:
                    print("COLLISION!")
                    self.game.game_over()

    def reset(self):
        self.player.sprite.hideturtle()
        self.player = None
        for obstacle in self.obstacles:
            obstacle.sprite.hideturtle()
            self.obstacles = []

    def spawn_obstacle(self):
        since_last = 1.0
        roll = random.randrange(0, 1000)
        if roll + (0.0002 * since_last) > 995:
            new_obstacle = Obstacle(500, 0, self.game.window)
            self.obstacles.append(new_obstacle)
            print("Spawning new obstacle.")
            print(f"Current obstacles: {len(self.obstacles)}")
        else:
            since_last += 0.5

    def start(self):
        self.player = Player(-200, 0, self.game.window)
        self.ground = Ground(-12, self.game.window)


class Game:
    """Main game instance."""

    def __init__(self):
        self.running = False
        self.window = turtle.Screen()
        self.window.tracer(0)
        self.screen = None
        self.stage = None
        self.score = 0

    def game_over(self):
        self.running = False
        self.stage.resettable = True

    def loop(self):
        """Main game loop. Starts event listener and runs core game logic."""
        self.window.listen()
        while self.running:
            self.score += 1
            self.stage.loop()
            self.stage.handle_input()
            self.render()
        turtle.mainloop()

    def render(self):
        """Draw all game entities."""
        self.screen.clear()
        self.screen.write(f"Score: {self.score // 10}", align='center')
        self.window.update()

        if not self.running:
            self.screen.clear()
            self.screen.write(f"Game Over! \n Score: {self.score}", align='center')
            self.screen.sety(162)
            self.screen.write("Press space to try again!", align='center')
            self.screen.sety(175)
            self.window.update()

    def reset(self):
        if self.stage.resettable:
            print("Resetting.")
            self.score = 0
            self.screen.clear()
            self.stage.reset()
            self.stage = None
            self.start()

    def start(self):
        """Set up the game instance and run the main loop."""
        print("Starting.")
        self.screen = turtle.Turtle()
        self.screen.hideturtle()
        self.screen.penup()
        self.screen.sety(175)
        self.stage = Stage(self)
        self.stage.start()
        self.running = True
        self.loop()

    def quit(self):
        print("Exiting...")
        turtle.Screen().bye()


if __name__ == '__main__':
    game = Game()
    game.start()
