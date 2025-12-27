import uuid
from datetime import datetime


def log_metric(metrics: list, metric_data: dict) -> dict:
    m_id = "m_" + str(uuid.uuid4())[:8]
    date = metric_data.get("date", datetime.now().strftime("%Y-%m-%d"))

    new_metric = {
        "id": m_id,
        "user_id": metric_data["user_id"],
        "date": date,
        "weight": float(metric_data.get("weight", 0)),
        "water": float(metric_data.get("water", 0)),
        "sleep": float(metric_data.get("sleep", 0)),
        "mood": metric_data.get("mood", "Neutral")
    }
    metrics.append(new_metric)
    return new_metric


def metrics_summary(metrics: list, user_id: str, metric_type: str, period: tuple) -> dict:
    start_date, end_date = period
    values = []

    for m in metrics:
        if m["user_id"] == user_id:
            m_date = m.get("date")
            if start_date <= m_date <= end_date:
                val = m.get(metric_type, 0)
                values.append(val)

    if not values:
        return {"average": 0, "min": 0, "max": 0, "count": 0}

    return {
        "metric": metric_type,
        "average": sum(values) / len(values),
        "min": min(values),
        "max": max(values),
        "count": len(values)
    }


def goal_progress(users: list, metrics: list, user_id: str) -> dict:
    target_weight = 0
    start_weight = 0

    for u in users:
        if u["id"] == user_id:
            goals = u.get("goals", {})
            target_weight = goals.get("target_weight", 0)
            start_weight = u.get("weight_kg", 0)
            break

    user_metrics = [m for m in metrics if m["user_id"] == user_id]
    user_metrics.sort(key=lambda x: x["date"], reverse=True)

    current_weight = user_metrics[0]["weight"] if user_metrics else start_weight

    diff = current_weight - target_weight
    status = ""
    if target_weight == 0:
        status = "No target set"
    elif diff > 0:
        status = f"{abs(diff):.1f} kg to lose"
    elif diff < 0:
        status = f"{abs(diff):.1f} kg to gain"
    else:
        status = "Target Reached"

    return {
        "current_weight": current_weight,
        "target_weight": target_weight,
        "status": status
    }


def generate_ascii_chart(values: list) -> str:
    if not values:
        return "No data for chart."

    max_val = max(values) if values else 1
    min_val = min(values) if values else 0
    range_val = max_val - min_val if max_val != min_val else 1

    lines = []
    for v in values:
        normalized = (v - min_val) / range_val
        bar_len = int(normalized * 20)
        lines.append(f"{v:6.1f} | {'*' * bar_len}")

    return "\n".join(lines)