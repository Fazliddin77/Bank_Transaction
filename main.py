import psycopg2

conn = psycopg2.connect(
    dbname=input('Enter your DataBase Name:'),
    user=input('Enter your User Name:'),
    password=input('Enter your Password:'),
    host="localhost",
    port="5432"
)
cur = conn.cursor()


def transfer_money(sender_id_card, recipient_id_card, money):
    try:
        cur.execute("START TRANSACTION")
        cur.execute("SELECT balance FROM bank WHERE id_card = %s", (sender_id_card,))
        cur.execute("SELECT COUNT(*) FROM bank WHERE id_card = %s", (recipient_id_card,))
        receiver_exists = cur.fetchone()[0]
        if receiver_exists == 0:
            print("Receiver account does not exist. Transaction failed.")
            return
        cur.execute("UPDATE bank SET balance = balance - %s WHERE id_card = %s", (money, sender_id_card))
        cur.execute("UPDATE bank SET balance = balance + %s WHERE id_card = %s", (money, recipient_id_card))

        cur.execute("COMMIT")
        print("Transaction successful.")

    except Exception:
        cur.execute("ROLLBACK")
        print("Transaction failed Error:", str(Exception))


def check_balance(check):
    cur.execute("SELECT name, balance FROM bank WHERE id_card = %s", (check,))
    print(cur.fetchall())


def make_deposit(money, date):
    cur.execute("INSERT INTO bank (deposit, deposit_year) VALUES (%s, %s)", (money, date))


def show_deposit(date):
    cur.execute("SELECT name, deposit, deposit_year FROM bank WHERE deposit_year = %s", (date,))
    print(cur.fetchall())


def exit():
    return ERROR


def choose():
    while True:
        print("[1] Transfer Money")
        print("[2] Check Balance")
        print("[3] Make a Deposit")
        print("[4] Show Deposit")
        print("[5] Exit")

        choice = int(input())

        if choice == 1:
            transfer_money(98765, 12345, 560)

        elif choice == 2:
            check_balance(12345)

        elif choice == 3:
            make_deposit(4000, 3)
        elif choice == 4:
            show_deposit(3)
        elif choice == 5:
            exit()


if __name__ == '__main__':
    choose()