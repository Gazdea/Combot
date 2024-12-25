import logging
import wrapt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_execution(func):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        class_name = instance.__class__.__name__ if instance else 'Global'
        logger.info(f"Calling {class_name}.{wrapped.__name__} with args: {args}, kwargs: {kwargs}")
        result = wrapped(*args, **kwargs)
        logger.info(f"{class_name}.{wrapped.__name__} returned {result}")
        return result
    return wrapper(func)

def log_class(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and not attr_name.startswith('__'):
            setattr(cls, attr_name, log_execution(attr_value))
    return cls