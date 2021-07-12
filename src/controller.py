import argparse
import importlib
import concurrent.futures
import numpy
import pandas

import constants


def parse_args():
    parser = argparse.ArgumentParser(
        description='Simulates 100 games of snake with the given algorithms.')
    parser.add_argument('--visualize', '-v', action='store_true',
                        help='Turns on visualization of the supplied algorithm')
    parser.add_argument("--algorithm", '-a', default='ALL',
                        help=f'Target algorithm to benchmark / visualize.\nValid algorithms: {constants.ALGORITHM_LIST}')
    parser.add_argument("--threads", '-t', type=int, default=1,
                        help='Number of threads to use. Default 1')
    return parser.parse_args()


def import_algorithm(algo_name):
    algorithm_package = importlib.import_module(algo_name)
    return getattr(algorithm_package, algo_name)


def run_algorithm(algorithm_class, run=1, visualize=False):
    print(f"Algorithm: {algorithm_class.__name__}, Run: {run}")
    algorithm = algorithm_class(visualize)
    won, steps = algorithm.run()
    return won, steps


def benchmark_controller(target_algo, threads):
    if target_algo == 'ALL':
        algs_to_run = constants.ALGORITHM_LIST
    else:
        algs_to_run = [target_algo]

    overall_results = {}
    for algo in algs_to_run:
        results = []
        algo_class = import_algorithm(algo)

        if threads > 1:
            with concurrent.futures.ProcessPoolExecutor(max_workers=threads) as executor:
                future_to_run = {executor.submit(
                    run_algorithm, algo_class, run): run for run in range(0, constants.NUM_RUNS)}
                for future in concurrent.futures.as_completed(future_to_run):
                    run = future_to_run[future]
                    try:
                        won, steps = future.result()
                        results.append((run, won, steps))
                    except Exception as exc:
                        print(f'Run {run} generated an exception: {exc}')
        else:
            for run in range(0, constants.NUM_RUNS):
                won, steps = run_algorithm(algo_class, run)
                results.append((run, won, steps))
        overall_results[algo] = results

    process_results(overall_results)
    return overall_results


def process_results(overall_results):
    dataframe = pandas.DataFrame(
        columns=["mean", "stddev", "min", "q.25", "median", "q.75", "max", "lost"])
    for algorithm in overall_results:
        current_results = overall_results[algorithm]
        steps_list = []
        fail_count = 0
        for run in current_results:
            steps_list.append(run[2])
            if run[1] is False:
                fail_count += 1
        dataframe.loc[algorithm] = [numpy.mean(steps_list), numpy.std(steps_list), numpy.amin(steps_list), numpy.quantile(steps_list, 0.25, interpolation='nearest'),
                                    numpy.median(steps_list), numpy.quantile(steps_list, 0.75, interpolation='nearest'), numpy.amax(steps_list), f"{(fail_count / constants.NUM_RUNS * 100):.2f}%"]

        print(dataframe)


if __name__ == "__main__":
    args = parse_args()

    if args.algorithm not in constants.ALGORITHM_LIST + ['ALL']:
        print(
            f"ERROR: Algorithm '{args.algorithm}' is not valid.\nSee help for list of valid algorithms.")
        exit(1)

    if args.visualize is True:
        if args.algorithm == 'ALL':
            print("ERROR: Cannot visualize all algorithms.\nUse -a/--algorithm and specify an algorithm to visualize.")
            exit(1)
        algo_class = import_algorithm(args.algorithm)
        run_algorithm(algo_class, visualize=True)
    else:
        benchmark_controller(args.algorithm, args.threads)
