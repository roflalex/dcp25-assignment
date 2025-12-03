class ABCParser:
    """Parser for ABC music notation files."""
    
    def __init__(self, filename):
        self.filename = filename
        self.metadata = {}
        self.music_lines = []
        self.notes = []
        self.parse_file()
    
    def parse_file(self):
        """Parse the ABC file into metadata and music."""
        in_header = True
        
        with open(self.filename, "r") as file:
            for line in file:
                line = line.strip()
                
                if not line:
                    continue
                
                if in_header and ':' in line and line[0].isalpha() and line[1] == ':':
                    field = line[0]
                    value = line[2:].strip()
                    
                    field_names = {
                        'X': 'reference',
                        'T': 'title',
                        'M': 'meter',
                        'L': 'default_length',
                        'R': 'rhythm',
                        'K': 'key'
                    }
                    
                    if field in field_names:
                        self.metadata[field_names[field]] = value
                    
                    if field == 'K':
                        in_header = False
                else:
                    self.music_lines.append(line)
        
        self.extract_notes()
    
    def extract_notes(self):
        """Extract all notes from music notation."""
        for line in self.music_lines:
            for char in line:
                if char.isalpha() and char.lower() in 'abcdefg':
                    self.notes.append(char)
    
    def get_title(self):
        """Get the song title."""
        return self.metadata.get('title', 'Unknown')
    
    def get_key(self):
        """Get the key signature."""
        return self.metadata.get('key', 'Unknown')
    
    def get_meter(self):
        """Get the time signature."""
        return self.metadata.get('meter', 'Unknown')
    
    def count_notes(self):
        """Count frequency of each note."""
        counts = {}
        for note in self.notes:
            counts[note] = counts.get(note, 0) + 1
        return counts
    
    def count_bars(self):
        """Count the number of bars."""
        count = 0
        for line in self.music_lines:
            count += line.count('|')
        return count
    
    def total_notes(self):
        """Get total number of notes."""
        return len(self.notes)
    
    def unique_notes(self):
        """Get number of unique notes used."""
        return len(set(self.notes))
    
    def most_common_note(self):
        """Find the most frequently used note."""
        counts = self.count_notes()
        if not counts:
            return None, 0
        return max(counts.items(), key=lambda x: x[1])
    
    def display_info(self):
        """Display all information about the tune."""
        print(f"{'='*50}")
        print(f"Title: {self.get_title()}")
        print(f"Key: {self.get_key()}")
        print(f"Meter: {self.get_meter()}")
        print(f"Rhythm: {self.metadata.get('rhythm', 'Unknown')}")
        print(f"{'='*50}")
        print(f"Total notes: {self.total_notes()}")
        print(f"Unique notes: {self.unique_notes()}")
        print(f"Number of bars: {self.count_bars()}")
        
        note, count = self.most_common_note()
        print(f"Most common note: {note} ({count} times)")
        
        print(f"\nNote distribution:")
        for note, count in sorted(self.count_notes().items()):
            bar_length = int(count / self.total_notes() * 40)
            bar = '█' * bar_length
            print(f"  {note}: {bar} {count}")
    
    def get_music_text(self):
        """Get the music notation as text."""
        return '\n'.join(self.music_lines)
