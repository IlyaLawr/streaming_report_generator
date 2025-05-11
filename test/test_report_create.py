from pytest import mark
from unittest.mock import call, MagicMock

from application.use_case.create_payout_report import ParserEmployeeRecords, PayoutReportCreator
from application.use_case.create_payout_report import PayoutReportCreator

from conftest import mock_report_writer, mock_temp_storage


#-------------------------------------------------------------------------------------#
employee_record = {1: {'id': '1', 
             	       'email': 'alice@example.com',
             	       'name': 'Alice Johson',
                       'department': 'Marketing',
                       'hours_worked': '160',
                       'hourly_rate': '50'},

	               2: {'id': '32',
		               'email': 'bob@example.ru',
                       'name': 'Bob Makarti',
                       'department': 'Developers',
                       'hours_worked': '1000',
                       'salary': '2'},

	               3: {'id': '76',
		               'email': 'grisha@example.ru',
                       'name': 'Grisha Bikini',
                       'department': 'Europa',
                       'hours_worked': '222',
                       'rate': '3'}
}

expected = {1: ('Marketing', {'Alice Johson': {'hours': 160, 'rate': 50, 'payout': 8000}}),
	        2: ('Developers', {'Bob Makarti': {'hours': 1000, 'rate': 2, 'payout': 2000}}),
            3: ('Europa', {'Grisha Bikini': {'hours': 222, 'rate': 3, 'payout': 666}})
}

@mark.parametrize("employee_record,expected", 
                 [(employee_record[1], expected[1]),
			      (employee_record[2], expected[2]),
			      (employee_record[3], expected[3])]
)
def test_process_for_report(employee_record, expected):
    parser = ParserEmployeeRecords()
    assert parser.process_for_report(employee_record) == expected
#-------------------------------------------------------------------------------------#


#-------------------------------------------------------------------------------------#
employee_record = {'Alice Johson': {'hours': 160, 'rate': 50, 'payout': 8000},
                   'Silvestr Pididi': {'hours': 1000, 'rate': 2, 'payout': 2000},
	               'Ururu Lolov' : {'hours': 999, 'rate': 73, 'payout': 100}
}

expected = (2159, 10100)

@mark.parametrize("employee_record,expected", 
                 [(employee_record, expected)]
)
def test_department_data_calculation(employee_record, 
                                     expected, 
                                     mock_temp_storage, 
                                     mock_report_writer):

    payout_report_creator = PayoutReportCreator(temp_storage=mock_temp_storage,
						                        report_write=mock_report_writer)

    assert payout_report_creator.department_data_calculation(employee_record) == expected
#-------------------------------------------------------------------------------------#


#-------------------------------------------------------------------------------------#
employee_record = {1: {'id': '1', 
             	       'email': 'alice@example.com',
             	       'name': 'Alice Johson',
                       'department': 'Marketing',
                       'hours_worked': '160',
                       'rate': '50'},

	               2: {'id': '333',
                       'email': 'sil_pid@example.ru',
                       'name': 'Silvestr Pididi',
                       'department': 'Marketing',
                       'hours_worked': '1000',
                       'rate': '2'},
                       
	               3: {'id': '7891',
		               'email': 'grisha222@example.ru',
                       'name': 'Lay Sobak',
                       'department': 'Budka',
                       'hours_worked': '0',
                       'salary': '0'},

	               4: {'id': '0',
		               'email': '1@example.ru',
                       'name': 'Kot Ashot',
                       'department': 'Budka',
                       'hours_worked': '9999999',
                       'salary': '-1'}                     
}

expected = {1: {'Marketing': {'Alice Johson': {'hours': 160, 'rate': 50, 'payout': 8000},
                              'Silvestr Pididi': {'hours': 1000, 'rate': 2, 'payout': 2000}},
                             'total_hours': 1160, 
                             'total_payout': 10000},

            2: {'Budka': {'Lay Sobak': {'hours': 0, 'rate': 0, 'payout': 0},
                          'Kot Ashot': {'hours': 9999999, 'rate': -1, 'payout': -9999999}},
                         'total_hours': 9999999, 
                         'total_payout': -9999999}
}


@mark.asyncio
async def test_create_report(mock_temp_storage, mock_report_writer):

    async def mock_records():
        for i in range(1, 5):
            yield employee_record[i]

    mock_temp_storage.read = MagicMock(return_value=mock_records())

    payout_report_creator = PayoutReportCreator(temp_storage=mock_temp_storage,
						                        report_write=mock_report_writer)

    await payout_report_creator.create()
    
    mock_temp_storage.read.assert_called_once()
    mock_report_writer.write_part.assert_has_awaits([call(expected[1]), call(expected[2])])
#-------------------------------------------------------------------------------------#
