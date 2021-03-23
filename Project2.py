from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    with open(filename) as html:
        soup = BeautifulSoup(html, 'html.parser')
        books = soup.find_all('tr', itemtype = 'http://schema.org/Book')
        title_list = []
        author_list = []
        for book in books:
            title = book.find('a', class_ = 'bookTitle')
            author = book.find('a', class_ = 'authorName')
            title_list.append(title.text.strip())
            author_list.append(author.text.strip())

        tuples = tuple(zip(title_list, author_list))
        list = [(title_list[i], author_list[i]) for i in range(len(title_list))]
        return list


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    url = 'https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    urls = soup.find_all('a', class_ = 'bookTitle')[0:10]
    first_url_part = 'https://www.goodreads.com'
    list = []
    for url in urls:
        link = url.get('href')
        full_url = first_url_part + link
        list.append(full_url)

    return list


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    resp = requests.get(book_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title = soup.find('h1', id = 'bookTitle').text.strip()
    author = soup.find('a', class_ = 'authorName').text.strip()
    num_pages = soup.find('span', itemprop = 'numberOfPages').text.strip()
    num_pages = re.sub("\D", "", num_pages)

    return (title, author, int(num_pages))

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    
    with open(filepath, encoding="utf8") as html:
        list = []
        soup = BeautifulSoup(html, 'html.parser')
        books = soup.find_all('div', class_ = 'category clearFix')
        for book in books:
            category = book.find('h4', class_ = 'category__copy').text.strip()
            title = book.find('img', class_ = 'category__winnerImage').get('alt').strip()
            url = book.find('a').get('href').strip()
            list.append((category, title, url))
        return list


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Book title', 'Author Name'))
        writer.writerows(data)


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        returned = get_titles_from_search_results('search_results.htm')

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(returned), 20)

        # check that the variable you saved after calling the function is a list
        self.assertTrue(isinstance(returned, list))

        # check that each item in the list is a tuple
        for item in returned:
            self.assertTrue(isinstance(item, tuple))

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertTrue(returned[0][0], 'Harry Potter and the Deathly Hallows (Harry Potter, #7)')
        self.assertTrue(returned[0][1], 'J.K. Rowling')

        # check that the last title is correct (open search_results.htm and find it)
        self.assertTrue(returned[-1][0], 'Harry Potter: The Prequel (Harry Potter, #0.5)')
        self.assertTrue(returned[-1][1], 'J.K. Rowling')

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertTrue(isinstance(TestCases.search_urls, list))

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)

        # check that each URL in the TestCases.search_urls is a string
        for item in TestCases.search_urls:
            self.assertTrue(isinstance(item, str))

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        regex = r'https://www.goodreads.com/book/show/'
        for url in TestCases.search_urls:
            self.assertTrue(re.search(regex, url))
    '''
    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for url in TestCases.search_urls:
            summaries.append(get_book_summary(url))

        # check that the number of book summaries is correct (10)
        self.assertTrue(len(summaries), 10)
        
            # check that each item in the list is a tuple
        for item in summaries:
            self.assertTrue(isinstance(item, tuple))

            # check that each tuple has 3 elements
            self.assertTrue(len(item), 3)

            # check that the first two elements in the tuple are string
            self.assertTrue(isinstance(item[0], str))
            self.assertTrue(isinstance(item[1], str))

            # check that the third element in the tuple, i.e. pages is an int
            self.assertTrue(isinstance(item[2], int))

            # check that the first book in the search has 337 pages
        self.assertTrue(summaries[0][2], 337)  
    '''

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best_books = summarize_best_books('best_books_2020.htm')
        # check that we have the right number of best books (20)
        self.assertEqual(len(best_books), 20)
            # assert each item in the list of best books is a tuple
        for book in best_books:
            self.assertTrue(isinstance(book, tuple))
            # check that each tuple has a length of 3
            self.assertEqual(len(book), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best_books[0], ('Fiction', 'The Midnight Library', 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best_books[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        results = get_titles_from_search_results('search_results.htm')

        # call write csv on the variable you saved and 'test.csv'
        write_csv(results, 'test.csv')

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        f = open('test.csv', 'r')
        csv_lines = list(csv.reader(f))
        f.close()
        
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)

        # check that the header row is correct
        self.assertEqual(csv_lines[0], ['Book title','Author Name'])

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



