from application.interface.temp_storage import ITempStorage
from application.interface.report_creator import IReportCreator
from application.services.file_collector import FileCollectorServices
from application.services.data_aggregation import DataAggregationService


class ProcessingReportRequest:
    def __init__(self, 
                 file_collector: FileCollectorServices,
                 data_aggregation: DataAggregationService,
                 temp_storage: ITempStorage,
                 report_creator: IReportCreator) -> None:
        
        self._file_collector = file_collector
        self._data_aggregation = data_aggregation
        self._temp_storage = temp_storage
        self._report_creator = report_creator


    async def generate_report(self, file_data: list[str]) -> None:
        file_paths = self._file_collector.collect(file_data)
        result = await self._data_aggregation.aggregate(file_paths)
        if result:
            await self._report_creator.create()
        else:
            raise ValueError('Возникла ошибка при формировании отчета, проверьте исходные файлы.')
