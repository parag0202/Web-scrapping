from bs4 import BeautifulSoup
import requests
import re
import pandas
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

institute_name = list()
institute_location = list()
institute_contact = list()
institute_email = list()
institute_website = list()
institute_district = list()
institute_registrar = list()
registrar_contact = list()
institute_region = list()
institute_status = list()
institute_autostatus = list()
institute_region_type = list()
name = list()
region = ['Amravati', 'Aurangabad', 'Mumbai', 'Nagpur', 'Nashik', 'Pune']
region_id = 1
print("Please wait..System is scrapping details for you.")
for name in region:
    URL = ("http://www.dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID=" + str(region_id) + "&RegionName=" + name)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find("table", {"class": "DataGrid"})
    college_tags = tables.findChildren("td")

    i = 3

    url = list()
    data = []

    word1 = "Engineering"
    word2 = "Technology"
    word3 = "Technical"
    word4 = "Technological"
    institute_code = list()
    institute_link = list()
    while True:

        if i <= len(college_tags):
            name = college_tags[i].text
            if word1 in name or word2 in name or word3 in name or word4 in name:
                institute_code.append(college_tags[i - 1])
        else:
            break
        i = i + 3

    for institute in institute_code:
        clg_link = institute.find('a', {'href': re.compile("^frm")})
        institute_link.append("http://dtemaharashtra.gov.in/" + clg_link.get('href'))

    for i in institute_link:
        clg_page = requests.get(i)
        itable = BeautifulSoup(clg_page.content, 'html.parser')

        iname = itable.find("span", {"id": "ctl00_ContentPlaceHolder1_lblInstituteNameEnglish"})

        address = itable.find("span", {"id": "ctl00_ContentPlaceHolder1_lblAddressEnglish"})

        email = itable.find("span", {"id": "ctl00_ContentPlaceHolder1_lblEMailAddress"})

        website = itable.find("span", {"id": "ctl00_ContentPlaceHolder1_lblWebAddress"})

        district = itable.find("span", {"id": "ctl00_ContentPlaceHolder1_lblDistrict"})

        contact = itable.find("span", {"id": "ctl00_ContentPlaceHolder1_lblPersonalPhoneNo"}).getText().split()

        registrar_name = itable.find("span", {"id": "ctl00_ContentPlaceHolder1_lblRegistrarNameEnglish"}).getText()

        registrar = itable.find("span", {"id": "ctl00_ContentPlaceHolder1_lblOfficePhoneNo"}).getText().split()

        region = itable.find("span", {"id": "ctl00_ContentPlaceHolder1_lblRegion"}).getText()

        region_Type = itable.find("span", {"id": "ctl00_ContentPlaceHolder1_lblRegionType"}).getText()

        status = itable.find("span", {"id": "ctl00_ContentPlaceHolder1_lblStatus1"}).getText()

        auto_status = itable.find("span", {"id": "ctl00_ContentPlaceHolder1_lblStatus2"}).getText()

        if iname != "" and address != "" and email != "" and website != "" and district != "" and contact[
            0].isnumeric() and registrar_name != "" and registrar[0].isnumeric():
            institute_name.append(iname.text)
            institute_location.append(address.text)
            institute_email.append(email.text)
            institute_website.append(website.text)
            institute_district.append(district.text)
            institute_contact.append(contact[0])
            institute_registrar.append(registrar_name)
            registrar_contact.append(registrar[0])
            institute_region.append(region)
            institute_status.append(status)
            institute_autostatus.append(auto_status)
            institute_region_type.append(region_Type)

    clg_dict = {"College Name": institute_name,
                "Region": institute_region,
                "Region Type": institute_region_type,
                "Location": institute_location,
                "District": institute_district,
                "Contact Number": institute_contact,
                "Email Address": institute_email,
                "Website Link": institute_website,
                "Registrar Name": institute_registrar,
                "Registrar Contact Number": registrar_contact,
                "Status": institute_status,
                "Autonomous Status": institute_autostatus
                }
    region_id = region_id + 1
df = pandas.DataFrame(clg_dict)
df.to_csv('college_details.csv', index=False, header=True)
print("Thank You for your patience.")
print("Your csv file is ready.")

df = pd.read_csv("college_details.csv")

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

Region = df.groupby('Region').count()['College Name']

ax1.pie(Region, labels=Region.index , autopct='%1.1f%%')
ax1.set_title('No. of Colleges per Region')

Auto_By_Region = df.groupby(['Region','Autonomous Status']).count()['College Name']

auto = []
non_auto = []

for i in range(len(Auto_By_Region)):
    if i%2 == 0:
        auto.append(Auto_By_Region[i])
    else:
        non_auto.append(Auto_By_Region[i])

x = np.arange(len(Region.index))
width = 0.35

rect1 = ax2.bar(x - width/2, auto, width, label='Auto')
rect2 = ax2.bar(x + width/2, non_auto, width, label='Non Autonomous')
ax2.legend()
ax2.set_xticks(x)
ax2.set_xticklabels(Region.index)
ax2.set_ylabel('No. of Colleges')
ax2.set_title('No. of Autonmous and non-Autonomous per Region')

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax2.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
autolabel(rect1)
autolabel(rect2)

fig2.tight_layout()
plt.show()