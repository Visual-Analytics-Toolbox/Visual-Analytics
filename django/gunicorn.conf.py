import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

def post_fork(server, worker):
    # This forces the IDs to be available in every worker log
    LoggingInstrumentor().instrument(set_logging_format=True)
    DjangoInstrumentor().instrument()