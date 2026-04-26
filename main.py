import csv
import datetime

expenses = []

# ---------- Helper functions ----------
def get_valid_date():
    while True:
        date_input = input("\nEnter date (MM-DD-YYYY): ")
        try:
            date_obj = datetime.datetime.strptime(date_input, "%m-%d-%Y")
            
            # Get today's date
            today = datetime.datetime.now()
            
            # If the entered date is after today, show error
            if date_obj > today:
                print("Invalid date! You cannot enter a future date.")
                continue  # loop again

            return date_input  # valid date
        except ValueError:
            print("Invalid date format! Please use MM-DD-YYYY.")



def get_valid_amount():
    while True:
        amount = input("Enter amount: ")
        try:
            return float(amount)
        except ValueError:
            print("Invalid amount! Please enter a number.")


def get_valid_category():
    while True:
        category = input("Enter category: ")
        cleaned_category = category.strip()  # removes spaces at start and end
        if cleaned_category:
            return cleaned_category
        else:
            print("Category cannot be empty! Please enter a valid category.")



def get_valid_description():
    while True:
        description = input("Enter description: ")
        if description.strip():
            return description
        else:
            print("Description cannot be empty! Please enter a valid description.")


# ---------- Core functions ----------
def load_expenses():
    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            all_rows = list(reader)

            if not all_rows:
                return  # empty file

            # Skip header if present
            if all_rows[0][0].lower() == "date":
                all_rows = all_rows[1:]

            for row in all_rows:
                if len(row) == 4:
                    date = row[0]
                    amount = float(row[1])
                    category = row[2].strip().capitalize()
                    description = row[3].strip().capitalize()
                    expenses.append([date, amount, category, description])

    except FileNotFoundError:
        pass  # start fresh if file doesn't exist


def save_expenses():
    with open("expenses.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(expenses)


def add_expense():
    date = get_valid_date()
    amount = get_valid_amount()
    category = get_valid_category().strip().capitalize()
    description = get_valid_description().strip().capitalize()

    expenses.append([date, amount, category, description])
    save_expenses()
    print("\nExpense added successfully!\n")


def view_expenses():
    """Display all expenses and a merged category summary."""
    headers = ["Date", "Amount", "Category", "Description"]

    if not expenses:
        print("\nNo expenses found!\n")
        return

    # Column widths
    col_widths = [max(len(str(row[i])) for row in ([headers] + expenses)) for i in range(len(headers))]

    # Print header
    print("\nAll Expenses:")
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
    header_row = " | ".join(headers[i].ljust(col_widths[i]) for i in range(len(headers)))
    print(header_row)
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))

    # Print each expense
    for row in expenses:
        row_date = row[0]
        row_amount = row[1]
        row_category = row[2].strip().capitalize()
        row_description = row[3].strip().capitalize()
        print(f"{row_date.ljust(col_widths[0])} | {str(row_amount).ljust(col_widths[1])} | {row_category.ljust(col_widths[2])} | {row_description.ljust(col_widths[3])}")

    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))

    # Category summary -------------
    category_totals = {}
    for row in expenses:
        category = row[2].strip().capitalize()
        amount = float(row[1])
        category_totals[category] = category_totals.get(category, 0) + amount

    print("\n📊 Spending by Category:\n")
    for cat, total in category_totals.items():
        print(f"{cat}: ${total:.2f}")
    print("\n")



# ---------- Menu system ----------
def main_menu():
    print("Personal Finance Tracker")
    while True:  
        print("1. Add an expense")
        print("2. View expenses")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice! Please select 1, 2, or 3.\n")

# ---------- Entry point ----------
if __name__ == "__main__":
    load_expenses()
    main_menu()
