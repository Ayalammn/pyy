import pygame
import math

# ------------------- Initialize Pygame -------------------
pygame.init()

# ------------------- Constants --------------------------
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ------------------- Screen Setup -----------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Application")
screen.fill(WHITE)

# ------------------- State Variables --------------------
painting = False
last_pos = None
color = BLACK
mode = "pen"  # pen, rect, circle, eraser, square, rtriangle, etriangle, rhombus
start_pos = None
eraser_size = 10  # Initial eraser size

# ------------------- Game Loop -------------------------
running = True
while running:
    for event in pygame.event.get():
        # ---------- Quit ----------
        if event.type == pygame.QUIT:
            running = False
        
        # ---------- Mouse Down ----------
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                painting = True
                last_pos = event.pos
                start_pos = event.pos  # Start position for shapes
            
        # ---------- Mouse Up ----------
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                painting = False
                end_pos = event.pos
                width = end_pos[0] - start_pos[0]
                height = end_pos[1] - start_pos[1]
                
                # Draw rectangle
                if mode == "rect":
                    pygame.draw.rect(screen, color, pygame.Rect(start_pos, (width, height)), 2)
                
                # Draw circle
                elif mode == "circle":
                    radius = int(((width)**2 + (height)**2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, radius, 2)
                
                # Draw square
                elif mode == "square":
                    side = max(abs(width), abs(height))  # Make it a square
                    rect = pygame.Rect(start_pos, (side, side))
                    # Adjust for negative width/height
                    if width < 0: rect.x -= side
                    if height < 0: rect.y -= side
                    pygame.draw.rect(screen, color, rect, 2)
                
                # Draw right triangle
                elif mode == "rtriangle":
                    # Right triangle with right angle at start_pos
                    points = [start_pos, (start_pos[0] + width, start_pos[1]), (start_pos[0], start_pos[1] + height)]
                    pygame.draw.polygon(screen, color, points, 2)
                
                # Draw equilateral triangle
                elif mode == "etriangle":
                    side = max(abs(width), abs(height))
                    # Three points of equilateral triangle
                    p1 = start_pos
                    p2 = (start_pos[0] + side, start_pos[1])
                    p3 = (start_pos[0] + side//2, int(start_pos[1] - side * math.sin(math.radians(60))))
                    pygame.draw.polygon(screen, color, [p1, p2, p3], 2)
                
                # Draw rhombus
                elif mode == "rhombus":
                    side_x = width // 2
                    side_y = height // 2
                    cx, cy = start_pos
                    points = [
                        (cx, cy - side_y),  # Top
                        (cx + side_x, cy),  # Right
                        (cx, cy + side_y),  # Bottom
                        (cx - side_x, cy)   # Left
                    ]
                    pygame.draw.polygon(screen, color, points, 2)
        
        # ---------- Mouse Motion (for pen/eraser) ----------
        elif event.type == pygame.MOUSEMOTION:
            if painting:
                if mode == "pen":
                    pygame.draw.line(screen, color, last_pos, event.pos, 3)
                    last_pos = event.pos
                elif mode == "eraser":
                    pygame.draw.line(screen, WHITE, last_pos, event.pos, eraser_size)
                    last_pos = event.pos
        
        # ---------- Keyboard Controls ----------
        elif event.type == pygame.KEYDOWN:
            # Switch drawing modes
            if event.key == pygame.K_r:
                mode = "rect"
            elif event.key == pygame.K_c:
                mode = "circle"
            elif event.key == pygame.K_p:
                mode = "pen"
            elif event.key == pygame.K_e:
                mode = "eraser"
            elif event.key == pygame.K_s:
                mode = "square"
            elif event.key == pygame.K_t:
                mode = "rtriangle"
            elif event.key == pygame.K_y:
                mode = "etriangle"
            elif event.key == pygame.K_h:
                mode = "rhombus"
            
            # Change color
            elif event.key == pygame.K_1:
                color = (255, 0, 0)  # Red
            elif event.key == pygame.K_2:
                color = (0, 255, 0)  # Green
            elif event.key == pygame.K_3:
                color = (0, 0, 255)  # Blue
            elif event.key == pygame.K_4:
                color = BLACK  # Black
            
            # Eraser size
            elif event.key == pygame.K_LEFTBRACKET:  # [
                eraser_size = max(5, eraser_size - 5)
            elif event.key == pygame.K_RIGHTBRACKET:  # ]
                eraser_size += 5
    
    # Update display
    pygame.display.flip()

pygame.quit()
