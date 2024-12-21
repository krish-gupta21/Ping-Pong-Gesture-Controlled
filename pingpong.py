import pygame
import cv2
import mediapipe as mp
import sys

# Initialize MediaPipe Hands for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Initialize OpenCV for webcam
cap = cv2.VideoCapture(0)

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gesture-Controlled Ping Pong")

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 10

# Ball speed
ball_speed_x = 15
ball_speed_y = 15

# Initialize paddles and ball
left_paddle = pygame.Rect(30, (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(SCREEN_WIDTH - 50, (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Game clock
clock = pygame.time.Clock()

# Score tracking
score = 0

def reset_ball():
    """Reset the ball to the center and reverse its direction."""
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    global ball_speed_x, ball_speed_y
    ball_speed_x *= -1

def game_over_popup():
    """Display the Game Over screen with a restart button."""
    global score
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame for a mirror effect
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame)
        screen.blit(pygame.transform.rotate(frame_surface, -90), (0, 0))

        game_over_text = pygame.font.Font(None, 74).render("Game Over!", True, (255, 255, 255))
        restart_text = pygame.font.Font(None, 50).render("Click to Restart", True, (0, 0, 255))
        final_score_text = pygame.font.Font(None, 50).render(f"Final Score: {score}", True, (0, 255, 0))

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                score = 0  # Reset score
                return  # Restart the game

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame for mirror effect and convert to RGB
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with MediaPipe
    results = hands.process(rgb_frame)

    # Initialize variables to track hand positions
    left_hand_y = None
    right_hand_y = None

    # Get hand landmarks
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Determine hand side (Left/Right)
            hand_label = handedness.classification[0].label  # 'Left' or 'Right'

            # Get y-coordinate of the index finger tip (landmark 8)
            index_tip_y = int(hand_landmarks.landmark[8].y * SCREEN_HEIGHT)

            # Assign y-coordinate to the correct paddle
            if hand_label == "Left":
                left_hand_y = index_tip_y
            elif hand_label == "Right":
                right_hand_y = index_tip_y

    # Update paddle positions if hands are detected
    if left_hand_y is not None:
        left_paddle.y = left_hand_y - PADDLE_HEIGHT // 2
    if right_hand_y is not None:
        right_paddle.y = right_hand_y - PADDLE_HEIGHT // 2

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1
        score += 1  # Increment score when ball hits a paddle

    # Ball goes out of bounds
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        game_over_popup()
        left_paddle.y = (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2)
        right_paddle.y = (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2)
        reset_ball()

    # Ensure paddles stay on screen
    left_paddle.y = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, left_paddle.y))
    right_paddle.y = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, right_paddle.y))

    # Convert frame to Pygame surface and display it as the background
    frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(frame)
    screen.blit(pygame.transform.rotate(frame_surface, -90), (0, 0))

    # Draw paddles and ball
    pygame.draw.rect(screen, (0, 255, 0), left_paddle)
    pygame.draw.rect(screen, (255, 0, 0), right_paddle)
    pygame.draw.ellipse(screen, (255, 255, 255), ball)

    # Draw the score
    score_text = pygame.font.Font(None, 50).render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.flip()

    # Limit FPS
    clock.tick(60)

# Release resources
cap.release()
pygame.quit()
cv2.destroyAllWindows()
