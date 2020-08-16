import time
import multiprocessing


def is_prime(n):
    if n <= 1:
        return False

    if n <= 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


def check_single_digit(number, prime_array):
    time.sleep(2)
    prime_array.append({number: is_prime(number)})


if __name__ == "__main__":

    start = time.time()
    processes = []

    manager = multiprocessing.Manager()
    prime_numbers = manager.list()

    for number in range(1, 10):
        p = multiprocessing.Process(
            target=check_single_digit, args=(number, prime_numbers)
        )
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print(prime_numbers)
    print(f"Time Elapsed: {time.time() - start}")
