try:
    import win32ui
    import win32con
    import win32print
    from PIL import Image, ImageWin
    import fitz
    print("Imports OK")
except ImportError as e:
    print(f"Import Error: {e}")
except Exception as e:
    print(f"Error: {e}")
