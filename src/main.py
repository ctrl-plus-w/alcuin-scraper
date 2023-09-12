from bs4 import BeautifulSoup

from scrapper import scraper


def main():
    # agenda = scraper.scrape()
    # html = agenda.get_attribute("innerHTML")

    # with open("results.txt", "x") as file:
    #     file.write(html)

    with open("results.txt", "r") as html:
        soup = BeautifulSoup(html, features="html.parser")

        tbody = soup.select_one("tbody")

        rows = tbody.findChildren("tr", recursive=False)
        weeks = rows[2:]

        for week in weeks:
            cells = week.findChildren("td", recursive=False)
            days = cells[2:]

            for day in days:
                tables = day.findChildren("table", recursive=False)

                date_table = tables[0]
                courses_tables = tables[1:]

                date = int(date_table.get_text().strip())

                for course_table in courses_tables:
                    print(course_table)
                    break

                    # TODO : Parse the table to retrieve the course informations.

            break

        break

        # for week in weeks:
        #     print(week.name)

        # for week in weeks:
        #     cells = week.find_all("td")
        #     days = cells[1:]

        #     print(cells)

        #     break


if __name__ == "__main__":
    main()
