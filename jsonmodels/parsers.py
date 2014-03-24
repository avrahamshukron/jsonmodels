"""Parsers to change model structure into different one."""

from . import fields


def to_struct(model):
    """Cast instance of model to python structure.

    :param model: Model to be casted.
    :rtype: ``dict``

    """
    try:
        model.validate()
    except AttributeError:
        return model

    resp = {}
    for name, value in model:
        if value is None:
            continue

        if isinstance(value, list):
            resp[name] = [to_struct(item) for item in value]
        else:
            resp[name] = to_struct(value)
    return resp


def to_json_schema(model):
    """Generate JSON schema for given instance of model.

    :param model: Model to be casted.
    :rtype: ``dict``

    """

    resp = {
        'type': 'object',
        'additionalProperties': False,
    }

    prop = {}
    for name, _ in model:
        field = model.get_field(name)
        if isinstance(field, fields.StringField):
            prop[name] = {'type': 'string'}
        elif isinstance(field, fields.IntField):
            prop[name] = {'type': 'integer'}
        elif isinstance(field, fields.FloatField):
            prop[name] = {'type': 'float'}
    resp['properties'] = prop

    return resp
