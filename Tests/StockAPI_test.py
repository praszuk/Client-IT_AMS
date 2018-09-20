import json

from Controller.StockAPIController import StockAPIController as APIc
from Model.AssetStatusModel import AssetStatus


def read_json(path):
    with open(path) as data:
        return json.load(data)


SINGLE_HARDWARE_FOUND = read_json('Resources/StockAPI_SingleHardwareFound.json')

SINGLE_MODEL_ID_FOUND = read_json('Resources/StockAPI_SingleModelIDFound.json')
MODEL_ID_DUPLICATED_FOUND = read_json('Resources/StockAPI_ModelIDDuplicatedFound.json')

SINGLE_CATEGORY_ID_FOUND = read_json('Resources/StockAPI_SingleCategoryIDFound.json')
CATEGORY_ID_FOUND_DUPLICATED = read_json('Resources/StockAPI_CategoryIDDuplicatedFound.json')

CATEGORY_CREATED = read_json('Resources/StockAPI_CategoryCreated.json')
CATEGORY_NOT_CREATED = read_json('Resources/StockAPI_CategoryNotCreated.json')

MODEL_CREATED = read_json('Resources/StockAPI_ModelCreated.json')


# MODEL_NOT_CREATED = read_json('Resources/StockAPI_ModelNotCreated.json')


def test_get_hardware_200_ok(mocker):
    # Just part of response all is not needed

    mock = mocker.MagicMock(return_value=SINGLE_HARDWARE_FOUND)

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        asset = APIc.get_hardware(SINGLE_HARDWARE_FOUND['rows'][0]['serial'])

        assert asset.id == SINGLE_HARDWARE_FOUND['rows'][0]['id']
        assert asset.tag == SINGLE_HARDWARE_FOUND['rows'][0]['asset_tag']
        assert asset.name == SINGLE_HARDWARE_FOUND['rows'][0]['name']
        assert asset.serial_number == SINGLE_HARDWARE_FOUND['rows'][0]['serial']
        assert asset.model_id == SINGLE_HARDWARE_FOUND['rows'][0]['model']['id']
        assert asset.model_name == SINGLE_HARDWARE_FOUND['rows'][0]['model']['name']
        assert asset.category_id == SINGLE_HARDWARE_FOUND['rows'][0]['category']['id']
        assert asset.category_name == SINGLE_HARDWARE_FOUND['rows'][0]['category']['name']
        assert asset.status == AssetStatus.get_status(SINGLE_HARDWARE_FOUND['rows'][0]['status_label']['id'],
                                                      SINGLE_HARDWARE_FOUND['rows'][0]['status_label']['status_meta'])


def test_get_hardware_200_not_found(mocker):
    serial_number = 'Not_important'
    response = {
        "total": 0,
        "rows": []
    }

    mock = mocker.MagicMock(return_value=response)

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        asset = APIc.get_hardware(serial_number)

        assert asset.id == -1
        assert asset.name == ''
        assert asset.tag == ''
        assert asset.model_id == -1
        assert asset.model_name == ''
        assert asset.serial_number == serial_number
        assert asset.category_id == -1
        assert asset.category_name == ''
        assert asset.status == AssetStatus.ASSET_NOT_FOUND


def test_get_hardware_401_unauthorized(mocker):
    serial_number = 'Not_important'
    response = {
        "status": "error",
        "message": "Unauthorized."
    }

    mock = mocker.MagicMock(return_value=response)

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        asset = APIc.get_hardware(serial_number)

        assert asset.id == -1
        assert asset.name == ''
        assert asset.tag == ''
        assert asset.model_id == -1
        assert asset.model_name == ''
        assert asset.category_id == -1
        assert asset.category_name == ''
        assert asset.serial_number == serial_number
        assert asset.status == AssetStatus.STATUS_NOT_FOUND


def test_get_hardware_404_endpoint_not_found(mocker):
    serial_number = 'Not_important'
    response = {
        "status": "error",
        "messages": "404 endpoint not found",
        "payload": None
    }

    mock = mocker.MagicMock(return_value=response)

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        asset = APIc.get_hardware(serial_number)

        assert asset.id == -1
        assert asset.name == ''
        assert asset.tag == ''
        assert asset.model_id == -1
        assert asset.model_name == ''
        assert asset.category_id == -1
        assert asset.category_name == ''
        assert asset.serial_number == serial_number
        assert asset.status == AssetStatus.STATUS_NOT_FOUND


def test_get_hardware_io_error_not_connected(mocker):
    serial_number = 'Not_important'

    mock = mocker.MagicMock(side_effect=IOError('IOError'))

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        asset = APIc.get_hardware(serial_number)

        assert asset.id == -1
        assert asset.name == ''
        assert asset.tag == ''
        assert asset.model_id == -1
        assert asset.model_name == ''
        assert asset.category_id == -1
        assert asset.category_name == ''
        assert asset.serial_number == serial_number
        assert asset.status == AssetStatus.NOT_CONNECTED


