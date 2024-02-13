import argparse


class VerbositySelection():
    def __init__(self, selected_verbosity):
        self.__v = selected_verbosity

    V = {"full_display_ident":    1,
         "all_display_modes":     1,
         "available_full_config": 1,
         "picked_full_config":    1,
         "setups_unavailable":    2}

    @property
    def v(self):
        return self.__v

    def __getattr__(self, attr):
        try:
            return self.v >= self.V[attr]
        except KeyError:
            raise AttributeError(f"unknown verbosity-level: {attr}")


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description="Display placer")
    parser.add_argument("selection", nargs='?')
    parser.add_argument("-a", "--auto", action="store_true",
                        help="try to pick a good choice")
    parser.add_argument("-f", "--fallback", action="store_true",
                        help="add a screen-maxing fallback configuration")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help=("show additional diagnostic and info "
                              "(use multiple times to increase further)"))
    parser.add_argument("-d", "--dry", action="store_true",
                        help="only show what would be executed")
    args = parser.parse_args(args=argv)

    return args, VerbositySelection(args.verbose)
