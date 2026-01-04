import os
import datetime

def get_all_filenames(folder_path):
    """
    获取指定文件夹中所有文件的名称
    
    Args:
        folder_path (str): 目标文件夹路径
    
    Returns:
        list: 包含所有文件名的列表
    """
    try:
        # 获取文件夹中所有项目
        all_items = os.listdir(folder_path)
        
        # 过滤出文件（排除子文件夹）
        filenames = []
        for item in all_items:
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                filenames.append(item)
        
        return filenames
    except FileNotFoundError:
        print(f"错误：找不到路径 '{folder_path}'")
        return []
    except PermissionError:
        print(f"错误：没有权限访问 '{folder_path}'")
        return []

def get_all_filenames_recursive(folder_path):
    """
    递归获取指定文件夹及子文件夹中所有文件的名称
    
    Args:
        folder_path (str): 目标文件夹路径
    
    Returns:
        list: 包含所有文件名的列表（包含相对路径）
    """
    try:
        filenames = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # 获取相对于根目录的路径
                relative_path = os.path.relpath(os.path.join(root, file), folder_path)
                filenames.append(relative_path)
        return filenames
    except Exception as e:
        print(f"错误：{e}")
        return []

def save_filenames_to_file(filenames, output_folder, recursive=False):
    """
    将文件名列表保存到以当前日期时间命名的txt文件中
    
    Args:
        filenames (list): 文件名列表
        output_folder (str): 输出文件夹路径
        recursive (bool): 是否为递归模式
    """
    # 生成当前日期时间的文件名
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    mode_str = "_recursive" if recursive else ""
    filename = f"files_list_{current_time}{mode_str}.txt"
    filepath = os.path.join(output_folder, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"文件列表生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"扫描路径: {output_folder}\n")
            f.write(f"扫描模式: {'递归模式' if recursive else '仅当前文件夹'}\n")
            f.write(f"文件总数: {len(filenames)}\n")
            f.write("-" * 50 + "\n\n")
            
            for i, name in enumerate(filenames, 1):
                f.write(f"{i}. {name}\n")
        
        print(f"成功将 {len(filenames)} 个文件名保存到: {filepath}")
        return filepath
    except Exception as e:
        print(f"保存文件时出错: {e}")
        return None

def main():
    print("=== 文件夹文件名抓取并保存工具 ===")
    
    # 获取用户输入的文件夹路径
    folder_path = input("请输入要扫描的文件夹路径: ").strip()
    
    if not folder_path:
        print("错误：路径不能为空")
        return
    
    # 检查路径是否存在
    if not os.path.exists(folder_path):
        print(f"错误：路径 '{folder_path}' 不存在")
        return
    
    if not os.path.isdir(folder_path):
        print(f"错误：'{folder_path}' 不是一个文件夹")
        return
    
    print("\n请选择操作模式:")
    print("1. 仅获取当前文件夹中的文件")
    print("2. 递归获取所有子文件夹中的文件")
    
    choice = input("请输入选择 (1 或 2): ").strip()
    
    if choice == "1":
        filenames = get_all_filenames(folder_path)
        print(f"\n在文件夹 '{folder_path}' 中找到 {len(filenames)} 个文件:")
        for i, filename in enumerate(filenames[:10], 1):  # 只显示前10个
            print(f"{i}. {filename}")
        if len(filenames) > 10:
            print(f"... 还有 {len(filenames)-10} 个文件")
        
        # 保存到文件
        save_filenames_to_file(filenames, folder_path, recursive=False)
        
    elif choice == "2":
        filenames = get_all_filenames_recursive(folder_path)
        print(f"\n在文件夹 '{folder_path}' 及其子文件夹中找到 {len(filenames)} 个文件:")
        for i, filename in enumerate(filenames[:10], 1):  # 只显示前10个
            print(f"{i}. {filename}")
        if len(filenames) > 10:
            print(f"... 还有 {len(filenames)-10} 个文件")
        
        # 保存到文件
        save_filenames_to_file(filenames, folder_path, recursive=True)
    else:
        print("无效的选择")

if __name__ == "__main__":
    main()



