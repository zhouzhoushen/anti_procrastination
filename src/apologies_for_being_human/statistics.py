from apologies_for_being_human.db import connect_db


def get_checkin_task_statistics():
    """Get statistics for check-in tasks, including task names"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ct.checkin_task_name, 
               COUNT(c.checkin_record_id) as total_checkins, 
               SUM(CASE WHEN c.success = 1 THEN 1 ELSE 0 END) as completed_checkins,
               (SUM(CASE WHEN c.success = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(c.checkin_record_id)) as completion_rate
        FROM checkin_tasks ct
        LEFT JOIN checkin_records c ON ct.checkin_task_id = c.checkin_task_id
        GROUP BY ct.checkin_task_name;
    """)
    results = cursor.fetchall()
    conn.close()
    return results


def display_checkin_statistics(console):
    """Display check-in task statistics in the command line"""
    console.print("=== Check-in Task Statistics ===")

    console.print("\nCheck-in Task Completion Rates:")
    completion_rates = get_checkin_task_statistics()
    for task in completion_rates:
        console.print(
            f"{task[0]}: Total check-ins {task[1]}, Completed {task[2]}, Completion rate {task[3]}%"
        )


if __name__ == "__main__":
    display_checkin_statistics()
