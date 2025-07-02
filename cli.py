from assistant.core import start_focus_session, view_log

def main():
    while True:
        print("\n==== Anti-Procrastination Assistant ====")
        print("1. Start new task session")
        print("2. View task log")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            task = input("Enter your task name: ").strip()
            try:
                duration = int(input("Enter session duration in minutes (default 25): ") or 25)
                start_focus_session(task, duration)
            except ValueError:
                print("Invalid duration. Try again.")
        elif choice == '2':
            view_log()
        elif choice == '3':
            print("Goodbye. Stay mindful and consistent.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()