from Controller.APIController import APIController as APIc
from Model.AssetModel import AssetStatus


def test_parser_hardware_data_200_ok(mocker):
    # Just part of response all is not needed
    response = {
        'total': 1,
        'rows': [
            {
                'id': 1,
                'name': 'Something',
                'serial': 'ABC120S028D',
                'status_label': {
                    'id': 1,
                    'name': 'Deployed',
                    'status_meta': 'deployed'
                }
            }
        ]
    }

    mock = mocker.MagicMock(return_value=response)

    with mocker.patch('Controller.APIController.APIController.get_data_from_api', mock):
        asset = APIc.parse_hardware_data(response['rows'][0]['serial'])

        assert asset.get_id() == response['rows'][0]['id']
        assert asset.get_name() == response['rows'][0]['name']
        assert asset.get_serial_number() == response['rows'][0]['serial']
        assert asset.get_status() == AssetStatus.get_status(response['rows'][0]['status_label']['id'],
                                                            response['rows'][0]['status_label']['status_meta'])
