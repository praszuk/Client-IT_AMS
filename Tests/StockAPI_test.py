from Controller.StockAPIController import StockAPIController as APIc
from Model.AssetModel import AssetStatus


def test_parser_hardware_data_200_ok(mocker):
    # Just part of response all is not needed
    response = {
        'total': 1,
        'rows': [
            {
                'id': 1,
                'asset_tag': 'tag',
                'name': 'Something',
                'serial': 'ABC120S028D',
                'status_label': {
                    'id': 1,
                    'name': 'Deployed',
                    'status_meta': 'deployed'
                },
                'model': {
                    'id': 1234,
                    'name': 'model_name'
                },
                'notes': 'NOTES'
            }
        ]
    }

    mock = mocker.MagicMock(return_value=response)

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        asset = APIc.parse_hardware_data(response['rows'][0]['serial'])

        assert asset.id == response['rows'][0]['id']
        assert asset.tag == response['rows'][0]['asset_tag']
        assert asset.name == response['rows'][0]['name']
        assert asset.serial_number == response['rows'][0]['serial']
        assert asset.status == AssetStatus.get_status(response['rows'][0]['status_label']['id'],
                                                      response['rows'][0]['status_label']['status_meta'])


def test_parser_hardware_data_200_not_found(mocker):
    serial_number = 'Not_important'
    response = {
        "total": 0,
        "rows": []
    }

    mock = mocker.MagicMock(return_value=response)

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        asset = APIc.parse_hardware_data(serial_number)

        assert asset.id == -1
        assert asset.name == ''
        assert asset.tag == ''
        assert asset.serial_number == serial_number
        assert asset.status == AssetStatus.ASSET_NOT_FOUND


def test_parser_hardware_data_401_unauthorized(mocker):
    serial_number = 'Not_important'
    response = {
        "status": "error",
        "message": "Unauthorized."
    }

    mock = mocker.MagicMock(return_value=response)

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        asset = APIc.parse_hardware_data(serial_number)

        assert asset.id == -1
        assert asset.name == ''
        assert asset.tag == ''
        assert asset.serial_number == serial_number
        assert asset.status == AssetStatus.STATUS_NOT_FOUND


def test_parser_hardware_data_404_endpoint_not_found(mocker):
    serial_number = 'Not_important'
    response = {
        "status": "error",
        "messages": "404 endpoint not found",
        "payload": None
    }

    mock = mocker.MagicMock(return_value=response)

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        asset = APIc.parse_hardware_data(serial_number)

        assert asset.id == -1
        assert asset.name == ''
        assert asset.tag == ''
        assert asset.serial_number == serial_number
        assert asset.status == AssetStatus.STATUS_NOT_FOUND


def test_parser_hardware_data_io_error_not_connected(mocker):
    serial_number = 'Not_important'

    mock = mocker.MagicMock(side_effect=IOError('IOError'))

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        asset = APIc.parse_hardware_data(serial_number)

        assert asset.id == -1
        assert asset.name == ''
        assert asset.tag == ''
        assert asset.serial_number == serial_number
        assert asset.status == AssetStatus.NOT_CONNECTED


def test_parser_hardware_key_error_api_problem(mocker):
    serial_number = 'Not_important'

    mock = mocker.MagicMock(side_effect=KeyError('API Problem'))

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        asset = APIc.parse_hardware_data(serial_number)

        assert asset.id == -1
        assert asset.name == ''
        assert asset.tag == ''
        assert asset.serial_number == serial_number
        assert asset.status == AssetStatus.STATUS_NOT_FOUND