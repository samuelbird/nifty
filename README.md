# Spaced Repetition Learning App

A desktop application for quickly noting down nifty tidbits without disrupting your workflow, allowing for later spaced repetition learning to make these tidbits stick.

## Features

- Quick add items using a global hotkey (Ctrl+Shift+S)
- Spaced repetition algorithm for optimal learning intervals
- Review system with difficulty ratings
- Statistics tracking
- Local SQLite database for data persistence

## Installation

1. Make sure you have Python 3.x installed
2. Install the required dependencies:
   ```bash
   pip install keyboard
   ```
   (Note: tkinter and sqlite3 are included in Python's standard library)

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Adding Items:
   - Use the "Add Item" tab to add new items to learn
   - Or use the global hotkey Ctrl+Shift+S to quickly add items from anywhere

3. Reviewing Items:
   - Go to the "Review" tab
   - Click "Start Review" to begin reviewing items
   - Rate each item as "Hard", "Good", or "Easy"
   - The app will automatically schedule the next review based on your rating

4. Statistics:
   - Check the "Statistics" tab to see your learning progress
   - View total items, items due for review, and average reviews per item

## How It Works

The app uses a spaced repetition algorithm that:
- Increases intervals between reviews for items you find easy
- Decreases intervals for items you find hard
- Adjusts the difficulty factor based on your performance
- Automatically schedules reviews at optimal intervals

## Data Storage

All your learning items are stored in a local SQLite database (`learning_items.db`) in the same directory as the application.
