import show_statistic
import random
import additional
from alien import game_making
from bullet import ShellObject

settings = additional.check_settings()


def check_event(pygame, event, stat, freaze_game, pause_flag, death_flag, character,
                start_button, shell_objects, all_sprites, shell_object_img, CURRENT_SCORE,
                last_shell):
    return_dict = {}
    if event.type == pygame.QUIT:
        return_dict['running'] = False
        if settings.saving_after_quit: stat.rewrite_file()
        else: print('Your flag save statistic is turned off, your progress was not saved')

    if freaze_game:
        if pause_flag:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return_dict['current_score'] = stat.plus_temp()
                    return_dict['pause_flag'] = False
                    return_dict['freaze_game'] = False
                    additional.write_log_file('Game resumed with a score of {}'.format(CURRENT_SCORE))

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    if stat.max_score != 0 and stat.max_level != 0:
                        ss = show_statistic.ShowStat(stat)
                        flag = ss.show(stat)
                        if flag: game_making(random.randint(1, 3))
                        else: additional.write_log_file('The game was closed after viewing statistics')
                    else: return_dict['show_have_not_stat'] = True
                elif event.key == pygame.K_SPACE:
                    start_game_time = pygame.time.get_ticks()
                    character.lives = 1
                    if settings.sounds: pygame.mixer.music.unpause()
                    character.rect.center = settings.character_position
                    return_dict['freaze_game'] = False
                    return_dict['character'] = character
                    return_dict['start_game_time'] = start_game_time
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.pressed(pygame.mouse.get_pos()):
                    start_game_time = pygame.time.get_ticks()
                    return_dict['start_game_time'] = start_game_time
                    character.lives = 1
                    if settings.sounds: pygame.mixer.music.unpause()
                    character.rect.center = settings.character_position
                    return_dict['freaze_game'] = False
                    return_dict['character'] = character

    else:
        if death_flag:
            0
        else:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                now = pygame.time.get_ticks()
                count_of_shells = additional.read_temp_file(settings.files.temp_count_of_shells)[0]
                if count_of_shells < settings.max_count_of_shells and (now - last_shell) // 100 > 1:
                    last_shell = pygame.time.get_ticks()
                    count_of_shells += 1
                    additional.write_temp_file(settings.files.temp_count_of_shells, count_of_shells)
                    shell_object = ShellObject(shell_object_img, character)
                    shell_objects.add(shell_object)
                    all_sprites.add(shell_objects)
                    return_dict['shell_objects'] = shell_objects
                    return_dict['all_sprites'] = all_sprites
                    return_dict['last_shell'] = last_shell
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    character.go_left()
                    return_dict['character'] = character
                elif event.key == pygame.K_RIGHT:
                    character.go_right()
                    return_dict['character'] = character

                elif event.key == pygame.K_ESCAPE:
                    additional.write_log_file('The game is paused (Score: {})'.format(CURRENT_SCORE))
                    stat.add_temp_score(CURRENT_SCORE)
                    return_dict['pause_flag'] = True
                    return_dict['freaze_game'] = True
                    return_dict['stat'] = stat

                elif event.key == pygame.K_DELETE:
                    print('DEL save data')
                    additional.write_log_file('The game was closed (DEL) with score {}'.format(CURRENT_SCORE))
                    stat.add_max_score(CURRENT_SCORE)
                    stat.add_level(character.level)
                    # ~ running = False
                    return_dict['running'] = False
                    return_dict['stat'] = stat
                    stat.rewrite_file()

                '''
                # For testing death
                if event.key == pygame.K_KP_ENTER:
                    character.lives = 0
                    return_dict['character'] = character
                '''

    return return_dict
