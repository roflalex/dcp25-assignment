def count_notes(notes):
    """Count frequency of each note."""
    note_counts = {}
    for note in notes:
        if note in note_counts:
            note_counts[note] += 1
        else:
            note_counts[note] = 1
    return note_counts

def count_bars(music_lines):
    """Count the number of bars (measures)."""
    bar_count = 0
    for line in music_lines:
        # Count bar lines (|) but not repeat signs (:)
        bar_count += line.count('|')
    return bar_count

def find_note_range(notes):
    """Find the highest and lowest notes."""
    # In ABC notation:
    # C D E F G A B (lowercase) are higher octave
    # C, D, E, F, G, A, B, (with comma or capital) are lower octave
    
    if not notes:
        return None, None
    
    # For simplicity, just find first and last alphabetically
    # (this is a simplified version)
    note_set = set(notes)
    return min(note_set), max(note_set)

def get_most_common_note(notes):
    """Find the most frequently used note."""
    counts = count_notes(notes)
    most_common = max(counts.items(), key=lambda x: x[1])
    return most_common

# Analyze the tune
notes = extract_notes(song_data['music'])

print("=== Analysis ===")
print(f"Total notes: {len(notes)}")
print(f"Number of bars: {count_bars(song_data['music'])}")
print(f"Unique notes: {len(set(notes))}")

note_counts = count_notes(notes)
print(f"\nNote frequencies:")
for note, count in sorted(note_counts.items()):
    print(f"  {note}: {count}")

most_common_note, count = get_most_common_note(notes)
print(f"\nMost common note: {most_common_note} (appears {count} times)")