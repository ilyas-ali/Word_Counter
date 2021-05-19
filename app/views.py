from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import operator
from .models import Counter
import json

def index(request):
    return render(request,'app/index.html')

def result(request):
    link=request.POST.get('url')
    
    if Counter.objects.filter(urllink=link).exists():

        myobj=Counter.objects.filter(urllink=link).first() #object created of given url
        jsonDec = json.decoder.JSONDecoder()               
        sorted_list = jsonDec.decode(myobj.words)          #convert JSON string back to list

        return render(request,'app/alt.html',{"sorted":sorted_list})

    else:
        page = urlopen(link)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser") #soup object created
        text=soup.get_text()
        text=text.replace(':','')
        x = "+=|><?/(){[]}"
        y = "             "
        mytable = text.maketrans(x, y)

        text=text.translate(mytable)
        text=text.lower()                 #text of entire webpage in formatted way
        word_list = text.split()          #list of all the words
        word_dictionary={}
        #string of 100 common words      
        common="""a
about
all
also
and
as
at
be
because
but
by
can
come
could
day
do
even
find
first
for
from
get
give
go
have
he
her
here
him
his
how
i
if
in
into
it
is
its
just
know
like
look
make
man
many
me
more
my
new
no
not
now
of
on
one
only
or
other
our
out
people
say
see
she
so
some
take
tell
than
that
the
their
them
then
there
these
they
thing
think
this
those
time
to
two
up
use
very
want
way
we
well
what
when
which
who
will
with
would
year
you
your
.
,
!
@
#
$
%
^
&
*
(
)
1
2
3
4
5
6
7
8
9
0
|
/
+
-
~
_
=
"""
        
        common_words=common.replace("\n"," ")
        common_words_list=common_words.split() #common words list
        wordlist=[x for x in word_list if x not in common_words_list] #list of all the uncommon words in html page
        for word in wordlist:
            if word in word_dictionary:
                
                word_dictionary[word] += 1
            else:
                
                word_dictionary[word] = 1
        
        sortedwords = sorted(word_dictionary.items(),key=lambda x: x[1], reverse = True) #sort in descending order
        
        sorted_words=sortedwords[0:10] #top 10 words from list
        print(sorted_words) 
        sorted_words1=sorted_words     #copy to be used for JSON conversion
        words=json.dumps(sorted_words1) #convert list to JSON
        obj=Counter.objects.create(urllink=link,words=words) #object creation
        obj.save()
        
        return render(request, 'app/counter.html', {'fulltext':text,'count':len(wordlist),'word_dictionary':word_dictionary,'sorted':sorted_words})
    #return render(request,'app/counter.html',{"text":text})