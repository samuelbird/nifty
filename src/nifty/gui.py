import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                            QTabWidget, QMessageBox)
from PyQt6.QtCore import Qt
from .logic import SpacedRepetitionDB, calculate_next_interval_and_ease
from .hotkey import HotkeyListener

class SpacedRepetitionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spaced Repetition Learning")
        self.setGeometry(100, 100, 600, 400)
        
        # Initialize database
        self.db = SpacedRepetitionDB()
        
        # Create main UI
        self.create_ui()
        
        # Register global hotkey (Ctrl+Shift+S) using pynput
        self.hotkey_listener = HotkeyListener('<ctrl>+<shift>+s', self.show_quick_add_window)
        self.hotkey_listener.start()
    
    def create_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Review tab
        self.review_tab = QWidget()
        self.tabs.addTab(self.review_tab, "Review")
        self.setup_review_tab()
        
        # Add item tab
        self.add_tab = QWidget()
        self.tabs.addTab(self.add_tab, "Add Item")
        self.setup_add_tab()
        
        # Stats tab
        self.stats_tab = QWidget()
        self.tabs.addTab(self.stats_tab, "Statistics")
        self.setup_stats_tab()
    
    def setup_review_tab(self):
        layout = QVBoxLayout(self.review_tab)
        
        # Review label
        self.review_label = QLabel("Click 'Start Review' to begin")
        self.review_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.review_label)
        
        # Start review button
        self.start_review_btn = QPushButton("Start Review")
        self.start_review_btn.clicked.connect(self.start_review)
        layout.addWidget(self.start_review_btn)
        
        # Answer buttons
        self.answer_layout = QHBoxLayout()
        self.answer_buttons = []
        for rating in ["Hard", "Good", "Easy"]:
            btn = QPushButton(rating)
            btn.clicked.connect(lambda checked, r=rating: self.rate_answer(r))
            self.answer_layout.addWidget(btn)
            self.answer_buttons.append(btn)
        layout.addLayout(self.answer_layout)
        self.hide_answer_buttons()
    
    def setup_add_tab(self):
        layout = QVBoxLayout(self.add_tab)
        
        # Add item label
        layout.addWidget(QLabel("Add New Item to Learn:"))
        
        # Content text area
        self.content_text = QTextEdit()
        layout.addWidget(self.content_text)
        
        # Add button
        add_btn = QPushButton("Add Item")
        add_btn.clicked.connect(self.add_item)
        layout.addWidget(add_btn)
    
    def setup_stats_tab(self):
        layout = QVBoxLayout(self.stats_tab)
        
        # Statistics label
        self.stats_label = QLabel("Loading statistics...")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.stats_label)
        self.update_stats()
    
    def show_quick_add_window(self):
        self.quick_window = QWidget()
        self.quick_window.setWindowTitle("Quick Add")
        self.quick_window.setGeometry(200, 200, 300, 200)
        
        layout = QVBoxLayout(self.quick_window)
        
        # Add item label
        layout.addWidget(QLabel("Enter item to learn:"))
        
        # Content text area
        content_entry = QTextEdit()
        layout.addWidget(content_entry)
        
        # Save button
        save_btn = QPushButton("Save")
        def save_and_close():
            content = content_entry.toPlainText().strip()
            if content:
                self.db.add_item(content)
                self.update_stats()
            self.quick_window.close()
        save_btn.clicked.connect(save_and_close)
        layout.addWidget(save_btn)
        self.quick_window.show()
        content_entry.setFocus()
    
    def add_item(self):
        content = self.content_text.toPlainText().strip()
        if content:
            self.db.add_item(content)
            self.content_text.clear()
            QMessageBox.information(self, "Success", "Item added successfully!")
            self.update_stats()
        else:
            QMessageBox.warning(self, "Warning", "Please enter some content!")
    
    def start_review(self):
        item = self.db.get_due_item()
        if item:
            self.current_item = item
            self.review_label.setText(item.content)
            self.show_answer_buttons()
        else:
            self.review_label.setText("No items due for review!")
            self.hide_answer_buttons()
    
    def rate_answer(self, rating):
        if not hasattr(self, 'current_item'):
            return
        item = self.current_item
        interval, ease_factor = calculate_next_interval_and_ease(item.review_count, item.ease_factor, rating)
        self.db.update_item_review(item.id, item.review_count + 1, ease_factor, interval)
        self.start_review()
        self.update_stats()
    
    def show_answer_buttons(self):
        for btn in self.answer_buttons:
            btn.show()
    
    def hide_answer_buttons(self):
        for btn in self.answer_buttons:
            btn.hide()
    
    def update_stats(self):
        total, due, avg_reviews = self.db.get_stats()
        stats_text = f"""Statistics:\nTotal Items: {total}\nItems Due for Review: {due}\nAverage Reviews per Item: {avg_reviews:.1f}"""
        self.stats_label.setText(stats_text)
    
    def closeEvent(self, event):
        self.db.close()
        self.hotkey_listener.stop()
        event.accept()

def run_gui():
    app = QApplication(sys.argv)
    window = SpacedRepetitionApp()
    window.show()
    sys.exit(app.exec()) 