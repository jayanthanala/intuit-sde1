"""
Pretty-print helpers for analysis results.
"""


def _header(title: str):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_kv_dict(title, d):
    _header(title)
    for k, v in d.items():
        print(f"{k:20} {v:10.2f}")


def print_top_products(title, items):
    _header(title)
    for name, rev in items:
        print(f"{name:30} {rev:12.2f}")


def print_salesperson_summary(perf_map, top: int = 5):
    """
    Print top-N salespeople by total revenue.
    """
    _header(f"Top {top} Salespeople by Performance")

    ranked = sorted(
        perf_map.items(),
        key=lambda item: item[1]["total_revenue"],
        reverse=True,
    )[:top]

    for sp, stats in ranked:
        print(
            f"{sp:12} "
            f"rev={stats['total_revenue']:.2f}  "
            f"orders={stats['orders']:3d}  "
            f"customers={stats['customers']:3d}  "
            f"regions={stats['regions']:2d}  "
            f"eff_disc={stats['effective_discount']*100:5.1f}%"
        )
