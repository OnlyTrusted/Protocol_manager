"""
Main entry point for the Protocol Clipboard Manager application.
"""
import sys
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox

from .app.main_window import MainWindow

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Launch the application."""
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Protocol Clipboard Manager")
        
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec_())
    except ImportError as e:
        print(f"Failed to import required modules: {e}")
        print("Please ensure PyQt5 is installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error occurred")
        try:
            QMessageBox.critical(
                None,
                "Application Error",
                f"An unexpected error occurred:\n\n{str(e)}\n\n"
                "Please check the logs for more details."
            )
        except:
            # If even the message box fails, just print
            print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
