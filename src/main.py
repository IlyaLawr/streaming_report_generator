from sys import exit
from asyncio import run

from settings import Setting

from infrastructure.csv_file_reader import AiofilesAsyncFileReader
from infrastructure.sqlite_storage import SQLTempStorage
from infrastructure.json_file_write import JSONWriter

from application.interface.report_creator import IReportCreator
from application.interface.temp_storage import ITempStorage
from application.services.file_collector import FileCollectorServices
from application.services.data_aggregation import DataAggregationService
from application.use_case.create_payout_report import PayoutReportCreator
from application.use_case.processing_report_request import ProcessingReportRequest

from presentation.printers import ConsoleWriter
from presentation.formatters import ConsolePayoutReportFormatter
from presentation.cli import SetupCliParser


def report_factory(output_format: str, 
                   report_name: str,
                   temp_storage: ITempStorage,
                   file_report_name: str | None = None) -> IReportCreator:

    if report_name == 'payout':
        if output_format == 'json':
                return PayoutReportCreator(temp_storage=temp_storage,
                                           report_write=JSONWriter(f'{file_report_name}.json'))
        elif output_format == 'console':
            return PayoutReportCreator(temp_storage=temp_storage,
                                       report_write=ConsoleWriter(formatter=ConsolePayoutReportFormatter()))
        else:
            raise ValueError(f'Не поддерживаемый формат "{output_format}" или тип отчета "{report_name}"')


async def main():
    cli_parser = SetupCliParser('Generating reports.')

    try:
        args = cli_parser.parse()
    except SystemExit:
        print('\n-----Incorrect data, please read the help information and try again.-----\n')
        cli_parser.parser.print_help()
        exit(1)

    setting = Setting()

    file_collector = FileCollectorServices(base_dir=setting.base_dir, file_format=setting.file_format)
    file_reader = AiofilesAsyncFileReader()
    temp_storage = SQLTempStorage(setting.db_path, args.report.title())
    data_aggregation = DataAggregationService(file_reader=file_reader,
                                              temp_storage=temp_storage)

    report_creator = report_factory(output_format=args.output,
                                    report_name=args.report,
                                    temp_storage=temp_storage,
                                    file_report_name=args.report_name)

    processing_report_request = ProcessingReportRequest(file_collector=file_collector,
                                                        data_aggregation=data_aggregation,
                                                        temp_storage=temp_storage,
                                                        report_creator=report_creator)


    await processing_report_request.generate_report(args.files)


if __name__ == "__main__":
    run(main())
