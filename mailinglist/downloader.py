from datetime import datetime, timedelta

end_date = datetime(2003, 4, 1)
start_date = datetime.today().replace(day=1)

def months_iterator(start, end):
    current = start
    while current >= end:
        yield current
        if current.month == 1:
            current = current.replace(year=current.year - 1, month=12)
        else:
            current = current.replace(month=current.month - 1)

def main():
    for month in months_iterator(start = start_date, end = end_date):
        url = f"https://lists.nongnu.org/archive/html/qemu-devel/{month.strftime("%Y-%m")}/threads.html"
        print(url)

if __name__ == "__main__":
    main()
