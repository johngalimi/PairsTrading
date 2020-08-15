import time
import multiprocessing

prime_numbers = []


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


def test_single_digit(number):
    time.sleep(2)
    if is_prime(number):
        prime_numbers.append(number)


if __name__ == "__main__":
    start = time.time()

    for number in range(1, 10):
        test_single_digit(number)

    print(prime_numbers)

    # ~18s on average
    print(f"Time Elapsed: {time.time() - start}")

    start = time.time()
    processes = []

    for number in range(1, 10):
        p = multiprocessing.Process(target=test_single_digit, args=(number,))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print(prime_numbers)

    # ~2s on average
    print(f"Time Elapsed: {time.time() - start}")
