from abc import ABC, abstractmethod


class IReportFormatter(ABC):
    @abstractmethod
    def format_report(self, report_data: dict[str, dict | str]) -> str:
        pass


class ConsolePayoutReportFormatter(IReportFormatter):
    def format_report(self, report_data: dict[str, dict | str]) -> str:

        total_hours = report_data.pop('total_hours')
        total_payout = report_data.pop('total_payout')

        department, employees = next(iter(report_data.items()))

        indent = '  '
        output = f'{indent}{department}\n'

        for name, info in employees.items():
            hours = info['hours']
            rate = info['rate']
            payout = info['payout']
            currency = '$'
            output += f'{indent}{'-'*14} {name:<20} {hours:>7} {rate:>7} {currency:>7}{payout}\n'

        output += f'{indent}{'':<14} {'':<20} {total_hours:>7} {currency:>15}{total_payout}\n'

        return output
