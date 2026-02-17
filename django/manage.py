#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.development")

    # --- ADD THIS BLOCK START ---
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.instrumentation.django import DjangoInstrumentor
        from opentelemetry.instrumentation.logging import LoggingInstrumentor
        from opentelemetry.sdk.resources import SERVICE_NAME, Resource
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

        otlp_exporter = OTLPSpanExporter(
            endpoint="http://alloy.alloy.svc.cluster.local:4317", 
            insecure=True
        )

        resource = Resource(attributes={SERVICE_NAME: "django-api"})
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        trace.set_tracer_provider(provider)

        # Instrument BEFORE Django starts
        LoggingInstrumentor().instrument(set_logging_format=True)
        DjangoInstrumentor().instrument()
        print("OTel: Instrumentation successful")
    except Exception as e:
        print(f"OTel: Instrumentation failed: {e}")
    # --- ADD THIS BLOCK END ---


    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
