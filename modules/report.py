from modules.database import connect

def get_violations():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, image, result, confidence, timestamp
        FROM violations
        ORDER BY id DESC
    """)

    data = cur.fetchall()

    conn.close()

    return data


# FILTER BY DATE
def get_filtered_violations(start, end):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, image, result, confidence, timestamp
        FROM violations
        WHERE DATE(timestamp) BETWEEN ? AND ?
        ORDER BY id DESC
    """, (start, end))

    data = cur.fetchall()

    conn.close()

    return data


# DASHBOARD STATS
def get_violation_stats():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT result, COUNT(*)
        FROM violations
        GROUP BY result
    """)

    rows = cur.fetchall()

    conn.close()

    stats = {
        "Mask": 0,
        "No Mask": 0
    }

    for r in rows:

        stats[r[0]] = r[1]

    return stats


# CHART DATA
def get_chart_data():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT result, COUNT(*)
        FROM violations
        GROUP BY result
    """)

    result_data = cur.fetchall()

    cur.execute("""
        SELECT DATE(timestamp), COUNT(*)
        FROM violations
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp)
    """)

    daily_data = cur.fetchall()

    conn.close()

    return result_data, daily_data