try :
    from bs4 import BeautifulSoup
    import requests
    import random
    import fpdf
    import PyPDF2
    import Movies as m
except ImportError as i :
    print("It can't import module r sub-module", i)

url = 'https://www.imdb.com/chart/top/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
movies = soup.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
years = soup.select('span.secondaryInfo')
#Temoporary array to store class instances
_temp_ = []

for index in range(0, len(movies)):
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]
    year = years[index].get_text()
    position = index+1
    movie_instances = m.ExtractMovies(movie_title, year, crew[index], m.first2(ratings[index]))
    _temp_.append(movie_instances)

pdf = fpdf.FPDF()
pdf.add_page()
pdf.set_font("Arial", size = 10)
pdf.cell(200,10, txt = "Here r the some movies to kill BOREDOM : ", ln = 1)
pdf.cell(200,10, txt = "", ln = 2)
random.shuffle(_temp_)
i=1
for obj in _temp_:
    t = "\t" + str(i) + "\t|\t" + obj.title + "\t" + obj.year + " ==>\t" + obj.star + "\t==> (ratings) " + obj.ratings
    pdf.cell(200,10, txt = t, ln = i+2 )
    i=i+1
    if i==11 :
        break

pdf.output("output.pdf")

input_file = open("output.pdf",'rb')
input_pdf = PyPDF2.PdfReader(input_file)
watermark_file = open("watermark.pdf",'rb')
watermark_pdf = PyPDF2.PdfReader(watermark_file)

pdf_page = input_pdf.pages[0]
watermark_page = watermark_pdf.pages[0]
pdf_page.merge_page(watermark_page)

out = PyPDF2.PdfWriter()
out.add_page(pdf_page)

merged_file = open("final_output.pdf",'wb')
out.write(merged_file)

merged_file.close()
watermark_file.close()
input_file.close()