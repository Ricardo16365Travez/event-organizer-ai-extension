def optimize_spaces(events):
    # Lógica de optimización
    optimized_schedule = sorted(events, key=lambda x: x.date)
    return optimized_schedule
