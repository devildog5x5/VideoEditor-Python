"""
Core Video Editor Application
Main window and application logic
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFileDialog, QLabel, QSlider,
                             QMessageBox, QSplitter, QToolBar, QStatusBar)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QKeySequence
import os
from timeline import TimelineWidget
from preview import PreviewWidget
from project_manager import ProjectManager
from export_manager import ExportManager
from ui.properties_panel import PropertiesPanel
from ui.media_library import MediaLibrary
from ui.theme_selector import ThemeSelector
from themes import ThemeManager

class VideoEditor(QMainWindow):
    """Main video editor application window"""
    
    def __init__(self):
        super().__init__()
        self.project_manager = ProjectManager()
        self.export_manager = ExportManager()
        self.theme_manager = ThemeManager()
        self.current_project = None
        self.clips = []  # List of video clips on timeline
        self.selected_clip = None
        self.playback_position = 0
        self.is_playing = False
        
        self.init_ui()
        self.setup_shortcuts()
        self.apply_theme()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Professional Video Editor")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main splitter (horizontal)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel: Media Library
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Media Library"))
        self.media_library = MediaLibrary()
        self.media_library.media_selected.connect(self.on_media_selected)
        left_layout.addWidget(self.media_library)
        
        # Center: Preview and Timeline
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        
        # Preview window
        self.preview = PreviewWidget()
        center_layout.addWidget(self.preview)
        
        # Timeline
        self.timeline = TimelineWidget()
        self.timeline.clip_selected.connect(self.on_clip_selected)
        self.timeline.position_changed.connect(self.on_timeline_position_changed)
        center_layout.addWidget(self.timeline)
        
        # Right panel: Properties and Theme
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Theme selector
        self.theme_selector = ThemeSelector(self.theme_manager)
        self.theme_selector.theme_changed.connect(self.on_theme_changed)
        right_layout.addWidget(self.theme_selector)
        
        # Properties panel
        self.properties_panel = PropertiesPanel()
        self.properties_panel.properties_changed.connect(self.on_properties_changed)
        right_layout.addWidget(self.properties_panel)
        
        right_layout.addStretch()
        
        # Add panels to splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(center_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 3)
        main_splitter.setStretchFactor(2, 1)
        
        main_layout.addWidget(main_splitter)
        
        # Create status bar
        self.statusBar().showMessage("Ready")
        
        # Playback timer
        self.playback_timer = QTimer()
        self.playback_timer.timeout.connect(self.update_playback)
        
    def create_toolbar(self):
        """Create the main toolbar"""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        # File actions
        new_action = QAction("New Project", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_project)
        toolbar.addAction(new_action)
        
        open_action = QAction("Open Project", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_project)
        toolbar.addAction(open_action)
        
        save_action = QAction("Save Project", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_project)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Import
        import_action = QAction("Import Video", self)
        import_action.triggered.connect(self.import_video)
        toolbar.addAction(import_action)
        
        toolbar.addSeparator()
        
        # Playback controls
        play_action = QAction("▶ Play", self)
        play_action.setShortcut(Qt.Key.Key_Space)
        play_action.triggered.connect(self.toggle_playback)
        toolbar.addAction(play_action)
        
        stop_action = QAction("⏹ Stop", self)
        stop_action.triggered.connect(self.stop_playback)
        toolbar.addAction(stop_action)
        
        toolbar.addSeparator()
        
        # Editing tools
        cut_action = QAction("✂ Cut", self)
        cut_action.setShortcut("S")
        cut_action.triggered.connect(self.cut_at_playhead)
        toolbar.addAction(cut_action)
        
        delete_action = QAction("🗑 Delete", self)
        delete_action.setShortcut(Qt.Key.Key_Delete)
        delete_action.triggered.connect(self.delete_selected)
        toolbar.addAction(delete_action)
        
        toolbar.addSeparator()
        
        # Export
        export_action = QAction("Export Video", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_video)
        toolbar.addAction(export_action)
        
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Undo/Redo
        undo_action = QAction(self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self.undo)
        self.addAction(undo_action)
        
        redo_action = QAction(self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self.redo)
        self.addAction(redo_action)
        
    def new_project(self):
        """Create a new project"""
        if self.current_project and self.has_unsaved_changes():
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Create new project anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        self.current_project = self.project_manager.create_new()
        self.clips = []
        self.timeline.clear()
        self.preview.clear()
        self.statusBar().showMessage("New project created")
        
    def open_project(self):
        """Open an existing project"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", "Video Editor Projects (*.vep)"
        )
        if filename:
            try:
                self.current_project = self.project_manager.load(filename)
                self.load_project_data()
                self.statusBar().showMessage(f"Project loaded: {os.path.basename(filename)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load project:\n{str(e)}")
    
    def save_project(self):
        """Save the current project"""
        if not self.current_project:
            self.current_project = self.project_manager.create_new()
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Project", "", "Video Editor Projects (*.vep)"
        )
        if filename:
            try:
                project_data = {
                    'clips': [clip.to_dict() for clip in self.clips],
                    'timeline_data': self.timeline.get_timeline_data()
                }
                self.project_manager.save(filename, project_data)
                self.statusBar().showMessage(f"Project saved: {os.path.basename(filename)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save project:\n{str(e)}")
    
    def import_video(self):
        """Import video files"""
        filenames, _ = QFileDialog.getOpenFileNames(
            self, "Import Videos", "",
            "Video Files (*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.webm);;All Files (*)"
        )
        for filename in filenames:
            self.media_library.add_media(filename)
        self.statusBar().showMessage(f"Imported {len(filenames)} video(s)")
    
    def on_media_selected(self, filepath):
        """Handle media selection from library"""
        # Add to timeline at current position
        from clip import VideoClip
        clip = VideoClip(filepath)
        clip.start_time = self.playback_position
        self.clips.append(clip)
        self.timeline.add_clip(clip)
        self.statusBar().showMessage(f"Added {os.path.basename(filepath)} to timeline")
    
    def on_clip_selected(self, clip):
        """Handle clip selection from timeline"""
        self.selected_clip = clip
        self.properties_panel.set_clip(clip)
        self.preview.set_clip(clip)
    
    def on_timeline_position_changed(self, position):
        """Handle timeline position change"""
        self.playback_position = position
        self.preview.set_position(position)
    
    def on_properties_changed(self, properties):
        """Handle property changes"""
        if self.selected_clip:
            self.selected_clip.update_properties(properties)
            self.timeline.update_clip(self.selected_clip)
            self.preview.refresh()
    
    def toggle_playback(self):
        """Toggle playback"""
        if self.is_playing:
            self.pause_playback()
        else:
            self.start_playback()
    
    def start_playback(self):
        """Start playback"""
        self.is_playing = True
        self.playback_timer.start(33)  # ~30 FPS
        self.statusBar().showMessage("Playing...")
    
    def pause_playback(self):
        """Pause playback"""
        self.is_playing = False
        self.playback_timer.stop()
        self.statusBar().showMessage("Paused")
    
    def stop_playback(self):
        """Stop playback"""
        self.pause_playback()
        self.playback_position = 0
        self.timeline.set_position(0)
        self.preview.set_position(0)
    
    def update_playback(self):
        """Update playback position"""
        duration = self.timeline.get_total_duration()
        if self.playback_position < duration:
            self.playback_position += 0.033  # ~30 FPS
            self.timeline.set_position(self.playback_position)
            self.preview.set_position(self.playback_position)
        else:
            self.stop_playback()
    
    def cut_at_playhead(self):
        """Cut selected clip at playhead position"""
        if self.selected_clip:
            cut_time = self.playback_position - self.selected_clip.start_time
            if 0 < cut_time < self.selected_clip.duration:
                new_clip = self.selected_clip.split(cut_time)
                self.clips.append(new_clip)
                self.timeline.add_clip(new_clip)
                self.statusBar().showMessage("Clip cut")
    
    def delete_selected(self):
        """Delete selected clip"""
        if self.selected_clip:
            self.clips.remove(self.selected_clip)
            self.timeline.remove_clip(self.selected_clip)
            self.selected_clip = None
            self.properties_panel.clear()
            self.statusBar().showMessage("Clip deleted")
    
    def undo(self):
        """Undo last action"""
        # TODO: Implement undo system
        self.statusBar().showMessage("Undo")
    
    def redo(self):
        """Redo last action"""
        # TODO: Implement redo system
        self.statusBar().showMessage("Redo")
    
    def export_video(self):
        """Export the edited video"""
        if not self.clips:
            QMessageBox.warning(self, "No Clips", "Add clips to timeline before exporting")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Video", "", "MP4 Files (*.mp4);;AVI Files (*.avi);;MOV Files (*.mov)"
        )
        if filename:
            try:
                self.statusBar().showMessage("Exporting video...")
                self.export_manager.export(self.clips, filename, self.on_export_progress)
                self.statusBar().showMessage(f"Video exported: {os.path.basename(filename)}")
                QMessageBox.information(self, "Success", "Video exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export video:\n{str(e)}")
                self.statusBar().showMessage("Export failed")
    
    def on_export_progress(self, progress):
        """Handle export progress updates"""
        self.statusBar().showMessage(f"Exporting... {progress}%")
    
    def load_project_data(self):
        """Load project data into UI"""
        # TODO: Implement project loading
        pass
    
    def has_unsaved_changes(self):
        """Check if there are unsaved changes"""
        # TODO: Implement change tracking
        return False
    
    def apply_theme(self):
        """Apply current theme to application"""
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            theme_colors = self.theme_manager.apply_theme(app)
            stylesheet = self.theme_manager.get_stylesheet()
            app.setStyleSheet(stylesheet)
            
            # Store theme colors for custom widgets
            app.setProperty('theme_colors', theme_colors)
            
            # Apply theme-specific styling to custom widgets
            self.apply_custom_theme_styling(theme_colors)
    
    def apply_custom_theme_styling(self, theme_colors):
        """Apply theme to custom widgets"""
        # Timeline styling
        self.timeline.setStyleSheet(
            f"background-color: {theme_colors['timeline_bg'].name()};"
            f"color: {theme_colors['timeline_fg'].name()};"
        )
        
        # Preview styling
        self.preview.setStyleSheet(
            f"background-color: {theme_colors['preview_bg'].name()};"
        )
        
        # Media library styling
        self.media_library.setStyleSheet(
            f"background-color: {theme_colors['base_bg'].name()};"
            f"color: {theme_colors['base_fg'].name()};"
        )
    
    def on_theme_changed(self, theme):
        """Handle theme change"""
        self.apply_theme()
        self.statusBar().showMessage(f"Theme changed to {self.theme_manager.get_theme_name(theme)}")
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.has_unsaved_changes():
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Exit anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
        event.accept()

