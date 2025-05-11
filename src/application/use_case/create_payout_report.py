from application.interface.temp_storage import ITempStorage
from application.interface.report_writer import IReportWriter
from application.interface.report_creator import IReportCreator


class ParserEmployeeRecords:
    def __init__(self) -> None:
        self.possible_salary_designations = ('rate', 
                                             'salary',
                                             'hourly_rate')
        self.employee_data = ('id', 'email',
                              'name', 'department',
                              'hours_worked')


    def process_for_report(self, employee_record: dict) -> tuple[str, dict]:
        for designation in self.possible_salary_designations:
            if designation in employee_record:

                rate = int(employee_record[designation])
                hours = int(employee_record['hours_worked'])
                payout = rate * hours
                return employee_record['department'], {employee_record['name']: {'hours': hours, 
                                                       			                 'rate': rate, 
                                                                                 'payout': payout}}
        else:
            raise ValueError('Формат файла не корректный для отчета "payout", проверьте файл/файлы на наличие ошибок.')


class PayoutReportCreator(IReportCreator):
    def __init__(self,
                 temp_storage: ITempStorage,
                 report_write: IReportWriter) -> None:

        self._temp_storage = temp_storage
        self._report_write = report_write
        self._parser_empl_records = ParserEmployeeRecords()


    def department_data_calculation(self, department_employees: dict) -> tuple[int, int]:
        total_hours = sum(department_employees[employee]['hours'] for employee in department_employees)
        total_payout = sum(department_employees[employee]['payout'] for employee in department_employees)
        return total_hours, total_payout


    async def create(self) -> None:
        part_report = {}

        async with self._temp_storage as temp_storage:
            employee_records = temp_storage.read(group_by='department')

            record = await anext(employee_records)
            department, employee_record = self._parser_empl_records.process_for_report(record)
            part_report[department] = employee_record

            async with self._report_write as report_write:

                async for record in employee_records:
                    department, employee_record = self._parser_empl_records.process_for_report(record)

                    if department in part_report:
                        part_report[department].update(employee_record)
                    else:
                        current_department = next(iter(part_report))
                        total_hours, total_payout = self.department_data_calculation(part_report[current_department])
                        part_report['total_hours'] = total_hours
                        part_report['total_payout'] = total_payout
                        await report_write.write_part(part_report)
                        part_report = {}
                        part_report[department] = employee_record

                if part_report:
                    total_hours, total_payout = self.department_data_calculation(part_report[department])
                    part_report['total_hours'] = total_hours
                    part_report['total_payout'] = total_payout
                    await report_write.write_part(part_report)
