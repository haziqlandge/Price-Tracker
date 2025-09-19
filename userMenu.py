import csv
from proj import csvReader, csvUpdater, csvWriter, productDetails, response

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
dataFile = "dataSet.csv"

def urlAppender(urlFile, urlList):
    count = 0
    
    with open(urlFile, "a+", newline="") as fa:
        writer = csv.writer(fa)
          
        for url in urlList: #url1, url2
            urlData = csvReader(urlFile)
            for nstList in urlData: #u_1, u_2,u_3
                if url == nstList[1]:
                    break
            else:
                count+=1
                PID = len(urlData)+count
                tempList = [PID, url]
                writer.writerow(tempList)
    
def inputUrls ():
    userUrlList = input("Enter URLS separated by ',': ").split(',')
    return userUrlList

def inputPID():
    PID = (input("Enter Product ID(s) separated by ',': ")).split(',')
    print(PID)
    return PID

def trackPrice(dataFile, UA):
    
    URLS = inputUrls()
   
    for url in URLS:
        try:
            if response(url):
                product = productDetails(url, UA)
                print(f"{'Product Name':<60} |{'Price'}")
                csvUpdater(dataFile, product)
                print(f"{nameShortner(product[0].split()):<60} |Rs. {product[1]}")
                print("Being Tracked.")
                urlAppender("urlData.csv", URLS)
            
        except:
            print("Invalid URL:", url)
    
    
def nameShortner(nameLong):
    """
    Parameters:
    ------------
    nameLong: list[] ex: ["This","is" ,"an" ,"example" ,"product" ,"hello" ,"hello" ,"123"]
    
    Description:
    ------------
    Takes a sentence (name of the product) and shortens it to 5 blocks.
    
    Returns:
    ------------
    nameShort: string
    """
    nameShort = nameLong
    
    if len(nameLong) > 5:
        nameShort = nameLong[:5]
        nameShort = " ".join(nameShort) + ".."
        return nameShort
    
    else:
        nameShort = " ".join(nameShort)
        return nameShort

def displayInfoName(dataOfProduct):
    """
    Parameters:
    ------------
    dataOfProduct: list ["Name", price1, date1, price2, date2]
    
    Description:
    ------------
    prints PID |Name |Price |Data
    in the format
    1 |name1   |Rs. 123   |12-07-23
    2 |name2   |Rs. 100   |15-07-23..
    
    Returns:
    ------------
    Nothing
    
    """
    count = 0
    name = dataOfProduct[1].split()     
            
    name = nameShortner(name)
    PID = dataOfProduct[0]
    print(f"{PID:<10}|{name:<60}", end="")                #prints the name of the product
    
    allPrices, dates = [], []
            
    for price in range(2, len(dataOfProduct), 2 ):                          # k[2] ,k[4]  ,k[6]
                allPrices.append(dataOfProduct[price])
                                                                           #123, 100
            
    for date in range(3, len(dataOfProduct), 2):                      #k[3] k[5] k[7]          
        dates.append(dataOfProduct[date]) 
                                                                #"12-07-23", "15-07-23"

    for price, date in zip(allPrices, dates):           #(price1, date1), (price2, date2)....
        if count>=1:
            print(f"{'':<10}|{'':<61}|Rs. {price:<10} |{date}")
        else:
            print(f"{' '*1}|Rs. {price:<10} |{date}")
            count +=1   
            
def displayFile(dataFile):
    
    """
    Parameters:
    ------------
    dataFile: .csv File
    
    Description:
    ------------
    Takes the .csv File; checks if the first column is the header and then prints it
    if its not then it prints all the products with their prices and the date
    Returns:
    ------------
    Nothing
    """
    
    for row in csvReader(dataFile):            
        
        if row[2] == "Price":
            print(f"{row[0]:<10}|{row[1]:<60} |{row[2]:<15}|{row[3]}")    #PID    |Name          | Price     | Date
            
        else:
            
            displayInfoName(row)
            
def lowestValueOf(dataFile, UA):
    """
    Parameters:
    ------------
    dataFile: .csv File
    UA: string User Agent
    
    Description:
    ------------
    Takes PID(s) frpm the user, iterates through them, if the PID exists in dataFile,
    it will print product's lowest price and the date
    if PID doesn't exist, invalid message will be printed
    
    Returns:
    ------------
    Nothing
    """

    PID = inputPID()
    existing_data = csvReader(dataFile) 
 
    for pid in PID:
        allPrices = []
        dates = []       
        for rows in existing_data:

            if rows[0] == pid:
                
                for price in range (2 , len(rows), 2):
                    allPrices.append(rows[price])
                    
                for x in range(3 , len(rows), 2): 
                    dates.append(rows[x])
                    
                name = rows[1].split()   
                name = nameShortner(name)
                print(f"\n{'PID':<10}|{'Name':<60} |{'Lowest Price':<15} | {'Date'}")
                
                low = min(allPrices)
                index = allPrices.index(low)
                print(f"{pid:<10}|{name:<60} |Rs. {low:<11} |{dates[index]}" )
                print()
                
                break
                
        else:
            print("Invalid PID:", pid)
    
def averageValue(dataFile, UA):
    """
    Parameters:
    ------------
    dataFile: .csv File
    UA: string User Agent
    
    Description:
    ------------
    Asks the User for PID(s), iterates through them, if the PID exists(if it doesn't then prints an invalid message), 
    it finds the average of product and prints it
    
    Returns:
    ------------
    Nothing
    """
    
    PID = inputPID()
    existing_file = csvReader(dataFile)
    
    for pid in PID:
        
        allPrices = []
        
        for rows in existing_file:

            name = nameShortner(rows[1].split())
            if rows[0] == pid:
                    
                for i in range (2 , len(rows), 2):
                    allPrices.append(float(rows[i]))

                avg = round(sum(allPrices)/len(allPrices),2)

                print(f"{'PID':<10}|{'Name':<60} |{'Average Price'}")
                print(f"{pid:<10}|{name:<60} |Rs. {avg:<10}")
                print()
                break
        else:
            print("Invalid PID: ", pid)

def detailsOfProduct(dataFile, UA):
    """
    Parameters:
    ------------
    dataFile: .csv File
    UA: string User Agent
    
    Description:
    ------------
    
    Returns:
    ------------
    Nothing
    """
    
    PID= inputPID()

    for pid in PID:
        
           
        for row in csvReader(dataFile):            

            if row[0] == pid:
                print(f"{'PID':<10}|{'Name':<60} |{'Price':<14} |{'Date'}")
                displayInfoName(row)
                print()
                break
        else:
            print("Invalid PID: ", pid)

try:
    with open(dataFile, "r"):
        pass
except FileNotFoundError:
    header = ["PID", "Name", "Price", "Date"]
    csvWriter(dataFile, [header])

while True:
    print("\nMenu:")
    print("1. Display File")
    print("2. Track Price")
    print("3. Lowest Value Of")
    print("4. Average Value")
    print("5. Details of Product")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        displayFile(dataFile)
    elif choice == "2":
        trackPrice(dataFile, UA)
    elif choice == "3":
        lowestValueOf(dataFile, UA)
    elif choice == "4":
        averageValue(dataFile, UA)
    elif choice == "5":
        detailsOfProduct(dataFile, UA)
    elif choice == "6":
        break
    
    else:
        print("Invalid choice")
