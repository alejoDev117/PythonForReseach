from ImagesFuntions import analyze_images_in_folder
from AudioFuntions import  analyze_audio_folder
from TextFuntions import analyze_text_folder
if __name__ == "__main__":
    menu = """Welcome to the analysis software
    1. Images Analysis
    2. Audio Analysis
    3. Text Analysis
    4. Exit
    """
    print(menu)
    decision = int(input("Please, select the option number you want\n"))
    while decision < 4:
        if decision == 1:
            folder_path = "data/images"
            num_colors = 3
            analyze_images_in_folder(folder_path, num_colors=num_colors)
        elif decision == 2:
            folder_path="data/audios"
            analyze_audio_folder(folder_path)
        elif decision == 3:
            folder_path="data/texts"
            analyze_text_folder(folder_path)
        print(menu)
        decision = int(input("Please, select the option number you want\n"))

