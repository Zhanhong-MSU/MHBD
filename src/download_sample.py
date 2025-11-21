import urllib.request
import os

def download_sample():
    # Get project root directory (parent of src)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_dir = os.path.join(project_root, "dataset")
    
    # Ensure dataset directory exists
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    # Use picsum.photos to get a random 300x300 image
    # This size is suitable for local MapReduce testing (visible effect, reasonable runtime)
    url = "https://picsum.photos/300/300"
    save_path = os.path.join(dataset_dir, "source_image.jpg")

    print(f"Downloading sample image from {url}...")
    try:
        urllib.request.urlretrieve(url, save_path)
        print(f"Download successful! Image saved to: {save_path}")
        print("You can now run 'python3 main.py' to test.")
    except Exception as e:
        print(f"Download failed: {e}")

if __name__ == "__main__":
    download_sample()
