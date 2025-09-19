import sys
import csv
from bs4 import BeautifulSoup as BS
import requests
from datetime import datetime 

urlList = []
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
fileName = r"C:\Users\User\Desktop\[rpject2.0\dataSet.csv"
urlData = r"C:\Users\User\Desktop\[rpject2.0\urlData.csv"

def response(url):
    rp = requests.get(url)
    if rp.status_code ==200:
        rp = True
    else:
        rp = False
    return rp

def csvReader(fileName):
    
    """
    Parameters:
    ----------
    fileName: .csv File
    
    Description:
    ------------   
    returns the data of the file as a list ex: [["PID","Name", "Price", "Date"], ["1", "Lian Li", 10000, "11-08-23"]]
    
    Returns:
    -------
    list [[row1], [row2],...]
    """
    
    oldData = []
    
    try:
        with open(fileName, "r") as fr:
            reader = csv.reader(fr)
            for rows in reader:
                oldData.append(rows)

        return oldData

    except FileNotFoundError:
        return oldData

def csvWriter(fileName, updatedData):
    
    """
    Parameters
    ------------
    fileName: .csv File,
    updatedData: list with nested lists. [[row1], [row2],...]
    
    Description:
    ------------
    overwrites the file with Data provided where Data is [[row1], [row2],...]
    data and file can be empty as well then the overwritten file will be empty.
    
    Returns:
    ------------
    Nothing
    
    """
    
    with open(fileName, "w", newline="") as fw:
        writer = csv.writer(fw)
        writer.writerows(updatedData)

def csvUpdater(fileName, productDetails):
    
    """
    Parameters:
    ------------
    fileName: .csv File,
    productDetails: [nameOfProduct, priceOfProduct]
    
    Description:
    ------------
    Takes the csv file and the details of the product [nameOfProduct, priceOfProduct].
    
    Creates a variable(newData) that reads and stores the previous data of the file
    [[row1], [row2],...] or it can be empty [].
    
    Then it appends the productDetails[nameOfProduct, priceOfProduct] to the data
    if the product already exists, it will append the price to the column next to it along with today's date,
    if it doesn't then it will append productDetails to a new row with today's date.
    
    Returns:
    ------------
    Nothing
    """
    
    
    newData = csvReader(fileName)
    PID = len(newData)
    now = datetime.now()
    date = now.strftime("%d-%m-%y")

    for rows in newData:
        if rows[1] == productDetails[0]:
            rows.append(productDetails[1])
            rows.append(date)
            break

    else:
        newData.append([PID,productDetails[0], productDetails[1], date])

    csvWriter(fileName, newData)

def productDetails(url,UA):
    
    component = requests.get(url)
    htmlReader = BS(component.content, "html.parser")
    
    print("\n",component)  # response<200> connection made successfully
    
    
    try:
        productName= htmlReader.find("h1", {"class" : "product-name"}).text.strip()
        
    except:
        productName = ""
        
    price = htmlReader.find("span", {"class" : "current"}).text.strip()
    
    productPrice = ""
    
    for i in price:
        if i.isdigit() or i == ".":
            productPrice += i
            
    productPrice = float(productPrice.lstrip("."))
    details = [productName, productPrice]
    return details
    


def startup():
    with open(r"C:\Users\User\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start.bat", "w") as batch_file:
        batch_file.write(f'@echo off\n')
        batch_file.write(f'start python "{sys.argv[0]}" proj.py\n')
        batch_file.write(f'exit\n')


def urlDataUpdater(urlList, fileName):
    for i in range(len(urlList)):
        
        url = urlList[i][1]
        if response(url):
            details = productDetails(url, UA)
            productName = details[0]
            productPrice = details[1]
            
            print("PID: ",urlList[i][0], "Name: ",productName, "Price: ",productPrice, sep="\n", end = "\n\n")
            csvUpdater(fileName,details)
    
def main():
    
    try: 
        with open(urlData, "r") as fr:
            pass
        with open(fileName, "r"):
            pass
        
    except FileNotFoundError:
        startup()
        header = ["PID", "Name", "Price", "Date"]
        csvWriter(fileName, [header])
        with open("urlData.csv", "w"):
            pass
        
    with open(urlData, "r", newline="") as fr:
        reader = csv.reader(fr)
        for row in reader:
            urlList.append(row)
            
    urlDataUpdater(urlList, fileName)

if __name__ == "__main__":
    main()
