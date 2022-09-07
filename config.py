import os

basedir = os.path.abspath(os.path.dirname(__file__))

config = {
    # DataBase
    'DB': {'DATABASE': os.path.join(basedir, 'database', 'game.db')},
    # Images
    'IMG': {'RED_BOARD': os.path.join(basedir, 'statics', 'board', 'red_board.png'),
            'GREEN_BOARD': os.path.join(basedir, 'statics', 'board', 'green_board.png'),
            'LEADER_BOARD': os.path.join(basedir, 'statics', 'board', 'leader_board.png'),
            'GREEN_BTN': os.path.join(basedir, 'statics', 'buttons', 'gree_button.png'),
            'RED_BTN': os.path.join(basedir, 'statics', 'buttons', 'red_button.png'),
            'GREEN_HALO': os.path.join(basedir, 'statics', 'board', 'green_halo.png'),
            'RED_HALO': os.path.join(basedir, 'statics', 'board', 'red_halo.png'),
            'RED_SLASH': os.path.join(basedir, 'statics', 'slash', 'slash1.png'),
            'BLUE_SLASH': os.path.join(basedir, 'statics', 'slash', 'slash2.png'),
            'BROKEN1': os.path.join(basedir, 'statics', 'board', 'broken1.png'),
            'BROKEN2': os.path.join(basedir, 'statics', 'board', 'broken2.png'),
            'RED_ARROW': os.path.join(basedir, 'statics', 'board', 'red_arrow.png'),
            'GREEN_ARROW': os.path.join(basedir, 'statics', 'board', 'green_arrow.png'),
            'DICE1': os.path.join(basedir, 'statics', 'dice', '1.png'),
            'DICE2': os.path.join(basedir, 'statics', 'dice', '2.png'),
            'DICE3': os.path.join(basedir, 'statics', 'dice', '3.png'),
            'DICE4': os.path.join(basedir, 'statics', 'dice', '4.png'),
            'DICE5': os.path.join(basedir, 'statics', 'dice', '5.png'),
            'DICE6': os.path.join(basedir, 'statics', 'dice', '6.png'),
            'BITCOIN': os.path.join(basedir, 'statics', 'bitcoin.png'),
            'TROPHY': os.path.join(basedir, 'statics', 'trophy.png'),
            'LOGO': os.path.join(basedir, 'statics', 'logo.png'),
            'DESTROY_SYSTEM': os.path.join(basedir, 'statics', 'how_to_play', 'destroy_dices.png'),
            'POINTS_SYSTEM': os.path.join(basedir, 'statics', 'how_to_play', 'points_system.png'),
            },
    # Music
    'MUSIC': {'SLASH': os.path.join(basedir, 'statics', 'sound', 'slash1_sound.mp3')},
    # Sounds
    'SOUND': {'SLASH': os.path.join(basedir, 'statics', 'sound', 'slash1_sound.mp3'),
              'RANDOM_ROLLING': os.path.join(basedir, 'statics', 'sound', 'dice_random_rolling_effect.mp3'),
              'THROW_DICE': os.path.join(basedir, 'statics', 'sound', 'dice_roll.mp3'),
              'PIANO_BTN': os.path.join(basedir, 'statics', 'sound', 'piano_key.WAV'),
              },
    'FONT': {'MAGIC': os.path.join(basedir, 'statics', 'font', 'Magical Story.ttf'),
             'BEBAS': os.path.join(basedir, 'statics', 'font', 'BebasNeue-Regular.ttf'),
             }
}
