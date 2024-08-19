import os
import psutil
import threading

def allocate_memory(target_percent):
    mem = psutil.virtual_memory()
    target_usage = mem.total * target_percent / 100
    block_size = 1024 * 1024  # 1 MB block size
    num_blocks = int(target_usage / block_size)
    
    # 使用全域列表保持記憶體塊，防止垃圾回收
    global blocks
    blocks = []
    
    try:
        for i in range(num_blocks):
            blocks.append(bytearray(block_size))
            # 檢查目前記憶體使用情況，確保不會超出目標
            current_usage = psutil.virtual_memory().percent
            if current_usage >= target_percent:
                print(f"記憶體使用已達到 {current_usage}%，停止分配。")
                break
        print(f"最終記憶體使用：{current_usage}%")
    except MemoryError:
        print("沒有足夠的記憶體可供分配。")

def get_input():
    try:
        percent_input = input("請輸入記憶體使用百分比（若 3 秒內無輸入，將預設為 60%）：")
        return int(percent_input)
    except ValueError:
        return None

def input_with_timeout(timeout, default_value=60):
    input_event = threading.Event()

    def wait_for_input():
        nonlocal user_input
        user_input = get_input()
        input_event.set()

    user_input = None
    input_thread = threading.Thread(target=wait_for_input)
    input_thread.start()

    input_thread.join(timeout)
    if not input_event.is_set():
        print("\n未收到輸入，將預設為 60%...")
        return default_value
    else:
        return user_input if user_input is not None else default_value

if __name__ == "__main__":
    percent = input_with_timeout(3)
    print("開始")
    allocate_memory(percent)
    input("記憶體已釋放，按下 Enter 鍵退出程式。")
    blocks = None  # 手動釋放記憶體
