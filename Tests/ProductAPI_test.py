import json

from Controller.ProductAPIController import ProductAPIController as APIc
from Model.AssetStatusModel import AssetStatus


def read_json(path):
    with open(path) as data:
        return json.load(data)


api = APIc()
single_product = read_json('Resources/ProductAPI_SingleProductFound.json')
duplication_products = read_json('Resources/ProductAPI_ProductDuplicatedFound.json')
product_not_found = read_json('Resources/ProductAPI_ProductNotFound.json')


def test_parser_product_data_single_product_found_200_ok(mocker):
    mock = mocker.MagicMock(return_value=single_product)
    with mocker.patch('Controller.ProductAPIController.ProductAPIController.get_data_from_api', mock):
        asset = api.parse_product_data(single_product['product_list'][0]['sr_no'])

        assert asset.id == -1
        assert asset.tag == single_product['product_list'][0]['sr_no']
        assert asset.name == single_product['product_list'][0]['base_pid']
        assert asset.serial_number == single_product['product_list'][0]['sr_no']
        assert asset.status == AssetStatus.READY_TO_ADD


def test_parser_product_data_duplication_products_found_200_ok(mocker):
    mock = mocker.MagicMock(return_value=duplication_products)
    with mocker.patch('Controller.ProductAPIController.ProductAPIController.get_data_from_api', mock):
        asset = api.parse_product_data(single_product['product_list'][0]['sr_no'])

        assert asset is None


def test_parser_product_data_not_found_200_ok(mocker):
    mock = mocker.MagicMock(return_value=product_not_found)
    with mocker.patch('Controller.ProductAPIController.ProductAPIController.get_data_from_api', mock):
        asset = api.parse_product_data(single_product['product_list'][0]['sr_no'])

        assert asset is None


def test_parser_product_data_api_error_403(mocker):
    responses = ['Forbidden', 'Not Authorized', 'Account Inactive', 'Account Over Queries Per Second Limit',
                 'Account Over Rate Limit', 'Rate Limit Exceeded']

    for response in responses:
        mock = mocker.MagicMock(return_value=response)
        with mocker.patch('Controller.ProductAPIController.ProductAPIController.get_data_from_api', mock):
            asset = api.parse_product_data('serial_number')

            assert asset is None