def test_parser_hardware_key_error_api_problem(mocker):
    serial_number = 'Not_important'

    mock = mocker.MagicMock(side_effect=KeyError('API Problem'))

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        asset = APIc.get_hardware(serial_number)

        assert asset.id == -1
        assert asset.name == ''
        assert asset.tag == ''
        assert asset.model_id == -1
        assert asset.model_name == ''
        assert asset.category_id == -1
        assert asset.category_name == ''
        assert asset.serial_number == serial_number
        assert asset.status == AssetStatus.STATUS_NOT_FOUND


def test_get_model_id_by_model_name_single(mocker):
    mock = mocker.MagicMock(return_value=SINGLE_MODEL_ID_FOUND)

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        model_id = APIc.get_model_id(SINGLE_MODEL_ID_FOUND['rows'][0]['name'])

        assert model_id == SINGLE_MODEL_ID_FOUND['rows'][0]['id']


def test_get_model_id_by_model_name_duplicated(mocker):
    mock = mocker.MagicMock(return_value=MODEL_ID_DUPLICATED_FOUND)

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        model_id = APIc.get_model_id(MODEL_ID_DUPLICATED_FOUND['rows'][2]['name'])

        assert model_id == MODEL_ID_DUPLICATED_FOUND['rows'][2]['id']


def test_get_model_id_by_model_name_not_found(mocker):
    mock = mocker.MagicMock(return_value={'total': 0, 'rows': []})

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        model_id = APIc.get_model_id('model_name')

        assert model_id == -1


def test_get_category_id_by_category_name_single(mocker):
    mock = mocker.MagicMock(return_value=SINGLE_CATEGORY_ID_FOUND)

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        category_id = APIc.get_category_id(SINGLE_CATEGORY_ID_FOUND['rows'][0]['name'])

        assert category_id == SINGLE_CATEGORY_ID_FOUND['rows'][0]['id']


def test_get_category_id_by_category_name_duplicated(mocker):
    mock = mocker.MagicMock(return_value=CATEGORY_ID_FOUND_DUPLICATED)

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        category_id = APIc.get_category_id(CATEGORY_ID_FOUND_DUPLICATED['rows'][2]['name'])

        assert category_id == CATEGORY_ID_FOUND_DUPLICATED['rows'][2]['id']


def test_get_category_id_by_category_name_not_found(mocker):
    mock = mocker.MagicMock(return_value={'total': 0, 'rows': []})

    with mocker.patch('Controller.StockAPIController.StockAPIController.get_data_from_api', mock):
        category_id = APIc.get_category_id('category_name')

        assert category_id == -1


def test_created_category(mocker):
    mock = mocker.MagicMock(return_value=CATEGORY_CREATED)

    with mocker.patch('Controller.StockAPIController.StockAPIController.create_data_at_api', mock):
        category_id = APIc.create_category('category_name')

        assert category_id == CATEGORY_CREATED['payload']['id']


def test_cannot_create_category(mocker):
    mock = mocker.MagicMock(return_value=CATEGORY_NOT_CREATED)

    with mocker.patch('Controller.StockAPIController.StockAPIController.create_data_at_api', mock):
        category_id = APIc.create_category('category_name')

        assert category_id == -1


def test_created_model_not_exists(mocker):
    create_data_at_api_mock = mocker.MagicMock(return_value=CATEGORY_CREATED)
    get_model_id_mock = mocker.MagicMock(return_value=-1)

    mocker.patch('Controller.StockAPIController.StockAPIController.create_data_at_api', create_data_at_api_mock)
    mocker.patch('Controller.StockAPIController.StockAPIController.get_model_id', get_model_id_mock)

    assert APIc.create_model(CATEGORY_CREATED['payload']['name'], 1, 1) == CATEGORY_CREATED['payload']['id']
    assert APIc.create_model(CATEGORY_CREATED['payload']['name'].upper(), 1, 1) == CATEGORY_CREATED['payload']['id']
    assert APIc.create_model(CATEGORY_CREATED['payload']['name'].lower(), 1, 1) == CATEGORY_CREATED['payload']['id']


def test_cannot_create_model_exists(mocker):
    create_data_at_api_mock = mocker.MagicMock(return_value=CATEGORY_CREATED)
    get_model_id_mock = mocker.MagicMock(return_value=CATEGORY_CREATED['payload']['id'])

    mocker.patch('Controller.StockAPIController.StockAPIController.create_data_at_api', create_data_at_api_mock)
    mocker.patch('Controller.StockAPIController.StockAPIController.get_model_id', get_model_id_mock)

    assert APIc.create_model(CATEGORY_CREATED['payload']['name'], 1, 1) == CATEGORY_CREATED['payload']['id']
