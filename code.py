import pygame
import random
import os
from ob import Player, Road, Tree, Pr

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

SCREEN = WIDTH, HEIGHT = 750, 600
win = pygame.display.set_mode(SCREEN)
pygame.display.set_caption("Racing Game")

# Load sounds and music
try:
    engine_sound = pygame.mixer.Sound('data/Assets/sounds/engine.wav')
    crash_sound = pygame.mixer.Sound('data/Assets/sounds/crash.wav')
    game_over_sound = pygame.mixer.Sound('data/Assets/sounds/game_over.wav')
    pygame.mixer.music.load('data/Assets/sounds/background_music.mp3')
    pygame.mixer.music.set_volume(0.5)
    has_audio = True
except:
    print("Audio files missing. Game will run without sound.")
    has_audio = False

# Game settings
clock = pygame.time.Clock()
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT = pygame.font.SysFont('Arial', 30)
LARGE_FONT = pygame.font.SysFont('Arial', 50)

# Load images
home_img = pygame.image.load('data/Assets/home.png')
home_img = pygame.transform.scale(home_img, (WIDTH, HEIGHT))
bg = pygame.image.load('data/Assets/bg.png')
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Game objects
p = Player(WIDTH // 2, HEIGHT - 150, 0)
p.visible = False
road = Road()
base_speed = 6
tree_group = pygame.sprite.Group()
Pr_group = pygame.sprite.Group()

# Game states
home_page = True
game_page = False
game_over = False
score = 0
high_score = 0
lives = 3
move_left = False
move_right = False
has_given_life = False
bonus_text_alpha = 0  # For "+1 LIFE!" fade-out effect

# Load high score
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_RETURN:
                if home_page:
                    home_page = False
                    game_page = True
                    p.visible = True
                    lives = 3
                    score = 0
                    if has_audio:
                        pygame.mixer.music.play(-1)
                        engine_sound.play(-1)
                elif game_over:
                    game_over = False
                    home_page = True
                    if has_audio:
                        pygame.mixer.music.stop()
                        engine_sound.stop()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False

    # Home screen
    if home_page:
        win.blit(home_img, (0, 0))
        start_text = FONT.render("Press ENTER To Start", True, BLACK)
        win.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT - 60))
        hs_text = FONT.render(f"Highest Score: {high_score}", True, BLACK)
        win.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, 50))

    # Game screen
    elif game_page and not game_over:
        # Dynamic speed increase based on score
        current_speed = base_speed + (score * 0.005)
        current_speed = min(current_speed, 10)  # Cap max speed

        win.blit(bg, (0, 0))
        road.update(current_speed)
        road.draw(win)

        score += 0.1
        score_text = FONT.render(f"Score: {int(score)}", True, WHITE)
        
        # Extra life every 500 points
        if int(score) > 0 and int(score) % 500 == 0 and not has_given_life:
            lives += 1
            has_given_life = True
            bonus_text_alpha = 255  # Show "+1 LIFE!" text
        elif int(score) % 500 != 0:
            has_given_life = False

        # Fade-out effect for bonus text
        if bonus_text_alpha > 0:
            bonus_text = FONT.render("+1 LIFE!", True, GREEN)
            bonus_text.set_alpha(bonus_text_alpha)
            win.blit(bonus_text, (WIDTH//2 - bonus_text.get_width()//2, 100))
            bonus_text_alpha -= 3

        lives_text = FONT.render(f"Lives: {lives}", True, WHITE)
        #speed_text = FONT.render(f"Speed: {current_speed:.1f}", True, WHITE)
        win.blit(score_text, (20, 20))
        win.blit(lives_text, (WIDTH - 120, 20))
        #win.blit(speed_text, (20, 60))

        # Spawn obstacles and trees
        if random.random() < 0.02 and (not Pr_group or Pr_group.sprites()[-1].rect.y > 150):
            obs_type = random.choices([1, 2, 3], weights=[6, 2, 2], k=1)[0]
            Pr_group.add(Pr(obs_type))

        if random.random() < 0.01:
            tree = Tree(random.choice([-2, WIDTH - 35]), -20)
            tree_group.add(tree)

        tree_group.update(current_speed)
        tree_group.draw(win)
        Pr_group.update(current_speed)
        Pr_group.draw(win)

        # Collision detection
        for obstacle in Pr_group:
            if pygame.sprite.collide_mask(p, obstacle):
                lives -= 1
                obstacle.kill()
                if has_audio:
                    crash_sound.play()
                if lives <= 0:
                    if score > high_score:
                        high_score = int(score)
                        with open("highscore.txt", "w") as f:
                            f.write(str(high_score))
                    if has_audio:
                        pygame.mixer.music.stop()
                        engine_sound.stop()
                        game_over_sound.play()
                    game_page = False
                    game_over = True
                    p.visible = False
                    Pr_group.empty()
                    tree_group.empty()
                break

    # Game Over screen
    elif game_over:
        win.fill(BLACK)
        game_over_text = LARGE_FONT.render("GAME OVER", True, RED)
        final_score_text = FONT.render(f"Final Score: {int(score)}", True, WHITE)
        hs_text = FONT.render(f"Highest Score: {high_score}", True, WHITE)
        restart_text = FONT.render("Press ENTER to Continue", True, WHITE)

        win.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
        win.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, HEIGHT//2 - 30))
        win.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, HEIGHT//2 + 20))
        win.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 100))

    # Player update
    p.update(move_left, move_right)
    p.draw(win)

    pygame.display.update()
    clock.tick(FPS)

# Clean up
if has_audio:
    pygame.mixer.music.stop()
    pygame.mixer.quit()
pygame.quit() # type: ignore