import argparse
from algorithm import replicate

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-a', "--asset", type=float,
                        help="Close Price of the Asset today")

    # parser.add_argument('-o', "--option", type=float,
                        # help="Close Price of the Option today")

    parser.add_argument('-d', "--delta", type=float,
                        help="Close Delta of the Option today")

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity", default=False)

    parser.add_argument("-m", "--mode",
                        help="prod or test", default='prod', choices=['prod', 'test'])


    args = parser.parse_args()

    replicate(
            args.asset,
            # args.option,
            args.delta,
            args.verbose,
            args.mode,
            )


