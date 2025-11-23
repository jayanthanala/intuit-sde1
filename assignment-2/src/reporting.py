"""
Pretty-print helpers for analysis results.

Example outputs showing formatted data display:
  - print_kv_dict: Region/Category revenue tables
  - print_top_products: Top N products ranked by revenue
  - print_salesperson_summary: Salesperson leaderboard with metrics
"""


def _header(title: str):
    """Print section header with divider lines."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_kv_dict(title, d):
    """Print key-value dict as aligned table.
    
    Example output:
      ============================================================
      Revenue by Region
      ============================================================
      East                    xxxxx.xxx
      North                   xxxx.xxx
      South                   xxxxx.xxx
      West                     xxxx.xxx
      
    Raises:
        TypeError: If d is not a dict
        ValueError: If d is empty
    """
    if not isinstance(d, dict):
        raise TypeError(f"Expected dict, got {type(d).__name__}")
    if not d:
        raise ValueError("Cannot print empty dictionary")
    
    _header(title)
    for k, v in d.items():
        try:
            print(f"{k:20} {v:10.2f}")
        except (ValueError, TypeError) as e:
            print(f"{k:20} {str(v):>10} (formatting error)")


def print_top_products(title, items):
    """Print top products as ranked list.
    
    Input: [('Laptop Pro 15', 9876.54), ('Conference Table', 1103.65), ...]
    Output:
      ============================================================
      Top 5 Products by Revenue
      ============================================================
      xxxxxxxxxxxxxxxxx                       xxxx.xxx
      xxxxxxxxxxxxxxxxx                   xxxx.xxx
      xxxxxxxxxxxxxxxxx                       xxxx.xxx
      xxxxxxxxxxxxxxxxx                 xxxx.xxx
      xxxxxxxxxxxxxxxxx                      xxxx.xxx
      
    Raises:
        TypeError: If items is not iterable
        ValueError: If items is empty or malformed
    """
    if not hasattr(items, '__iter__'):
        raise TypeError(f"Expected iterable, got {type(items).__name__}")
    
    items_list = list(items)
    if not items_list:
        raise ValueError("Cannot print empty product list")
    
    _header(title)
    for item in items_list:
        try:
            name, rev = item
            print(f"{name:30} {rev:12.2f}")
        except (ValueError, TypeError) as e:
            print(f"Error formatting item {item}: {e}")


def print_salesperson_summary(perf_map, top: int = 5):
    """Print top-N salespeople by total revenue with all metrics.
    
    Input: {'Alice Johnson': {'total_revenue': 12345.67, 'orders': 25, ...}, ...}
    
    Process:
      1. Sort by total_revenue descending
      2. Take top N salespeople
      3. Format each with all metrics on one line
    
    Example output:
      ============================================================
      Top 5 Salespeople by Performance
      ============================================================
      Alice Johnson  rev=12345.67  orders= 25  customers= 22  regions= 4  eff_disc= 9.8%
      Bob Smith      rev=10234.56  orders= 23  customers= 21  regions= 4  eff_disc= 7.2%
      Carol Davis    rev= 9876.54  orders= 21  customers= 19  regions= 3  eff_disc= 5.4%
      David Lee      rev= 8765.43  orders= 20  customers= 18  regions= 4  eff_disc= 8.1%
      
    Raises:
        TypeError: If perf_map is not a dict or top is not an int
        ValueError: If perf_map is empty or top is invalid
    """
    if not isinstance(perf_map, dict):
        raise TypeError(f"Expected dict, got {type(perf_map).__name__}")
    if not perf_map:
        raise ValueError("Cannot print empty performance map")
    if not isinstance(top, int) or top <= 0:
        raise ValueError(f"top must be a positive integer, got {top}")
    
    _header(f"Top {top} Salespeople by Performance")

    # Sort by revenue descending, take top N
    try:
        ranked = sorted(
            perf_map.items(),
            key=lambda item: item[1]["total_revenue"],
            reverse=True,
        )[:top]
    except (KeyError, TypeError) as e:
        raise ValueError(f"Invalid performance data structure: {e}")

    for sp, stats in ranked:
        print(
            f"{sp:12} "
            f"rev={stats['total_revenue']:.2f}  "
            f"orders={stats['orders']:3d}  "
            f"customers={stats['customers']:3d}  "
            f"regions={stats['regions']:2d}  "
            f"eff_disc={stats['effective_discount']*100:5.1f}%"
        )
