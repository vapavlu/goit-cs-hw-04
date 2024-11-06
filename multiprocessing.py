import multiprocessing
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

# Функція для обробки файлів у процесі
def process_files_process(file_paths, keywords, result_queue):
    result = {}
    for file_path in file_paths:
        found_keywords = search_keywords_in_file(file_path, keywords)
        for keyword in found_keywords:
            if keyword not in result:
                result[keyword] = []
            result[keyword].append(file_path)
    result_queue.put(result)

# Функція для паралельного пошуку з використанням процесів
def multiprocessing_search(file_list, keywords, num_processes=4):
    result_queue = multiprocessing.Queue()
    processes = []
    result_dict = {}
    chunk_size = len(file_list) // num_processes
    start_time = time.time()

    for i in range(num_processes):
        chunk = file_list[i*chunk_size:(i+1)*chunk_size]
        process = multiprocessing.Process(target=process_files_process, args=(chunk, keywords, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Збір результатів із черги
    while not result_queue.empty():
        result = result_queue.get()
        for keyword, files in result.items():
            if keyword not in result_dict:
                result_dict[keyword] = []
            result_dict[keyword].extend(files)

    end_time = time.time()
    print(f"Multiprocessing search completed in {end_time - start_time} seconds.")
    return result_dict

# Приклад запуску багатопроцесорної функції
result_multiprocessing = multiprocessing_search(file_list, keywords)
print("Multiprocessing Search Results:", result_multiprocessing)
