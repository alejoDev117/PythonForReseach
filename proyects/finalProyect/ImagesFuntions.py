import os
import shutil
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from PIL import Image

def extract_dominant_colors(image, num_colors=5):
    image_array = np.array(image)
    pixels = image_array.reshape(-1, 3)
    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(pixels)
    dominant_colors = kmeans.cluster_centers_.astype(int)
    return dominant_colors

def classify_by_dominant_color(dominant_colors):
    dominant_color = np.mean(dominant_colors, axis=0)
    r, g, b = dominant_color

    if g > r and g > b:
        return "Green"
    elif r > g and r > b:
        return "Red"
    elif b > r and b > g:
        return "Blue"
    else:
        return "Indeterminate"

def plot_dominant_colors(colors, image_name="", save_path=None):
    fig, ax = plt.subplots(1, len(colors), figsize=(len(colors) * 2, 2))
    if len(colors) == 1:
        ax = [ax]
    for i, color in enumerate(colors):
        ax[i].imshow([[color / 255.0]])
        ax[i].axis('off')
    if image_name:
        plt.suptitle(f"Dominant colors for: {image_name}", fontsize=16)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def create_output_folder(folder_path):
    output_folder = os.path.join(folder_path, 'output')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def create_category_folder(output_folder, category):
    category_folder = os.path.join(output_folder, category)
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)
    return category_folder

def move_image_to_category(image_path, category, category_folder):
    new_image_name = f"{category}_{os.path.basename(image_path)}"
    new_image_path = os.path.join(category_folder, new_image_name)
    shutil.copy(image_path, new_image_path)

def analyze_images_in_folder(folder_path, num_colors=5):
    output_folder = create_output_folder(folder_path)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)

            print(f"Analyzing {filename}...")
            dominant_colors = extract_dominant_colors(image, num_colors=num_colors)
            print(f"Dominant colors for {filename}: {dominant_colors}")

            category = classify_by_dominant_color(dominant_colors)
            print(f"Classified as: {category}")
            category_folder = create_category_folder(output_folder, category)
            plot_dominant_colors(dominant_colors, image_name=filename, save_path=os.path.join(category_folder, f"{category}_dominant_colors.png"))
            move_image_to_category(image_path, category, category_folder)
            print(f"Classification of {filename}: {category}\n")