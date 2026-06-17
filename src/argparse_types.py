import argparse


class CustomFormatter(
    argparse.RawTextHelpFormatter,
    argparse.ArgumentDefaultsHelpFormatter
):
    pass


def int_range(imin, imax):
    def parse(value):
        n = int(value)
        if n < imin:
            raise argparse.ArgumentTypeError(f"value less than {imin}")
        if n > imax:
            raise argparse.ArgumentTypeError(f"value greater than {imax}")
        return n
    return parse


def str_except(invalid_set):
    def parse(value):
        for c in invalid_set:
            if c in value:
                raise argparse.ArgumentTypeError(f"invalid character")
        return value
    return parse
