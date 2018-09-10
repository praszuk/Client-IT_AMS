import json

from Controller.ProductAPIController import APIController as APIc
from Model.AssetModel import AssetStatus


def read_json(path):
    with open(path) as data:
        return json.load(data)


api = APIc()
single_product = read_json('Resources/ProductAPI_SingleProductFound.json')


def test_parser_product_data_single_product_found_200_ok(mocker):
    mock = mocker.MagicMock(return_value=single_product)
    with mocker.patch('Controller.ProductAPIController.APIController.get_data_from_api', mock):
        asset = api.parse_product_data(single_product['product_list'][0]['sr_no'])

        assert asset.get_id() == -1
        assert asset.get_asset_tag() == single_product['product_list'][0]['sr_no']
        assert asset.get_name() == single_product['product_list'][0]['base_pid']
        assert asset.get_serial_number() == single_product['product_list'][0]['sr_no']
        assert asset.get_status() == AssetStatus.READY_TO_ADD
