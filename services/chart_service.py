from __future__ import annotations

from statistics import mean


def build_chart_payload(payload: dict) -> dict:
    chart_type = payload.get("chartType", "bar")
    labels = payload.get("labels") or ["Q1", "Q2", "Q3", "Q4"]
    data = payload.get("data") or [24, 38, 57, 73]
    numeric_data = [float(item) for item in data if isinstance(item, (int, float))]

    return {
        "chartType": chart_type if chart_type in {"bar", "line", "pie"} else "bar",
        "labels": labels,
        "data": data,
        "analytics": {
            "average": round(mean(numeric_data), 2) if numeric_data else 0,
            "max": max(numeric_data) if numeric_data else 0,
            "min": min(numeric_data) if numeric_data else 0,
            "trend": "upward" if len(numeric_data) > 1 and numeric_data[-1] >= numeric_data[0] else "mixed",
        },
    }
