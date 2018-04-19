import sys
import pygame

from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    #response press keyboard
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True    
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    #response keyboard release
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
                       
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    #reflect keyboard and mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
            
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    #press play to start game
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #reset game setting
        ai_settings.initialize_dynamic_settings()
        #make mouse point disappear
        pygame.mouse.set_visible(False)
        #reset statistic information of game
        stats.reset_stats()
        stats.game_active = True
        
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        #empty aliens and bullets
        aliens.empty()
        bullets.empty()
    
        #create a new group of aliens and put the ship in the middle of bottom of screen
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    #update screen and switch to a new screen
    #switch to a new screen every time entering a loop
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        
    ship.blitme()
    aliens.draw(screen)
    
    #show score
    sb.show_score()
    
    #if the state of game is inactive, draw play button
    if not stats.game_active:
        play_button.draw_button()
    
    #show lastest screen
    pygame.display.flip()  
    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    #delete disappeared bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #check if any bullets hit aliens
    #if yes,delete related bullet and alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        #delete all current bullets and create a new group of aliens
        bullets.empty()
        ai_settings.increase_speed()
        
        #level up
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)
            
def fire_bullet(ai_settings, screen, ship, bullets):
    #eject a bullet if not reach bullet_allowed
    #create a bullets and add it to group bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
                
def get_number_aliens_x(ai_settings, alien_width):
    #calculate number of alien in one row
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))    
    return number_alien_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    #create an alien and add it on current row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien) 
    
def create_fleet(ai_settings, screen, ship, aliens):
    #create a group of alien
    #create an alien, then calculate number of alien in one row
    #width between two aliens is the width of alien
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #create first row of alien
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
        
def get_number_rows(ai_settings, ship_height, alien_height):
    # calculate how many alien could have on the screen
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    #check if aliens are on edge and update position of all aliens
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)
    
    #check collision between ship and alien
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    
def check_fleet_edges(ai_settings, aliens):
    #measures when alien reach the edges
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    #downward the group of aliens and change the direction
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    #response collision of ship by alien
    #ships_left sub 1
    if stats.ships_left > 0:
        stats.ships_left -= 1
        
        sb.prep_ships()
    
        #empty alien list and bullet list
        aliens.empty()
        bullets.empty()
    
        #create a new group of aliens and put ship in the middle of the bottom screen
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    
        #pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    #check if any aliens reach the bottom of screen
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #handle it like the collision of the ship
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break
        
def check_high_score(stats, sb):
    #check if there is a new highest score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        
        
        


    
    
    
    
    
