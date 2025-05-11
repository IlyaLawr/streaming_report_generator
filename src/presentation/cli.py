from argparse import ArgumentParser, Action, Namespace


class OutputAction(Action):
    def __call__(self,
                 parser: ArgumentParser,
                 namespace: Namespace,
                 value: str,
                 option: str | None = None):

        setattr(namespace, self.dest, value)

        for action in parser._actions:
            if action.dest == 'report_name':
                action.required = (value == 'json')


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
                            action=OutputAction,
                            help='report output format.'
        )
        self.parser.add_argument('--report-name',
                            dest='report_name',
                            help='report name if save to file mode is selected'
        )

        return self.parser.parse_args()
