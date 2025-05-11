from argparse import ArgumentParser


class SetupCliParser:
    def __init__(self, description: str) -> None:
        self.parser = ArgumentParser(description=description)


    def parse(self) -> list[str]:
        self.parser.add_argument('files', 
                            metavar='CSV', 
                            nargs='+', 
                            help='files or paths to files, paths can be absolute or from the current directory'
        )
        self.parser.add_argument('--report', 
                            required=True, 
                            choices=['payout'], 
                            help='the name of the report to generate.'
        )
        self.parser.add_argument('--output', 
                            required=True, 
                            choices=['console', 'json'], 
                            help='report output format.'
        )

        return self.parser.parse_args()
