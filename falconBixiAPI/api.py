import falcon
import json
from connect import connect


class getStationOccupancy:
    """ 
    This Class is implemented to return product information
    """
    def on_put(self, req, resp, id):
        try:
            connect = connect()
            content = connect.productInformation()
            if content:
                resp.body = json.dumps(content)
                resp.content_type = falcon.MEDIA_JSON
                resp.status = falcon.HTTP_200
            else:
                resp.content_type = falcon.MEDIA_JSON
                resp.status = falcon.HTTP_400

        except falcon.HTTPInvalidHeader as e:
            resp.body = str(e)
            resp.status = falcon.HTTP_404

            

api = application = falcon.API()
api.add_route('/getStationOccupancy/{date}/}{day}/{hour}/{short_name}/', getStationOccupancy())
