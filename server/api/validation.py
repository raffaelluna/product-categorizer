from marshmallow import Schema, fields
from marshmallow import ValidationError

class InvalidEnputError(Exception):
    """Invalid model input."""
    
class ProductCategorizerRequestSchema(Schema):
    product_id = fields.Integer(allow_none=False)
    seller_id = fields.Integer(allow_none=False)
    query = fields.String(allow_none=False)
    search_page = fields.Integer(allow_none=False)
    position = fields.Integer(allow_none=False)
    title = fields.String(allow_none=False)
    concatenated_tags = fields.String(allow_none=False)
    creation_date = fields.String(allow_none=False)
    price = fields.Float(allow_none=False)
    weight = fields.Float(allow_none=False)
    express_delivery = fields.Integer()
    minimum_quantity = fields.Integer()
    view_counts = fields.Integer(allow_none=False)
    order_counts = fields.Float(allow_none=True)
    category = fields.String()
    
def validate_input(data):
    
    schema = ProductCategorizerRequestSchema(many=True)
    
    errors = None
    try:
        schema.load(data)
    except ValidationError as exc:
        errors = exc.messages
        print(errors)  
    
    validated_data = data
    
    return validated_data, errors