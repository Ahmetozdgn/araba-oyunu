import pygame
import random
import sys

# Pygame başlatma
pygame.init()

# Ses ayarları
pygame.mixer.init()
background_music = pygame.mixer.Sound(r"oyun.wav")
crash_sound = pygame.mixer.Sound(r"çarptı.wav")
game_over_sound = pygame.mixer.Sound(r"bitti.wav")

# Müziği başlat
pygame.mixer.Sound.play(background_music, loops=-1)

# Ekran boyutları
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Yarış Oyunu")  # Doğru işlev adı

# Renkler
white = (255, 255, 255)

# Araba karakterin başlangıç özellikleri
car_width, car_height = 60, 90
car_x = width // 2 - car_width // 2
car_y = height - car_height - 10

# Arka plan resmi yükleme
background_image = pygame.image.load(r"engel.png")
background_image = pygame.transform.scale(background_image, (width, height))

# Oyun bittiğinde gösterilecek arka plan
game_over_background = pygame.image.load(r"bitti.png")
game_over_background = pygame.transform.scale(game_over_background, (width, height))

# Araba resmini yükle
car_image = pygame.image.load(r"auto.png")
car_image = pygame.transform.scale(car_image, (car_width, car_height))

# Boom efekti resmi
boom_image = pygame.image.load(r"yangın.png")
boom_image = pygame.transform.scale(boom_image, (car_width * 2, car_height * 2))

# Engel arabaları yükle
enemy_car_images = [
    pygame.image.load(r"kırmızı.png"),
    pygame.image.load(r"sarı.png"),
    pygame.image.load(r"sports-car.png"),
    pygame.image.load(r"turuncu.png")
]

# Engel arabalarını boyutlandır
enemy_car_images = [pygame.transform.scale(img, (car_width, car_height)) for img in enemy_car_images]

# Engel ayarları
obstacle_speed = 5
obstacles = []
last_obstacle_time = 0
obstacle_delay = 1000  # 1000 ms yani 1 saniyede bir yeni engel gelsin

# Engel oluşturma fonksiyonu
def create_obstacle():
    obstacle_width = car_width
    x_position = random.randint(0, width - obstacle_width)
    x_speed = random.choice([-3, 3])  # Engelin sağa veya sola hareket etmesi için rastgele bir hız
    return (x_position, -car_height, random.choice(enemy_car_images), x_speed)

# Puan Sistemi
score = 0
font = pygame.font.Font(None, 36)

# FPS ayarları
clock = pygame.time.Clock()

# Arka plan hareket değişkenleri
bg_speed = 5  # Arka planın hareket hızı
bg_y1 = 0  # Arka planın Y koordinatı
bg_y2 = -height  # İkinci arka plan hemen üstten başlasın

# Oyun döngüsü
running = True
crash_effect = False
boom_effect_start_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # Klavye ile araba hareketi
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= 5
    if keys[pygame.K_RIGHT] and car_x < width - car_width:
        car_x += 5

    # Zamanlayıcı kontrolü ile engel oluşturma
    if pygame.time.get_ticks() - last_obstacle_time > obstacle_delay:
        obstacles.append(create_obstacle())
        last_obstacle_time = pygame.time.get_ticks()

    # Engel hareketi
    for i in range(len(obstacles)):
        obstacle_x, obstacle_y, enemy_car_image, x_speed = obstacles[i]
        obstacle_y += obstacle_speed
        obstacle_x += x_speed  # Engelin x ekseninde sağa sola kayması
        
        # Eğer engel ekranın dışına çıkarsa yönünü değiştir
        if obstacle_x < 0 or obstacle_x > width - car_width:
            x_speed *= -1
        
        obstacles[i] = (obstacle_x, obstacle_y, enemy_car_image, x_speed)

        if obstacle_y > height:
            obstacles.pop(i)
            score += 1
            break

    if score % 10 == 0 and score != 0:
        obstacle_speed += 0.5

    # Arka plan hareketi
    bg_y1 += bg_speed
    bg_y2 += bg_speed

    # Arka plan döngüsü
    if bg_y1 >= height:
        bg_y1 = -height
    if bg_y2 >= height:
        bg_y2 = -height

    # Arka planı ekrana çiz
    screen.blit(background_image, (0, bg_y1))
    screen.blit(background_image, (0, bg_y2))

    # Puanı ekrana yaz
    score_text = font.render(f"Puan: {score}", True, white)
    screen.blit(score_text, (10, 10))

    # Engelleri çiz
    for obstacle_x, obstacle_y, enemy_car_image, _ in obstacles:
        screen.blit(enemy_car_image, (obstacle_x, obstacle_y))

    # Araba karakterini ekrana çiz
    screen.blit(car_image, (car_x, car_y))

    # Çarpışma kontrolü
    for obstacle_x, obstacle_y, enemy_car_image, _ in obstacles:  # enemy_car_image'i ekleyerek dördüncü öğeyi alıyoruz
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, car_width, car_height)
        if obstacle_rect.colliderect(pygame.Rect(car_x, car_y, car_width, car_height)):
            pygame.mixer.Sound.play(crash_sound)
            pygame.mixer.Sound.stop(background_music)
            boom_effect_start_time = pygame.time.get_ticks()

            screen.blit(boom_image, (car_x - car_width // 2, car_y - car_height // 2))
            pygame.display.flip()
            pygame.time.wait(5000)

            screen.blit(game_over_background, (0, 0))
            # Oyun bittiğinde puan ve mesajın renklendirilmesi
            game_over_text = font.render("Game Over! Puan: " + str(score), True, (255, 0, 0))  # Kırmızı renkte
            screen.blit(game_over_text, (width // 2 - 100, height // 2 - 20))

            pygame.display.flip()

            pygame.mixer.Sound.play(game_over_sound)
            pygame.time.wait(5000)

            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(100)
