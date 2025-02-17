DIFFICULTY_BEGINNER = 'beginner'
DIFFICULTY_INTERMEDIATE = 'intermediate'
DIFFICULTY_EXPERT = 'expert'

difficulty_mapping = {
    DIFFICULTY_BEGINNER: {
        "name": "beginner",
        "width": 9,
        "height": 9,
        "cell_width": "24px",
        "mine_count": 10
    },
    DIFFICULTY_INTERMEDIATE: {
        "name": "intermediate",
        "width": 16,
        "height": 16,
        "cell_width": "24px",
        "mine_count": 40
    },
    DIFFICULTY_EXPERT: {
        "name": "expert",
        "width": 30,
        "height": 16,
        "cell_width": "24px",
        "mine_count": 99
    }
}

MAX_HIGHSCORE_COUNT_PER_DIFFICULTY = 300  # 900 total, because there are 3 difficulties
