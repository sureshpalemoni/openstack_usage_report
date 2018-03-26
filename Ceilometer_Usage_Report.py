import ceilometerclient.client
from datetime import datetime, timedelta
import xlwt
from openstack import connection


days = input("Enter the Number of Days for the report: ")
time_format = "%Y-%m-%dT00:00:00"
time_start = (datetime.today() - timedelta(days=days)).strftime(time_format)
time_end = datetime.today().strftime(time_format)


auth_args = {
    'auth_url': 'https://____:5000/v3',
    'project_name': 'admin',
    'username': 'admin',
    'password': '#####',
    'project_domain_name': '####',
    'user_domain_name': '####'
}

tenants = []

# Getting the Connection to the admin
conn = connection.Connection(**auth_args)

# Get the projects using for loop
# Then connect to ceilometer for every project
for proj in conn.identity.tenants():
	project =  str(proj.name)
	tenants.append(project)
	cclient = ceilometerclient.client.get_client(2, username="admin", password="XXXXX",tenant_name=project, auth_url="https://____:5000/v3")

	workbook = xlwt.Workbook()

	def stats(meter):
	   query = [dict(field="timestamp", op="ge", value=time_start),dict(field="timestamp", op="lt", value=time_end)]
	   return cclient.statistics.list(meter, q=query, period=3600)

	headers = ["Period", "Meter", "Count", "Max", "Min", "Average", "Sum"]
	def file_create(sheetname):
	  sheet = workbook.add_sheet(sheetname)
	  row = sheet.row(0)
	  for i,j in enumerate(headers):
	    row.write(i, j)
	  return sheet

	met_list = []

	for i in cclient.meters.list():
	  if i.name not in met_list:
	    met_list.append(i.name)
	    file = file_create(i.name)
	    for hr,j in enumerate(stats(i.name)):
	      row_data = [hr+1,i.name,j.count,j.max,j.min,j.avg,j.sum]
	      for k,l in enumerate(row_data):
		file.row(hr+1).write(k,l)  

	workbook.save(proj.name+'.xls')
