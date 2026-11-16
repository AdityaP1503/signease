import sqlite3
import os
import hashlib
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'signease.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Table for Lessons
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        sign_code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        hand_instructions TEXT NOT NULL,
        movement_notes TEXT,
        image_path TEXT NOT NULL,
        is_supported_in_ml INTEGER DEFAULT 1
    )
    ''')

    # Table for Daily Assignments
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assignment_date TEXT UNIQUE NOT NULL,
        total_questions INTEGER DEFAULT 5,
        status TEXT DEFAULT 'pending', -- 'pending' or 'completed'
        score INTEGER DEFAULT 0,
        completed_at TEXT
    )
    ''')

    # Table for Questions in a Daily Assignment
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS assignment_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assignment_id INTEGER NOT NULL,
        question_num INTEGER NOT NULL,
        sign_code TEXT NOT NULL,
        question_text TEXT NOT NULL,
        is_correct INTEGER DEFAULT 0,
        attempts_count INTEGER DEFAULT 0,
        last_predicted_sign TEXT,
        last_confidence REAL DEFAULT 0.0,
        FOREIGN KEY (assignment_id) REFERENCES daily_assignments (id)
    )
    ''')

    # Seed Lessons if empty
    cursor.execute('SELECT COUNT(*) FROM lessons')
    if cursor.fetchone()[0] == 0:
        seed_lessons(cursor)

    conn.commit()
    conn.close()

def seed_lessons(cursor):
    lessons_data = [
        # Basic Words
        (
            'words', 'HELLO', 'Hello / Namaste',
            'A warm, universal greeting in Indian Sign Language.',
            'Open your dominant hand fully with all 5 fingers spread naturally, palm facing forward toward the camera at upper chest or chin level.',
            'Hold the open palm steady or do a gentle natural wave.',
            '/static/images/signs/hello.svg', 1
        ),
        (
            'words', 'YES', 'Yes / Agree',
            'Used to indicate affirmation, agreement, or confirmation.',
            'Form a firm fist and extend your thumb straight upward (classic thumbs-up gesture). Keep your knuckles facing front.',
            'Hold the thumbs-up sign steady facing the camera.',
            '/static/images/signs/yes.svg', 1
        ),
        (
            'words', 'NO', 'No / Disagree',
            'Used to express negation, refusal, or disagreement.',
            'Extend your index finger straight up toward the sky while curling the other three fingers and thumb securely into a fist.',
            'Hold the index finger upright facing the camera.',
            '/static/images/signs/no.svg', 1
        ),
        (
            'words', 'THANK_YOU', 'Thank You',
            'Expresses gratitude, appreciation, and respect.',
            'Keep all 4 fingers held straight and together with thumb tucked alongside the palm (flat handshape), oriented upright facing front.',
            'Hold the flat palm steady facing the camera at chest level.',
            '/static/images/signs/thank_you.svg', 1
        ),
        (
            'words', 'PLEASE', 'Please',
            'Polite request sign used when asking for assistance or permission.',
            'Place the flat open palm resting gracefully at the center of the chest.',
            'Hold flat palm against or near the chest showing polite intent.',
            '/static/images/signs/please.svg', 1
        ),
        (
            'words', 'HELP', 'Help / Support',
            'Essential sign used to request or offer aid and assistance.',
            'Form a fist with thumb upright on your right hand, supported by flat left palm underneath, or hold thumbs-up at chest level.',
            'Hold clear hand shape facing camera.',
            '/static/images/signs/help.svg', 1
        ),
        (
            'words', 'SORRY', 'Sorry / Apology',
            'Used to convey apologies, regret, or sympathy.',
            'Make a loose fist with thumb across fingers and place over the heart/chest.',
            'Hold fist over the chest with a polite facial expression.',
            '/static/images/signs/sorry.svg', 0
        ),

        # Numbers
        (
            'numbers', '1', 'Number 1',
            'Represents numeral 1 in Indian Sign Language counting.',
            'Extend your index finger straight up. Fold your thumb, middle, ring, and pinky fingers tightly against your palm.',
            'Keep your index finger pointed vertically upwards.',
            '/static/images/signs/num1.svg', 1
        ),
        (
            'numbers', '2', 'Number 2',
            'Represents numeral 2 in Indian Sign Language counting.',
            'Extend your index and middle fingers upward in a clear V-shape. Keep your ring finger and pinky folded under your thumb.',
            'Keep the two fingers separated like a victory sign facing the camera.',
            '/static/images/signs/num2.svg', 1
        ),
        (
            'numbers', '3', 'Number 3',
            'Represents numeral 3 in Indian Sign Language counting.',
            'Extend three fingers: index, middle, and ring fingers straight up. Fold your pinky down with your thumb resting over it.',
            'Keep the three fingers upright and visible.',
            '/static/images/signs/num3.svg', 1
        ),
        (
            'numbers', '4', 'Number 4',
            'Represents numeral 4 in Indian Sign Language counting.',
            'Extend all four fingers (index, middle, ring, pinky) straight up. Fold your thumb across your palm.',
            'Keep all four fingers standing upright facing front.',
            '/static/images/signs/num4.svg', 1
        ),
        (
            'numbers', '5', 'Number 5',
            'Represents numeral 5 in Indian Sign Language counting.',
            'Extend all five fingers (thumb and four fingers) fully outward and spread apart with open palm facing front.',
            'Show your open five fingers clearly to the camera.',
            '/static/images/signs/num5.svg', 1
        ),

        # Alphabets
        (
            'alphabets', 'C', 'Letter C',
            'Alphabet sign for letter C in ISL finger spelling.',
            'Curve all four fingers together and arch your thumb backward to form the curved letter "C" shape.',
            'Turn your hand sideways slightly so the camera clearly sees the "C" arc.',
            '/static/images/signs/letter_c.svg', 1
        ),
        (
            'alphabets', 'L', 'Letter L',
            'Alphabet sign for letter L in ISL finger spelling.',
            'Extend your index finger straight up and your thumb outward horizontally at a 90-degree angle, folding the remaining three fingers.',
            'Show the distinct right-angled "L" shape clearly to the camera.',
            '/static/images/signs/letter_l.svg', 1
        ),
        (
            'alphabets', 'O', 'Letter O',
            'Alphabet sign for letter O in ISL finger spelling.',
            'Curve your fingers and touch the tips of all four fingers directly to the tip of your thumb, forming a circle.',
            'Show the circular "O" opening facing the camera.',
            '/static/images/signs/letter_o.svg', 1
        ),
        (
            'alphabets', 'V', 'Letter V',
            'Alphabet sign for letter V in ISL finger spelling.',
            'Extend index and middle fingers in a sharp V shape with knuckles facing front.',
            'Hold the V shape steady facing camera.',
            '/static/images/signs/letter_v.svg', 1
        )
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO lessons 
    (category, sign_code, name, description, hand_instructions, movement_notes, image_path, is_supported_in_ml)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', lessons_data)

def get_lessons(category=None):
    conn = get_db()
    cursor = conn.cursor()
    if category:
        cursor.execute('SELECT * FROM lessons WHERE category = ? ORDER BY id ASC', (category,))
    else:
        cursor.execute('SELECT * FROM lessons ORDER BY category, id ASC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_lesson_by_code(sign_code):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lessons WHERE sign_code = ?', (sign_code,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_supported_ml_signs():
    """Returns list of sign codes that are supported in the ML model."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT sign_code, name, category, image_path FROM lessons WHERE is_supported_in_ml = 1 ORDER BY id ASC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_or_create_daily_assignment(date_str=None):
    """
    Retrieves or generates 5 daily assignment questions rotated deterministically by date.
    """
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM daily_assignments WHERE assignment_date = ?', (date_str,))
    assignment = cursor.fetchone()

    if not assignment:
        # Create assignment for today
        cursor.execute('''
        INSERT INTO daily_assignments (assignment_date, total_questions, status, score)
        VALUES (?, 5, 'pending', 0)
        ''', (date_str,))
        assignment_id = cursor.lastrowid

        # Deterministically select 5 distinct supported signs based on date hash
        supported = [
            'HELLO', 'YES', 'NO', 'THANK_YOU',
            '1', '2', '3', '4', '5',
            'C', 'L', 'O'
        ]

        # Use date string to seed selection
        date_int = int(hashlib.md5(date_str.encode('utf-8')).hexdigest()[:8], 16)
        
        # Pick 5 questions rotating through supported signs
        total = len(supported)
        selected_signs = []
        for i in range(5):
            idx = (date_int + i * 3) % total
            candidate = supported[idx]
            offset = 1
            while candidate in selected_signs:
                candidate = supported[(idx + offset) % total]
                offset += 1
            selected_signs.append(candidate)

        for num, sign_code in enumerate(selected_signs, 1):
            # Fetch lesson details
            cursor.execute('SELECT name FROM lessons WHERE sign_code = ?', (sign_code,))
            l = cursor.fetchone()
            name = l['name'] if l else sign_code
            question_text = f"Show the ISL sign for {name.upper()}"

            cursor.execute('''
            INSERT INTO assignment_questions 
            (assignment_id, question_num, sign_code, question_text, is_correct, attempts_count, last_predicted_sign, last_confidence)
            VALUES (?, ?, ?, ?, 0, 0, '', 0.0)
            ''', (assignment_id, num, sign_code, question_text))

        conn.commit()
        cursor.execute('SELECT * FROM daily_assignments WHERE id = ?', (assignment_id,))
        assignment = cursor.fetchone()

    # Fetch questions
    cursor.execute('''
    SELECT q.*, l.name as sign_name, l.description, l.hand_instructions, l.image_path
    FROM assignment_questions q
    JOIN lessons l ON q.sign_code = l.sign_code
    WHERE q.assignment_id = ?
    ORDER BY q.question_num ASC
    ''', (assignment['id'],))
    questions = cursor.fetchall()

    conn.close()
    return dict(assignment), [dict(q) for q in questions]

def update_question_result(assignment_id, question_num, predicted_sign, confidence, is_correct):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE assignment_questions
    SET attempts_count = attempts_count + 1,
        last_predicted_sign = ?,
        last_confidence = ?,
        is_correct = CASE WHEN is_correct = 1 THEN 1 ELSE ? END
    WHERE assignment_id = ? AND question_num = ?
    ''', (predicted_sign, confidence, 1 if is_correct else 0, assignment_id, question_num))

    # Recalculate score for assignment
    cursor.execute('''
    SELECT COUNT(*) as total, SUM(is_correct) as correct
    FROM assignment_questions
    WHERE assignment_id = ?
    ''', (assignment_id,))
    res = cursor.fetchone()
    total = res['total'] or 5
    correct = res['correct'] or 0

    score = int((correct / total) * 100)
    all_attempted = False
    cursor.execute('''
    SELECT COUNT(*) FROM assignment_questions 
    WHERE assignment_id = ? AND attempts_count > 0
    ''', (assignment_id,))
    attempted_count = cursor.fetchone()[0]
    if attempted_count >= total:
        all_attempted = True

    status = 'completed' if all_attempted else 'pending'
    completed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if all_attempted else None

    cursor.execute('''
    UPDATE daily_assignments
    SET score = ?,
        status = ?,
        completed_at = COALESCE(completed_at, ?)
    WHERE id = ?
    ''', (score, status, completed_at, assignment_id))

    conn.commit()
    conn.close()
    return {'score': score, 'status': status, 'correct_count': correct, 'total': total}

def get_progress_summary():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM daily_assignments WHERE status = "completed"')
    total_assignments_completed = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(attempts_count) FROM assignment_questions')
    val = cursor.fetchone()[0]
    total_questions_attempted = val if val is not None else 0

    cursor.execute('SELECT COUNT(*) FROM assignment_questions WHERE is_correct = 1')
    correct_answers = cursor.fetchone()[0]

    incorrect_answers = max(0, total_questions_attempted - correct_answers)

    if total_questions_attempted > 0:
        accuracy = round((correct_answers / total_questions_attempted) * 100, 1)
    else:
        accuracy = 0.0

    cursor.execute('''
    SELECT id, assignment_date, score, status, completed_at,
           (SELECT COUNT(*) FROM assignment_questions WHERE assignment_id = daily_assignments.id AND is_correct = 1) as correct_count,
           total_questions
    FROM daily_assignments
    ORDER BY assignment_date DESC
    ''')
    history = cursor.fetchall()

    conn.close()
    return {
        'total_assignments_completed': total_assignments_completed,
        'total_questions_attempted': total_questions_attempted,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'accuracy': accuracy,
        'history': [dict(h) for h in history]
    }
