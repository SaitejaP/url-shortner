'''Utility funcitons for the project'''


def get_response(status, data=None, message=None):
    return {
        'status': status,
        'data': data,
        'message': message
    }
