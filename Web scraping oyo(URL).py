#project on Web scraper using Beautfulsoup4 and requests
import requests
from bs4 import BeautifulSoup
import pandas
import structured_query_language
oyo_url= 'https://www.oyorooms.com/hotels-in-bangalore/?page='
page_num_max=3
scraped_info_list = []
structured_query_language.connect(args.dbname)
for page_num in range(1,page_num_max):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"}
    req=requests.get(oyo_url + str(page_num),headers=headers) #request is nothing but it request the url
    contents = req.content     #from the request we'll extrect the content
    soup = BeautifulSoup(contents,"html.parser")
    all_hotels=soup.find_all("div",{"class":"hotelCardListing"})

    for hotel in all_hotels:
        hotel_dict = {}
        hotel_dict["name"] = hotel.find("h3",{"class":"listingHotelDescription__hotelName"}).get_text()
        hotel_dict["address"] = hotel.find("div", {"class": "listingHotelDescription__hotelAddress"}).get_text()
        hotel_dict["price"] = hotel.find("span", {"class": "listingPrice__finalPrice"}).get_text()
        #try an except
        try:
            hotel_dict["rating"] = hotel.find("span", {"class": "hotelRating__rating"}).get_text()
        except AttributeError:
            pass
        parent_amenities_elements = hotel.find("div",{"class":"amenityWrapper"})
        amenities_list=[]
        for amenity in parent_amenities_elements.find_all("div",{"class":"amenityWrapper__amenity"}):
            amenities_list.append(amenity.find("span",{"class":"d-body-sm"}).text)
        hotel_dict["amenities"] = ', '.join(amenities_list[:-1])
        scraped_info_list.append(hotel_dict)
        connect.insert_into_table(args.dbname, tuple(hotel_dict.values()))
        #print(hotel_name,hotel_address,hotel_price, hotel_rating ,amenities_list)
dataFrame = pandas.DataFrame(scraped_info_list)
dataFrame.to_csv("oyo.csv")
connect.get_hotel_info(args.dbname)
