import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 694, 360
PLAYGROUND_TOP, PLAYGROUND_BOTTOM = 60, HEIGHT - 60  # Adjust these values as needed
BALL_RADIUS = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60  # Adjust paddle size
WHITE = (255, 255, 255)
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Add this before the main game loop
background_image = pygame.image.load("images/background.jpg")  # Replace "background.jpg" with your image file
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Resize image
background_rect = background_image.get_rect()

# Initialize clock
clock = pygame.time.Clock()

# Initialize paddles and ball
player_paddle = pygame.Rect(
    120, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT
)
opponent_paddle = pygame.Rect(
    WIDTH - 50 - PADDLE_WIDTH,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
)
ball = pygame.Rect(
    WIDTH // 2 - BALL_RADIUS // 2,
    HEIGHT // 2 - BALL_RADIUS // 2,
    BALL_RADIUS,
    BALL_RADIUS,
)

# Initial ball speed
ball_speed = [5, 5]

# Game state
menu_loop = True
game_running = False
game_over = False
selected_option = 0

# Score variables
score = 0
high_score = 0

# Create the menu options
menu_options = ["Start Game", "Quit"]

# Render the menu options and high score
font = pygame.font.Font(None, 36)
menu_options_rendered = [
    font.render(option, True, (255, 255, 255)) for option in menu_options
]

# Speed multiplier
speed_multiplier = 1.0
speed_increment = 0.001  # Adjust this value based on the desired speed increase rate

# Paddle speed for player (adjust this value)
player_paddle_speed = 15

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # If in menu loop
    if menu_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            selected_option = (selected_option - 1) % len(menu_options)
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            selected_option = (selected_option + 1) % len(menu_options)
        elif keys[pygame.K_RETURN]:
            if menu_options[selected_option] == "Start Game":
                menu_loop = False
                game_running = True
                game_over = False
                selected_option = 0  # Reset selected option

                # Set the initial position of the ball when restarting
                ball.x = WIDTH // 2 - BALL_RADIUS // 2
                ball.y = HEIGHT // 2 - BALL_RADIUS // 2

                score = 0  # Reset the score
            elif menu_options[selected_option] == "Quit":
                pygame.quit()
                sys.exit()

        # Draw the menu options and highlight the selected option
        screen.blit(background_image, background_rect)  # Blit background image
        for i, option in enumerate(menu_options_rendered):
            color = (255, 255, 255) if i == selected_option else (128, 128, 128)
            text_rect = option.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
            screen.blit(option, text_rect)

        # Display high score on the menu screen
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(high_score_text, high_score_rect)

    # If in game loop
    elif game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Process other events here

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_paddle.top > PLAYGROUND_TOP:
            player_paddle.y -= player_paddle_speed
        if keys[pygame.K_DOWN] and player_paddle.bottom < PLAYGROUND_BOTTOM:
            player_paddle.y += player_paddle_speed

        # Update ball position
        ball.x += int(ball_speed[0] * speed_multiplier)
        ball.y += int(ball_speed[1] * speed_multiplier)

        # Ball collision with walls
        if ball.top <= PLAYGROUND_TOP:
            ball.y = PLAYGROUND_TOP + 1  # Move the ball down slightly to stay within the top boundary
            ball_speed[1] = -ball_speed[1]
        elif ball.bottom >= PLAYGROUND_BOTTOM:
            ball.y = PLAYGROUND_BOTTOM - BALL_RADIUS - 1  # Move the ball up slightly to stay within the bottom boundary
            ball_speed[1] = -ball_speed[1]

        # Ball collision with paddles
        if ball.colliderect(player_paddle):
            ball_speed[0] = -ball_speed[0]

            # Increase the score on successful ball hits
            score += 1

        if ball.colliderect(opponent_paddle):
            ball_speed[0] = -ball_speed[0]

        # Opponent AI
        if opponent_paddle.centery < ball.centery:
            opponent_paddle.y += min(5 + int(speed_multiplier * 2), PLAYGROUND_BOTTOM - opponent_paddle.bottom)
        elif opponent_paddle.centery > ball.centery:
            opponent_paddle.y -= min(5 + int(speed_multiplier * 2), opponent_paddle.top - PLAYGROUND_TOP)

        # Check if opponent misses the ball
        if ball.right > WIDTH:
            score += 1
            ball.x = WIDTH // 2 - BALL_RADIUS // 2
            ball.y = HEIGHT // 2 - BALL_RADIUS // 2

        # Check if player missed the ball
        if ball.left < 0:
            game_running = False
            game_over = True

        # Draw everything
        screen.blit(background_image, background_rect)  # Blit background image
        pygame.draw.rect(screen, WHITE, player_paddle)
        pygame.draw.rect(screen, WHITE, opponent_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)

        # Draw the center line
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, PLAYGROUND_TOP), (WIDTH // 2, PLAYGROUND_BOTTOM))

        # Display the player's score in the top-left corner
        score_text = font.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(topleft=(10, 10))
        screen.blit(score_text, score_rect)

        # Increase speed multiplier
        speed_multiplier += speed_increment

    # If in game over state
    elif game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Process other events here

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            game_running = True
            selected_option = 0  # Reset selected option

            # Set the initial position of the ball when restarting
            ball.x = WIDTH // 2 - BALL_RADIUS // 2
            ball.y = HEIGHT // 2 - BALL_RADIUS // 2

            score = 0  # Reset the score
            speed_multiplier = 1.0  # Reset speed multiplier
        elif keys[pygame.K_q]:
            game_over = False
            menu_loop = True
            game_running = False
            selected_option = 0  # Reset selected option

            # Update the high score
            if score > high_score:
                high_score = score

        # Draw game over text and options
        screen.blit(background_image, background_rect)  # Blit background image
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(text, text_rect)

        restart_text = font.render("Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(restart_text, restart_rect)

        menu_text = font.render("Main Menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(menu_text, menu_rect)

        # Display the final score on the game over screen
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 100)
        )
        screen.blit(final_score_text, final_score_rect)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

    # Update display for the menu loop
    pygame.display.update()
