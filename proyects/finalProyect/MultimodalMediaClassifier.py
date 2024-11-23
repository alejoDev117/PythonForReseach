from ImagesFuntions import analyze_images_in_folder
from AudioFuntions import  analyze_audio_folder
if __name__ == "__main__":
    menu = """Welcome to the analysis software
    1. Images Analysis
    2. Audio Analysis
    3. Text Analysis
    4. Exit
    """
    decision = int(input("Please, select the option number you want\n"))
    while decision < 4:
        if decision == 1:
            folder_path = "data/images"
            num_colors = 3
            analyze_images_in_folder(folder_path, num_colors=num_colors)
        elif decision == 2:
            folder_path="data/audios"
            analyze_audio_folder(folder_path)
        decision = int(input("Please, select the option number you want\n"))

