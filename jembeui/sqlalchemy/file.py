import sqlalchemy as sa
from flask import json
from jembe import File

__all__ = ("SaFile",)


class SaFile(sa.TypeDecorator):
    impl = sa.VARCHAR
    cache_ok = True

    def coerce_compared_value(self, op, value):
        if op in (sa.sql.operators.like_op, sa.sql.operators.notlike_op):
            return sa.String()
        return self

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(File.dump_init_param(value))
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = File.load_init_param(json.loads(value))
        return value

