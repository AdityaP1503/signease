"""
Generates clean, modern, high-contrast SVG reference illustrations
for Indian Sign Language (ISL) signs.
"""
import os

SIGNS_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images', 'signs')
os.makedirs(SIGNS_DIR, exist_ok=True)

SVG_TEMPLATES = {
    'hello': {
        'title': 'HELLO / GREETING',
        'sub': 'Open Palm (5 Fingers Spread)',
        'art': '''
            <!-- Palm -->
            <path d="M100 150 C100 180, 110 200, 150 200 C190 200, 200 180, 200 150 L195 120 L105 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Wrist -->
            <path d="M120 195 L120 250 L180 250 L180 195 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <!-- Thumb -->
            <path d="M103 145 C80 140, 60 120, 65 105 C70 95, 85 100, 105 125 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4" stroke-linejoin="round"/>
            <!-- Index Finger -->
            <path d="M106 122 L104 55 C104 42, 122 42, 122 55 L124 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Middle Finger -->
            <path d="M127 120 L127 40 C127 28, 147 28, 147 40 L147 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Ring Finger -->
            <path d="M150 120 L152 48 C152 36, 172 36, 172 48 L170 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Pinky Finger -->
            <path d="M174 122 L180 70 C180 58, 198 58, 198 70 L194 125 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Wave Accents -->
            <path d="M50 75 C40 85, 40 105, 50 115" stroke="#4F46E5" stroke-width="4" stroke-linecap="round" fill="none"/>
            <path d="M215 75 C225 85, 225 105, 215 115" stroke="#4F46E5" stroke-width="4" stroke-linecap="round" fill="none"/>
        '''
    },
    'yes': {
        'title': 'YES / AGREE',
        'sub': 'Thumbs Up (Fist Closed, Thumb Up)',
        'art': '''
            <!-- Fist Base / Palm -->
            <rect x="95" y="110" width="105" height="85" rx="20" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Wrist -->
            <path d="M110 190 L110 250 L170 250 L170 190 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <!-- Thumb Extended Up -->
            <path d="M100 130 C90 100, 85 50, 105 40 C120 40, 125 70, 125 115 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4" stroke-linejoin="round"/>
            <!-- Curled Finger Knuckles -->
            <path d="M125 125 C145 120, 175 120, 195 130" stroke="#4A3B32" stroke-width="4" fill="none"/>
            <path d="M125 145 C145 140, 175 140, 195 150" stroke="#4A3B32" stroke-width="4" fill="none"/>
            <path d="M125 165 C145 160, 175 160, 195 170" stroke="#4A3B32" stroke-width="4" fill="none"/>
            <!-- Thumbs up shine -->
            <path d="M105 25 L105 15 M80 30 L72 24 M130 30 L138 24" stroke="#10B981" stroke-width="4" stroke-linecap="round"/>
        '''
    },
    'no': {
        'title': 'NO / NUMBER 1',
        'sub': 'Index Finger Extended Upward',
        'art': '''
            <!-- Fist -->
            <rect x="100" y="115" width="100" height="80" rx="18" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Wrist -->
            <path d="M115 190 L115 250 L175 250 L175 190 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <!-- Curled Thumb across knuckles -->
            <path d="M100 150 C100 130, 140 135, 160 145 C150 160, 120 160, 100 150 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <!-- Index Finger Straight Up -->
            <path d="M106 120 L106 40 C106 26, 128 26, 128 40 L128 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Knuckle grooves -->
            <path d="M132 140 L190 140" stroke="#4A3B32" stroke-width="3"/>
            <path d="M132 165 L190 165" stroke="#4A3B32" stroke-width="3"/>
        '''
    },
    'thank_you': {
        'title': 'THANK YOU',
        'sub': 'Flat Hand, Fingers Together',
        'art': '''
            <!-- Flat Palm -->
            <path d="M100 140 C100 180, 110 200, 150 200 C190 200, 195 180, 195 140 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Wrist -->
            <path d="M115 195 L115 250 L175 250 L175 195 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <!-- 4 Fingers together upright -->
            <path d="M105 140 L105 45 C105 32, 190 32, 190 45 L190 140 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Vertical finger separator lines -->
            <path d="M126 35 L126 140 M147 33 L147 140 M168 35 L168 140" stroke="#4A3B32" stroke-width="3"/>
            <!-- Thumb resting along side -->
            <path d="M105 140 C95 130, 90 115, 95 105 C102 98, 108 110, 105 130 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="3"/>
            <!-- Direction arrow forward/chin -->
            <path d="M210 110 L235 110 M230 100 L240 110 L230 120" stroke="#8B5CF6" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
        '''
    },
    'please': {
        'title': 'PLEASE',
        'sub': 'Flat Hand Over Chest / Heart',
        'art': '''
            <!-- Chest silhouette -->
            <path d="M60 250 C70 170, 230 170, 240 250 Z" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="3"/>
            <!-- Flat open hand -->
            <ellipse cx="150" cy="140" rx="45" ry="35" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Fingers -->
            <path d="M120 120 L115 65 C115 55, 175 55, 175 65 L170 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <path d="M133 60 L133 115 M147 58 L147 115 M160 60 L160 115" stroke="#4A3B32" stroke-width="3"/>
            <!-- Circular gesture indicator -->
            <path d="M150 95 A 60 60 0 1 1 140 96" fill="none" stroke="#6366F1" stroke-width="4" stroke-dasharray="6,4"/>
            <polygon points="140,88 140,104 128,96" fill="#6366F1"/>
        '''
    },
    'help': {
        'title': 'HELP',
        'sub': 'Thumbs-Up Fist on Flat Base Hand',
        'art': '''
            <!-- Lower Supporting Hand (Flat palm facing up) -->
            <rect x="70" y="195" width="160" height="25" rx="10" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <path d="M50 207 L70 207" stroke="#4A3B32" stroke-width="4"/>
            <!-- Upper Fist -->
            <rect x="110" y="125" width="80" height="65" rx="15" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Thumb pointing up -->
            <path d="M115 135 C108 115, 105 75, 120 65 C132 65, 136 90, 136 125 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Lifting arrow -->
            <path d="M210 160 L210 115 M200 125 L210 110 L220 125" stroke="#3B82F6" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
        '''
    },
    'sorry': {
        'title': 'SORRY',
        'sub': 'Closed Fist Circular over Chest',
        'art': '''
            <!-- Chest silhouette -->
            <path d="M60 250 C70 170, 230 170, 240 250 Z" fill="#FDF2F8" stroke="#FBCFE8" stroke-width="3"/>
            <!-- Closed fist -->
            <rect x="110" y="120" width="80" height="70" rx="20" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <path d="M110 150 C120 135, 150 135, 165 145" stroke="#4A3B32" stroke-width="4" fill="none"/>
            <path d="M110 168 C120 155, 150 155, 165 165" stroke="#4A3B32" stroke-width="4" fill="none"/>
            <!-- Circular motion arrow -->
            <path d="M150 90 A 65 65 0 1 1 138 92" fill="none" stroke="#EC4899" stroke-width="4" stroke-dasharray="6,4"/>
            <polygon points="138,84 138,100 126,92" fill="#EC4899"/>
        '''
    },
    'num1': {
        'title': 'NUMBER 1',
        'sub': 'Index Finger Upward',
        'art': '''
            <rect x="100" y="115" width="100" height="80" rx="18" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <path d="M115 190 L115 250 L175 250 L175 190 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <path d="M100 150 C100 130, 140 135, 160 145 C150 160, 120 160, 100 150 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <path d="M106 120 L106 40 C106 26, 128 26, 128 40 L128 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <circle cx="230" cy="60" r="22" fill="#2563EB"/>
            <text x="230" y="68" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF" text-anchor="middle">1</text>
        '''
    },
    'num2': {
        'title': 'NUMBER 2 / V',
        'sub': 'Index & Middle Up (V-Sign)',
        'art': '''
            <rect x="100" y="115" width="100" height="80" rx="18" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <path d="M115 190 L115 250 L175 250 L175 190 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <path d="M100 150 C100 130, 140 135, 160 145 C150 160, 120 160, 100 150 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <!-- Index Finger angled left -->
            <path d="M110 120 L96 45 C94 32, 114 26, 118 38 L130 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Middle Finger angled right -->
            <path d="M135 120 L146 38 C150 26, 170 32, 168 45 L155 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <circle cx="230" cy="60" r="22" fill="#2563EB"/>
            <text x="230" y="68" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF" text-anchor="middle">2</text>
        '''
    },
    'num3': {
        'title': 'NUMBER 3',
        'sub': 'Index, Middle & Ring Fingers Up',
        'art': '''
            <rect x="100" y="115" width="100" height="80" rx="18" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <path d="M115 190 L115 250 L175 250 L175 190 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <!-- Thumb over pinky -->
            <path d="M100 150 C110 135, 150 135, 168 150 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <!-- 3 Fingers Up -->
            <path d="M106 120 L102 45 C102 32, 122 32, 124 45 L125 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <path d="M128 120 L137 40 C137 28, 157 28, 157 40 L154 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <path d="M157 120 L168 46 C168 34, 188 34, 188 46 L182 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <circle cx="230" cy="60" r="22" fill="#2563EB"/>
            <text x="230" y="68" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF" text-anchor="middle">3</text>
        '''
    },
    'num4': {
        'title': 'NUMBER 4',
        'sub': 'Four Fingers Up, Thumb Folded',
        'art': '''
            <rect x="100" y="115" width="100" height="80" rx="18" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <path d="M115 190 L115 250 L175 250 L175 190 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <!-- Thumb folded inside -->
            <path d="M98 150 C110 140, 140 140, 150 155 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <!-- 4 Fingers upright -->
            <path d="M104 120 L104 46 C104 35, 122 35, 122 46 L123 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <path d="M126 120 L126 40 C126 28, 144 28, 144 40 L144 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <path d="M147 120 L147 42 C147 30, 165 30, 165 42 L165 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <path d="M168 120 L170 54 C170 42, 188 42, 188 54 L185 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <circle cx="230" cy="60" r="22" fill="#2563EB"/>
            <text x="230" y="68" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF" text-anchor="middle">4</text>
        '''
    },
    'num5': {
        'title': 'NUMBER 5',
        'sub': 'All 5 Fingers Extended & Spread',
        'art': '''
            <!-- Palm -->
            <path d="M100 150 C100 180, 110 200, 150 200 C190 200, 200 180, 200 150 L195 120 L105 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Wrist -->
            <path d="M120 195 L120 250 L180 250 L180 195 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <!-- Thumb -->
            <path d="M103 145 C80 140, 60 120, 65 105 C70 95, 85 100, 105 125 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4" stroke-linejoin="round"/>
            <!-- Index Finger -->
            <path d="M106 122 L104 55 C104 42, 122 42, 122 55 L124 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Middle Finger -->
            <path d="M127 120 L127 40 C127 28, 147 28, 147 40 L147 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Ring Finger -->
            <path d="M150 120 L152 48 C152 36, 172 36, 172 48 L170 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Pinky Finger -->
            <path d="M174 122 L180 70 C180 58, 198 58, 198 70 L194 125 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <circle cx="230" cy="60" r="22" fill="#2563EB"/>
            <text x="230" y="68" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF" text-anchor="middle">5</text>
        '''
    },
    'letter_c': {
        'title': 'LETTER C',
        'sub': 'Curved Fingers & Thumb ("C" Shape)',
        'art': '''
            <!-- C Shape Arch -->
            <path d="M120 190 L120 250 L170 250 L170 190 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <!-- Curved upper fingers -->
            <path d="M130 140 C120 90, 150 50, 190 50 C205 50, 215 65, 205 75 C180 75, 150 95, 150 135 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Curved bottom thumb -->
            <path d="M130 145 C120 165, 150 185, 190 185 C205 185, 215 170, 205 160 C180 160, 150 155, 150 140 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <circle cx="230" cy="60" r="22" fill="#7C3AED"/>
            <text x="230" y="68" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF" text-anchor="middle">C</text>
        '''
    },
    'letter_l': {
        'title': 'LETTER L',
        'sub': 'Index Up & Thumb Out (Right Angle)',
        'art': '''
            <!-- Base fist -->
            <rect x="105" y="115" width="90" height="75" rx="15" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <path d="M120 190 L120 250 L170 250 L170 190 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <!-- Horizontal Thumb -->
            <path d="M110 135 L50 135 C38 135, 38 155, 50 155 L110 155 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Vertical Index -->
            <path d="M110 120 L110 40 C110 26, 130 26, 130 40 L130 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <!-- Curled other fingers -->
            <path d="M135 135 C150 135, 175 135, 185 145" stroke="#4A3B32" stroke-width="4" fill="none"/>
            <path d="M135 155 C150 155, 175 155, 185 165" stroke="#4A3B32" stroke-width="4" fill="none"/>
            <circle cx="230" cy="60" r="22" fill="#7C3AED"/>
            <text x="230" y="68" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF" text-anchor="middle">L</text>
        '''
    },
    'letter_o': {
        'title': 'LETTER O',
        'sub': 'Fingertips Touching Thumb ("O" Circle)',
        'art': '''
            <path d="M120 190 L120 250 L170 250 L170 190 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <!-- O Circle Formation -->
            <path d="M130 145 C115 110, 130 65, 170 65 C205 65, 215 100, 210 120 C205 135, 190 140, 175 140 C165 140, 155 135, 155 125 C155 105, 175 95, 175 95 C150 95, 140 125, 145 145 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <circle cx="230" cy="60" r="22" fill="#7C3AED"/>
            <text x="230" y="68" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF" text-anchor="middle">O</text>
        '''
    },
    'letter_v': {
        'title': 'LETTER V',
        'sub': 'Index & Middle Up (V Shape)',
        'art': '''
            <rect x="100" y="115" width="100" height="80" rx="18" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <path d="M115 190 L115 250 L175 250 L175 190 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <path d="M100 150 C100 130, 140 135, 160 145 C150 160, 120 160, 100 150 Z" fill="#FFCC80" stroke="#4A3B32" stroke-width="4"/>
            <path d="M110 120 L96 45 C94 32, 114 26, 118 38 L130 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <path d="M135 120 L146 38 C150 26, 170 32, 168 45 L155 120 Z" fill="#FFE0B2" stroke="#4A3B32" stroke-width="4"/>
            <circle cx="230" cy="60" r="22" fill="#7C3AED"/>
            <text x="230" y="68" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF" text-anchor="middle">V</text>
        '''
    }
}

def generate_svgs():
    for name, data in SVG_TEMPLATES.items():
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" width="100%" height="100%">
  <defs>
    <linearGradient id="cardGrad_{name}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EFF6FF"/>
    </linearGradient>
  </defs>
  <!-- Background Card -->
  <rect width="300" height="300" rx="24" fill="url(#cardGrad_{name})" stroke="#E2E8F0" stroke-width="2"/>
  
  <!-- Artwork -->
  <g id="gesture-art">
    {data['art']}
  </g>

  <!-- Title Badge -->
  <rect x="15" y="258" width="270" height="32" rx="10" fill="#1E293B" opacity="0.9"/>
  <text x="150" y="279" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">{data['title']}</text>
</svg>'''
        filepath = os.path.join(SIGNS_DIR, f"{name}.svg")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"[SVG] Generated {filepath}")

if __name__ == '__main__':
    generate_svgs()
