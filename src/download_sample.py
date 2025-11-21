import urllib.request
import os

def download_sample():
    # 获取项目根目录 (src 的上一级)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_dir = os.path.join(project_root, "dataset")
    
    # 确保 dataset 目录存在
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    # 使用 picsum.photos 获取一张 300x300 的随机图片
    # 这个尺寸对于 MapReduce 本地测试来说非常合适（既能看清效果，又不会跑太久）
    url = "https://picsum.photos/300/300"
    save_path = os.path.join(dataset_dir, "source_image.jpg")

    print(f"正在从 {url} 下载测试图片...")
    try:
        urllib.request.urlretrieve(url, save_path)
        print(f"下载成功！图片已保存为: {save_path}")
        print("现在您可以运行 'python src/driver.py' 来测试了。")
    except Exception as e:
        print(f"下载失败: {e}")

if __name__ == "__main__":
    download_sample()
