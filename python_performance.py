import argparse
import logging
import sys
import time
from collections import namedtuple
from typing import Dict, List, Set


def main():
    logger = init_logging()
    args = init_cli()

    loops = args.iterations

    logger.info("Python {}\n".format(sys.version))
    logger.info("Starting performance tests...")
    logger.info("Using size: {}".format(loops))
    mylist: List[MySlots] = []
    instantiating_objects_with_slots(mylist, loops)
    accessing_attributes_with_slots(mylist)

    mylist: List[namedtuple] = []
    instantiating_namedtuples(mylist, loops)
    accessing_attributes_with_namedtuples(mylist)


def init_logging() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    logger.setLevel(logging.INFO)
    return logger


def init_cli():
    parser = argparse.ArgumentParser(description="Test speed of Python data containers.")
    parser.add_argument(
        "--iterations",
        default=10000,
        help="Size of data containers to use for speed test",
        type=int,
    )
    return parser.parse_args()


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            print("%r  %2.2f ms" % (method.__name__, (te - ts) * 1000))
        return result

    return timed


class MySlots(object):
    __slots__: ["x", "y", "z"]

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


@timeit
def instantiating_objects_with_slots(input_list: List[MySlots], count: int) -> None:
    for x in range(count):
        input_list.append(MySlots("x", "y", "z"))


@timeit
def accessing_attributes_with_slots(input_list: List[MySlots]) -> None:
    for x in range(len(input_list)):
        input_list[x].x


@timeit
def instantiating_namedtuples(input_list: List, count: int) -> None:
    Point = namedtuple("Point", ["x", "y", "z"])
    for x in range(count):
        input_list.append(Point("x", "y", "z"))


@timeit
def accessing_attributes_with_namedtuples(input_list: List) -> None:
    for x in range(len(input_list)):
        input_list[x].x


if __name__ == "__main__":
    main()
