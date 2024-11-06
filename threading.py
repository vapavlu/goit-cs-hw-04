import threading
import os
import time

# Функція для пошуку ключових слів у файлі
def search_keywords_in_file(file_path, keywords):
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results.append(keyword)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return results

# Функція для обробки частини файлів у потоці
def process_files_thread(file_paths, keywords, result_dict, lock):
    for file_path in file_paths:
        found_keywords = search_keywords_in_file(file_path, keywords)
        with lock:
            for keyword in found_keywords:
                if keyword not in result_dict:
                    result_dict[keyword] = []
                result_dict[keyword].append(file_path)

# Функція для паралельного пошуку з використанням потоків
def threaded_search(file_list, keywords, num_threads=4):
    lock = threading.Lock()
    result_dict = {}
    threads = []
    chunk_size = len(file_list) // num_threads
    start_time = time.time()

    for i in range(num_threads):
        chunk = file_list[i*chunk_size:(i+1)*chunk_size]
        thread = threading.Thread(target=process_files_thread, args=(chunk, keywords, result_dict, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Threaded search completed in {end_time - start_time} seconds.")
    return result_dict

# Приклад запуску багатопотокової функції
file_list = ['file1.txt', 'file2.txt', 'file3.txt']  # замініть на актуальні файли
keywords = ['Python', 'threading', 'multiprocessing']
result_threaded = threaded_search(file_list, keywords)
print("Threaded Search Results:", result_threaded)
