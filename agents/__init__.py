__all__ = ["SentinelAuditAgent", "PhantomForecastAgent"]


def __getattr__(name):
    if name == "SentinelAuditAgent":
        from .sentinel_audit_agent import SentinelAuditAgent
        return SentinelAuditAgent
    if name == "PhantomForecastAgent":
        from .phantom_forecast_agent import PhantomForecastAgent
        return PhantomForecastAgent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
