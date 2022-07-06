import scrapy
import re
import redis

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    r = redis.Redis(host='localhost', port=6379, db=0)
    def start_requests(self):
        with open('/home/zhiiw/Videos/Books.csv','r') as f:
            i=0
            for line in f:
                line=line.split(',')
                name=line[1]
                ISBN = line[0]

                yield scrapy.Request(url='http://zh.sg1lib.org/s/'+name,meta={"ISBN":ISBN}, callback=self.parse)
                print("name is "+name)
                i+=1
                if(i==2):
                    break
                
        # urls = [
        #     'http://zh.sg1lib.org/s/ee'
        # ]
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        add_url = response.css('h3 a::attr(href)')[0].get()
        if add_url:
            print(add_url)
            yield scrapy.Request(url='http://zh.sg1lib.org'+add_url,meta=response.meta ,callback=self.ee)
    
    def ee(self,response):
        print(response.url)
        a=response.css('div#bookDescriptionBox span').get()
        b= response.css('div.property_year div.property_value').get()
                # delete the div tag
        if b is not None:
            b= b.replace('<div class="property_value ">','')
            b=b.replace('</div>','')
        c= response.css('div.property_pages div.property_value span').get()
        # delete the span tag
        if c is not None:

            c=c.replace('<span title="Pages paperback">','')
            c=c.replace('</span>','')
        
        d=response.css('span.book-rating-interest-score').get()
        # get the first number of d
        if d is not None:
            for i in d:
                if i.isdigit():
                    d=i
                    break
        # connect to redis
        # save the data to redis
        # write res to file res.txt
        with open('res.txt','a') as f:
            f.write("ISBN:"+response.meta["ISBN"]+',')

            if(a is not None):
                f.write("detail:"+a+',')
            else:
                f.write(",")
            if(b is not None):
                f.write("year: "+b+',')
            else:
                f.write(",")
            if(c is not None):
                f.write("pageCount: "+ c+',')
            else:
                f.write(",")
            if(d is not None):
                f.write("rating: "+d+',')
            else:
                f.write(",")
            f.write('\n')
 
    