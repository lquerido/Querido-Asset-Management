# view_config.py or top of your main app
VIEW_STRUCTURE = {
    "Performance Summary": ["PM Update", "Performance Analytics"],
    "Detailed Investment Performance Analysis": [
        "Trade-by-Trade Analysis",
        "Time-Weighted Returns",
        "Portfolio Composition",
        "Portfolio Holdings",
        "Portfolio Risk",
        "Attribution Analysis",
        "Performance Factors"  # e.g. turnover, win ratio, etc.
    ],
    "Investment Research": ["Macro", "Equities"],
    "About Us": ["About", "Our Strategies", "Dashboard Logic"]
}

VIEW_MODULES = {
    "Performance Summary": "views.performance_summary",
    "Detailed Investment Performance Analysis": "views.detailed_analysis",
    "Investment Research": "views.investment_research",
    "About Us": "views.about_us"
}
