def status_with_icon(status):
    status_map = {
        "Ready to Deploy": "✅ Ready",
        "Deployed": "⬆️ Deployed",
        "Broken": "💥 Broken",
        "Archived": "🗃️ Archived",
        "Checked Out": "⬆️ Checked Out",
        "Lost/Stolen": "🚫 Lost/Stolen",
        "Pending": "⏳ Pending"
    }

    return status_map.get(status, status)
