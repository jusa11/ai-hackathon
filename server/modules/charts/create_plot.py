import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use("Agg")  


def plot_metric(result: dict, title="График", kind="bar") -> str:
    """Строит график из словаря и возвращает base64."""
    x = list(result.keys())
    y = list(result.values())

    plt.figure(figsize=(8, 5))
    if kind == "bar":
        plt.bar(x, y)
    elif kind == "line":
        plt.plot(x, y, marker='o')
    elif kind == "pie":
        plt.pie(y, labels=x, autopct='%1.1f%%')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')
